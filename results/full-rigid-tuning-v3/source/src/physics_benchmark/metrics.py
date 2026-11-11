"""Physical metrics and an independent nonlinear rigid-pendulum ODE reference."""

import itertools

import numpy as np


def column(rows, name):
    return np.array([r[name] for r in rows], dtype=float)


def states(rows, name):
    return np.r_[rows[0][name + "_start"], column(rows, name + "_end")]


def sustained_time(times, mask, earliest=0.0):
    """First sampled time whose entire remaining trajectory satisfies mask."""
    suffix = np.logical_and.accumulate(mask[::-1])[::-1]
    valid = np.flatnonzero(suffix & (times >= earliest))
    return float(times[valid[0]]) if len(valid) else None


def hinge_reference(cfg, times, max_step=0.00005):
    """RK4 numerical solution of I*theta'' = tau - m*g*l/2*sin(theta).

    The torque is held constant per subinterval, with exact splits at discontinuities.
    This is an independent ODE reference, not a closed-form analytical solution.
    """
    mass, length, width = (cfg[k] for k in ("hinge_mass_kg", "hinge_length_m", "hinge_width_m"))
    inertia = mass * (length**2 / 3 + width**2 / 12)
    gravity_torque = mass * cfg["gravity_m_s2"] * length / 2
    pulse_start, pulse_end = cfg["pulse_start_s"], cfg["pulse_end_s"]
    state = np.array([cfg["hinge_initial_angle_rad"], 0.0])
    result = [state.copy()]

    def rhs(y, torque):
        return np.array([y[1], (torque - gravity_torque * np.sin(y[0])) / inertia])

    for start, end in itertools.pairwise(times):
        boundaries = [start] + [t for t in (pulse_start, pulse_end) if start < t < end] + [end]
        for left, right in itertools.pairwise(boundaries):
            torque = cfg["pulse_torque_nm"] if pulse_start <= (left + right) / 2 < pulse_end else 0
            n = max(1, int(np.ceil((right - left) / max_step)))
            h = (right - left) / n
            for _ in range(n):
                k1 = rhs(state, torque)
                k2 = rhs(state + h * k1 / 2, torque)
                k3 = rhs(state + h * k2 / 2, torque)
                k4 = rhs(state + h * k3, torque)
                state += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        result.append(state.copy())
    return np.array(result)


def measure(scene, cfg, rows):
    dt = rows[0]["t_end_s"] - rows[0]["t_start_s"]
    times = np.r_[0.0, column(rows, "t_end_s")]
    metrics = {"scene": scene, "dt_s": dt, "steps": len(rows)}
    if scene == "hinge":
        ref = hinge_reference(cfg, times)
        theta, omega = states(rows, "qpos0"), states(rows, "qvel0")
        metrics.update(
            max_angle_error_rad=float(np.max(np.abs(theta - ref[:, 0]))),
            rms_angle_error_rad=float(np.sqrt(np.mean((theta - ref[:, 0]) ** 2))),
            max_velocity_error_rad_s=float(np.max(np.abs(omega - ref[:, 1]))),
            torque_impulse_nms=float(column(rows, "applied_torque_nm").sum() * dt),
        )
        for index, row in enumerate(rows):
            row["reference_angle_start_rad"] = float(ref[index, 0])
            row["reference_angle_end_rad"] = float(ref[index + 1, 0])
            row["reference_velocity_end_rad_s"] = float(ref[index + 1, 1])
        return metrics
    velocities = np.column_stack([states(rows, f"qvel{i}") for i in range(3)])
    speed = np.linalg.norm(velocities, axis=1)
    active = np.flatnonzero(column(rows, "contact_force_norm_n") > 1e-9)
    first = float(rows[active[0]]["t_start_s"]) if len(active) else None
    metrics.update(
        peak_contact_force_n=float(column(rows, "contact_force_norm_n").max()),
        peak_contact_fz_n=float(column(rows, "contact_fz_n").max()),
        max_penetration_m=float(
            max(column(rows, "penetration_start_m").max(), column(rows, "penetration_end_m").max())
        ),
        first_contact_s=first,
        settled_time_s=sustained_time(times, speed < cfg["stop_speed_m_s"], first)
        if first is not None
        else None,
        max_momentum_residual_ns=float(column(rows, "momentum_residual_ns").max()),
        max_constraint_force_error_n=float(column(rows, "constraint_force_error_n").max())
        if "constraint_force_error_n" in rows[0]
        else None,
    )
    # Integrate only the overlap with [first_contact, first_contact + window].
    # For a partial final step, use its solver force as a constant step-average force.
    window = cfg["impulse_window_s"]
    if first is not None and first + window <= times[-1] + 1e-12:
        overlap = np.maximum(
            0,
            np.minimum(column(rows, "t_end_s"), first + window)
            - np.maximum(column(rows, "t_start_s"), first),
        )
        for axis in "xyz":
            metrics[f"window_contact_j{axis}_ns"] = float(
                np.sum(column(rows, f"contact_f{axis}_n") * overlap)
            )
        metrics["impulse_window_complete"] = True
    else:
        metrics.update({f"window_contact_j{a}_ns": None for a in "xyz"})
        metrics["impulse_window_complete"] = False
    if scene == "slide":
        stop = sustained_time(times, np.abs(velocities[:, 0]) < cfg["stop_speed_m_s"])
        x = states(rows, "qpos0")
        metrics.update(
            stop_time_s=stop,
            stop_distance_m=float(x[np.searchsorted(times, stop)] - x[0])
            if stop is not None
            else None,
            final_displacement_m=float(x[-1] - x[0]),
            max_com_lift_m=float(states(rows, "qpos2").max() - cfg["cube_side_m"] / 2),
            ideal_coulomb_distance_m=cfg["slide_speed_m_s"] ** 2
            / (2 * cfg["sliding_friction"] * cfg["gravity_m_s2"])
            if cfg["sliding_friction"]
            else None,
        )
    else:
        metrics["minimum_com_height_m"] = float(states(rows, "qpos2").min())
        metrics["ideal_first_contact_s"] = float(
            np.sqrt(2 * (cfg["drop_height_m"] - cfg["cube_side_m"] / 2) / cfg["gravity_m_s2"])
        )
    return metrics
