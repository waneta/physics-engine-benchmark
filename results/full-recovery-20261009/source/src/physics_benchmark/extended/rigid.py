"""Native rigid solvers sharing a frozen reference and a 1 kHz torque controller."""

import importlib.metadata
import os
from pathlib import Path
from xml.etree import ElementTree as ET

import mujoco as mj
import numpy as np

from .model import KD, KP, LIMIT, rotation


def array(a):
    return a.detach().cpu().numpy().copy() if hasattr(a, "detach") else np.asarray(a)


def contact_wrenches(model, data):
    out = np.zeros((model.nbody, 6))
    f = np.zeros(6)
    for i in range(data.ncon):
        c = data.contact[i]
        mj.mj_contactForce(model, data, i, f)
        force = c.frame.reshape(3, 3).T @ f[:3]
        torque = c.frame.reshape(3, 3).T @ f[3:]
        for g, sign in [(c.geom1, -1), (c.geom2, 1)]:
            b = model.geom_bodyid[g]
            out[b, :3] += sign * force
            out[b, 3:] += sign * (torque + np.cross(c.pos - data.xpos[b], force))
    return out


class CPU:
    def __init__(self, scene):
        self.m = scene.model
        self.d = scene.data
        self.kin = mj.MjData(self.m)
        self.audit = {
            "engine": "mujoco",
            "version": mj.__version__,
            "precision": "float64",
            "device": "cpu",
        }

    def state(self):
        mj.mj_copyData(self.kin, self.m, self.d)
        mj.mj_kinematics(self.m, self.kin)
        mj.mj_comPos(self.m, self.kin)
        mj.mj_comVel(self.m, self.kin)
        return self.d.qpos.copy(), self.d.qvel.copy(), self.kin.xpos.copy(), self.kin.xquat.copy()

    def set_state(self, q, v):
        self.d.qpos[:] = q
        self.d.qvel[:] = v
        mj.mj_forward(self.m, self.d)

    def step(self, command):
        self.d.qfrc_applied[: len(command)] = command
        mj.mj_step(self.m, self.d)
        if any(w.number for w in self.d.warning):
            raise RuntimeError("MuJoCo numerical/capacity warning")
        return contact_wrenches(self.m, self.d)

    def close(self):
        pass


class Warp:
    def __init__(self, scene):
        import mujoco_warp as mw
        import warp as wp

        self.wp, self.mw = wp, mw
        self.m = scene.model
        wp.config.kernel_cache_dir = str(Path(".cache/warp").resolve())
        wp.init()
        wp.set_device("cuda:0")
        self.gm = mw.put_model(self.m)
        self.capacity = max(256, 16 * self.m.ngeom)
        self.constraints = max(1024, 8 * self.capacity)
        for key in (
            "body_mass",
            "body_inertia",
            "body_ipos",
            "body_iquat",
            "jnt_axis",
            "dof_armature",
            "geom_friction",
        ):
            np.testing.assert_allclose(
                getattr(self.gm, key).numpy().reshape(getattr(self.m, key).shape),
                getattr(self.m, key),
                rtol=2e-6,
                atol=1e-8,
            )
        warm = mw.put_data(self.m, scene.data, naconmax=self.capacity, njmax=self.constraints)
        self.ids = wp.array(np.arange(self.capacity, dtype=np.int32), dtype=wp.int32)
        self.forces = wp.zeros(self.capacity, dtype=wp.spatial_vector)
        mw.step(self.gm, warm)
        mw.contact_force(self.gm, warm, self.ids, True, self.forces)
        mw.kinematics(self.gm, warm)
        wp.synchronize()
        self.d = mw.put_data(self.m, scene.data, naconmax=self.capacity, njmax=self.constraints)
        with wp.ScopedCapture() as capture:
            mw.step(self.gm, self.d)
            mw.contact_force(self.gm, self.d, self.ids, True, self.forces)
        self.graph = capture.graph
        self.command = np.zeros((1, self.m.nv), np.float32)
        self.audit = {
            "engine": "mujoco-warp",
            "version": mw.__version__,
            "precision": "float32",
            "device": "cuda:0",
            "contact_capacity": self.capacity,
            "constraint_capacity": self.constraints,
        }

    def state(self):
        self.mw.kinematics(self.gm, self.d)
        self.wp.synchronize()
        return (
            self.d.qpos.numpy()[0],
            self.d.qvel.numpy()[0],
            self.d.xpos.numpy()[0],
            self.d.xquat.numpy()[0],
        )

    def set_state(self, q, v):
        self.d.qpos.assign(np.asarray(q, np.float32)[None])
        self.d.qvel.assign(np.asarray(v, np.float32)[None])
        self.d.qacc_warmstart.zero_()
        self.mw.forward(self.gm, self.d)
        self.wp.synchronize()

    def step(self, command):
        self.command[0, : len(command)] = command
        self.d.qfrc_applied.assign(self.command)
        self.wp.capture_launch(self.graph)
        self.wp.synchronize()
        n = int(self.d.nacon.numpy()[0])
        nc = int(self.d.nefc.numpy()[0])
        if n >= self.capacity or nc >= self.constraints:
            raise RuntimeError("MuJoCo-Warp contact/constraint capacity reached")
        out = np.zeros((self.m.nbody, 6))
        forces = self.forces.numpy()[:n]
        geoms = self.d.contact.geom.numpy()[:n]
        pos = self.d.contact.pos.numpy()[:n]
        origins = self.d.xpos.numpy()[0]
        for pair, force, point in zip(geoms, forces, pos):
            for g, sign in [(pair[0], -1), (pair[1], 1)]:
                b = self.m.geom_bodyid[g]
                out[b, :3] += sign * force[:3]
                out[b, 3:] += sign * (force[3:] + np.cross(point - origins[b], force[:3]))
        return out

    def close(self):
        pass


class Genesis:
    def __init__(self, scene):
        os.environ.setdefault("GS_CACHE_FILE_PATH", str(Path(".cache/genesis").resolve()))
        import genesis as gs

        if not gs._initialized:
            gs.init(backend=gs.cuda, precision="64", logging_level="warning", seed=0)
        self.m = scene.model
        self.sim = gs.Scene(
            sim_options=gs.options.SimOptions(dt=scene.case["dt"], substeps=1),
            rigid_options=gs.options.RigidOptions(
                integrator=gs.integrator.Euler,
                constraint_solver=gs.constraint_solver.Newton,
                friction_cone=gs.friction_cone.elliptic,
                iterations=100,
                tolerance=1e-10,
                use_hibernation=False,
            ),
            show_viewer=False,
            show_FPS=False,
        )
        self.entity = self.sim.add_entity(
            gs.morphs.MJCF(file=ET.fromstring(scene.xml), decimate=False)
        )
        self.sim.build()
        e = self.entity
        e.set_dofs_armature(np.zeros(e.n_dofs))
        e.set_dofs_damping(np.zeros(e.n_dofs))
        e.set_dofs_frictionloss(np.zeros(e.n_dofs))
        e.set_qpos(scene.data.qpos.copy())
        e.set_dofs_velocity(scene.data.qvel.copy())
        self.links = {b: e.get_link(self.m.body(b).name) for b in range(1, self.m.nbody)}
        self.global_to_body = {l.idx: b for b, l in self.links.items()}
        errors = {}
        for b, l in self.links.items():
            if self.m.body_mass[b] <= 0:
                continue
            idx = l.idx - e.link_start
            mass = float(array(e.get_links_mass([idx]))[0])
            com = array(e.get_links_COM([idx]))[0]
            R = rotation(l.desc.inertial_quat)
            I = R @ array(e.get_links_inertia([idx]))[0] @ R.T
            R0 = rotation(self.m.body_iquat[b])
            I0 = R0 @ np.diag(self.m.body_inertia[b]) @ R0.T
            error = max(
                abs(mass - self.m.body_mass[b]),
                np.max(abs(com - self.m.body_ipos[b])),
                np.max(abs(I - I0)),
            )
            errors[self.m.body(b).name] = float(error)
            if error > 1e-6:
                raise RuntimeError(f"Genesis import mismatch {self.m.body(b).name}: {error}")
        self.audit = {
            "engine": "genesis",
            "version": importlib.metadata.version("genesis-world"),
            "precision": "float64",
            "device": "cuda:0",
            "import_errors": errors,
        }

    def state(self):
        e = self.entity
        p = np.zeros((self.m.nbody, 3))
        q = np.zeros((self.m.nbody, 4))
        q[:, 0] = 1
        allp = array(e.get_links_pos())
        allq = array(e.get_links_quat())
        for b, l in self.links.items():
            p[b] = allp[l.idx - e.link_start]
            q[b] = allq[l.idx - e.link_start]
        return array(e.get_qpos()), array(e.get_dofs_velocity()), p, q

    def set_state(self, q, v):
        self.entity.set_qpos(q)
        self.entity.set_dofs_velocity(v)

    def step(self, command):
        if len(command):
            self.entity.control_dofs_force(command, dofs_idx_local=np.arange(len(command)))
        self.sim.step()
        out = np.zeros((self.m.nbody, 6))
        c = {k: array(v) for k, v in self.entity.get_contacts().items()}
        p = array(self.entity.get_links_pos())
        for i in range(len(c["link_a"])):
            for side in ("a", "b"):
                idx = int(c["link_" + side][i])
                b = self.global_to_body.get(idx)
                if b is None:
                    continue
                force = c["force_" + side][i]
                out[b, :3] += force
                point = c["position"][i]
                out[b, 3:] += np.cross(point - p[idx - self.entity.link_start], force)
        return out

    def close(self):
        self.sim.destroy()


class Controller:
    def __init__(self, scene):
        self.s = scene
        self.d = mj.MjData(scene.model)
        self.filtered = np.zeros(6)
        self.shift = np.zeros(3)
        self.angle = np.zeros(3)
        self.last_wrench = np.zeros(6)

    def command(self, step, q, v, wrench, positions):
        s = self.s
        n = s.controlled
        if not n:
            return np.zeros(0)
        i = min(round(step * s.case["dt"] / s.reference["dt"]), len(s.reference["q"]) - 1)
        ff = s.reference["feedforward"][i].copy()
        if s.case["family"] == "panda_open_loop":
            return ff
        kp = KP[:n].copy()
        kd = KD[:n].copy()
        kp[:7] *= s.case.get("kp_scale", 4 if s.case["family"] == "sweep" else 1)
        kd[:7] *= s.case.get("kd_scale", 2 if s.case["family"] == "sweep" else 1)
        u = ff + kp * (s.reference["q"][i] - q[:n]) + kd * (s.reference["v"][i] - v[:n])
        if s.case["family"] == "insertion":
            m = s.model
            d = self.d
            d.qpos[:] = q
            d.qvel[:] = v
            mj.mj_forward(m, d)
            h = m.body("hand").id
            jp = np.zeros((3, m.nv))
            jr = np.zeros_like(jp)
            mj.mj_jacBody(m, d, jp, jr, h)
            R = d.xmat[h].reshape(3, 3)
            goal = s.reference["hand_rotation"][i]
            contact = np.zeros(6)
            for name in ("hand", "left_finger", "right_finger", "peg"):
                b = mj.mj_name2id(m, mj.mjtObj.mjOBJ_BODY, name)
                if b >= 0:
                    contact[:3] += wrench[b, :3]
                    contact[3:] += wrench[b, 3:] + np.cross(
                        positions[b] - positions[h], wrench[b, :3]
                    )
            self.last_wrench = contact
            if s.case.get("guided"):
                self.filtered += 0.1 * (contact - self.filtered)
                # Compliant displacement follows measured contact, independent of hole position.
                self.shift[:2] = np.clip(
                    self.shift[:2] + 0.001 * 0.003 * self.filtered[:2], -0.003, 0.003
                )
                self.shift[2] = np.clip(
                    self.shift[2] + 0.001 * 0.001 * (max(self.filtered[2] - 5, 0)), 0, 0.003
                )
                tip = R @ np.array(s.parameters["peg_tip_local"])
                moment = self.filtered[3:] - np.cross(tip, self.filtered[:3])
                self.angle = np.clip(self.angle + 0.001 * 0.02 * moment, -0.05, 0.05)
            err = s.reference["hand"][i] + self.shift - d.xpos[h]
            angular = 0.5 * sum(np.cross(R[:, j], goal[:, j]) for j in range(3)) + self.angle
            force = 1500 * err - 80 * (jp @ v)
            torque = 40 * angular - 4 * (jr @ v)
            force *= min(1, 20 / max(np.linalg.norm(force), 1e-12))
            torque *= min(1, 2 / max(np.linalg.norm(torque), 1e-12))
            # A redundant arm needs posture control in the task Jacobian's nullspace.
            # Without it, the frozen reference feedforward cannot prevent free-space
            # drift in the seventh DOF, even with no peg contact at all.
            jac = np.vstack([jp[:, :7], jr[:, :7]])
            posture = kp[:7] * (s.reference["q"][i, :7] - q[:7]) - kd[:7] * v[:7]
            nullspace = np.eye(7) - jac.T @ np.linalg.solve(
                jac @ jac.T + np.eye(6) * 1e-8, jac
            )
            u[:7] = ff[:7] + (jp.T @ force + jr.T @ torque)[:7] + nullspace @ posture
        limits = LIMIT[:n].copy()
        if n == 9:
            limits[7:] = s.case.get("finger_force", 4.0)
        return np.clip(u, -limits, limits)


def run(scene, engine, output):
    """Retain a trajectory prefix and explicit status even when a native solver fails."""
    import json
    import time

    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / "scene.xml").write_text(scene.xml)
    (output / "case.json").write_text(json.dumps(scene.case, indent=2))
    if scene.reference:
        np.savez_compressed(output / "reference.npz", **scene.reference)
    sim = None
    records = []
    start = time.perf_counter()
    status = "completed"
    error = None
    audit = {}
    try:
        from .physx import PhysX

        sim = {"mujoco": CPU, "mujoco-warp": Warp, "genesis": Genesis, "physx": PhysX}[engine](
            scene
        )
        audit = sim.audit
        if "scene_usda" in audit:
            (output / "scene.usda").write_text(audit.pop("scene_usda"))
        if scene.controlled:
            checks = []
            initial_q = scene.data.qpos.copy()
            initial_v = scene.data.qvel.copy()
            kin_check = mj.MjData(scene.model)
            for delta in (
                np.zeros(7),
                0.05 * np.sin(np.arange(7)),
                -0.05 * np.sin(np.arange(7)),
                0.05 * np.cos(np.arange(7)),
                -0.05 * np.cos(np.arange(7)),
            ):
                check_q = initial_q.copy()
                check_q[:7] += delta
                sim.set_state(check_q, initial_v.copy())
                native_q, _, native_pos, native_quat = sim.state()
                kin_check.qpos[:] = check_q
                mj.mj_kinematics(scene.model, kin_check)
                position_error = float(np.max(abs(native_pos[1:] - kin_check.xpos[1:])))
                rotation_error = max(
                    float(np.linalg.norm(rotation(a) - rotation(b)))
                    for a, b in zip(native_quat[1:], kin_check.xquat[1:])
                )
                joint_error = float(np.max(abs(native_q - check_q)))
                checks.append(
                    {
                        "position_error_m": position_error,
                        "rotation_frobenius_error": rotation_error,
                        "joint_error": joint_error,
                    }
                )
                if position_error > 1e-5 or rotation_error > 1e-4 or joint_error > 1e-5:
                    raise RuntimeError("Five-pose native import validation failed")
            sim.set_state(initial_q, initial_v)
            audit["five_pose_fk_checks"] = checks
        q, v, p, quat = sim.state()
        kin = mj.MjData(scene.model)
        controller = Controller(scene)
        np.testing.assert_allclose(q, scene.data.qpos, atol=1e-6)
        np.testing.assert_allclose(v, scene.data.qvel, atol=1e-6)
        audit["initial_fk_error_m"] = float(np.max(abs(p[1:] - scene.data.xpos[1:])))
        if audit["initial_fk_error_m"] > 1e-5:
            raise RuntimeError("Initial native FK mismatch")
        wrench = np.zeros((scene.model.nbody, 6))
        u = np.zeros(scene.controlled)
        records.append(
            (0.0, q.copy(), v.copy(), p.copy(), quat.copy(), wrench.copy(), u.copy(), 0.0)
        )
        stride = round(0.001 / scene.case["dt"])
        if stride < 1 or abs(stride * scene.case["dt"] - 0.001) > 1e-10:
            raise ValueError("dt must divide controller interval 0.001 s")
        for step in range(round(scene.case["duration"] / scene.case["dt"])):
            if step % max(1, round(0.5 / scene.case["dt"])) == 0:
                (output / "progress.json").write_text(
                    json.dumps(
                        {
                            "step": step,
                            "simulated_seconds": step * scene.case["dt"],
                            "wall_seconds": time.perf_counter() - start,
                        }
                    )
                )
            if step % stride == 0:
                u = controller.command(step, q, v, wrench, p)
            wrench = sim.step(u)
            q, v, p, quat = sim.state()
            if not all(np.isfinite(x).all() for x in (q, v, p, quat, wrench)):
                raise FloatingPointError("Non-finite native state")
            kin.qpos[:] = q
            mj.mj_kinematics(scene.model, kin)
            fk = float(np.max(np.linalg.norm(p[1:] - kin.xpos[1:], axis=1)))
            records.append(
                (
                    (step + 1) * scene.case["dt"],
                    q.copy(),
                    v.copy(),
                    p.copy(),
                    quat.copy(),
                    wrench.copy(),
                    u.copy(),
                    fk,
                )
            )
            if fk > 1e-5:
                raise RuntimeError(f"Trajectory native FK mismatch: {fk}")
            if scene.case["family"] == "insertion" and (
                np.linalg.norm(controller.last_wrench[:3]) > 40
                or np.linalg.norm(controller.last_wrench[3:]) > 4
            ):
                status = "overload"
                break
    except (Exception, KeyboardInterrupt) as exc:  # noqa: BLE001 - retain native failures as auditable results
        import traceback

        status = "interrupted" if isinstance(exc, KeyboardInterrupt) else "error"
        error = str(exc)
        (output / "error.txt").write_text(traceback.format_exc())
    finally:
        if sim is not None:
            try:
                sim.close()
            except Exception as exc:  # noqa: BLE001 - preserve measurements on native teardown failure
                status = "error"
                error = (error + "; " if error else "") + f"Native cleanup failed: {exc}"
                (output / "cleanup-error.txt").write_text(str(exc))
    names = ("time", "q", "v", "position", "quaternion", "contact_wrench", "command", "fk_error")
    arrays = {name: np.array([r[i] for r in records]) for i, name in enumerate(names)}
    np.savez_compressed(output / "trajectory.npz", **arrays)
    from .metrics import evaluate

    result = evaluate(scene, arrays, status)
    result.update(
        engine=engine,
        case=scene.case,
        status=status,
        error=error,
        wall_seconds=time.perf_counter() - start,
        reference_sha256=scene.reference.get("sha256"),
        samples=len(records),
        audit=audit,
    )
    (output / "result.json").write_text(json.dumps(result, indent=2, allow_nan=False))
    return result
