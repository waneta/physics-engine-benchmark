"""Common SI sample schema; measured forces are never inferred from velocity changes."""

import numpy as np

from .simulation import cube_penetration


def make_row(
    scene,
    cfg,
    dt,
    step,
    q_before,
    v_before,
    q_after,
    v_after,
    force,
    contacts,
    torque,
    constraint_force=None,
    native_impulse=None,
):
    force = np.asarray(force, dtype=float)
    impulse = force * dt if native_impulse is None else np.asarray(native_impulse, dtype=float)
    row = {
        "step": step,
        "t_start_s": step * dt,
        "t_end_s": (step + 1) * dt,
        "contacts": int(contacts),
        "applied_torque_nm": float(torque),
    }
    for label, before, after in (("qpos", q_before, q_after), ("qvel", v_before, v_after)):
        for index in range(len(before)):
            row[f"{label}{index}_start"] = float(before[index])
            row[f"{label}{index}_end"] = float(after[index])
    for i, axis in enumerate("xyz"):
        row[f"contact_f{axis}_n"] = float(force[i])
        row[f"contact_j{axis}_ns"] = float(impulse[i])
    row["contact_force_norm_n"] = float(np.linalg.norm(force))
    if scene != "hinge":
        mass = cfg["cube_mass_kg"]
        gravity = np.array([0, 0, -cfg["gravity_m_s2"]])
        net = force + mass * gravity
        residual = (
            mass * (np.asarray(v_after[:3]) - np.asarray(v_before[:3]))
            - impulse
            - mass * gravity * dt
        )
        row["net_fz_n"] = float(net[2])
        row["momentum_residual_ns"] = float(np.linalg.norm(residual))
        if constraint_force is not None:
            row["constraint_force_error_n"] = float(np.linalg.norm(force - constraint_force))
        row["penetration_start_m"] = cube_penetration(np.asarray(q_before), cfg["cube_side_m"])
        row["penetration_end_m"] = cube_penetration(np.asarray(q_after), cfg["cube_side_m"])
    if not all(np.isfinite(v) for v in row.values()):
        raise RuntimeError(f"Nonfinite sample at step {step}")
    return row
