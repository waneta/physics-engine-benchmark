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


def coulomb_reference(cfg, times):
    """Ideal translating block on a rigid horizontal plane, with no startup transient."""
    speed = cfg["slide_speed_m_s"]
    deceleration = cfg["sliding_friction"] * cfg["gravity_m_s2"]
    moving_time = np.minimum(times, speed / deceleration) if deceleration else times
    return (
        speed * moving_time - 0.5 * deceleration * moving_time**2,
        np.maximum(speed - deceleration * times, 0),
    )


def slide_friction_metrics(cfg, rows, times, first_contact):
    fx, fy, fz = (column(rows, f"contact_f{a}_n") for a in "xyz")
    vx, vy = (column(rows, f"qvel{i}_start") for i in range(2))
    horizontal_speed = np.hypot(vx, vy)
    tangential = np.hypot(fx, fy)
    # Exclude contact startup and the stopping tail; use the same mask in every engine.
    valid = (column(rows, "t_start_s") >= (first_contact or 0) + cfg["impulse_window_s"]) & (
        horizontal_speed > 10 * cfg["stop_speed_m_s"]
    )
    contact = valid & (fz > 1e-9)
    dt = times[1] - times[0]
    reference_x, reference_v = coulomb_reference(cfg, times)
    x = states(rows, "qpos0") - rows[0]["qpos0_start"]
    velocity = states(rows, "qvel0")
    for i, row in enumerate(rows):
        row.update(
            friction_force_n=float(tangential[i]),
            normal_force_n=float(fz[i]),
            friction_metric_sample=int(valid[i]),
            # Zero is only a raw plotting placeholder when there is no normal force.
            effective_friction_coefficient=float(tangential[i] / fz[i]) if fz[i] > 1e-9 else 0.0,
            reference_displacement_end_m=float(reference_x[i + 1]),
            reference_velocity_end_m_s=float(reference_v[i + 1]),
        )
    result = {
        "configured_friction_coefficient": cfg["sliding_friction"],
        "friction_measurement_samples": int(valid.sum()),
        "friction_contact_samples": int(contact.sum()),
        "mean_friction_force_n": float(tangential[valid].mean()) if valid.any() else None,
        "mean_normal_force_n": float(fz[valid].mean()) if valid.any() else None,
        "effective_friction_coefficient": float(tangential[contact].sum() / fz[contact].sum())
        if contact.any()
        else None,
        "mean_deceleration_m_s2": float((-np.diff(velocity) / dt)[valid].mean())
        if valid.any()
        else None,
        "friction_opposes_motion": bool(np.all((fx * vx + fy * vy)[valid] <= 1e-9))
        if valid.any()
        else None,
        "total_contact_jx_ns": float(column(rows, "contact_jx_ns").sum()),
        "max_displacement_error_m": float(np.max(np.abs(x - reference_x))),
        "rms_displacement_error_m": float(np.sqrt(np.mean((x - reference_x) ** 2))),
        "max_slide_velocity_error_m_s": float(np.max(np.abs(velocity - reference_v))),
        "max_lateral_displacement_m": float(
            np.max(np.abs(states(rows, "qpos1") - rows[0]["qpos1_start"]))
        ),
        "ideal_coulomb_stop_time_s": cfg["slide_speed_m_s"]
        / (cfg["sliding_friction"] * cfg["gravity_m_s2"])
        if cfg["sliding_friction"]
        else None,
    }
    return result


def drop_metrics(cfg, rows, times, first_contact):
    """Measure free fall, contact response and observed rigid-body settling separately."""
    height = states(rows, "qpos2")
    vertical_velocity = states(rows, "qvel2")
    linear = np.linalg.norm(np.column_stack([states(rows, f"qvel{i}") for i in range(3)]), axis=1)
    angular = np.linalg.norm(
        np.column_stack([states(rows, f"qvel{i}") for i in range(3, 6)]), axis=1
    )
    # The furthest vertex bounds the rotational contribution to surface velocity.
    radius = np.sqrt(3) * cfg["cube_side_m"] / 2
    normal = column(rows, "contact_fz_n")
    supported = np.r_[False, normal > 1e-9]
    resting = (
        (linear < cfg["stop_speed_m_s"]) & (angular * radius < cfg["stop_speed_m_s"]) & supported
    )
    settled = sustained_time(times, resting, first_contact) if first_contact is not None else None
    ideal_time = np.sqrt(2 * (cfg["drop_height_m"] - cfg["cube_side_m"] / 2) / cfg["gravity_m_s2"])
    reference_height = cfg["drop_height_m"] - cfg["gravity_m_s2"] * times**2 / 2
    reference_velocity = -cfg["gravity_m_s2"] * times
    free_fall = (
        times <= first_contact + 1e-12
        if first_contact is not None
        else np.ones(len(times), dtype=bool)
    )
    for i, row in enumerate(rows):
        row.update(
            free_fall_reference_height_end_m=float(reference_height[i + 1]),
            free_fall_reference_velocity_end_m_s=float(reference_velocity[i + 1]),
            free_fall_sample=int(free_fall[i + 1]),
        )
    active = np.flatnonzero(column(rows, "contact_force_norm_n") > 1e-9)
    post_velocity = vertical_velocity[active[0] + 1 :] if len(active) else None
    window = cfg["impulse_window_s"]
    tail_force = None
    if first_contact is not None and times[-1] - window >= first_contact - 1e-12:
        overlap = np.maximum(
            0,
            column(rows, "t_end_s") - np.maximum(column(rows, "t_start_s"), times[-1] - window),
        )
        tail_force = float(np.sum(normal * overlap) / window)
    displacement = np.hypot(
        states(rows, "qpos0") - rows[0]["qpos0_start"],
        states(rows, "qpos1") - rows[0]["qpos1_start"],
    )
    return {
        "first_contact_time_error_s": float(first_contact - ideal_time)
        if first_contact is not None
        else None,
        "preimpact_vertical_velocity_m_s": float(rows[active[0]]["qvel2_start"])
        if len(active)
        else None,
        "ideal_impact_vertical_velocity_m_s": float(-cfg["gravity_m_s2"] * ideal_time),
        "peak_rebound_vertical_velocity_m_s": float(max(0, post_velocity.max()))
        if post_velocity is not None
        else None,
        "max_free_fall_height_error_m": float(
            np.max(np.abs(height[free_fall] - reference_height[free_fall]))
        ),
        "max_free_fall_velocity_error_m_s": float(
            np.max(np.abs(vertical_velocity[free_fall] - reference_velocity[free_fall]))
        ),
        "final_com_height_m": float(height[-1]),
        "final_linear_speed_m_s": float(linear[-1]),
        "final_angular_speed_rad_s": float(angular[-1]),
        "rigid_settled_time_s": settled,
        "rest_observation_duration_s": float(times[-1] - settled) if settled is not None else None,
        "settled_within_duration": settled is not None,
        "settling_angular_speed_threshold_rad_s": float(cfg["stop_speed_m_s"] / radius),
        "mean_tail_normal_force_n": tail_force,
        "tail_support_weight_ratio": tail_force / (cfg["cube_mass_kg"] * cfg["gravity_m_s2"])
        if tail_force is not None
        else None,
        "max_horizontal_displacement_m": float(displacement.max()),
        "total_contact_jz_ns": float(column(rows, "contact_jz_ns").sum()),
    }


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
        metrics.update(slide_friction_metrics(cfg, rows, times, first))
        ideal = metrics["ideal_coulomb_distance_m"]
        metrics["stop_distance_error_percent"] = (
            100 * (metrics["stop_distance_m"] - ideal) / ideal
            if ideal and metrics["stop_distance_m"] is not None
            else None
        )
    else:
        metrics["minimum_com_height_m"] = float(states(rows, "qpos2").min())
        metrics["ideal_first_contact_s"] = float(
            np.sqrt(2 * (cfg["drop_height_m"] - cfg["cube_side_m"] / 2) / cfg["gravity_m_s2"])
        )
        metrics.update(drop_metrics(cfg, rows, times, first))
    return metrics
