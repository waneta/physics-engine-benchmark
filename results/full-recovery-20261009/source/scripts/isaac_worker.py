"""Persistent Isaac Sim worker. Only JSON requests/samples cross the container boundary."""

import json
import sys
import traceback
from pathlib import Path

import numpy as np
from isaacsim import SimulationApp

app = SimulationApp(
    {"headless": True, "hide_ui": True, "disable_viewport_updates": True, "width": 64, "height": 64}
)

import omni.physx
import omni.usd
from isaacsim.core.api import World
from omni.physx.scripts import physicsUtils
from pxr import (
    Gf,
    PhysicsSchemaTools,
    PhysxSchema,
    Sdf,
    UsdGeom,
    UsdPhysics,
    UsdShade,
)

PREFIX = "PHYSICS_BENCH:"


def emit(kind, **payload):
    print(PREFIX + json.dumps({"kind": kind, **payload}, allow_nan=False), flush=True)


def box(stage, path, position, size, mass, collision=True):
    body_xform = UsdGeom.Xform.Define(stage, path)
    body_xform.AddTranslateOp().Set(Gf.Vec3d(*position))
    body_xform.AddOrientOp().Set(Gf.Quatf(1.0))
    prim = body_xform.GetPrim()
    geom = UsdGeom.Cube.Define(stage, path + "/geometry")
    geom.CreateSizeAttr(1.0)
    geom.AddScaleOp().Set(Gf.Vec3f(*size))
    UsdPhysics.RigidBodyAPI.Apply(prim)
    mass_api = UsdPhysics.MassAPI.Apply(prim)
    mass_api.CreateMassAttr(mass)
    mass_api.CreateCenterOfMassAttr(Gf.Vec3f(0))
    inertia = [mass * (size[(i + 1) % 3] ** 2 + size[(i + 2) % 3] ** 2) / 12 for i in range(3)]
    mass_api.CreateDiagonalInertiaAttr(Gf.Vec3f(*inertia))
    mass_api.CreatePrincipalAxesAttr(Gf.Quatf(1.0))
    body = PhysxSchema.PhysxRigidBodyAPI.Apply(prim)
    body.CreateLinearDampingAttr(0.0)
    body.CreateAngularDampingAttr(0.0)
    body.CreateSleepThresholdAttr(0.0)
    body.CreateStabilizationThresholdAttr(0.0)
    body.CreateSolverPositionIterationCountAttr(100)
    body.CreateSolverVelocityIterationCountAttr(1)
    if collision:
        UsdPhysics.CollisionAPI.Apply(geom.GetPrim())
        contact = PhysxSchema.PhysxCollisionAPI.Apply(geom.GetPrim())
        contact.CreateContactOffsetAttr(0.001)
        contact.CreateRestOffsetAttr(0.0)
    return prim


def run(request):
    scene, cfg, dt = request["scene"], request["config"], request["dt"]
    World.clear_instance()
    omni.usd.get_context().new_stage()
    app.update()  # Dispatch stage-open before World installs its stage callbacks.
    world = World(
        physics_dt=dt,
        rendering_dt=dt,
        stage_units_in_meters=1.0,
        backend="numpy",
        device="cpu",
        physics_prim_path="/World/physicsScene",
    )
    stage = omni.usd.get_context().get_stage()
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    physics = world.get_physics_context()
    physics.set_gravity(-cfg["gravity_m_s2"])
    physics.set_solver_type("TGS")
    physics.enable_gpu_dynamics(False)
    physics.set_broadphase_type("MBP")
    target = "/World/object"
    if scene == "hinge":
        root = UsdGeom.Xform.Define(stage, "/World/pendulum").GetPrim()
        UsdPhysics.ArticulationRootAPI.Apply(root)
        articulation_api = PhysxSchema.PhysxArticulationAPI.Apply(root)
        articulation_api.CreateEnabledSelfCollisionsAttr(False)
        articulation_api.CreateSolverPositionIterationCountAttr(100)
        articulation_api.CreateSolverVelocityIterationCountAttr(1)
        base = box(stage, "/World/pendulum/base", [0, 0, 0.5], [0.01] * 3, 0.1, False)
        target = "/World/pendulum/link"
        length, width = cfg["hinge_length_m"], cfg["hinge_width_m"]
        box(
            stage,
            target,
            [0, 0, 0.5 - length / 2],
            [width, width, length],
            cfg["hinge_mass_kg"],
            False,
        )
        fixed = UsdPhysics.FixedJoint.Define(stage, "/World/pendulum/fixed")
        fixed.CreateBody1Rel().SetTargets([base.GetPath()])
        fixed.CreateLocalPos0Attr(Gf.Vec3f(0, 0, 0.5))
        joint = UsdPhysics.RevoluteJoint.Define(stage, "/World/pendulum/hinge")
        joint.CreateBody0Rel().SetTargets([base.GetPath()])
        joint.CreateBody1Rel().SetTargets([Sdf.Path(target)])
        joint.CreateAxisAttr("Y")
        joint.CreateLocalPos0Attr(Gf.Vec3f(0))
        joint.CreateLocalPos1Attr(Gf.Vec3f(0, 0, length / 2))
        PhysxSchema.PhysxJointAPI.Apply(joint.GetPrim()).CreateArmatureAttr(0.0)
    else:
        side = cfg["cube_side_m"]
        height = side / 2 if scene == "slide" else cfg["drop_height_m"]
        prim = box(stage, target, [0, 0, height], [side] * 3, cfg["cube_mass_kg"])
        if scene == "slide":
            UsdPhysics.RigidBodyAPI(prim).CreateVelocityAttr(Gf.Vec3f(cfg["slide_speed_m_s"], 0, 0))
        physicsUtils.add_ground_plane(stage, "/World/ground", "Z", 10.0, Gf.Vec3f(0), Gf.Vec3f(0.5))
        material = UsdShade.Material.Define(stage, "/World/material")
        material_api = UsdPhysics.MaterialAPI.Apply(material.GetPrim())
        material_api.CreateStaticFrictionAttr(cfg["sliding_friction"])
        material_api.CreateDynamicFrictionAttr(cfg["sliding_friction"])
        material_api.CreateRestitutionAttr(0.0)
        physicsUtils.add_physics_material_to_prim(stage, prim, material.GetPath())
        for floor in stage.Traverse():
            if str(floor.GetPath()).startswith("/World/ground") and floor.HasAPI(
                UsdPhysics.CollisionAPI
            ):
                physicsUtils.add_physics_material_to_prim(stage, floor, material.GetPath())
                collision = PhysxSchema.PhysxCollisionAPI.Apply(floor)
                collision.CreateContactOffsetAttr(0.001)
                collision.CreateRestOffsetAttr(0.0)
        PhysxSchema.PhysxContactReportAPI.Apply(prim).CreateThresholdAttr(0.0)
    impulse = np.zeros(3)
    contact_count = 0

    def on_contacts(headers, contacts):
        nonlocal contact_count
        for header in headers:
            first = str(PhysicsSchemaTools.intToSdfPath(header.actor0)) == target
            second = str(PhysicsSchemaTools.intToSdfPath(header.actor1)) == target
            if first == second:
                continue
            for i in range(
                header.contact_data_offset, header.contact_data_offset + header.num_contact_data
            ):
                impulse[:] += np.asarray(contacts[i].impulse) * (1.0 if first else -1.0)
                contact_count += 1

    subscription = omni.physx.get_physx_simulation_interface().subscribe_contact_report_events(
        on_contacts
    )
    world.reset()
    view = world.physics_sim_view
    view.set_subspace_roots("/")
    rigid = view.create_rigid_body_view(target)
    contact_view = (
        None
        if scene == "hinge"
        else view.create_rigid_contact_view(
            target, ["/World/ground/CollisionPlane"], max_contact_data_count=64
        )
    )
    indices = np.array([0], dtype=np.uint32)
    if scene == "hinge":
        articulation = view.create_articulation_view("/World/pendulum")
        articulation.set_dof_armatures(np.zeros((1, 1), dtype=np.float32), indices)
        articulation.set_dof_dampings(np.zeros((1, 1), dtype=np.float32), indices)
        articulation.set_dof_positions(
            np.array([[cfg["hinge_initial_angle_rad"]]], dtype=np.float32), indices
        )
        articulation.set_dof_velocities(np.zeros((1, 1), dtype=np.float32), indices)
        view.update_articulations_kinematic()
    else:
        transforms = np.array([[0, 0, height, 0, 0, 0, 1]], dtype=np.float32)
        velocities = np.zeros((1, 6), dtype=np.float32)
        if scene == "slide":
            velocities[0, 0] = cfg["slide_speed_m_s"]
        rigid.set_transforms(transforms, indices)
        rigid.set_velocities(velocities, indices)
    imported = {
        "engine": "physx",
        "execution_path": "Isaac Sim / PhysX CPU TGS",
        "isaac_sim_version": Path("/isaac-sim/VERSION").read_text().strip(),
        "precision": "float32",
        "solver": "TGS",
        "gpu_dynamics": False,
        "position_iterations": 100,
        "velocity_iterations": 1,
        "mass_kg": rigid.get_masses().tolist(),
        "inertia_kg_m2": rigid.get_inertias().tolist(),
        "com_local": rigid.get_coms().tolist(),
        "force_source": "PhysX contact-report normal impulse + RigidContactView friction impulse, divided by dt",
        "contact_offset_m": 0.001,
        "rest_offset_m": 0.0,
        "restitution": 0.0,
        "implementation_difference": "Isaac Sim 6.0.1 image, not article 6.1; hard contact has no solref/solimp",
        "scene_usda": stage.GetRootLayer().ExportToString(),
    }
    expected_mass = cfg["hinge_mass_kg"] if scene == "hinge" else cfg["cube_mass_kg"]
    np.testing.assert_allclose(rigid.get_masses(), expected_mass, rtol=2e-6)
    dimensions = (
        [cfg["hinge_width_m"], cfg["hinge_width_m"], cfg["hinge_length_m"]]
        if scene == "hinge"
        else [cfg["cube_side_m"]] * 3
    )
    expected_inertia = [
        expected_mass * (dimensions[(i + 1) % 3] ** 2 + dimensions[(i + 2) % 3] ** 2) / 12
        for i in range(3)
    ]
    np.testing.assert_allclose(
        rigid.get_inertias()[0].reshape(3, 3), np.diag(expected_inertia), rtol=2e-6, atol=1e-10
    )
    np.testing.assert_allclose(rigid.get_coms()[0, :3], 0, atol=1e-10)
    if scene != "hinge":
        imported["material_properties"] = rigid.get_material_properties().tolist()
        imported["contact_offsets"] = rigid.get_contact_offsets().tolist()
        imported["rest_offsets"] = rigid.get_rest_offsets().tolist()
        np.testing.assert_allclose(
            rigid.get_material_properties()[0, 0],
            [cfg["sliding_friction"], cfg["sliding_friction"], 0],
            atol=1e-7,
        )
        np.testing.assert_allclose(rigid.get_contact_offsets(), 0.001, atol=1e-9)
        np.testing.assert_allclose(rigid.get_rest_offsets(), 0, atol=1e-12)
    if scene == "hinge":
        imported["armature"] = articulation.get_dof_armatures().tolist()
        imported["damping"] = articulation.get_dof_dampings().tolist()
        imported["friction"] = articulation.get_dof_friction_coefficients().tolist()
        np.testing.assert_allclose(articulation.get_dof_armatures(), 0, atol=1e-12)
        np.testing.assert_allclose(articulation.get_dof_dampings(), 0, atol=1e-12)
    imported["validation"] = "passed"

    def state():
        if scene == "hinge":
            return articulation.get_dof_positions()[0].copy(), articulation.get_dof_velocities()[
                0
            ].copy()
        transform = rigid.get_transforms()[0].copy()
        velocity = rigid.get_velocities()[0].copy()
        quat = transform[[6, 3, 4, 5]]
        # Tensor angular velocity is world-frame; common free-joint schema uses body-frame.
        rotation = Gf.Matrix3d(Gf.Quatd(float(quat[0]), Gf.Vec3d(*map(float, quat[1:]))))
        velocity[3:] = np.asarray(rotation) @ velocity[3:]
        return np.r_[transform[:3], quat], velocity

    q_before, v_before = state()
    if scene == "hinge":
        np.testing.assert_allclose(q_before, [cfg["hinge_initial_angle_rad"]], atol=1e-7)
        expected_center = [
            -length / 2 * np.sin(q_before[0]),
            0,
            0.5 - length / 2 * np.cos(q_before[0]),
        ]
        np.testing.assert_allclose(rigid.get_transforms()[0, :3], expected_center, atol=1e-6)
    else:
        np.testing.assert_allclose(q_before, [0, 0, height, 1, 0, 0, 0], atol=1e-7)
    expected_velocity = (
        [cfg["slide_speed_m_s"], 0, 0, 0, 0, 0] if scene == "slide" else np.zeros(len(v_before))
    )
    np.testing.assert_allclose(v_before, expected_velocity, atol=1e-7)
    imported.update(initial_qpos=q_before.tolist(), initial_qvel=v_before.tolist())
    emit("imported", data=imported)
    for step in range(round(cfg["durations_s"][scene] / dt)):
        torque = (
            cfg["pulse_torque_nm"]
            if scene == "hinge"
            and (round(cfg["pulse_start_s"] / dt) <= step < round(cfg["pulse_end_s"] / dt))
            else 0.0
        )
        if scene == "hinge":
            articulation.set_dof_actuation_forces(np.array([[torque]], dtype=np.float32), indices)
        impulse[:] = 0
        contact_count = 0
        world.step(render=False)
        normal_impulse = impulse.copy()
        friction_impulse = np.zeros(3)
        if contact_view is not None:
            # dt=1 returns native impulses. Contact reports contain normal impulses only.
            friction, _, counts, starts = contact_view.get_friction_data(1.0)
            for count, start in zip(counts.ravel(), starts.ravel()):
                if start + count > 64:
                    raise RuntimeError("PhysX friction buffer overflow")
                friction_impulse += friction[start : start + count].sum(axis=0)
            impulse[:] += friction_impulse
        q_after, v_after = state()
        emit(
            "sample",
            step=step,
            q_before=q_before.tolist(),
            v_before=v_before.tolist(),
            q_after=q_after.tolist(),
            v_after=v_after.tolist(),
            impulse=impulse.tolist(),
            contacts=contact_count,
            torque=torque,
            normal_impulse=normal_impulse.tolist(),
            friction_impulse=friction_impulse.tolist(),
        )
        q_before, v_before = q_after.copy(), v_after.copy()
    subscription.unsubscribe()
    world.stop()
    emit("done")


if __name__ == "__main__":
    emit("ready")
    try:
        for line in sys.stdin:
            try:
                run(json.loads(line))
            except Exception:  # noqa: BLE001 - send failures to host audit log
                emit("error", error=traceback.format_exc())
    finally:
        app.close()
