"""Freeze a recovery batch, reuse compatible evidence, and serialize Isaac containers.

Reused records retain their original version, source hashes, and absolute provenance.
Insertion evidence from before the nullspace fix is excluded. Throughput is never reused.
"""

import argparse
import contextlib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = {"id", "phase", "candidate", "controller", "selected_by", "duration", "purpose"}


def physical_case(case):
    value = {k: v for k, v in case.items() if k not in META}
    value.setdefault("dt", 0.001)
    value.setdefault("repeat", 0)
    if value["family"] == "push":
        for key, default in (("kp_scale", 1), ("kd_scale", 1), ("push_duration", 3)):
            value.setdefault(key, default)
    return value


def compatible(row, manifest, environment, case, versions, hashes):
    if row["status"] not in ("completed", "overload", "inverted"):
        return False
    if physical_case(row["case"]) != physical_case(case):
        return False
    packages = environment.get("packages", {})
    if any(packages.get(name) != version for name, version in versions.items()):
        return False
    asset = "configs/assets/panda/source.xml"
    if manifest["source_hashes"].get(asset) != hashes.get(asset):
        return False
    # Only the insertion branch of the shared controller changed in this recovery.
    if case["family"] == "insertion":
        code = "src/physics_benchmark/extended/rigid.py"
        if manifest["source_hashes"].get(code) != hashes[code]:
            return False
    return True


def seed_stage(stage, engine, cases, inputs, versions, hashes):
    if stage.exists():
        return
    stage.mkdir(parents=True)
    manifest = {"engine": engine, "cases": cases, "source_hashes": hashes}
    if cases and not cases[0]["family"].startswith("soft_"):
        manifest["schema"] = 1
    (stage / "manifest.json").write_text(json.dumps(manifest, indent=2))
    candidates = []
    for source in inputs:
        for file in sorted(source.rglob("manifest.json")):
            previous = json.loads(file.read_text())
            env = file.parent / "environment.json"
            if previous.get("engine") != engine or not env.exists():
                continue
            environment = json.loads(env.read_text())
            for planned in previous.get("cases", []):
                trial = file.parent / planned["id"]
                attempts = sorted(trial.glob("attempt-*/result.json"))
                record = attempts[-1] if attempts else trial / "result.json"
                if not record.exists():
                    continue
                if not (record.parent / "trajectory.npz").exists():
                    continue
                candidates.append((record, previous, environment, env))
    reused = []
    for case in cases:
        matches = []
        for record, previous, environment, env in candidates:
            row = json.loads(record.read_text())
            if compatible(row, previous, environment, case, versions, hashes):
                matches.append((record.stat().st_mtime, record, row, previous, env))
        if not matches:
            continue
        _, source, row, previous, env = max(matches, key=lambda entry: entry[0])
        target = stage / case["id"]
        target.mkdir()
        for artifact in source.parent.iterdir():
            if artifact.is_file() and artifact.name not in ("result.json", "case.json"):
                (target / artifact.name).symlink_to(artifact.resolve())
        row["provenance"] = {
            "source_result": str(source.resolve()),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "source_case": row["case"],
            "source_hashes": previous["source_hashes"],
            "source_environment": str(env.resolve()),
            "reuse_note": "Identical physical inputs; retained observation, not an independent rerun.",
        }
        row["case"] = dict(case, duration=row["case"].get("duration", case.get("duration")))
        (target / "case.json").write_text(json.dumps(row["case"], indent=2))
        (target / "result.json").write_text(json.dumps(row, indent=2))
        reused.append({"id": case["id"], "source": str(source.resolve())})
    (stage / "reuse.json").write_text(json.dumps(reused, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input", type=Path, action="append", default=[])
    parser.add_argument("--genesis-python", type=Path, default=ROOT / ".venv-genesis/bin/python")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    output = args.output.absolute()
    inputs = [p.absolute() for p in args.input]
    request = {
        "inputs": list(map(str, inputs)),
        "genesis_python": str(args.genesis_python.absolute()),
    }
    if output.exists():
        if not args.resume or json.loads((output / "request.json").read_text()) != request:
            raise ValueError("Resume requires the same recovery request")
    else:
        output.mkdir(parents=True)
        (output / "request.json").write_text(json.dumps(request, indent=2))
        for directory in ("src", "scripts", "configs", "requirements"):
            shutil.copytree(
                ROOT / directory,
                output / "source" / directory,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
        (output / "source/.venv").symlink_to(ROOT / ".venv", target_is_directory=True)
    sys.path.insert(0, str(output / "source/src"))
    from physics_benchmark.extended.soft import cases as soft_cases
    from physics_benchmark.extended.suite import (
        heldout_cases,
        rigid_cases,
        select,
        source_hashes,
        transfer_cases,
        tuning_cases,
    )

    hashes = source_hashes()
    paths = {
        "mujoco": ROOT / ".venv/bin/python",
        "physx": ROOT / ".venv/bin/python",
        "mujoco-warp": ROOT / ".venv-warp/bin/python",
        "genesis": args.genesis_python.absolute(),
        "newton-vbd": ROOT / ".venv-newton/bin/python",
    }
    names = {
        "mujoco": ["mujoco"],
        "physx": ["mujoco"],
        "mujoco-warp": ["mujoco", "mujoco-warp", "warp-lang"],
        "genesis": ["mujoco", "genesis-world", "torch", "quadrants"],
        "newton-vbd": ["newton", "mujoco-warp", "warp-lang"],
    }
    versions = {
        e: json.loads(
            subprocess.check_output(
                [
                    str(paths[e]),
                    "-c",
                    "import json,importlib.metadata as m;print(json.dumps({n:m.version(n) for n in "
                    + repr(names[e])
                    + "}))",
                ],
                text=True,
            )
        )
        for e in paths
    }
    env = os.environ.copy()
    env.update(
        PYTHONPATH=str(output / "source/src"),
        PYTHONUNBUFFERED="1",
        MPLCONFIGDIR=str(ROOT / ".cache/matplotlib"),
    )
    logs = output / "logs"
    logs.mkdir(exist_ok=True)
    state_lock, heavy_lock, gpu_lock = threading.Lock(), threading.Lock(), threading.Lock()
    status_file = output / "status.json"
    status = json.loads(status_file.read_text()) if status_file.exists() else {"jobs": {}}
    if status.get("versions") and status["versions"] != versions:
        raise ValueError("Resume requires the same installed native package versions")
    status.update(pid=os.getpid(), versions=versions)
    planned_jobs = [
        (s, e)
        for e in ("mujoco", "physx", "mujoco-warp", "genesis")
        for s in ("rigid", "tuning", "soft", "transfer")
    ]
    planned_jobs += [("soft", "newton-vbd")]
    planned_jobs += [("throughput", e) for e in ("mujoco", "mujoco-warp", "genesis")]
    for scope, engine in planned_jobs:
        status["jobs"].setdefault(scope + "/" + engine, {"state": "queued"})

    def save():
        status["updated_at"] = datetime.now(UTC).isoformat()
        temporary = status_file.with_suffix(".tmp")
        temporary.write_text(json.dumps(status, indent=2))
        temporary.replace(status_file)

    def execute_job(scope, engine):
        key = scope + "/" + engine
        with state_lock:
            if status["jobs"].get(key, {}).get("state") == "completed":
                return
        with contextlib.ExitStack() as resources:
            if engine == "physx" or scope == "soft":
                resources.enter_context(heavy_lock)
            if engine in ("mujoco-warp", "genesis", "newton-vbd") or (
                engine == "physx" and scope == "soft"
            ):
                resources.enter_context(gpu_lock)
            stage = output / scope / engine
            with state_lock:
                status["jobs"][key] = {
                    "state": "running",
                    "started_at": datetime.now(UTC).isoformat(),
                }
                save()
            if scope != "throughput":
                cases = (
                    rigid_cases()
                    if scope == "rigid"
                    else tuning_cases()
                    if scope == "tuning"
                    else soft_cases(engine)
                    if scope == "soft"
                    else transfer_cases(output / "tuning")[0]
                )
                seed_stage(
                    stage,
                    engine,
                    cases,
                    inputs + [output / "rigid", output / "tuning"],
                    versions[engine],
                    hashes,
                )
                if not (stage / "environment.json").exists():
                    (stage / "environment.json").write_text(
                        subprocess.check_output(
                            [
                                str(paths[engine]),
                                "-c",
                                "import json;from physics_benchmark.cli import environment;print(json.dumps(environment("
                                + repr(engine)
                                + ")))",
                            ],
                            env=env,
                            cwd=ROOT,
                            text=True,
                        )
                    )
                if scope == "tuning":
                    cached = [
                        json.loads((stage / c["id"] / "result.json").read_text())
                        for c in cases
                        if (stage / c["id"] / "result.json").exists()
                    ]
                    if len([r for r in cached if r["case"].get("phase") == "train"]) == 81:
                        try:
                            validation = heldout_cases(select(cached))
                        except ValueError as exc:
                            if str(exc) != "No candidate passed all three training validity gates":
                                raise
                            validation = [
                                c
                                for c in heldout_cases(
                                    {"kp_scale": 1, "kd_scale": 1, "push_duration": 3}
                                )
                                if c["controller"] == "baseline"
                            ]
                        heldout = stage / "heldout"
                        seed_stage(heldout, engine, validation, inputs, versions[engine], hashes)
                        if not (heldout / "environment.json").exists():
                            shutil.copy2(stage / "environment.json", heldout / "environment.json")
            command = [
                str(paths[engine]),
                "-u",
                "-m",
                "physics_benchmark.extended.suite",
                scope,
                "--engine",
                engine,
                "--output",
                str(stage),
            ]
            if stage.exists():
                command.append("--resume")
            if scope == "transfer":
                command += ["--selection-root", str(output / "tuning")]
            with (logs / (scope + "-" + engine + ".log")).open("a") as log:
                code = subprocess.run(
                    command, env=env, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=False
                ).returncode
            # Held-out cases depend on selection and are prepared by the native suite.
            with state_lock:
                status["jobs"][key].update(
                    state="completed" if code == 0 else "error",
                    exit_code=code,
                    finished_at=datetime.now(UTC).isoformat(),
                )
                save()
            print(key, code, flush=True)

    def job(scope, engine):
        try:
            execute_job(scope, engine)
        except Exception as exc:  # noqa: BLE001 - keep other independent engine jobs running
            key = scope + "/" + engine
            (logs / (scope + "-" + engine + "-runner-error.txt")).write_text(traceback.format_exc())
            with state_lock:
                status["jobs"][key].update(
                    state="error", error=str(exc), finished_at=datetime.now(UTC).isoformat()
                )
                save()
            print(key, "runner error:", exc, flush=True)

    save()

    def accuracy(engine):
        for scope in ("rigid", "tuning", "soft"):
            job(scope, engine)

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(accuracy, e) for e in ("mujoco", "physx")]

        def gpu_accuracy():
            for e in ("mujoco-warp", "genesis"):
                for scope in ("rigid", "tuning"):
                    job(scope, e)
            for e in ("mujoco-warp", "genesis", "newton-vbd"):
                job("soft", e)

        futures.append(pool.submit(gpu_accuracy))
        for future in futures:
            future.result()
        futures = [pool.submit(job, "transfer", e) for e in ("mujoco", "physx")]
        for e in ("mujoco-warp", "genesis"):
            job("transfer", e)
        for future in futures:
            future.result()
    for e in ("mujoco", "mujoco-warp", "genesis"):
        job("throughput", e)
    subprocess.run(
        [
            str(paths["mujoco"]),
            "-m",
            "physics_benchmark.extended.suite",
            "report",
            "--output",
            str(output),
        ],
        env=env,
        cwd=ROOT,
        check=True,
    )
    return int(any(j["state"] != "completed" for j in status["jobs"].values()))


if __name__ == "__main__":
    raise SystemExit(main())
