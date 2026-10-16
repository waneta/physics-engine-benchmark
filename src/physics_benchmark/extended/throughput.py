"""Rendering-free full-trajectory timing with device-resident GPU controllers."""

import argparse
import json
import os
import statistics
import subprocess
import sys
import time
import traceback
from pathlib import Path
from xml.etree import ElementTree as ET

import mujoco as mj
import numpy as np

from .model import KD, KP, LIMIT, build

BATCHES = (1, 128, 8192, 32768, 131072)


def measure(engine, batch, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    s = build({"family": "throughput", "dt": 0.001})
    steps = 2500
    ref = s.reference
    qref = ref["q"][::2].astype(np.float32)
    vref = ref["v"][::2].astype(np.float32)
    ff = ref["feedforward"][::2].astype(np.float32)
    cleanup = lambda: None
    memory = lambda: None
    if engine == "mujoco":
        if batch != 1:
            raise ValueError("CPU control is a single-world baseline")
        data = mj.MjData(s.model)

        def reset():
            mj.mj_resetData(s.model, data)
            data.qpos[:] = s.data.qpos
            mj.mj_forward(s.model, data)

        def step(i):
            data.qfrc_applied[:] = np.clip(
                ref["feedforward"][2 * i]
                + KP[:7] * (ref["q"][2 * i] - data.qpos)
                + KD[:7] * (ref["v"][2 * i] - data.qvel),
                -LIMIT[:7],
                LIMIT[:7],
            )
            mj.mj_step(s.model, data)

        synchronize = lambda: None

        def positions():
            return data.qpos[None].copy()

        precision = "float64"
    elif engine == "mujoco-warp":
        import mujoco_warp as mw
        import warp as wp

        from .throughput_kernels import advance, control

        wp.config.kernel_cache_dir = str(Path(".cache/warp").resolve())
        wp.init()
        wp.set_device("cuda:0")
        gm = mw.put_model(s.model)
        data = mw.put_data(s.model, s.data, nworld=batch, naconmax=1, njmax=1)
        qr = wp.array(qref, dtype=wp.float32)
        vr = wp.array(vref, dtype=wp.float32)
        feed = wp.array(ff, dtype=wp.float32)
        kp = wp.array(KP[:7].astype(np.float32))
        kd = wp.array(KD[:7].astype(np.float32))
        limits = wp.array(LIMIT[:7].astype(np.float32))
        index = wp.zeros(1, dtype=wp.int32)
        initial = wp.array(np.tile(s.data.qpos.astype(np.float32), (batch, 1)))

        def reset():
            wp.copy(data.qpos, initial)
            data.qvel.zero_()
            data.qacc_warmstart.zero_()
            data.time.zero_()
            data.qfrc_applied.zero_()
            index.zero_()

        def device_step():
            wp.launch(
                control,
                dim=(batch, 7),
                inputs=[
                    index,
                    data.qpos,
                    data.qvel,
                    qr,
                    vr,
                    feed,
                    kp,
                    kd,
                    limits,
                    data.qfrc_applied,
                ],
            )
            mw.step(gm, data)
            wp.launch(advance, dim=1, inputs=[index])

        device_step()
        wp.synchronize()
        reset()
        with wp.ScopedCapture() as capture:
            device_step()

        def step(i):
            wp.capture_launch(capture.graph)

        synchronize = wp.synchronize

        def positions():
            return data.qpos.numpy()

        memory = lambda: {
            "warp_pool_peak_bytes": wp.get_mempool_used_mem_high("cuda:0"),
            "warp_pool_current_bytes": wp.get_mempool_used_mem_current("cuda:0"),
        }
        precision = "float32"
    elif engine == "genesis":
        import genesis as gs
        import torch

        os.environ.setdefault("GS_CACHE_FILE_PATH", str(Path(".cache/genesis").resolve()))
        if not gs._initialized:
            gs.init(backend=gs.cuda, precision="64", logging_level="warning", seed=0)
        sim = gs.Scene(
            sim_options=gs.options.SimOptions(dt=0.001, substeps=1),
            rigid_options=gs.options.RigidOptions(
                integrator=gs.integrator.Euler,
                constraint_solver=gs.constraint_solver.Newton,
                friction_cone=gs.friction_cone.elliptic,
                iterations=100,
                tolerance=1e-10,
                max_collision_pairs=1,
            ),
            show_viewer=False,
        )
        entity = sim.add_entity(gs.morphs.MJCF(file=ET.fromstring(s.xml)))
        sim.build(n_envs=batch)
        entity.set_dofs_armature(np.zeros(7))
        entity.set_dofs_damping(np.zeros(7))
        entity.set_dofs_frictionloss(np.zeros(7))

        def tensor(a):
            return torch.as_tensor(a, device=gs.device, dtype=gs.tc_float)

        qr = tensor(ref["q"][::2])
        vr = tensor(ref["v"][::2])
        feed = tensor(ref["feedforward"][::2])
        kp = tensor(KP[:7])
        kd = tensor(KD[:7])
        limits = tensor(LIMIT[:7])
        initial = tensor(s.data.qpos).repeat(batch, 1)

        def reset():
            sim.reset()
            entity.set_qpos(initial)
            entity.set_dofs_velocity(torch.zeros_like(initial))

        def step(i):
            u = (
                feed[i]
                + kp * (qr[i] - entity.get_qpos())
                + kd * (vr[i] - entity.get_dofs_velocity())
            )
            entity.control_dofs_force(torch.clamp(u, -limits, limits))
            sim.step()

        synchronize = torch.cuda.synchronize

        def positions():
            return entity.get_qpos().cpu().numpy()

        memory = lambda: {
            "torch_allocator_peak_bytes": torch.cuda.max_memory_allocated(),
            "note": "Excludes native Quadrants allocations; not total device peak.",
        }
        cleanup = sim.destroy
        precision = "float64"
    else:
        raise ValueError(
            "Device-batched benchmark supports MuJoCo, direct Warp and Genesis. PhysX IPC diagnostics are not comparable GPU throughput."
        )
    checkpoints = (250, 625, 1250, 1875, 2500)
    try:
        # Compile/warm up the complete physical trajectory; explicitly excluded from measured intervals.
        reset()
        warm = []
        for i in range(steps):
            step(i)
            if i + 1 in checkpoints:
                synchronize()
                q = positions()
                if not np.isfinite(q).all():
                    raise FloatingPointError("Invalid warmup trajectory")
                warm.append(q[[0, batch // 2, batch - 1]].copy())
        synchronize()
        timings = []
        max_error = 0.0
        for repeat in range(3):
            reset()
            synchronize()
            start = time.perf_counter()
            for i in range(steps):
                step(i)
            synchronize()
            timings.append(time.perf_counter() - start)
            q = positions()
            if not np.isfinite(q).all():
                raise FloatingPointError("Invalid measured trajectory")
            max_error = max(max_error, float(np.max(abs(q - warm[-1][0]))))
        tolerance = 1e-4 if engine == "mujoco-warp" else 1e-8
        if max_error > tolerance:
            raise RuntimeError(f"Batch/reset equivalence failed: {max_error}")
        np.savez_compressed(
            output / "verification.npz",
            checkpoints=checkpoints,
            sampled_warmup_q=np.array(warm),
            final_q=q[[0, batch // 2, batch - 1]],
        )
        result = {
            "engine": engine,
            "case": {"family": "throughput", "batch": batch},
            "batch": batch,
            "status": "completed",
            "precision": precision,
            "dt_s": 0.001,
            "steps_per_repeat": steps,
            "repeats": 3,
            "wall_seconds": timings,
            "median_seconds": statistics.median(timings),
            "min_seconds": min(timings),
            "max_seconds": max(timings),
            "world_steps_per_second": batch * steps / statistics.median(timings),
            "max_batch_reset_error_rad": max_error,
            "reference_sha256": ref["sha256"],
            "memory": memory(),
            "timing_scope": "Controller + physics + native host launch overhead; full trajectory warmup, reset, graph capture, state readback and rendering excluded; synchronized GPU boundaries.",
        }
        (output / "result.json").write_text(json.dumps(result, indent=2))
        return result
    finally:
        cleanup()


def main(args):
    if args.engine not in ("mujoco", "mujoco-warp", "genesis"):
        raise ValueError("Throughput engines: mujoco, mujoco-warp, genesis")
    batches = (1,) if args.engine == "mujoco" else BATCHES
    if args.case_index is not None:
        batches = (batches[args.case_index],)
    if args.plan_only:
        print(json.dumps({"engine": args.engine, "batches": batches}))
        return 0
    from ..cli import environment
    from .suite import source_hashes

    manifest = {
        "engine": args.engine,
        "cases": [{"id": f"batch-{b}", "family": "throughput", "batch": b} for b in batches],
        "source_hashes": source_hashes(),
    }
    if args.output.exists():
        if not args.resume or json.loads((args.output / "manifest.json").read_text()) != manifest:
            raise ValueError("Resume requires identical throughput source and batch plan")
    else:
        args.output.mkdir(parents=True)
        (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2))
        (args.output / "environment.json").write_text(
            json.dumps(environment(args.engine), indent=2)
        )
    results = []
    for batch in batches:
        directory = args.output / f"batch-{batch}"
        attempts = sorted(directory.glob("attempt-*/result.json"))
        if attempts:
            directory = attempts[-1].parent
        if (directory / "result.json").exists() and args.resume:
            r = json.loads((directory / "result.json").read_text())
        else:
            directory = args.output / f"batch-{batch}"
            if directory.exists():
                directory = directory / f"attempt-{len(list(directory.glob('attempt-*'))) + 1:04d}"
            # An OOM in a native runtime must not contaminate subsequent batch sizes.
            cmd = [
                sys.executable,
                "-m",
                __name__,
                "--engine",
                args.engine,
                "--batch",
                str(batch),
                "--output",
                str(directory),
            ]
            with (args.output / f"batch-{batch}.log").open("w") as log:
                process = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)
            if (directory / "result.json").exists():
                r = json.loads((directory / "result.json").read_text())
            else:
                directory.mkdir(exist_ok=True)
                r = {
                    "engine": args.engine,
                    "batch": batch,
                    "status": "error",
                    "error": f"Process exit {process.returncode}; inspect batch log",
                }
                (directory / "result.json").write_text(json.dumps(r, indent=2))
        r["case"] = {"id": f"batch-{batch}", "family": "throughput", "batch": batch}
        r["artifact_directory"] = str(directory.relative_to(args.output))
        (directory / "result.json").write_text(json.dumps(r, indent=2))
        results.append(r)
        (args.output / "results.json").write_text(json.dumps(results, indent=2))
        print(args.engine, batch, r["status"], flush=True)
    # Check the same trajectory checkpoints against the engine's independent single-world run.
    baseline_result = next((r for r in results if r["batch"] == 1), None)
    baseline = (
        args.output / baseline_result["artifact_directory"] / "verification.npz"
        if baseline_result
        else args.output / "batch-1/verification.npz"
    )
    if baseline.exists():
        with np.load(baseline) as data:
            gold = data["sampled_warmup_q"][:, 0]
        for r in results:
            p = args.output / r["artifact_directory"]
            if r["status"] != "completed":
                continue
            with np.load(p / "verification.npz") as data:
                error = float(np.max(abs(data["sampled_warmup_q"] - gold[:, None])))
            r["max_single_world_equivalence_error_rad"] = error
            r["trajectory_validated"] = error < 1e-4
            (p / "result.json").write_text(json.dumps(r, indent=2))
        (args.output / "results.json").write_text(json.dumps(results, indent=2))
    return int(
        any(r["status"] != "completed" or not r.get("trajectory_validated", False) for r in results)
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--engine", required=True)
    p.add_argument("--batch", type=int, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    try:
        measure(a.engine, a.batch, a.output)
    except Exception as exc:
        a.output.mkdir(parents=True, exist_ok=True)
        (a.output / "error.txt").write_text(traceback.format_exc())
        (a.output / "result.json").write_text(
            json.dumps(
                {
                    "engine": a.engine,
                    "batch": a.batch,
                    "case": {"family": "throughput", "batch": a.batch},
                    "status": "error",
                    "error": str(exc),
                },
                indent=2,
            )
        )
        raise
