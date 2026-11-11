"""Genesis implicit FEM/SAP with an explicit, unchanged tetrahedral rest mesh."""

import os
from pathlib import Path
from unittest.mock import patch

import numpy as np

from .model import rotation, smooth
from .rigid import Controller, array
from .soft import prepare, surface


class Simulation:
    def __init__(self, case):
        os.environ.setdefault("GS_CACHE_FILE_PATH", str(Path(".cache/genesis").resolve()))
        import genesis as gs
        from genesis.engine.entities.fem_entity import FEMEntity, FEMVisGeom

        if not gs._initialized:
            gs.init(backend=gs.cuda, precision="64", logging_level="warning", seed=0)
        self.gs = gs
        self.case = case
        self.scene, root, self.rest, self.elements, self.masses = prepare(case)
        self.n = 9 if self.scene else 0
        self.sim = gs.Scene(
            sim_options=gs.options.SimOptions(
                dt=case["dt"], substeps=1, gravity=(0, 0, -9.81 if self.n else 0)
            ),
            rigid_options=gs.options.RigidOptions(
                integrator=gs.integrator.Euler, iterations=100, tolerance=1e-10
            ),
            fem_options=gs.options.FEMOptions(
                use_implicit_solver=True,
                n_newton_iterations=10,
                n_pcg_iterations=100,
                damping_alpha=0,
                damping_beta=0,
                floor_height=-100,
            ),
            coupler_options=gs.options.SAPCouplerOptions(
                n_sap_iterations=case.get("sap_iterations", 5),
                fem_floor_contact_type="none",
                rigid_floor_contact_type="none",
                enable_fem_self_tet_contact=False,
            ),
            show_viewer=False,
        )
        if self.n:
            self.robot = self.sim.add_entity(gs.morphs.MJCF(file=root, decimate=False))
            self.controller = Controller(self.scene)
        else:
            self.sim.add_entity(
                gs.morphs.Box(pos=(100, 100, 100), size=(0.001, 0.001, 0.001), collision=False),
                material=gs.materials.Rigid(),
            )
            self.plates = [
                self.sim.add_entity(
                    gs.morphs.Box(pos=(sign * 0.04, 0, 0), size=(0.02, 0.16, 0.16), fixed=True),
                    material=gs.materials.Rigid(friction=0.5),
                )
                for sign in (-1, 1)
            ]
        vertices, elements = self.rest, self.elements

        def sample(entity):
            import trimesh

            visual = gs.Mesh.from_trimesh(
                trimesh.Trimesh(vertices=vertices, faces=surface(elements), process=False)
            )
            entity._vgeoms = gs.List(
                [
                    FEMVisGeom(
                        entity,
                        entity._vvert_start,
                        entity._vface_start,
                        visual,
                        np.arange(len(vertices)),
                    )
                ]
            )
            entity.instantiate(vertices.copy(), elements.copy())

        # The pinned release has no public tetrahedral-array morph. Scope this hook to one construction;
        # no installed source is changed and read back the complete native rest mesh below.
        with patch.object(FEMEntity, "sample", sample):
            self.ball = self.sim.add_entity(
                gs.morphs.Sphere(radius=0.03),
                material=gs.materials.FEM.Elastic(
                    E=20000, nu=0.3, rho=1000, friction_mu=0.5, model="linear_corotated"
                ),
            )
        self.sim.build()
        np.testing.assert_allclose(array(self.ball.init_positions), self.rest, atol=1e-12)
        np.testing.assert_array_equal(self.ball.elems, self.elements)
        if self.n:
            e = self.robot
            e.set_qpos(self.scene.data.qpos.copy())
            e.set_dofs_velocity(self.scene.data.qvel.copy())
            e.set_dofs_armature(np.zeros(e.n_dofs))
            e.set_dofs_damping(np.zeros(e.n_dofs))
            e.set_dofs_frictionloss(np.zeros(e.n_dofs))
        checks = {}
        if self.n:
            m = self.scene.model
            for b in range(1, m.nbody):
                link = self.robot.get_link(m.body(b).name)
                idx = link.idx - self.robot.link_start
                R = rotation(link.desc.inertial_quat)
                R0 = rotation(m.body_iquat[b])
                error = max(
                    abs(float(array(self.robot.get_links_mass([idx]))[0]) - m.body_mass[b]),
                    np.max(abs(array(self.robot.get_links_COM([idx]))[0] - m.body_ipos[b])),
                    np.max(
                        abs(
                            R @ array(self.robot.get_links_inertia([idx]))[0] @ R.T
                            - R0 @ np.diag(m.body_inertia[b]) @ R0.T
                        )
                    ),
                )
                fk = float(np.max(abs(array(link.get_pos()) - self.scene.data.xpos[b])))
                if error > 1e-6 or fk > 1e-5:
                    raise RuntimeError(f"Genesis FEM robot import mismatch: {m.body(b).name}")
                checks[m.body(b).name] = {"mass_com_inertia_error": float(error), "fk_error_m": fk}
        self.u = np.zeros(self.n)
        self.last_momentum = np.zeros(3)
        self.max_residual = 0.0
        self.compression_load = 0.0
        self.audit = {
            "engine": "genesis",
            "robot_import_checks": checks,
            "material": "linear_corotated",
            "solver": f"implicit FEM + SAP ({case.get('sap_iterations', 5)} iterations)",
            "sap_iterations": case.get("sap_iterations", 5),
            "precision": "float64",
            "device": "cuda",
            "vertex_count": len(self.rest),
            "element_count": len(self.elements),
            "mass_kg": float(self.masses.sum()),
            "rest_mesh_validation": "passed",
            "force_validated": False,
            "mesh_import": "scoped FEMEntity.sample hook, no remeshing",
        }

    def step(self, i):
        if self.n:
            if i % round(0.001 / self.case["dt"]) == 0:
                self.u = self.controller.command(
                    i,
                    array(self.robot.get_qpos()),
                    array(self.robot.get_dofs_velocity()),
                    np.zeros((self.scene.model.nbody, 6)),
                    np.zeros((self.scene.model.nbody, 3)),
                )
            self.robot.control_dofs_force(self.u, dofs_idx_local=np.arange(self.n))
        else:
            t = i * self.case["dt"]
            compression = 0.006 * smooth(t, 0.2, 0.6) * (1 - smooth(t, 0.9, 1.3))
            for sign, plate in zip((-1, 1), self.plates):
                plate.set_pos((sign * (0.04 - compression), 0, 0))
        self.sim.step()
        state = self.ball.get_state()
        velocity = array(state.vel).reshape(-1, 3)
        impulse = self.sim._sim.coupler.fem_state_v.impulse.to_numpy()[0]
        momentum = np.sum(self.masses[:, None] * velocity, axis=0)
        gravity = np.array([0, 0, -9.81 if self.n else 0])
        residual = np.linalg.norm(
            momentum
            - self.last_momentum
            - self.masses.sum() * gravity * self.case["dt"]
            - impulse.sum(axis=0)
        )
        self.max_residual = max(self.max_residual, float(residual))
        self.last_momentum = momentum
        self.audit["max_momentum_residual_ns"] = self.max_residual
        self.audit["force_validated"] = self.max_residual <= 5e-6
        self.audit["force_source"] = (
            "SAP native fem_state_v.impulse; checked against nodal momentum"
        )
        if not self.n:
            self.compression_load = -float(impulse[self.rest[:, 0] > 0, 0].sum()) / self.case["dt"]
        return array(state.pos).reshape(-1, 3)

    def close(self):
        self.sim.destroy()
