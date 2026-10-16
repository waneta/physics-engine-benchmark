"""Genesis CUDA rigid solver with native contact-force sampling."""

import importlib.metadata
import os
from pathlib import Path
from xml.etree import ElementTree

import mujoco
import numpy as np

from ..sampling import make_row
from ..scenes import build_model
from ..simulation import Run


def array(value):
    return value.detach().cpu().numpy().copy() if hasattr(value, "detach") else np.asarray(value)


def rotation(quat):
    result = np.empty(9)
    mujoco.mju_quat2Mat(result, np.asarray(quat, dtype=float))
    return result.reshape(3, 3)


def simulate(scene, cfg, dt, rows=None, on_sample=None):
    os.environ.setdefault("GS_CACHE_FILE_PATH", str(Path(".cache/genesis").resolve()))
    import genesis as gs

    if not gs._initialized:
        gs.init(backend=gs.cuda, precision="64", logging_level="warning", seed=0)
    if gs.backend != gs.cuda or gs.device.type != "cuda":
        raise RuntimeError("Genesis requires CUDA; no CPU fallback is allowed")
    rows = [] if rows is None else rows
    _model, initial, expected, xml = build_model(scene, cfg, dt)
    simulation = gs.Scene(
        sim_options=gs.options.SimOptions(dt=dt, substeps=1, gravity=(0, 0, -cfg["gravity_m_s2"])),
        rigid_options=gs.options.RigidOptions(
            integrator=gs.integrator.Euler,
            constraint_solver=gs.constraint_solver.Newton,
            friction_cone=gs.friction_cone.elliptic,
            iterations=cfg["solver_iterations"],
            tolerance=cfg["solver_tolerance"],
            constraint_timeconst=cfg["contact_solref"][0],
            use_hibernation=False,
        ),
        show_viewer=False,
        show_FPS=False,
    )
    try:
        entity = simulation.add_entity(gs.morphs.MJCF(file=ElementTree.fromstring(xml)))
        simulation.build()
        link = entity.get_link("object")
        local = link.idx - entity.link_start
        entity.set_dofs_armature(np.zeros(entity.n_dofs))
        entity.set_dofs_damping(np.zeros(entity.n_dofs))
        entity.set_dofs_frictionloss(np.zeros(entity.n_dofs))
        entity.set_qpos(initial.qpos.copy())
        entity.set_dofs_velocity(initial.qvel.copy())
        inertia = array(entity.get_links_inertia([local]))[0]
        inertial_rotation = rotation(link.desc.inertial_quat)
        inertia = inertial_rotation @ inertia @ inertial_rotation.T
        imported = {
            "engine": "genesis",
            "engine_version": importlib.metadata.version("genesis-world"),
            "precision": "float64",
            "device": str(gs.device),
            "solver": "Newton",
            "cone": "elliptic",
            "integrator": "Euler",
            "substeps": 1,
            "iterations": cfg["solver_iterations"],
            "tolerance": cfg["solver_tolerance"],
            "timestep_s": dt,
            "mass_kg": float(array(entity.get_links_mass([local]))[0]),
            "com_local_m": array(entity.get_links_COM([local]))[0].tolist(),
            "inertia_body_kg_m2": inertia.tolist(),
            "armature": array(entity.get_dofs_armature()).tolist(),
            "damping": array(entity.get_dofs_damping()).tolist(),
            "frictionloss": array(entity.get_dofs_frictionloss()).tolist(),
            "geom_friction": [array(g.get_friction()).tolist() for g in link.geoms],
            "geom_sol_params": [array(g.get_sol_params()).tolist() for g in link.geoms],
            "force_source": "RigidEntity.get_contacts force_a/force_b in world frame after scene.step",
            "implementation_difference": "Genesis 1.4.3 CUDA float64; explicit zero armature overrides importer default",
        }
        for name in ("mass_kg", "com_local_m", "inertia_body_kg_m2"):
            np.testing.assert_allclose(imported[name], expected[name], rtol=2e-6, atol=1e-10)
        for name in ("armature", "damping", "frictionloss"):
            np.testing.assert_allclose(imported[name], 0, atol=1e-12)
        if scene != "hinge":
            np.testing.assert_allclose(
                imported["geom_friction"], cfg["sliding_friction"], atol=1e-8
            )
            for geom in link.geoms:
                np.testing.assert_allclose(
                    array(geom.get_sol_params()),
                    cfg["contact_solref"] + cfg["contact_solimp"],
                    atol=1e-8,
                )
                np.testing.assert_allclose(array(geom.get_friction_torsional()), 0, atol=1e-12)
                np.testing.assert_allclose(array(geom.get_friction_rolling()), 0, atol=1e-12)
        else:
            axes = [joint.desc.dofs_motion_ang.tolist() for joint in entity.joints if joint.n_dofs]
            imported["joint_axes"] = axes
            np.testing.assert_allclose(np.asarray(axes).reshape(-1, 3), [[0, 1, 0]], atol=1e-12)

        def state():
            if scene == "hinge":
                return array(entity.get_qpos()), array(entity.get_dofs_velocity())
            quat = array(link.get_quat())
            return (
                np.r_[array(link.get_pos()), quat],
                np.r_[array(link.get_vel()), rotation(quat).T @ array(link.get_ang())],
            )

        q_before, v_before = state()
        np.testing.assert_allclose(q_before, initial.qpos, atol=1e-8)
        np.testing.assert_allclose(v_before, initial.qvel, atol=1e-8)
        imported.update(
            initial_qpos=q_before.tolist(), initial_qvel=v_before.tolist(), validation="passed"
        )
        for step in range(round(cfg["durations_s"][scene] / dt)):
            torque = (
                cfg["pulse_torque_nm"]
                if scene == "hinge"
                and (round(cfg["pulse_start_s"] / dt) <= step < round(cfg["pulse_end_s"] / dt))
                else 0.0
            )
            if scene == "hinge":
                entity.control_dofs_force([torque])
            simulation.step()
            total, contacts = np.zeros(3), 0
            if scene != "hinge":
                data = {k: array(v) for k, v in entity.get_contacts().items()}
                for i in range(len(data["link_a"])):
                    if data["link_a"][i] == link.idx:
                        total += data["force_a"][i]
                        contacts += 1
                    elif data["link_b"][i] == link.idx:
                        total += data["force_b"][i]
                        contacts += 1
                net = array(entity.get_links_net_contact_force())[local]
            else:
                net = None
            q_after, v_after = state()
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
                    contacts,
                    torque,
                    constraint_force=net,
                )
            )
            q_before, v_before = q_after.copy(), v_after.copy()
            if on_sample is not None:
                on_sample(rows[-1])
        return Run(rows, imported, xml)
    finally:
        simulation.destroy()
