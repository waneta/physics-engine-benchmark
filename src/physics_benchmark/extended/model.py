"""One pinned Panda asset, analytic fixtures and frozen cross-engine references."""

import copy
import hashlib
import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

import mujoco as mj
import numpy as np

ASSET = Path(__file__).resolve().parents[3] / "configs/assets/panda/source.xml"
HOME = np.array([0, -np.pi / 4, 0, -3 * np.pi / 4, 0, np.pi / 2, np.pi / 4])
KP = np.array([80, 80, 60, 60, 20, 15, 8, 400, 400], float)
KD = np.array([18, 18, 14, 14, 5, 4, 2, 4, 4], float)
LIMIT = np.array([87] * 4 + [12] * 3 + [4, 4], float)


def numbers(a):
    return " ".join(f"{x:.16g}" for x in np.asarray(a).ravel())


def rotation(q):
    out = np.empty(9)
    mj.mju_quat2Mat(out, np.asarray(q, dtype=float))
    return out.reshape(3, 3)


def smooth(t, start, end):
    s = np.clip((np.asarray(t) - start) / (end - start), 0, 1)
    return s**3 * (10 - 15 * s + 6 * s * s)


def panda_xml(active_fingers=True):
    original = ET.parse(ASSET).getroot()
    robot = copy.deepcopy(original.find("worldbody/body"))
    for body in robot.iter("body"):
        body.attrib.pop("childclass", None)
        for geom in list(body.findall("geom")):
            body.remove(geom)
        for joint in body.findall("joint"):
            finger = "finger" in joint.get("name", "")
            joint.attrib.pop("class", None)
            joint.set("axis", "0 1 0" if finger else "0 0 1")
            joint.set("type", "slide" if finger else "hinge")
            joint.set("range", joint.get("range", "0 0.04" if finger else "-2.8973 2.8973"))
            joint.set("limited", "true" if finger else "false")
            joint.set("armature", "0")
            joint.set("damping", "0")
            joint.set("frictionloss", "0")
            if finger and not active_fingers:
                pos = np.fromstring(body.get("pos", "0 0 0"), sep=" ")
                pos += rotation(np.fromstring(body.get("quat", "1 0 0 0"), sep=" ")) @ [0, 0.04, 0]
                body.set("pos", numbers(pos))
                body.remove(joint)
        if "finger" in body.get("name", "") and active_fingers:
            ET.SubElement(
                body,
                "geom",
                name=body.get("name") + "_pad",
                type="box",
                pos="0 0.004 0.0445",
                size="0.012 0.004 0.016",
                mass="0",
                contype="1",
                conaffinity="2",
                rgba=".3 .3 .35 1",
            )
    return robot


def root_xml(dt, friction=0.5):
    root = ET.Element("mujoco", model="extended")
    ET.SubElement(root, "compiler", angle="radian", autolimits="true", fusestatic="false")
    ET.SubElement(
        root,
        "option",
        timestep=str(dt),
        gravity="0 0 -9.81",
        integrator="Euler",
        solver="Newton",
        cone="elliptic",
        iterations="100",
        tolerance="1e-10",
    )
    default = ET.SubElement(root, "default")
    ET.SubElement(
        default,
        "geom",
        condim="3",
        friction=f"{friction} 0 0",
        solref=".01 1",
        solimp=".99 .999 .001 .5 2",
        margin="0",
        gap="0",
    )
    ET.SubElement(root, "asset")
    ET.SubElement(root, "worldbody")
    return root


def mesh(root, name, vertices, faces):
    ET.SubElement(
        root.find("asset"), "mesh", name=name, vertex=numbers(vertices), face=numbers(faces)
    )


def prism_mesh(sides, radius, halfheight, phase=0):
    angles = np.arange(sides) * 2 * np.pi / sides + phase
    vertices = np.array(
        [
            [radius * np.cos(a), radius * np.sin(a), z]
            for z in [-halfheight, halfheight]
            for a in angles
        ]
    )
    faces = []
    for i in range(1, sides - 1):
        faces.extend([[0, i + 1, i], [sides, sides + i, sides + i + 1]])
    for i in range(sides):
        j = (i + 1) % sides
        faces.extend([[i, j, sides + j], [i, sides + j, sides + i]])
    return vertices, faces


def solid(
    root,
    name,
    pos,
    size,
    mass=None,
    kind="box",
    quat=None,
    inertia=None,
    contype=2,
    conaffinity=7,
    parent=None,
):
    world = root.find("worldbody") if parent is None else parent
    body = ET.SubElement(world, "body", name=name, pos=numbers(pos))
    if quat is not None:
        body.set("quat", numbers(quat))
    if mass is not None:
        ET.SubElement(body, "freejoint", name=name + "_free")
    attrs = {
        "name": name + "_geom",
        "type": kind,
        "contype": str(contype),
        "conaffinity": str(conaffinity),
    }
    if kind == "mesh":
        attrs["mesh"] = size
    else:
        attrs["size"] = numbers(size)
    if mass is not None:
        attrs["mass"] = str(mass)
    if inertia is not None:
        ET.SubElement(body, "inertial", mass=str(mass), pos="0 0 0", diaginertia=numbers(inertia))
    ET.SubElement(body, "geom", **attrs)
    return body


def compile_model(root, active_fingers=True):
    xml = ET.tostring(root, encoding="unicode")
    model = mj.MjModel.from_xml_string(xml)
    data = mj.MjData(model)
    if mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, "hand") >= 0:
        data.qpos[:7] = HOME
        if active_fingers:
            data.qpos[7:9] = 0.04
    mj.mj_forward(model, data)
    return model, data, xml


def ik(model, q, target, orientation, tolerance=2e-7):
    data = mj.MjData(model)
    data.qpos[: len(q)] = q
    hand = model.body("hand").id
    jp = np.zeros((3, model.nv))
    jr = np.zeros_like(jp)
    for _ in range(250):
        mj.mj_forward(model, data)
        current = data.xmat[hand].reshape(3, 3)
        error = np.r_[
            target - data.xpos[hand],
            0.5 * sum(np.cross(current[:, i], orientation[:, i]) for i in range(3)),
        ]
        if np.linalg.norm(error) < tolerance:
            return data.qpos[: len(q)].copy()
        mj.mj_jacBody(model, data, jp, jr, hand)
        jac = np.vstack([jp[:, :7], jr[:, :7]])
        dq = jac.T @ np.linalg.solve(jac @ jac.T + np.eye(6) * 1e-5, error)
        data.qpos[:7] += np.clip(dq, -0.08, 0.08)
    raise RuntimeError(f"IK did not converge: {np.linalg.norm(error):.5g}")


@dataclass
class Scene:
    case: dict
    model: object
    data: object
    xml: str
    controlled: int
    reference: dict
    objects: list
    parameters: dict


def build(case):
    family = case["family"]
    dt = case.get("dt", 0.001)
    robot = family != "collision_chain"
    active = family not in ("panda_open_loop", "panda_tracking", "throughput")
    root = root_xml(dt, 0.3 if not robot else 0.5)
    if robot:
        root.find("worldbody").append(panda_xml(active))
    params = {}
    objects = []
    if family == "collision_chain":
        ET.SubElement(
            root.find("worldbody"),
            "geom",
            name="floor",
            type="plane",
            size="2 2 .1",
            contype="4",
            conaffinity="2",
        )
        solid(root, "sphere", [-0.18, -0.012, 0.03], [0.03], 0.15, "sphere")
        solid(root, "cube", [0, 0, 0.03], [0.03] * 3, 0.1)
        vertices, faces = prism_mesh(3, 0.09 / np.sqrt(3), 0.03, np.pi / 2)
        mesh(root, "triangle", vertices, faces)
        ix = 0.1 * (0.09**2 / 24 + 0.06**2 / 12)
        iz = 0.1 * 0.09**2 / 12
        solid(root, "prism", [0.1, 0.02, 0.03], "triangle", 0.1, "mesh", inertia=[ix, ix, iz])
        objects = ["sphere", "cube", "prism"]
        duration = 1.0
    else:
        m, d, _ = compile_model(root, active)
        hand = m.body("hand").id
        hand0 = d.xpos[hand].copy()
        orientation = d.xmat[hand].reshape(3, 3).copy()
        grip = hand0 + orientation @ np.array([0, 0, 0.1029])
        table_z = grip[2] - 0.02
        params.update(
            hand0=hand0.tolist(),
            orientation=orientation.tolist(),
            grip0=grip.tolist(),
            table_z=table_z,
        )
        duration = {
            "panda_open_loop": 0.5,
            "panda_tracking": 2.5,
            "throughput": 2.5,
            "grasp": 3.5,
            "stack": 6.0,
            "push": case.get("push_duration", 3.0) + 2.0,
            "sweep": 12.5,
            "insertion": 4.0,
            "soft_grasp": 4.5,
        }.get(family)
        if duration is None:
            raise ValueError(f"Unknown family {family}")
        if active:
            solid(
                root,
                "table",
                [grip[0] + 0.1, 0, table_z - 0.025],
                [0.5, 0.5, 0.025],
                contype=4,
                conaffinity=2,
            )
        if family in ("grasp", "stack"):
            shift = np.array([case.get("perturb_x", 0), case.get("perturb_y", 0), 0])
            position = (
                grip
                + orientation[:, 0] * (case.get("offset", 0) if family == "grasp" else 0)
                + shift
            )
            solid(root, "cube", position, [0.02] * 3, 0.1)
            objects = ["cube"]
            if family == "stack":
                base = grip + np.array([0.1, 0, 0])
                solid(root, "lower_cube", base, [0.02] * 3, 0.1)
                objects.append("lower_cube")
                params["stack_target"] = base.tolist()
        elif family == "push":
            rear = grip + np.array([0.043, case.get("rear_y", 0), 0])
            front = grip + np.array([0.085, 0, 0])
            for i, pos in enumerate([rear, front + [0, -0.022, 0], front + [0, 0.022, 0]]):
                name = f"cube{i}"
                solid(root, name, pos, [0.02] * 3, 0.1)
                objects.append(name)
            entry = front[0] + 0.036
            width = case.get("width", 0.09)
            for sign in [-1, 1]:
                solid(
                    root,
                    f"wall_{sign}",
                    [entry + 0.15, sign * (width / 2 + 0.015), table_z + 0.05],
                    [0.15, 0.015, 0.05],
                    contype=4,
                    conaffinity=2,
                )
            params.update(entry_x=entry, goal_x=entry + 0.06)
        elif family == "sweep":
            hand_node = root.find('.//body[@name="hand"]')
            ET.SubElement(hand_node, "body", name="paddle", pos="0 0 .0929")
            paddle = hand_node[-1]
            ET.SubElement(
                paddle,
                "geom",
                name="paddle_geom",
                type="box",
                size=".012 .11 .03",
                mass=".15",
                contype="1",
                conaffinity="6",
            )
            for i in range(15):
                x = grip[0] + 0.07 + 0.045 * (i // 5)
                y = -0.09 + 0.045 * (i % 5)
                kind = ("sphere", "box", "mesh")[i % 3]
                name = f"object{i}"
                r = 0.018
                h = 0.02
                if kind == "sphere":
                    size = [r]
                    mass = 500 * 4 * np.pi * r**3 / 3
                    inertia = None
                elif kind == "box":
                    size = [r] * 3
                    mass = 500 * (2 * r) ** 3
                    inertia = None
                else:
                    size = f"cylinder{i}"
                    vertices, faces = prism_mesh(32, r, h)
                    mesh(root, size, vertices, faces)
                    mass = 500 * np.pi * r * r * 2 * h
                    inertia = [mass * (3 * r * r + 4 * h * h) / 12] * 2 + [mass * r * r / 2]
                solid(
                    root,
                    name,
                    [x, y, table_z + (h if kind == "mesh" else r)],
                    size,
                    mass,
                    kind,
                    inertia=inertia,
                )
                objects.append(name)
            entry = grip[0] + 0.25
            tray_z = table_z - 0.015
            solid(
                root,
                "tray",
                [entry + 0.15, 0, tray_z - 0.025],
                [0.15, 0.15, 0.025],
                contype=4,
                conaffinity=3,
            )
            # Replace the table by a finite surface, followed by a shared sloping ramp.
            table = root.find('.//body[@name="table"]')
            table.set("pos", numbers([grip[0] - 0.1, 0, table_z - 0.025]))
            table.find("geom").set("size", numbers([0.35, 0.5, 0.025]))
            vertices = np.array(
                [
                    [x, y, z]
                    for x, z in [(entry - 0.02, table_z), (entry + 0.06, tray_z)]
                    for y in [-0.15, 0.15]
                ]
            )
            vertices = np.vstack([vertices, vertices - [0, 0, 0.025]])
            faces = [
                [0, 1, 3],
                [0, 3, 2],
                [4, 6, 7],
                [4, 7, 5],
                [0, 4, 5],
                [0, 5, 1],
                [2, 3, 7],
                [2, 7, 6],
                [0, 2, 6],
                [0, 6, 4],
                [1, 5, 7],
                [1, 7, 3],
            ]
            mesh(root, "ramp_mesh", vertices, faces)
            solid(root, "ramp", [0, 0, 0], "ramp_mesh", kind="mesh", contype=4, conaffinity=3)
            for sign in (-1, 1):
                solid(
                    root,
                    f"passage_{sign}",
                    [entry + 0.15, sign * 0.16, tray_z + 0.04],
                    [0.15, 0.01, 0.04],
                    contype=4,
                    conaffinity=3,
                )
            angle = -np.pi / 4
            solid(
                root,
                "guide",
                [entry - 0.04, 0.19, table_z + 0.04],
                [np.sqrt(2) * 0.04, 0.008, 0.04],
                quat=[np.cos(angle / 2), 0, 0, np.sin(angle / 2)],
                contype=4,
                conaffinity=3,
            )
            params.update(tray_bounds=[entry, entry + 0.3, -0.15, 0.15, tray_z, tray_z + 0.1])
        elif family == "insertion":
            # Explicit 64-faced peg and segmented, chamfered convex hole wall.
            hand_node = root.find('.//body[@name="hand"]')
            radius = 0.01
            length = 0.04
            vertices, faces = prism_mesh(64, radius, length / 2)
            mesh(root, "peg_mesh", vertices, faces)
            peg = ET.SubElement(hand_node, "body", name="peg", pos="0 0 .12")
            ET.SubElement(
                peg,
                "geom",
                name="peg_geom",
                type="mesh",
                mesh="peg_mesh",
                mass=".1",
                contype="1",
                conaffinity="4",
            )
            clearance = case.get("clearance", 0.0001)
            hole = grip.copy()
            hole[2] -= 0.055
            inner = radius + clearance
            outer = 0.028
            chamfer = 0.002
            depth = 0.03
            for i in range(64):
                angles = np.array([i, i + 1]) * 2 * np.pi / 64
                verts = []
                for z, rin in [(0, inner + chamfer), (-chamfer, inner), (-depth, inner)]:
                    for r in [rin, outer]:
                        for a in angles:
                            verts.append([r * np.cos(a), r * np.sin(a), z])
                # Convex hull triangulated by MuJoCo/PhysX/Genesis from identical vertices.
                faces = [[0, 1, 3], [0, 3, 2], [8, 10, 11], [8, 11, 9]]
                for lo, hi in [(0, 4), (4, 8)]:
                    for a, b in [(0, 2), (2, 3), (3, 1), (1, 0)]:
                        faces.extend([[lo + a, lo + b, hi + b], [lo + a, hi + b, hi + a]])
                name = f"hole_segment{i}"
                mesh(root, name, verts, faces)
                solid(root, name, hole, name, kind="mesh", contype=4, conaffinity=1)
            # Table must not intersect the insertion bore.
            root.find("worldbody").remove(root.find('.//body[@name="table"]'))
            params.update(hole_center=hole.tolist(), peg_tip_local=[0, 0, 0.14], target_depth=0.02)
    model, data, xml = compile_model(root, active)
    controlled = (9 if active else 7) if robot else 0
    if not robot:
        data.qvel[:3] = [1.4, 0, 0]
        data.qvel[3:6] = [0, 1.4 / 0.03, 0]
        mj.mj_forward(model, data)
    scene = Scene(
        dict(case, duration=duration, dt=dt), model, data, xml, controlled, {}, objects, params
    )
    if robot:
        scene.reference = frozen_reference(scene)
    return scene


def frozen_reference(scene):
    """Every runtime, including Newton's older MuJoCo, consumes the same 3.15 tape."""
    ignored = {
        "dt",
        "repeat",
        "id",
        "phase",
        "candidate",
        "controller",
        "kp_scale",
        "kd_scale",
        "finger_force",
        "refined",
        "guided",
    }
    case = {k: v for k, v in scene.case.items() if k not in ignored}
    signature = (
        json.dumps(case, sort_keys=True).encode() + ASSET.read_bytes() + Path(__file__).read_bytes()
    )
    directory = ASSET.parents[3] / ".cache" / "extended-references"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (hashlib.sha256(signature).hexdigest() + ".npz")
    if not path.exists():
        if mj.__version__ != "3.15.0":
            python = ASSET.parents[3] / ".venv" / "bin" / "python"
            subprocess.run(
                [
                    str(python),
                    "-c",
                    "import json,sys;from physics_benchmark.extended.model import build;build(json.loads(sys.argv[1]))",
                    json.dumps(scene.case),
                ],
                check=True,
            )
            if not path.exists():
                raise RuntimeError("Canonical reference environment must use MuJoCo 3.15.0")
        else:
            ref = reference(scene)
            with tempfile.NamedTemporaryFile(dir=directory, suffix=".npz", delete=False) as file:
                np.savez_compressed(file, **ref)
                temporary = Path(file.name)
            temporary.replace(path)
    with np.load(path) as data:
        ref = {key: data[key].copy() for key in data.files}
    ref["dt"] = float(ref["dt"])
    ref["sha256"] = str(ref["sha256"])
    scene.data.qpos[: scene.controlled] = ref["q"][0]
    scene.data.qvel[: scene.controlled] = 0
    mj.mj_forward(scene.model, scene.data)
    return ref


def reference(scene):
    model = scene.model
    n = scene.controlled
    family = scene.case["family"]
    duration = scene.case["duration"]
    dt = 0.0005
    times = np.arange(round(duration / dt) + 1) * dt
    q0 = scene.data.qpos[:n].copy()
    q = np.tile(q0, (len(times), 1))
    orientation = np.array(scene.parameters["orientation"])
    hand0 = np.array(scene.parameters["hand0"])

    def target(delta, rot=None):
        return ik(model, q0, hand0 + delta, orientation if rot is None else rot)

    def segment(start, end, left, right):
        idx = times >= start
        alpha = smooth(times[idx], start, end)[:, None]
        q[idx] = left + (right - left) * alpha

    if family in ("panda_tracking", "throughput"):
        goal = q0.copy()
        goal[:7] += [0.3, 0.25, 0.2, 0.2, -0.25, 0.15, 0.3]
        segment(0, 1.25, q0, goal)
        segment(1.25, 2.5, goal, q0)
    elif family in ("grasp", "stack", "soft_grasp"):
        closed = q0.copy()
        closed[7:] = 0.012 if family != "soft_grasp" else 0.017
        raised = target([0, 0, 0.08])
        raised[7:] = closed[7:]
        segment(0.3, 0.8, q0, closed)
        segment(1, 1.8, closed, raised)
        if family == "grasp":
            opened = raised.copy()
            opened[7:] = 0.04
            segment(2.3, 2.7, raised, opened)
        elif family == "soft_grasp":
            segment(2.3, 3.1, raised, closed)
            segment(3.3, 3.7, closed, q0)
        else:
            moved = target([0.1 + scene.case.get("offset", 0), 0, 0.08])
            moved[7:] = 0.012
            down = target([0.1 + scene.case.get("offset", 0), 0, 0.04])
            down[7:] = 0.012
            opened = down.copy()
            opened[7:] = 0.04
            withdraw = moved.copy()
            withdraw[7:] = 0.04
            segment(1.8, 2.7, raised, moved)
            segment(2.7, 3.5, moved, down)
            segment(3.6, 4, down, opened)
            segment(4.1, 4.8, opened, withdraw)
    elif family == "push":
        q0[7:] = 0.014
        q[:] = q0
        goal = target([0.24, 0, 0])
        goal[7:] = 0.014
        # IK at 61 Cartesian waypoints preserves a straight hand path.
        us = np.linspace(0, 1, 61)
        path = np.array([target([0.24 * u, 0, 0]) for u in us])
        path[:, 7:] = 0.014
        alpha = smooth(times, 0.5, 0.5 + scene.case.get("push_duration", 3.0))
        for j in range(n):
            q[:, j] = np.interp(alpha, us, path[:, j])
    elif family == "sweep":
        goals = [
            (0, 0.5, [0, 0, 0.12], 0),
            (0.5, 1.5, [0, -0.06, 0.03], np.pi / 4),
            (1.5, 2, [0, -0.06, 0], np.pi / 4),
            (2, 5, [0.13, 0.07, 0], np.pi / 4),
            (5, 6, [0.13, 0.07, 0], 0),
            (6, 9, [0.31, 0, -0.015], 0),
            (9, 10, [0.31, 0, 0.12], 0),
            (10, 11, [0, 0, 0.15], 0),
        ]
        left = q0
        for a, b, delta, angle in goals:
            yaw = np.array(
                [[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]]
            )
            right = target(delta, yaw @ orientation)
            segment(a, b, left, right)
            left = right
    elif family == "insertion":
        tilt = np.deg2rad(scene.case.get("tilt_deg", 0))
        r = np.array([[np.cos(tilt), 0, np.sin(tilt)], [0, 1, 0], [-np.sin(tilt), 0, np.cos(tilt)]])
        orient = r @ orientation
        hole = np.array(scene.parameters["hole_center"])
        hand_start = (
            hole
            - orient @ np.array(scene.parameters["peg_tip_local"])
            + [scene.case.get("offset", 0), 0, 0.006]
        )
        q0 = ik(model, q0, hand_start, orient)
        q[:] = q0
        path = np.array(
            [ik(model, q0, hand_start - [0, 0, 0.026 * u], orient) for u in np.linspace(0, 1, 61)]
        )
        alpha = smooth(times, 0.5, 3.5)
        for j in range(n):
            q[:, j] = np.interp(alpha, np.linspace(0, 1, 61), path[:, j])
    v = np.gradient(q, dt, axis=0, edge_order=2)
    a = np.gradient(v, dt, axis=0, edge_order=2)
    ff = np.zeros_like(q)
    poses = np.zeros((len(q), 3))
    rotations = np.zeros((len(q), 3, 3))
    state = mj.MjData(model)
    state.qpos[:] = scene.data.qpos
    hand = model.body("hand").id
    flags = model.opt.disableflags
    model.opt.disableflags |= int(mj.mjtDisableBit.mjDSBL_CONTACT) | int(
        mj.mjtDisableBit.mjDSBL_LIMIT
    )
    for i in range(len(q)):
        state.qpos[:n] = q[i]
        state.qvel[:n] = v[i]
        state.qacc[:n] = a[i]
        mj.mj_inverse(model, state)
        ff[i] = state.qfrc_inverse[:n]
        poses[i] = state.xpos[hand]
        rotations[i] = state.xmat[hand].reshape(3, 3)
    model.opt.disableflags = flags
    if family == "panda_open_loop":
        ff[:] = ff[0]
        ff[(times >= 0.05) & (times < 0.15), 1] += 2
        ff[(times >= 0.15) & (times < 0.25), 3] -= 1
    scene.data.qpos[:n] = q[0]
    scene.data.qvel[:n] = 0
    mj.mj_forward(model, scene.data)
    return {
        "dt": dt,
        "q": q,
        "v": v,
        "feedforward": ff,
        "hand": poses,
        "hand_rotation": rotations,
        "sha256": hashlib.sha256(q.tobytes() + v.tobytes() + ff.tobytes()).hexdigest(),
    }
