"""Explicit scene construction and post-import physical-parameter checks."""

import json
import math
from pathlib import Path

import mujoco
import numpy as np

SCENES = ("slide", "drop", "hinge")


def load_config(path: Path) -> dict:
    cfg = json.loads(path.read_text())
    positive = (
        "gravity_m_s2",
        "cube_mass_kg",
        "cube_side_m",
        "drop_height_m",
        "hinge_mass_kg",
        "hinge_length_m",
        "hinge_width_m",
        "stop_speed_m_s",
        "impulse_window_s",
        "momentum_tolerance_ns",
        "solver_tolerance",
    )
    for key in positive:
        if not math.isfinite(cfg[key]) or cfg[key] <= 0:
            raise ValueError(f"{key} must be finite and positive")
    for key in ("slide_speed_m_s", "sliding_friction"):
        if not math.isfinite(cfg[key]) or cfg[key] < 0:
            raise ValueError(f"{key} must be finite and nonnegative")
    for key in ("hinge_initial_angle_rad", "pulse_torque_nm"):
        if not math.isfinite(cfg[key]):
            raise ValueError(f"{key} must be finite")
    if not isinstance(cfg["solver_iterations"], int) or cfg["solver_iterations"] <= 0:
        raise ValueError("solver_iterations must be a positive integer")
    if cfg["drop_height_m"] <= cfg["cube_side_m"] / 2:
        raise ValueError("drop must start above the floor")
    if not 0 <= cfg["pulse_start_s"] < cfg["pulse_end_s"] <= cfg["durations_s"]["hinge"]:
        raise ValueError("pulse must lie within the hinge episode")
    sr, si = cfg["contact_solref"], cfg["contact_solimp"]
    if len(sr) != 2 or not all(math.isfinite(x) and x > 0 for x in sr):
        raise ValueError("contact_solref must contain two positive values")
    if (
        len(si) != 5
        or not all(math.isfinite(x) for x in si)
        or not 0 < si[0] <= si[1] < 1
        or si[2] <= 0
        or not 0 < si[3] < 1
        or si[4] < 1
    ):
        raise ValueError("invalid contact_solimp")
    for scene in SCENES:
        duration = cfg["durations_s"][scene]
        steps = cfg["timesteps_s"][scene]
        if not math.isfinite(duration) or duration <= 0 or not steps:
            raise ValueError(f"invalid duration/timesteps for {scene}")
        if len(set(steps)) != len(steps):
            raise ValueError(f"duplicate timesteps for {scene}")
        for dt in steps:
            if not math.isfinite(dt) or dt <= 0 or dt > duration:
                raise ValueError(f"invalid timestep for {scene}")
            boundaries = [duration]
            if scene == "hinge":
                boundaries += [cfg["pulse_start_s"], cfg["pulse_end_s"]]
            if any(
                not math.isclose(t / dt, round(t / dt), abs_tol=1e-8, rel_tol=0) for t in boundaries
            ):
                raise ValueError(f"{scene}: duration and pulse boundaries must align to dt={dt}")
            if scene != "hinge" and sr[0] < 2 * dt:
                raise ValueError("solref time constant must be >= 2*dt to avoid silent clamping")
    return cfg


def scene_xml(scene: str, cfg: dict, dt: float) -> str:
    if scene not in SCENES:
        raise ValueError(f"unknown scene: {scene}")
    half = cfg["cube_side_m"] / 2
    sr = " ".join(map(str, cfg["contact_solref"]))
    si = " ".join(map(str, cfg["contact_solimp"]))
    if scene == "hinge":
        length, width = cfg["hinge_length_m"], cfg["hinge_width_m"]
        body = f'''<body name="object" pos="0 0 0.5">
          <joint name="hinge" type="hinge" axis="0 1 0" limited="false"
                 damping="0" armature="0" frictionloss="0"/>
          <geom name="object_geom" type="box" pos="0 0 {-length / 2}"
                size="{width / 2} {width / 2} {length / 2}" mass="{cfg["hinge_mass_kg"]}"
                contype="0" conaffinity="0"/>
        </body>'''
        floor = ""
    else:
        height = half if scene == "slide" else cfg["drop_height_m"]
        body = f'''<body name="object" pos="0 0 {height}">
          <freejoint name="free"/>
          <geom name="object_geom" type="box" size="{half} {half} {half}"
                mass="{cfg["cube_mass_kg"]}"/>
        </body>'''
        floor = '<geom name="floor" type="plane" size="2 2 0.1"/>'
    return f'''<mujoco model="{scene}">
      <compiler angle="radian"/>
      <option timestep="{dt}" gravity="0 0 {-cfg["gravity_m_s2"]}"
              integrator="Euler" solver="Newton" cone="elliptic"
              iterations="{cfg["solver_iterations"]}" tolerance="{cfg["solver_tolerance"]}"/>
      <default><geom condim="3" friction="{cfg["sliding_friction"]} 0 0"
                     solref="{sr}" solimp="{si}" margin="0" gap="0"/></default>
      <worldbody>{floor}{body}</worldbody>
    </mujoco>'''


def build_model(scene: str, cfg: dict, dt: float):
    xml = scene_xml(scene, cfg, dt)
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    if scene == "slide":
        data.qvel[0] = cfg["slide_speed_m_s"]
    elif scene == "hinge":
        data.qpos[0] = cfg["hinge_initial_angle_rad"]
    mujoco.mj_forward(model, data)
    body = model.body("object").id
    mass = cfg["hinge_mass_kg"] if scene == "hinge" else cfg["cube_mass_kg"]
    if scene == "hinge":
        w, length = cfg["hinge_width_m"], cfg["hinge_length_m"]
        expected_inertia = mass / 12 * np.array([w * w + length * length] * 2 + [2 * w * w])
        expected_com = [0, 0, -length / 2]
        np.testing.assert_allclose(model.jnt_axis[0], [0, 1, 0], atol=1e-12)
        np.testing.assert_allclose(
            data.xipos[body],
            [-length / 2 * np.sin(data.qpos[0]), 0, 0.5 - length / 2 * np.cos(data.qpos[0])],
            atol=1e-12,
        )
    else:
        expected_inertia = np.full(3, mass * cfg["cube_side_m"] ** 2 / 6)
        expected_com = [0, 0, 0]
    rotation = np.empty(9)
    mujoco.mju_quat2Mat(rotation, model.body_iquat[body])
    rotation = rotation.reshape(3, 3)
    inertia_body = rotation @ np.diag(model.body_inertia[body]) @ rotation.T
    np.testing.assert_allclose(model.body_mass[body], mass, atol=1e-12)
    np.testing.assert_allclose(inertia_body, np.diag(expected_inertia), atol=1e-12)
    np.testing.assert_allclose(model.body_ipos[body], expected_com, atol=1e-12)
    geom = model.geom("object_geom").id
    expected_size = (
        [cfg["hinge_width_m"] / 2, cfg["hinge_width_m"] / 2, cfg["hinge_length_m"] / 2]
        if scene == "hinge"
        else [cfg["cube_side_m"] / 2] * 3
    )
    np.testing.assert_allclose(model.geom_size[geom], expected_size, atol=1e-12)
    np.testing.assert_allclose(
        model.geom_friction[geom], [cfg["sliding_friction"], 0, 0], atol=1e-12
    )
    np.testing.assert_allclose(model.geom_solref[geom], cfg["contact_solref"], atol=1e-12)
    np.testing.assert_allclose(model.geom_solimp[geom], cfg["contact_solimp"], atol=1e-12)
    np.testing.assert_array_equal(model.dof_damping, 0)
    np.testing.assert_array_equal(model.dof_armature, 0)
    np.testing.assert_array_equal(model.dof_frictionloss, 0)
    imported = {
        "mass_kg": float(model.body_mass[body]),
        "com_local_m": model.body_ipos[body].tolist(),
        "inertia_body_kg_m2": inertia_body.tolist(),
        "joint_axis": model.jnt_axis.tolist(),
        "joint_position": model.jnt_pos.tolist(),
        "joint_limited": model.jnt_limited.tolist(),
        "damping": model.dof_damping.tolist(),
        "armature": model.dof_armature.tolist(),
        "frictionloss": model.dof_frictionloss.tolist(),
        "geom_friction": model.geom_friction.tolist(),
        "geom_solref": model.geom_solref.tolist(),
        "geom_solimp": model.geom_solimp.tolist(),
        "geom_size": model.geom_size.tolist(),
        "geom_condim": model.geom_condim.tolist(),
        "geom_margin": model.geom_margin.tolist(),
        "geom_gap": model.geom_gap.tolist(),
        "geom_contype": model.geom_contype.tolist(),
        "geom_conaffinity": model.geom_conaffinity.tolist(),
        "gravity_m_s2": model.opt.gravity.tolist(),
        "timestep_s": model.opt.timestep,
        "integrator": "Euler",
        "solver": "Newton",
        "cone": "elliptic",
        "iterations": model.opt.iterations,
        "tolerance": model.opt.tolerance,
        "initial_qpos": data.qpos.tolist(),
        "initial_qvel": data.qvel.tolist(),
        "validation": "passed",
    }
    return model, data, imported, xml
