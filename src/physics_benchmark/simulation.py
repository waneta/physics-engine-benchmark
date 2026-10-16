"""Measure solver forces on the same interval as the integrated state change."""

from dataclasses import dataclass

import mujoco
import numpy as np

from .scenes import build_model


@dataclass
class Run:
    rows: list[dict]
    imported: dict
    xml: str


def contact_force_world(model, data, body_id: int) -> np.ndarray:
    """Sum forces ON the target body; MuJoCo's frame rows are contact axes."""
    total = np.zeros(3)
    wrench = np.zeros(6)
    for index in range(data.ncon):
        contact = data.contact[index]
        first = model.geom_bodyid[contact.geom[0]] == body_id
        second = model.geom_bodyid[contact.geom[1]] == body_id
        if first == second:
            continue
        mujoco.mj_contactForce(model, data, index, wrench)
        force = contact.frame.reshape(3, 3).T @ wrench[:3]
        total += force if second else -force
    return total


def cube_penetration(qpos: np.ndarray, side: float) -> float:
    rotation = np.empty(9)
    mujoco.mju_quat2Mat(rotation, qpos[3:7])
    lowest_z = qpos[2] - side / 2 * np.abs(rotation.reshape(3, 3)[2]).sum()
    return float(max(0.0, -lowest_z))


def simulate(scene: str, cfg: dict, dt: float, rows: list[dict] | None = None, on_sample=None) -> Run:
    """Fresh model/data each run. A supplied rows list retains samples on failure."""
    model, data, imported, xml = build_model(scene, cfg, dt)
    rows = [] if rows is None else rows
    body = model.body("object").id
    count = round(cfg["durations_s"][scene] / dt)
    pulse_start = round(cfg["pulse_start_s"] / dt)
    pulse_end = round(cfg["pulse_end_s"] / dt)
    for step in range(count):
        q_before, v_before = data.qpos.copy(), data.qvel.copy()
        # Integer boundaries keep a pulse from drifting by a step with float time.
        torque = (
            cfg["pulse_torque_nm"] if scene == "hinge" and pulse_start <= step < pulse_end else 0
        )
        data.qfrc_applied[:] = 0
        if scene == "hinge":
            data.qfrc_applied[0] = torque
        mujoco.mj_step1(model, data)
        mujoco.mj_step2(model, data)
        # Contacts and efc_force still describe t_start, while qpos/qvel are at t_end.
        # Never call mj_forward here: that would overwrite the force used for this step.
        force = contact_force_world(model, data, body)
        row = {
            "step": step,
            "t_start_s": step * dt,
            "t_end_s": (step + 1) * dt,
            "contacts": data.ncon,
            "applied_torque_nm": torque,
        }
        for label, before, after in (("qpos", q_before, data.qpos), ("qvel", v_before, data.qvel)):
            for index in range(len(before)):
                row[f"{label}{index}_start"] = float(before[index])
                row[f"{label}{index}_end"] = float(after[index])
        for axis, value in zip("xyz", force):
            row[f"contact_f{axis}_n"] = float(value)
            row[f"contact_j{axis}_ns"] = float(value * dt)
        row["contact_force_norm_n"] = float(np.linalg.norm(force))
        if scene != "hinge":
            net = force + model.body_mass[body] * model.opt.gravity
            residual = model.body_mass[body] * (data.qvel[:3] - v_before[:3]) - net * dt
            row["net_fz_n"] = float(net[2])
            row["momentum_residual_ns"] = float(np.linalg.norm(residual))
            row["constraint_force_error_n"] = float(
                np.linalg.norm(force - data.qfrc_constraint[:3])
            )
            row["penetration_start_m"] = cube_penetration(q_before, cfg["cube_side_m"])
            row["penetration_end_m"] = cube_penetration(data.qpos, cfg["cube_side_m"])
        if not all(np.isfinite(value) for value in row.values()):
            raise RuntimeError(f"non-finite sample at step {step}")
        rows.append(row)
        if any(w.number for w in data.warning):
            raise RuntimeError(f"MuJoCo warning at step {step}: {data.warning}")
        if not np.isclose(data.time, (step + 1) * dt, atol=1e-10, rtol=0):
            raise RuntimeError(f"engine time reset or drift at step {step}")
        if on_sample is not None:
            on_sample(row)
    return Run(rows, imported, xml)
