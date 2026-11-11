"""Serialize the canonical model; execute every physics step in Isaac Sim PhysX."""

import mujoco as mj
import numpy as np

from ..backends.physx import Worker

_worker = None


def specification(scene):
    m = scene.model
    zero = mj.MjData(m)
    mj.mj_forward(m, zero)
    bodies = []
    for b in range(1, m.nbody):
        joints = []
        for j in range(m.body_jntadr[b], m.body_jntadr[b] + m.body_jntnum[b]):
            joints.append(
                {
                    "name": m.joint(j).name,
                    "type": int(m.jnt_type[j]),
                    "axis": m.jnt_axis[j].tolist(),
                    "pos": m.jnt_pos[j].tolist(),
                    "range": m.jnt_range[j].tolist(),
                    "limited": bool(m.jnt_limited[j]),
                    "qadr": int(m.jnt_qposadr[j]),
                    "vadr": int(m.jnt_dofadr[j]),
                }
            )
        bodies.append(
            {
                "id": b,
                "mocap": int(m.body_mocapid[b]),
                "name": m.body(b).name,
                "parent": int(m.body_parentid[b]),
                "root": int(m.body_rootid[b]),
                "mass": float(m.body_mass[b]),
                "com": m.body_ipos[b].tolist(),
                "inertia": m.body_inertia[b].tolist(),
                "iquat": m.body_iquat[b].tolist(),
                "pos": m.body_pos[b].tolist(),
                "quat": m.body_quat[b].tolist(),
                "worldpos": zero.xpos[b].tolist(),
                "worldquat": zero.xquat[b].tolist(),
                "joints": joints,
            }
        )
    geoms = []
    for g in range(m.ngeom):
        spec = {
            "name": m.geom(g).name or f"geom{g}",
            "body": int(m.geom_bodyid[g]),
            "type": int(m.geom_type[g]),
            "size": m.geom_size[g].tolist(),
            "pos": m.geom_pos[g].tolist(),
            "quat": m.geom_quat[g].tolist(),
            "friction": float(m.geom_friction[g, 0]),
            "contype": int(m.geom_contype[g]),
            "conaffinity": int(m.geom_conaffinity[g]),
        }
        if m.geom_type[g] == mj.mjtGeom.mjGEOM_MESH:
            k = m.geom_dataid[g]
            start = m.mesh_vertadr[k]
            count = m.mesh_vertnum[k]
            fs = m.mesh_faceadr[k]
            nf = m.mesh_facenum[k]
            spec.update(
                vertices=m.mesh_vert[start : start + count].tolist(),
                faces=m.mesh_face[fs : fs + nf].tolist(),
            )
        geoms.append(spec)
    return {
        "bodies": bodies,
        "geoms": geoms,
        "case": scene.case,
        "controlled": scene.controlled,
        "q": scene.data.qpos.tolist(),
        "v": scene.data.qvel.tolist(),
        "nbody": m.nbody,
    }


class PhysX:
    def __init__(self, scene):
        global _worker
        if (
            _worker is None
            or _worker.closed
            or _worker.process.poll() is not None
            or _worker.process.stdin.closed
        ):
            _worker = Worker("isaac_extended_worker.py")
        self.worker = _worker
        self.m = scene.model
        self.send({"kind": "build", "spec": specification(scene)})
        reply = self.worker.receive()
        self.audit = reply["audit"]
        self.audit.update(
            container_image=self.worker.image, container_image_id=self.worker.image_id
        )
        self.current = reply["state"]

    def send(self, msg):
        self.worker.send(msg)

    def state(self):
        return tuple(np.asarray(self.current[k]) for k in ("q", "v", "position", "quaternion"))

    def set_state(self, q, v):
        self.send({"kind": "set_state", "q": q.tolist(), "v": v.tolist()})
        self.current = self.worker.receive()["state"]

    def step(self, command):
        self.send({"kind": "step", "command": command.tolist()})
        reply = self.worker.receive()
        self.current = reply["state"]
        return np.asarray(reply["wrench"])

    def close(self):
        if self.worker.closed or self.worker.process.poll() is not None:
            return
        self.send({"kind": "release"})
        self.worker.receive()
