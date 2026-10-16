"""Native MuJoCo-Warp CUDA adapter (not the Newton wrapper)."""

from pathlib import Path

import numpy as np

from ..sampling import make_row
from ..scenes import build_model
from ..simulation import Run


def simulate(scene, cfg, dt, rows=None, on_sample=None):
    import mujoco_warp as mjw
    import warp as wp

    wp.config.kernel_cache_dir = str(Path(".cache/warp").resolve())
    wp.init()
    device = wp.get_device("cuda:0")
    if not device.is_cuda:
        raise RuntimeError("MuJoCo-Warp requires CUDA; no CPU fallback is allowed")
    rows = [] if rows is None else rows
    model, initial, imported, xml = build_model(scene, cfg, dt)
    with wp.ScopedDevice(device):
        gpu_model = mjw.put_model(model)
        for name in (
            "body_mass",
            "body_inertia",
            "body_ipos",
            "body_iquat",
            "dof_armature",
            "dof_damping",
            "dof_frictionloss",
            "jnt_axis",
            "jnt_pos",
            "geom_size",
            "geom_pos",
            "geom_friction",
            "geom_solref",
            "geom_solimp",
        ):
            actual = getattr(gpu_model, name).numpy()
            expected = np.asarray(getattr(model, name))
            np.testing.assert_allclose(
                actual.reshape(expected.shape), expected, rtol=2e-6, atol=1e-9
            )
            imported[f"gpu_{name}"] = actual.tolist()
        # Compile kernels with a disposable state, then allocate the measured initial state afresh.
        warmup = mjw.put_data(model, initial, naconmax=64, njmax=128)
        mjw.step(gpu_model, warmup)
        wp.synchronize()
        data = mjw.put_data(model, initial, naconmax=64, njmax=128)
        contact_ids = wp.array(np.arange(64, dtype=np.int32), dtype=wp.int32)
        contact_forces = wp.zeros(64, dtype=wp.spatial_vector)
        mjw.contact_force(gpu_model, warmup, contact_ids, True, contact_forces)
        wp.synchronize()
        with wp.ScopedCapture() as capture:
            mjw.step(gpu_model, data)
            mjw.contact_force(gpu_model, data, contact_ids, True, contact_forces)
        q_before = data.qpos.numpy()[0].copy()
        v_before = data.qvel.numpy()[0].copy()
        target = model.body("object").id
        gpu_body_ids = gpu_model.geom_bodyid.numpy().reshape(-1)
        np.testing.assert_array_equal(gpu_body_ids, model.geom_bodyid)
        command = np.zeros((1, model.nv), dtype=np.float32)
        for step in range(round(cfg["durations_s"][scene] / dt)):
            torque = (
                cfg["pulse_torque_nm"]
                if scene == "hinge"
                and (round(cfg["pulse_start_s"] / dt) <= step < round(cfg["pulse_end_s"] / dt))
                else 0.0
            )
            if scene == "hinge":
                command[0, 0] = torque
                data.qfrc_applied.assign(command)
            wp.capture_launch(capture.graph)
            wp.synchronize()
            ncon = int(data.nacon.numpy()[0])
            if ncon > 64 or int(data.nefc.numpy()[0]) > 128:
                raise RuntimeError("MuJoCo-Warp contact/constraint buffer overflow")
            forces = contact_forces.numpy()[:ncon, :3]
            geoms = data.contact.geom.numpy()[:ncon]
            total = np.zeros(3)
            for pair, force in zip(geoms, forces):
                first, second = (gpu_body_ids[int(g)] == target for g in pair)
                if first != second:
                    total += force if second else -force
            q_after, v_after = data.qpos.numpy()[0], data.qvel.numpy()[0]
            rows.append(
                make_row(
                    scene,
                    cfg,
                    dt,
                    step,
                    q_before,
                    v_before,
                    q_after,
                    v_after,
                    total,
                    ncon,
                    torque,
                    constraint_force=data.qfrc_constraint.numpy()[0, :3]
                    if scene != "hinge"
                    else None,
                )
            )
            q_before, v_before = q_after.copy(), v_after.copy()
            if on_sample is not None:
                on_sample(rows[-1])
    imported.update(
        engine="mujoco-warp",
        precision="float32",
        device=str(device),
        engine_version=mjw.__version__,
        warp_version=wp.__version__,
        force_source="mujoco_warp.contact_force(world frame), current integration step",
        contact_capacity=64,
        constraint_capacity=128,
        implementation_difference="Direct MuJoCo-Warp, not Newton/MuJoCo-Warp",
    )
    return Run(rows, imported, xml)
