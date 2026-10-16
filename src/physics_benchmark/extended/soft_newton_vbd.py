"""Newton's native lagged MuJoCo-Warp/VBD proxy coupling; no surrogate ball."""

from pathlib import Path

import numpy as np

from .model import rotation, smooth
from .rigid import Controller
from .soft import prepare


class Simulation:
    def __init__(self, case):
        import newton
        import warp as wp
        from newton.solvers import SolverMuJoCo, SolverVBD
        from newton.solvers.experimental.coupled import SolverCoupledProxy

        wp.config.kernel_cache_dir = str(Path(".cache/newton").resolve())
        wp.init()
        wp.set_device("cuda:0")
        self.wp = wp
        self.newton = newton
        self.case = case
        self.scene, _root, self.rest, self.elements, self.masses = prepare(case)
        self.n = 9 if self.scene else 0
        builder = newton.ModelBuilder(gravity=(0, 0, -9.81 if self.n else 0))
        builder.default_shape_cfg.mu = 0.5
        builder.default_shape_cfg.ke = 2e6
        builder.default_shape_cfg.kd = 0.2
        if self.n:
            builder.add_mjcf(
                self.scene.xml,
                parse_visuals=False,
                enable_self_collisions=False,
                collapse_fixed_joints=False,
            )
            self.controller = Controller(self.scene)
            if len(builder.joint_q) != self.n:
                raise ValueError("Unexpected Newton robot joint coordinate mapping")
            builder.joint_q[:] = self.scene.data.qpos.tolist()
            builder.joint_target_ke[:] = [0.0] * len(builder.joint_target_ke)
            builder.joint_target_kd[:] = [0.0] * len(builder.joint_target_kd)
        else:
            for sign in (-1, 1):
                b = builder.add_body(
                    xform=wp.transform((sign * 0.04, 0, 0), wp.quat_identity()),
                    mass=0.0,
                    is_kinematic=True,
                )
                builder.add_shape_box(b, hx=0.01, hy=0.08, hz=0.08)
        rigid_count = builder.body_count
        E = 20000
        nu = 0.3
        mu = E / (2 * (1 + nu))
        lam = E * nu / ((1 + nu) * (1 - 2 * nu))
        builder.add_soft_mesh(
            pos=wp.vec3(0),
            rot=wp.quat_identity(),
            scale=1.0,
            vel=wp.vec3(0),
            vertices=self.rest.tolist(),
            indices=self.elements.ravel().tolist(),
            density=1000,
            k_mu=mu,
            k_lambda=lam,
            k_damp=0,
            particle_radius=0,
            add_surface_mesh_edges=False,
        )
        builder.color()
        self.model = builder.finalize()
        self.model.soft_contact_ke = 2e6
        self.model.soft_contact_kd = 0.2
        self.model.soft_contact_mu = 0.5
        self.model.shape_material_ke.fill_(2e6)
        self.model.shape_material_kd.fill_(0.2)
        self.model.shape_material_mu.fill_(0.5)
        kwargs = {
            "iterations": 10,
            "particle_enable_self_contact": False,
            "friction_epsilon": 0.001,
        }
        if self.n:
            self.solver = SolverCoupledProxy(
                model=self.model,
                entries=[
                    SolverCoupledProxy.Entry(
                        name="mjc",
                        solver=lambda v: SolverMuJoCo(
                            v,
                            use_mujoco_cpu=False,
                            use_mujoco_contacts=False,
                            integrator="euler",
                            iterations=100,
                            cone="elliptic",
                            tolerance=1e-10,
                            njmax=1024,
                        ),
                        bodies=list(range(rigid_count)),
                        joints=list(range(self.model.joint_count)),
                    ),
                    SolverCoupledProxy.Entry(
                        name="vbd",
                        solver=lambda v: SolverVBD(v, **kwargs),
                        bodies=[],
                        particles=list(range(self.model.particle_count)),
                    ),
                ],
                coupling=SolverCoupledProxy.Config(
                    proxies=[
                        SolverCoupledProxy.Proxy(
                            source="mjc",
                            destination="vbd",
                            bodies=list(range(rigid_count)),
                            mass_scale=1.0,
                            mode="lagged",
                            collision_pipeline=lambda model: newton.CollisionPipeline(
                                model, soft_contact_margin=0.001
                            ),
                            collide_interval=1,
                        )
                    ],
                    iterations=1,
                ),
            )
        else:
            self.solver = SolverVBD(self.model, **kwargs)
        self.state0 = self.model.state()
        self.state1 = self.model.state()
        self.control = self.model.control()
        if self.n:
            newton.eval_fk(self.model, self.model.joint_q, self.model.joint_qd, self.state0)
        self.pipeline = newton.CollisionPipeline(self.model, soft_contact_margin=0.001)
        self.contacts = self.pipeline.contacts()
        np.testing.assert_allclose(self.state0.particle_q.numpy(), self.rest, atol=1e-7)
        np.testing.assert_allclose(self.model.particle_mass.numpy(), self.masses, rtol=1e-5)
        import_checks = {}
        if self.n:
            canonical = self.scene.model
            poses = self.state0.body_q.numpy()
            masses = self.model.body_mass.numpy()
            centers = self.model.body_com.numpy()
            inertias = self.model.body_inertia.numpy()
            for b in range(1, canonical.nbody):
                name = canonical.body(b).name
                matches = [
                    i
                    for i, label in enumerate(self.model.body_label)
                    if label == name or label.endswith("/" + name)
                ]
                if len(matches) != 1:
                    raise RuntimeError(f"Ambiguous Newton body mapping: {name}")
                i = matches[0]
                R = rotation(canonical.body_iquat[b])
                expected_inertia = R @ np.diag(canonical.body_inertia[b]) @ R.T
                error = max(
                    abs(masses[i] - canonical.body_mass[b]),
                    np.max(abs(centers[i] - canonical.body_ipos[b])),
                    np.max(abs(inertias[i] - expected_inertia)),
                )
                fk = float(np.max(abs(poses[i, :3] - self.scene.data.xpos[b])))
                if error > 1e-6 or fk > 1e-5:
                    raise RuntimeError(
                        f"Newton robot import mismatch: {name} inertia/mass={error}, FK={fk}"
                    )
                import_checks[name] = {"mass_com_inertia_error": float(error), "fk_error_m": fk}
        self.u = np.zeros(self.n)
        self.audit = {
            "engine": "newton-vbd",
            "newton_version": newton.__version__,
            "robot_import_checks": import_checks,
            "rigid_solver": "MuJoCo-Warp",
            "soft_solver": "VBD",
            "coupling": "lagged proxy feedback",
            "shape_contact_damping": 0.2,
            "material": "VBD tetrahedral elasticity",
            "mass_kg": float(self.masses.sum()),
            "vertex_count": len(self.rest),
            "element_count": len(self.elements),
            "force_validated": False,
        }

    def step(self, i):
        wp = self.wp
        if self.n:
            if i % round(0.001 / self.case["dt"]) == 0:
                self.u = self.controller.command(
                    i,
                    self.state0.joint_q.numpy(),
                    self.state0.joint_qd.numpy(),
                    np.zeros((self.scene.model.nbody, 6)),
                    np.zeros((self.scene.model.nbody, 3)),
                )
            self.control.joint_f.assign(self.u.astype(np.float32))
        else:
            t = i * self.case["dt"]
            compression = 0.006 * smooth(t, 0.2, 0.6) * (1 - smooth(t, 0.9, 1.3))
            q = self.state0.body_q.numpy()
            q[0, 0] = -0.04 + compression
            q[1, 0] = 0.04 - compression
            self.state0.body_q.assign(q)
            self.state1.body_q.assign(q)
        self.state0.clear_forces()
        self.pipeline.collide(self.state0, self.contacts)
        self.solver.step(self.state0, self.state1, self.control, self.contacts, self.case["dt"])
        self.state0, self.state1 = self.state1, self.state0
        wp.synchronize()
        return self.state0.particle_q.numpy()

    def close(self):
        pass
