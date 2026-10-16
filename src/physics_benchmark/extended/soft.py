"""Shared tetrahedral mesh, deformation gates and native deformable experiments."""

import itertools
import json
import time
import traceback
from pathlib import Path
from xml.etree import ElementTree as ET

import mujoco as mj
import numpy as np

from .model import build, numbers, root_xml, smooth, solid


def volumes(vertices, elements):
    t = vertices[elements]
    return (
        np.linalg.det(np.stack((t[:, 1] - t[:, 0], t[:, 2] - t[:, 0], t[:, 3] - t[:, 0]), axis=2))
        / 6
    )


def mesh(refined=False):
    """125/384 coarse grid; midpoint refinement preserves the exact polyhedral boundary."""
    grid = np.array(list(itertools.product(np.linspace(-1, 1, 5), repeat=3)))
    norm = np.linalg.norm(grid, axis=1)
    scale = np.divide(np.max(abs(grid), axis=1), norm, out=np.zeros_like(norm), where=norm > 0)
    vertices = 0.03 * grid * scale[:, None]
    elements = []

    def idx(v):
        return int(v[0] * 25 + v[1] * 5 + v[2])

    for base in itertools.product(range(4), repeat=3):
        for order in itertools.permutations(range(3)):
            corner = np.array(base)
            tet = [idx(corner)]
            for axis in order:
                corner[axis] += 1
                tet.append(idx(corner))
            elements.append(tet)
    elements = np.asarray(elements, dtype=np.int32)
    neg = volumes(vertices, elements) < 0
    elements[neg] = elements[neg][:, [1, 0, 2, 3]]
    if refined:
        verts = vertices.tolist()
        edges = {}
        children = []

        def midpoint(a, b):
            key = tuple(sorted((int(a), int(b))))
            if key not in edges:
                edges[key] = len(verts)
                verts.append(((vertices[a] + vertices[b]) / 2).tolist())
            return edges[key]

        for a, b, c, d in elements:
            ab, ac, ad, bc, bd, cd = [
                midpoint(i, j) for i, j in ((a, b), (a, c), (a, d), (b, c), (b, d), (c, d))
            ]
            children.extend(
                [
                    [a, ab, ac, ad],
                    [b, ab, bc, bd],
                    [c, ac, bc, cd],
                    [d, ad, bd, cd],
                    [ab, ac, ad, cd],
                    [ab, ac, bc, cd],
                    [ab, bc, bd, cd],
                    [ab, ad, bd, cd],
                ]
            )
        vertices = np.asarray(verts)
        elements = np.asarray(children, dtype=np.int32)
        neg = volumes(vertices, elements) < 0
        elements[neg] = elements[neg][:, [1, 0, 2, 3]]
    vol = volumes(vertices, elements)
    if np.any(vol <= 0):
        raise ValueError("Invalid rest mesh")
    masses = np.zeros(len(vertices))
    np.add.at(masses, elements.ravel(), np.repeat(1000 * vol / 4, 4))
    return vertices, elements, masses


def surface(elements):
    faces = np.concatenate(
        [
            elements[:, [0, 2, 1]],
            elements[:, [1, 2, 3]],
            elements[:, [0, 1, 3]],
            elements[:, [0, 3, 2]],
        ]
    )
    _, ids, counts = np.unique(
        np.sort(faces, axis=1), axis=0, return_index=True, return_counts=True
    )
    return faces[ids[counts == 1]]


def prepare(case):
    grasp = case["family"] == "soft_grasp"
    dt = case["dt"]
    vertices, elements, masses = mesh(case.get("refined", False))
    if grasp:
        scene = build(case)
        root = ET.fromstring(scene.xml)
        center = np.array(scene.parameters["grip0"])
        center[2] += 0.01
    else:
        scene = None
        root = root_xml(dt)
        root.find("option").set("gravity", "0 0 0")
        center = np.zeros(3)
        for sign in (-1, 1):
            plate = solid(
                root,
                f"plate_{sign}",
                [sign * 0.04, 0, 0],
                [0.01, 0.08, 0.08],
                contype=1,
                conaffinity=2,
            )
            plate.set("mocap", "true")
    vertices = vertices + center
    return scene, root, vertices, elements, masses


def add_flex(root, vertices, elements, masses):
    body_names = []
    for i, (pos, mass) in enumerate(zip(vertices, masses)):
        name = f"ball_node_{i}"
        body_names.append(name)
        b = ET.SubElement(root.find("worldbody"), "body", name=name, pos=numbers(pos))
        ET.SubElement(b, "inertial", pos="0 0 0", mass=str(mass), diaginertia="1e-12 1e-12 1e-12")
        for axis in np.eye(3):
            ET.SubElement(b, "joint", type="slide", axis=numbers(axis), damping="0", armature="0")
    deform = ET.SubElement(root, "deformable")
    flex = ET.SubElement(
        deform,
        "flex",
        name="ball",
        dim="3",
        body=" ".join(body_names),
        vertex=numbers(np.zeros_like(vertices)),
        element=numbers(elements),
        radius="0",
    )
    ET.SubElement(
        flex,
        "contact",
        contype="2",
        conaffinity="5",
        condim="3",
        friction=".5 0 0",
        selfcollide="none",
        solref=".01 1",
        solimp=".99 .999 .001 .5 2",
    )
    ET.SubElement(flex, "elasticity", young="20000", poisson=".3", damping="0")
    return ET.tostring(root, encoding="unicode")


class MuJoCoSoft:
    def __init__(self, case, engine):
        from .rigid import Controller

        self.scene, root, self.rest, self.elements, self.masses = prepare(case)
        self.xml = add_flex(root, self.rest, self.elements, self.masses)
        self.model = mj.MjModel.from_xml_string(self.xml)
        self.data = mj.MjData(self.model)
        self.case = case
        self.engine = engine
        self.n = 0 if self.scene is None else self.scene.controlled
        if self.n:
            self.data.qpos[: self.n] = self.scene.data.qpos[: self.n]
        mj.mj_forward(self.model, self.data)
        self.controller = Controller(self.scene) if self.n else None
        self.u = np.zeros(self.n)
        self.vertices = self.data.flexvert_xpos.copy()
        self.last_momentum = np.zeros(3)
        self.max_momentum_residual = 0.0
        self.force_native = np.zeros(3)
        self.compression_load = 0.0
        self.audit = {
            "engine": engine,
            "mujoco_version": mj.__version__,
            "material": "MuJoCo flex elasticity",
            "force_validated": False,
            "vertex_count": len(self.rest),
            "element_count": len(self.elements),
            "mass_kg": float(self.masses.sum()),
        }
        if engine == "mujoco-warp":
            import mujoco_warp as mw
            import warp as wp

            self.wp, self.mw = wp, mw
            wp.config.kernel_cache_dir = str(Path(".cache/warp").resolve())
            wp.init()
            wp.set_device("cuda:0")
            self.gm = mw.put_model(self.model)
            self.gd = mw.put_data(self.model, self.data, naconmax=4096, njmax=16384)
            mw.step(self.gm, self.gd)
            wp.synchronize()
            self.gd = mw.put_data(self.model, self.data, naconmax=4096, njmax=16384)
            self.contact_ids = wp.array(np.arange(4096, dtype=np.int32), dtype=wp.int32)
            self.contact_forces = wp.zeros(4096, dtype=wp.spatial_vector)
            mw.contact_force(self.gm, self.gd, self.contact_ids, True, self.contact_forces)
            wp.synchronize()
            with wp.ScopedCapture() as capture:
                mw.step(self.gm, self.gd)
                mw.contact_force(self.gm, self.gd, self.contact_ids, True, self.contact_forces)
            self.graph = capture.graph

    def step(self, i):
        dt = self.case["dt"]
        t = i * dt
        if self.n and i % round(0.001 / dt) == 0:
            if self.engine == "mujoco-warp":
                q = self.gd.qpos.numpy()[0]
                v = self.gd.qvel.numpy()[0]
            else:
                q = self.data.qpos
                v = self.data.qvel
            s = self.scene
            self.u = self.controller.command(
                i,
                q[: s.model.nq],
                v[: s.model.nv],
                np.zeros((s.model.nbody, 6)),
                np.zeros((s.model.nbody, 3)),
            )
        if not self.n:
            compression = 0.006 * smooth(t, 0.2, 0.6) * (1 - smooth(t, 0.9, 1.3))
            positions = np.array([[-0.04 + compression, 0, 0], [0.04 - compression, 0, 0]])
        if self.engine == "mujoco-warp":
            if self.n:
                command = np.zeros((1, self.model.nv), np.float32)
                command[0, : self.n] = self.u
                self.gd.qfrc_applied.assign(command)
            else:
                self.gd.mocap_pos.assign(positions[None].astype(np.float32))
            self.wp.capture_launch(self.graph)
            self.mw.kinematics(self.gm, self.gd)
            self.mw.flex(self.gm, self.gd)
            self.wp.synchronize()
            self.vertices = self.gd.flexvert_xpos.numpy()[0]
            n = int(self.gd.nacon.numpy()[0])
            forces = self.contact_forces.numpy()[:n, :3]
            flexes = self.gd.contact.flex.numpy()[:n]
            self.force_native = np.sum(
                forces
                * (
                    np.equal(flexes[:, 1], 0).astype(float)
                    - np.equal(flexes[:, 0], 0).astype(float)
                )[:, None],
                axis=0,
            )
            velocity = self.gd.qvel.numpy()[0, self.n :].reshape(-1, 3)
            if not self.n:
                geoms = self.gd.contact.geom.numpy()[:n]
                plate = self.model.geom("plate_1_geom").id
                self.compression_load = float(
                    np.sum(
                        forces[:, 0]
                        * (
                            np.equal(geoms[:, 1], plate).astype(float)
                            - np.equal(geoms[:, 0], plate).astype(float)
                        )
                    )
                )
            if int(self.gd.nacon.numpy()[0]) >= 4096 or int(self.gd.nefc.numpy()[0]) >= 16384:
                raise RuntimeError("Flex contact/constraint capacity reached")
        else:
            if self.n:
                self.data.qfrc_applied[: self.n] = self.u
            else:
                self.data.mocap_pos[:] = positions
            mj.mj_step(self.model, self.data)
            if any(w.number for w in self.data.warning):
                raise RuntimeError("MuJoCo numerical warning")
            self.force_native = np.zeros(3)
            self.compression_load = 0.0
            cf = np.zeros(6)
            for k in range(self.data.ncon):
                c = self.data.contact[k]
                mj.mj_contactForce(self.model, self.data, k, cf)
                force = c.frame.reshape(3, 3).T @ cf[:3]
                sign = int(c.flex[1] == 0) - int(c.flex[0] == 0)
                self.force_native += sign * force
                if not self.n:
                    plate = self.model.geom("plate_1_geom").id
                    self.compression_load += (
                        int(c.geom2 == plate) - int(c.geom1 == plate)
                    ) * force[0]
            velocity = self.data.qvel[self.n :].reshape(-1, 3)
            mj.mj_kinematics(self.model, self.data)
            mj.mj_flex(self.model, self.data)
            self.vertices = self.data.flexvert_xpos.copy()
        momentum = (self.masses[:, None] * velocity).sum(axis=0)
        residual = np.linalg.norm(
            momentum
            - self.last_momentum
            - (self.force_native + self.masses.sum() * self.model.opt.gravity) * dt
        )
        self.max_momentum_residual = max(self.max_momentum_residual, float(residual))
        self.last_momentum = momentum
        self.audit["max_momentum_residual_ns"] = self.max_momentum_residual
        self.audit["force_validated"] = self.max_momentum_residual <= 5e-6
        return self.vertices.copy()

    def close(self):
        pass


def cases(engine):
    base = {
        "mujoco": 0.00005,
        "mujoco-warp": 0.00005,
        "physx": 0.001,
        "genesis": 0.001,
        "newton-vbd": 0.0005,
    }[engine]
    out = [
        {"family": "soft_compression", "dt": base, "refined": False, "duration": 1.5, "repeat": i}
        for i in range(3)
    ]
    out.append(
        {
            "family": "soft_compression",
            "dt": base / 2,
            "refined": False,
            "duration": 1.5,
            "repeat": 0,
        }
    )
    out.extend(
        {
            "family": "soft_grasp",
            "dt": base,
            "refined": False,
            "duration": 4.5,
            "finger_force": force,
            "repeat": 0,
        }
        for force in (1, 1.1, 1.5, 2)
    )
    out.extend(
        {
            "family": "soft_grasp",
            "dt": base / divisor,
            "refined": refined,
            "duration": 4.5,
            "finger_force": 2,
            "repeat": 0,
        }
        for refined, divisor in ((False, 2), (False, 4), (True, 2), (True, 4))
    )
    if engine == "genesis":
        out.append(
            {
                "family": "soft_compression",
                "dt": base,
                "refined": False,
                "duration": 1.5,
                "repeat": 0,
                "sap_iterations": 50,
                "purpose": "independent convergence/force diagnostic",
            }
        )
    for i, c in enumerate(out):
        c["id"] = f"{c['family']}-{i:02d}"
    return out


def run(case, engine, path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=False)
    sim = None
    records = []
    status = "completed"
    error = None
    audit = {}
    start = time.perf_counter()
    minimum = float("inf")
    (path / "case.json").write_text(json.dumps(case, indent=2))
    try:
        if engine in ("mujoco", "mujoco-warp"):
            sim = MuJoCoSoft(case, engine)
        else:
            from importlib import import_module

            sim = import_module(".soft_" + engine.replace("-", "_"), __package__).Simulation(case)
        audit = sim.audit
        if "scene_usda" in audit:
            (path / "scene.usda").write_text(audit.pop("scene_usda"))
        if sim.scene is not None:
            np.savez_compressed(path / "reference.npz", **sim.scene.reference)
            audit["reference_sha256"] = sim.scene.reference["sha256"]
        restvol = volumes(sim.rest, sim.elements)
        stride = max(1, round(0.005 / case["dt"]))
        np.savez_compressed(
            path / "mesh.npz", vertices=sim.rest, elements=sim.elements, masses=sim.masses
        )
        if getattr(sim, "xml", None):
            (path / "scene.xml").write_text(sim.xml)
        records.append((0.0, sim.rest.copy(), 1.0, 0.0))
        for i in range(round(case["duration"] / case["dt"])):
            verts = sim.step(i)
            if (i + 1) % max(1, round(0.05 / case["dt"])) == 0:
                (path / "progress.json").write_text(
                    json.dumps(
                        {
                            "step": i + 1,
                            "simulated_seconds": (i + 1) * case["dt"],
                            "wall_seconds": time.perf_counter() - start,
                            "planned_seconds": case["duration"],
                        }
                    )
                )
            if not np.isfinite(verts).all():
                raise FloatingPointError("Non-finite soft vertex")
            ratio = float(np.min(volumes(verts, sim.elements) / restvol))
            minimum = min(minimum, ratio)
            if ratio <= 0:
                records.append(
                    (
                        (i + 1) * case["dt"],
                        verts.copy(),
                        ratio,
                        float(getattr(sim, "compression_load", float("nan"))),
                    )
                )
                status = "inverted"
                break
            if (i + 1) % stride == 0:
                records.append(
                    (
                        (i + 1) * case["dt"],
                        verts.copy(),
                        ratio,
                        float(getattr(sim, "compression_load", float("nan"))),
                    )
                )
    except (Exception, KeyboardInterrupt) as exc:  # noqa: BLE001 - retain native failures as auditable results
        status = "interrupted" if isinstance(exc, KeyboardInterrupt) else "error"
        error = str(exc)
        (path / "error.txt").write_text(traceback.format_exc())
    finally:
        if sim is not None:
            try:
                sim.close()
            except Exception as exc:  # noqa: BLE001 - preserve measurements on native teardown failure
                status = "error"
                error = (error + "; " if error else "") + f"Native cleanup failed: {exc}"
                (path / "cleanup-error.txt").write_text(str(exc))
    success = False
    hold_lift = None
    hold_com_lift = None
    hold_covered = False
    if records:
        times = np.array([r[0] for r in records])
        verts = np.array([r[1] for r in records])
        ratios = np.array([r[2] for r in records])
        centroid = verts.mean(axis=1)
        com = np.sum(verts * sim.masses[None, :, None], axis=1) / sim.masses.sum()
        np.savez_compressed(
            path / "trajectory.npz",
            time=times,
            vertices=verts,
            centroid=centroid,
            com=com,
            min_volume_ratio=ratios,
            raw_compression_load_n=np.array([r[3] for r in records]),
        )
        hold = (times >= 1.9) & (times <= 2.2)
        hold_covered = bool(hold.any() and times[-1] >= 2.2)
        if hold_covered:
            hold_lift = float(np.mean(centroid[hold, 2]) - centroid[0, 2])
            hold_com_lift = float(np.mean(com[hold, 2]) - com[0, 2])
            success = bool(status == "completed" and hold_com_lift > 0.04)
        if case["family"] == "soft_compression":
            success = status == "completed"
    validated = bool(audit.get("force_validated"))
    load = None
    if validated and case["family"] == "soft_compression" and status == "completed":
        hold = (times >= 0.65) & (times <= 0.85)
        load = float(np.mean(np.array([r[3] for r in records])[hold]))
    result = {
        "engine": engine,
        "case": case,
        "status": status,
        "error": error,
        "numerically_valid": status == "completed",
        "task_success": success,
        "hold_lift_m": hold_lift,
        "hold_com_lift_m": hold_com_lift,
        "hold_window_covered": hold_covered,
        "minimum_volume_ratio": minimum if np.isfinite(minimum) else None,
        "force_n": load,
        "force_validated": validated,
        "force_note": "Native contact impulses passed nodal momentum balance."
        if validated
        else "Native deformable load accounting has not passed an independent momentum audit; no zero-load substitution.",
        "audit": audit,
        "samples": len(records),
        "wall_seconds": time.perf_counter() - start,
    }
    (path / "result.json").write_text(json.dumps(result, indent=2, allow_nan=False))
    return result


def main(args):
    plan = cases(args.engine)
    if args.family:
        plan = [c for c in plan if c["family"] in args.family]
    if args.case_index is not None:
        plan = [plan[args.case_index]]
    if args.plan_only:
        print(json.dumps(plan, indent=2))
        return 0
    from .suite import source_hashes

    manifest = {"engine": args.engine, "cases": plan, "source_hashes": source_hashes()}
    manifest_path = args.output / "manifest.json"
    if args.output.exists():
        if (
            not args.resume
            or not manifest_path.exists()
            or json.loads(manifest_path.read_text()) != manifest
        ):
            raise ValueError("Resume requires the same soft matrix and source; choose a new output")
    else:
        args.output.mkdir(parents=True)
        manifest_path.write_text(json.dumps(manifest, indent=2))
        from ..cli import environment

        (args.output / "environment.json").write_text(
            json.dumps(environment(args.engine), indent=2)
        )
    results = []
    for case in plan:
        path = args.output / case["id"]
        file = path / "result.json"
        attempts = sorted(path.glob("attempt-*/result.json")) if path.exists() else []
        if attempts:
            file = attempts[-1]
        if (
            file.exists()
            and args.resume
            and json.loads(file.read_text()).get("status") != "interrupted"
        ):
            r = json.loads(file.read_text())
        else:
            if path.exists():
                path = path / f"attempt-{len(list(path.glob('attempt-*'))) + 1:04d}"
            r = run(case, args.engine, path)
        results.append(r)
        (args.output / "results.json").write_text(json.dumps(results, indent=2))
        print(case["id"], r["status"], r.get("error"), flush=True)
        if r["status"] == "interrupted":
            return 130
    return int(any(r["status"] == "error" for r in results))
