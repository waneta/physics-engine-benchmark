"""Generic rigid Panda/fixture worker using the native Isaac tensor interface."""

import json
import re
import sys
import traceback

import numpy as np
from isaac_worker import (
    Gf,
    PhysicsSchemaTools,
    PhysxSchema,
    Sdf,
    UsdGeom,
    UsdPhysics,
    UsdShade,
    World,
    app,
    emit,
    omni,
    physicsUtils,
)


def quat(values):
    return Gf.Quatf(float(values[0]), Gf.Vec3f(*map(float, values[1:])))


def rot(q):
    w, x, y, z = np.asarray(q) / np.linalg.norm(q)
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ]
    )


class TensorProxy:
    """Keep host protocol arrays independent of the native tensor frontend."""

    def __init__(self, native):
        self.native = native

    def __getattr__(self, name):
        method = getattr(self.native, name)
        if not callable(method):
            return method

        def call(*args, **kwargs):
            import torch

            def incoming(value):
                return (
                    torch.as_tensor(
                        value,
                        device="cpu"
                        if name in ("set_dof_armatures", "set_dof_dampings")
                        else "cuda:0",
                    )
                    if isinstance(value, np.ndarray)
                    else value
                )

            def outgoing(value):
                if isinstance(value, torch.Tensor):
                    return value.detach().cpu().numpy()
                if isinstance(value, tuple):
                    return tuple(outgoing(v) for v in value)
                return value

            result = method(
                *(incoming(a) for a in args), **{k: incoming(v) for k, v in kwargs.items()}
            )
            return TensorProxy(result) if name.startswith("create_") else outgoing(result)

        return call


class Experiment:
    def __init__(self, s):
        self.s = s
        self.dt = s["case"]["dt"]
        self.n = s["controlled"]
        self.bodies = {b["id"]: b for b in s["bodies"]}
        World.clear_instance()
        omni.usd.get_context().new_stage()
        app.update()
        self.world = World(
            physics_dt=self.dt,
            rendering_dt=self.dt,
            stage_units_in_meters=1.0,
            backend="torch" if s.get("soft") else "numpy",
            device="cuda:0" if s.get("soft") else "cpu",
        )
        stage = omni.usd.get_context().get_stage()
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
        pc = self.world.get_physics_context()
        pc.set_gravity(-9.81)
        pc.set_solver_type("TGS")
        pc.enable_gpu_dynamics(bool(s.get("soft")))
        pc.set_broadphase_type("GPU" if s.get("soft") else "MBP")
        pc.set_gravity(0.0 if s["case"]["family"] == "soft_compression" else -9.81)
        self.robot_root = next((b["id"] for b in s["bodies"] if b["name"] == "link0"), None)
        root = UsdGeom.Xform.Define(stage, "/World/robot").GetPrim()
        if self.n:
            UsdPhysics.ArticulationRootAPI.Apply(root)
            a = PhysxSchema.PhysxArticulationAPI.Apply(root)
            a.CreateEnabledSelfCollisionsAttr(False)
            a.CreateSolverPositionIterationCountAttr(100)
            a.CreateSolverVelocityIterationCountAttr(1)
        self.paths = {}
        self.dynamic = []
        self.free = []
        for b in s["bodies"]:
            robot = b["root"] == self.robot_root
            free = any(j["type"] == 0 for j in b["joints"])
            dynamic = robot or free or b.get("mocap", -1) >= 0
            path = ("/World/robot/" if robot else "/World/objects/") + re.sub(
                r"[^A-Za-z0-9_]", "_", b["name"]
            )
            self.paths[b["id"]] = path
            xf = UsdGeom.Xform.Define(stage, path)
            xf.AddTranslateOp().Set(Gf.Vec3d(*b["worldpos"]))
            xf.AddOrientOp().Set(quat(b["worldquat"]))
            prim = xf.GetPrim()
            if dynamic:
                self.dynamic.append(b["id"])
                api = UsdPhysics.RigidBodyAPI.Apply(prim)
                if b.get("mocap", -1) >= 0:
                    api.CreateKinematicEnabledAttr(True)
                mass = UsdPhysics.MassAPI.Apply(prim)
                mass.CreateMassAttr(b["mass"])
                mass.CreateCenterOfMassAttr(Gf.Vec3f(*b["com"]))
                mass.CreateDiagonalInertiaAttr(Gf.Vec3f(*b["inertia"]))
                mass.CreatePrincipalAxesAttr(quat(b["iquat"]))
                rb = PhysxSchema.PhysxRigidBodyAPI.Apply(prim)
                rb.CreateLinearDampingAttr(0.0)
                rb.CreateAngularDampingAttr(0.0)
                rb.CreateSleepThresholdAttr(0.0)
                rb.CreateStabilizationThresholdAttr(0.0)
                rb.CreateSolverPositionIterationCountAttr(100)
                rb.CreateSolverVelocityIterationCountAttr(1)
                PhysxSchema.PhysxContactReportAPI.Apply(prim).CreateThresholdAttr(0.0)
            if free:
                self.free.append(b["id"])
        for b in s["bodies"]:
            if b["root"] != self.robot_root:
                continue
            j = b["joints"][0] if b["joints"] else None
            path = "/World/robot/joints/" + (j["name"] if j else "fixed_" + b["name"])
            cls = (
                UsdPhysics.RevoluteJoint
                if j and j["type"] == 3
                else UsdPhysics.PrismaticJoint
                if j and j["type"] == 2
                else UsdPhysics.FixedJoint
            )
            joint = cls.Define(stage, path)
            joint.CreateBody1Rel().SetTargets([Sdf.Path(self.paths[b["id"]])])
            if b["parent"]:
                joint.CreateBody0Rel().SetTargets([Sdf.Path(self.paths[b["parent"]])])
            jpos = np.array(j["pos"] if j else [0, 0, 0], dtype=float)
            joint.CreateLocalPos0Attr(Gf.Vec3f(*(np.array(b["pos"]) + rot(b["quat"]) @ jpos)))
            joint.CreateLocalPos1Attr(Gf.Vec3f(*jpos))
            joint.CreateLocalRot0Attr(quat(b["quat"]))
            joint.CreateLocalRot1Attr(Gf.Quatf(1.0))
            if j:
                axis = "XYZ"[int(np.argmax(np.abs(j["axis"])))]
                joint.CreateAxisAttr(axis)
                if j["limited"]:
                    scale = 180 / np.pi if j["type"] == 3 else 1
                    joint.CreateLowerLimitAttr(j["range"][0] * scale)
                    joint.CreateUpperLimitAttr(j["range"][1] * scale)
                PhysxSchema.PhysxJointAPI.Apply(joint.GetPrim()).CreateArmatureAttr(0.0)
        self.geom_paths = []
        for g in s["geoms"]:
            path = (
                (self.paths[g["body"]] if g["body"] else "/World")
                + "/"
                + re.sub(r"[^A-Za-z0-9_]", "_", g["name"])
            )
            kind = g["type"]
            size = g["size"]
            if kind == 6:
                geom = UsdGeom.Cube.Define(stage, path)
                geom.CreateSizeAttr(2.0)
                geom.AddScaleOp().Set(Gf.Vec3f(*size))
            elif kind == 2:
                geom = UsdGeom.Sphere.Define(stage, path)
                geom.CreateRadiusAttr(size[0])
            elif kind == 0:
                geom = UsdGeom.Cube.Define(stage, path)
                geom.CreateSizeAttr(2.0)
                geom.AddScaleOp().Set(Gf.Vec3f(10, 10, 0.05))
            elif kind == 7:
                geom = UsdGeom.Mesh.Define(stage, path)
                geom.CreatePointsAttr([Gf.Vec3f(*v) for v in g["vertices"]])
                geom.CreateFaceVertexCountsAttr([3] * len(g["faces"]))
                geom.CreateFaceVertexIndicesAttr(np.asarray(g["faces"]).ravel().tolist())
                geom.CreateSubdivisionSchemeAttr("none")
                UsdPhysics.MeshCollisionAPI.Apply(geom.GetPrim()).CreateApproximationAttr(
                    "convexHull"
                )
            else:
                raise ValueError(f"Unsupported canonical geometry {kind}")
            pos = np.array(g["pos"])
            pos[2] -= 0.05 if kind == 0 else 0
            # Set transform order explicitly: translation, orientation, scale.
            xf = UsdGeom.Xformable(geom.GetPrim())
            ops = xf.GetOrderedXformOps()
            tr = xf.AddTranslateOp()
            tr.Set(Gf.Vec3d(*pos))
            ori = xf.AddOrientOp()
            ori.Set(quat(g["quat"]))
            xf.SetXformOpOrder([tr, ori] + ops)
            prim = geom.GetPrim()
            UsdPhysics.CollisionAPI.Apply(prim)
            collision = PhysxSchema.PhysxCollisionAPI.Apply(prim)
            collision.CreateContactOffsetAttr(0.001)
            collision.CreateRestOffsetAttr(0.0)
            material = UsdShade.Material.Define(stage, path + "_material")
            ma = UsdPhysics.MaterialAPI.Apply(material.GetPrim())
            ma.CreateStaticFrictionAttr(g["friction"])
            ma.CreateDynamicFrictionAttr(g["friction"])
            ma.CreateRestitutionAttr(0.0)
            physicsUtils.add_physics_material_to_prim(stage, prim, material.GetPath())
            self.geom_paths.append(path)
        for i, g in enumerate(s["geoms"]):
            excluded = [
                Sdf.Path(self.geom_paths[j])
                for j, h in enumerate(s["geoms"])
                if j > i
                and not ((g["contype"] & h["conaffinity"]) or (h["contype"] & g["conaffinity"]))
            ]
            if excluded:
                UsdPhysics.FilteredPairsAPI.Apply(
                    stage.GetPrimAtPath(self.geom_paths[i])
                ).CreateFilteredPairsRel().SetTargets(excluded)
        if s.get("soft"):
            from omni.physx.scripts import deformableUtils

            soft = s["soft"]
            tet = UsdGeom.TetMesh.Define(stage, "/World/ball")
            tet.CreatePointsAttr([Gf.Vec3f(*v) for v in soft["vertices"]])
            tet.CreateTetVertexIndicesAttr([Gf.Vec4i(*t) for t in soft["elements"]])
            if not deformableUtils.set_physics_volume_deformable_body(
                stage, Sdf.Path("/World/ball")
            ):
                raise RuntimeError("PhysX deformable schema failed")
            deformableUtils.add_deformable_material(
                stage,
                "/World/soft_material",
                density=1000.0,
                static_friction=0.5,
                dynamic_friction=0.5,
                youngs_modulus=20000.0,
                poissons_ratio=0.3,
            )
            physicsUtils.add_physics_material_to_prim(
                stage, tet.GetPrim(), Sdf.Path("/World/soft_material")
            )
            collision = PhysxSchema.PhysxCollisionAPI.Apply(tet.GetPrim())
            collision.CreateContactOffsetAttr(0.001)
            collision.CreateRestOffsetAttr(0.0)
        self.normal = np.zeros((s["nbody"], 6))
        self.positions = np.zeros((s["nbody"], 3))
        self.actor_to_id = {v: k for k, v in self.paths.items()}

        def callback(headers, contacts):
            for header in headers:
                for actor, sign in [(header.actor0, 1), (header.actor1, -1)]:
                    b = self.actor_to_id.get(str(PhysicsSchemaTools.intToSdfPath(actor)))
                    if b is None:
                        continue
                    for i in range(
                        header.contact_data_offset,
                        header.contact_data_offset + header.num_contact_data,
                    ):
                        f = sign * np.asarray(contacts[i].impulse) / self.dt
                        point = np.asarray(contacts[i].position)
                        self.normal[b, :3] += f
                        self.normal[b, 3:] += np.cross(point - self.positions[b], f)

        self.subscription = (
            omni.physx.get_physx_simulation_interface().subscribe_contact_report_events(callback)
        )
        self.world.reset()
        self.view = (
            TensorProxy(self.world.physics_sim_view)
            if s.get("soft")
            else self.world.physics_sim_view
        )
        self.view.set_subspace_roots("/")
        self.index = np.array([0], np.uint32)
        self.rb = {b: self.view.create_rigid_body_view(self.paths[b]) for b in self.dynamic}
        self.contact = {
            b: self.view.create_rigid_contact_view(
                self.paths[b], self.geom_paths, max_contact_data_count=2048
            )
            for b in self.dynamic
            if not s.get("soft") and any(g["body"] == b for g in s["geoms"])
        }
        if self.n:
            self.art = self.view.create_articulation_view("/World/robot")
            names = list(self.art.shared_metatype.dof_names)
            canonical = [
                j["name"] for b in s["bodies"] if b["root"] == self.robot_root for j in b["joints"]
            ]
            self.order = np.array([names.index(name) for name in canonical])
            q = np.zeros((1, self.n), np.float32)
            q[0, self.order] = s["q"][: self.n]
            self.art.set_dof_armatures(np.zeros_like(q), self.index)
            self.art.set_dof_dampings(np.zeros_like(q), self.index)
            self.art.set_dof_positions(q, self.index)
            self.art.set_dof_velocities(np.zeros_like(q), self.index)
            self.view.update_articulations_kinematic()
        for b in self.free:
            j = self.bodies[b]["joints"][0]
            qa = j["qadr"]
            va = j["vadr"]
            q = np.array(s["q"][qa : qa + 7])
            v = np.array(s["v"][va : va + 6])
            v[3:] = rot(q[3:]) @ v[3:]
            self.rb[b].set_transforms(q[[0, 1, 2, 4, 5, 6, 3]][None].astype(np.float32), self.index)
            self.rb[b].set_velocities(v[None].astype(np.float32), self.index)
        errors = {}
        for b, view in self.rb.items():
            spec = self.bodies[b]
            R = rot(spec["iquat"])
            expected = R @ np.diag(spec["inertia"]) @ R.T
            errors[spec["name"]] = float(
                max(
                    np.max(abs(view.get_masses() - spec["mass"])),
                    np.max(abs(view.get_inertias()[0].reshape(3, 3) - expected)),
                    np.max(abs(view.get_coms()[0, :3] - spec["com"])),
                )
            )
            if errors[spec["name"]] > 1e-6:
                raise RuntimeError(f"PhysX import error {spec['name']}: {errors[spec['name']]}")
        if s.get("soft"):
            self.soft = self.view.create_volume_deformable_body_view("/World/ball")
            native = self.soft.get_rest_nodal_positions()[0]
            expected = np.array(s["soft"]["vertices"])
            dist = np.linalg.norm(expected[:, None] - native[None, :], axis=2)
            self.node_order = np.argmin(dist, axis=1)
            if (
                len(set(self.node_order)) != len(expected)
                or np.max(dist[np.arange(len(expected)), self.node_order]) > 1e-6
            ):
                raise RuntimeError("PhysX rest node mapping failed")
            native_elements = self.soft.get_simulation_element_indices()[0]
            inverse = np.argsort(self.node_order)
            if sorted(map(tuple, np.sort(inverse[native_elements], axis=1))) != sorted(
                map(tuple, np.sort(s["soft"]["elements"], axis=1))
            ):
                raise RuntimeError("PhysX tetrahedral connectivity changed")
            # World.reset performs warmup steps; restore the prescribed measured initial state.
            initial_nodes = np.zeros_like(native, dtype=np.float32)
            initial_nodes[self.node_order] = expected
            self.soft.set_simulation_nodal_positions(initial_nodes[None], self.index)
            self.soft.set_simulation_nodal_velocities(
                np.zeros_like(initial_nodes)[None], self.index
            )
        self.audit = {
            "engine": "physx",
            "precision": "float32",
            "solver": "CPU TGS",
            "import_errors": errors,
            "contact_force_source": "normal report + friction tensor impulses",
            "scene_usda": stage.GetRootLayer().ExportToString(),
        }

    def state(self):
        s = self.s
        q = np.array(s["q"])
        v = np.array(s["v"])
        p = np.zeros((s["nbody"], 3))
        qu = np.zeros((s["nbody"], 4))
        qu[:, 0] = 1
        if self.n:
            q[: self.n] = self.art.get_dof_positions()[0, self.order]
            v[: self.n] = self.art.get_dof_velocities()[0, self.order]
        for b, spec in self.bodies.items():
            if b in self.rb:
                tr = self.rb[b].get_transforms()[0]
                p[b] = tr[:3]
                qu[b] = tr[[6, 3, 4, 5]]
            else:
                p[b] = spec["worldpos"]
                qu[b] = spec["worldquat"]
            if b in self.free:
                j = spec["joints"][0]
                qa = j["qadr"]
                va = j["vadr"]
                q[qa : qa + 7] = np.r_[p[b], qu[b]]
                vel = self.rb[b].get_velocities()[0].copy()
                vel[3:] = rot(qu[b]).T @ vel[3:]
                v[va : va + 6] = vel
        self.positions = p
        out = {"q": q.tolist(), "v": v.tolist(), "position": p.tolist(), "quaternion": qu.tolist()}
        if self.s.get("soft"):
            out["vertices"] = self.soft.get_simulation_nodal_positions()[
                0, self.node_order
            ].tolist()
        return out

    def step(self, command):
        self.normal[:] = 0
        if self.n:
            force = np.zeros((1, self.n), np.float32)
            force[0, self.order] = command
            self.art.set_dof_actuation_forces(force, self.index)
        self.world.step(render=False)
        wrench = self.normal.copy()
        for b, contact in self.contact.items():
            friction, points, counts, starts = contact.get_friction_data(1.0)
            for count, start in zip(np.asarray(counts).ravel(), np.asarray(starts).ravel()):
                for i in range(int(start), int(start + count)):
                    force = friction[i] / self.dt
                    wrench[b, :3] += force
                    wrench[b, 3:] += np.cross(points[i] - self.positions[b], force)
        return wrench

    def close(self):
        self.subscription.unsubscribe()
        self.world.stop()


emit("ready")
experiment = None
try:
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if request["kind"] == "build":
                experiment = Experiment(request["spec"])
                emit("built", audit=experiment.audit, state=experiment.state())
            elif request["kind"] == "set_state":
                q = np.zeros((1, experiment.n), np.float32)
                v = np.zeros_like(q)
                q[0, experiment.order] = request["q"][: experiment.n]
                v[0, experiment.order] = request["v"][: experiment.n]
                experiment.art.set_dof_positions(q, experiment.index)
                experiment.art.set_dof_velocities(v, experiment.index)
                experiment.view.update_articulations_kinematic()
                emit("state", state=experiment.state())
            elif request["kind"] == "step":
                if "plates" in request:
                    for b, view in experiment.rb.items():
                        mocap = experiment.bodies[b].get("mocap", -1)
                        if mocap >= 0:
                            view.set_transforms(
                                np.array([request["plates"][mocap] + [0, 0, 0, 1]], np.float32),
                                experiment.index,
                            )
                wrench = experiment.step(request["command"])
                emit("sample", state=experiment.state(), wrench=wrench.tolist())
            elif request["kind"] == "release":
                experiment.close()
                experiment = None
                emit("done")
        except Exception:  # noqa: BLE001 - retain native failures as auditable results
            emit("error", error=traceback.format_exc())
finally:
    if experiment:
        experiment.close()
    app.close()
