"""Task outcome and numerical validity are separate measurements."""

import numpy as np

from .model import LIMIT, rotation


def evaluate(scene, a, status):
    result = {"numerically_valid": status in ("completed", "overload"), "task_success": False}
    if not len(a["time"]):
        return result
    t = a["time"]
    p = a["position"]
    family = scene.case["family"]
    m = scene.model
    result["simulated_seconds"] = float(t[-1])
    result["max_fk_error_m"] = float(a["fk_error"].max())
    result["peak_contact_force_n"] = float(
        np.linalg.norm(a["contact_wrench"][..., :3], axis=-1).max()
    )
    if scene.controlled:
        idx = np.minimum(
            np.rint(t / scene.reference["dt"]).astype(int), len(scene.reference["q"]) - 1
        )
        diff = a["q"][:, : scene.controlled] - scene.reference["q"][idx]
        result["joint_rmse_rad"] = float(np.sqrt(np.mean(diff[:, :7] ** 2)))
        result["normalized_squared_arm_effort"] = float(
            np.mean((a["command"][:, :7] / LIMIT[:7]) ** 2)
        )
        # Original arm limits remain monitored even when their enforcement is disabled.
        lo = m.jnt_range[:7, 0]
        hi = m.jnt_range[:7, 1]
        result["joint_limit_excess_rad"] = float(
            np.maximum(np.maximum(lo - a["q"][:, :7], a["q"][:, :7] - hi), 0).max()
        )
    checks = {}
    for name in scene.objects:
        b = m.body(name).id
        j = int(m.body_jntadr[b])
        dof = int(m.jnt_dofadr[j])
        mass = m.body_mass[b]
        velocity = a["v"][:, dof : dof + 3]
        residual = (
            mass * np.diff(velocity, axis=0)
            - (a["contact_wrench"][1:, b, :3] + mass * m.opt.gravity) * np.diff(t)[:, None]
        )
        checks[name] = float(np.max(np.linalg.norm(residual, axis=1))) if len(residual) else 0.0
    result["max_momentum_residual_ns"] = checks
    result["contact_force_validated"] = all(x <= 5e-6 for x in checks.values()) if checks else None
    complete = status == "completed"
    if family in ("panda_open_loop", "panda_tracking", "collision_chain", "throughput"):
        result["task_success"] = complete
    elif family in ("grasp", "stack"):
        b = m.body("cube").id
        z = p[:, b, 2]
        hold = (t >= 1.8) & (t <= 2.3)
        result["maximum_lift_m"] = float(z.max() - z[0])
        result["minimum_hold_lift_m"] = float(np.min(z[hold]) - z[0]) if hold.any() else 0.0
        result["task_success"] = bool(complete and result["minimum_hold_lift_m"] >= 0.05)
        if family == "stack":
            base = m.body("lower_cube").id
            rel = p[-1, b] - p[-1, base]
            tail = t >= t[-1] - 0.5
            speed = np.linalg.norm(np.diff(p[tail, b], axis=0) / np.diff(t[tail])[:, None], axis=1)
            result["final_relative_position_m"] = rel.tolist()
            result["settled"] = bool(len(speed) and speed.max() < 0.01)
            result["task_success"] = bool(
                complete
                and abs(rel[0]) <= 0.0205
                and abs(rel[1]) <= 0.0205
                and 0.035 <= rel[2] <= 0.045
                and result["settled"]
            )
    elif family == "push":
        ids = [m.body(name).id for name in scene.objects]
        x = p[-1, ids, 0]
        goal = scene.parameters["goal_x"]
        result["passed_objects"] = int(np.count_nonzero(x >= goal))
        result["minimum_progress_m"] = float(np.min(x - p[0, ids, 0]))
        result["minimum_capped_goal_progress_m"] = float(np.min(np.minimum(x, goal) - p[0, ids, 0]))
        result["task_success"] = bool(complete and result["passed_objects"] == 3)
    elif family == "sweep":
        ids = [m.body(name).id for name in scene.objects]
        xyz = p[-1, ids]
        bounds = scene.parameters["tray_bounds"]
        inside = np.ones(len(ids), bool)
        for j in range(3):
            inside &= (xyz[:, j] >= bounds[2 * j]) & (xyz[:, j] <= bounds[2 * j + 1])
        result["objects_in_tray"] = int(inside.sum())
        result["task_success"] = bool(complete and inside.all())
    elif family == "insertion":
        b = m.body("hand").id
        tip = np.array(
            [
                xyz + rotation(q) @ scene.parameters["peg_tip_local"]
                for xyz, q in zip(p[:, b], a["quaternion"][:, b])
            ]
        )
        depth = scene.parameters["hole_center"][2] - tip[:, 2]
        tail = t >= scene.case["duration"] - 0.25
        result["final_insertion_depth_m"] = float(depth[-1])
        result["minimum_final_hold_depth_m"] = float(depth[tail].min()) if tail.any() else None
        result["task_success"] = bool(complete and tail.any() and depth[tail].min() >= 0.019)
    return result
