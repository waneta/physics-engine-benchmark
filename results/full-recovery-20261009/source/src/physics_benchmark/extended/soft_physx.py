"""Isaac Sim GPU TetMesh, with native rest-node and connectivity checks."""

from xml.etree import ElementTree as ET

import mujoco as mj
import numpy as np

from ..backends.physx import Worker
from .model import Scene, smooth
from .physx import specification
from .rigid import Controller
from .soft import prepare


class Simulation:
    def __init__(self, case):
        self.case = case
        self.scene, root, self.rest, self.elements, self.masses = prepare(case)
        self.n = 9 if self.scene else 0
        self.xml = ET.tostring(root, encoding="unicode")
        if self.scene:
            scene = self.scene
            self.controller = Controller(scene)
        else:
            model = mj.MjModel.from_xml_string(self.xml)
            data = mj.MjData(model)
            mj.mj_forward(model, data)
            scene = Scene(case, model, data, self.xml, 0, {}, [], {})
        spec = specification(scene)
        spec["soft"] = {"vertices": self.rest.tolist(), "elements": self.elements.tolist()}
        self.worker = Worker("isaac_extended_worker.py")
        try:
            self.send({"kind": "build", "spec": spec})
            reply = self.worker.receive()
        except BaseException:
            self.worker.close()
            raise
        self.state = reply["state"]
        self.audit = reply["audit"]
        self.audit.update(
            engine="physx",
            solver="GPU PhysX deformable + TGS articulation",
            container_image=self.worker.image,
            container_image_id=self.worker.image_id,
            force_validated=False,
            vertex_count=len(self.rest),
            element_count=len(self.elements),
            mass_kg=float(self.masses.sum()),
            rest_mesh_validation="passed",
        )
        np.testing.assert_allclose(self.state["vertices"], self.rest, atol=1e-6)
        self.u = np.zeros(self.n)

    def send(self, msg):
        self.worker.send(msg)

    def step(self, i):
        if self.n and i % round(0.001 / self.case["dt"]) == 0:
            self.u = self.controller.command(
                i,
                np.array(self.state["q"]),
                np.array(self.state["v"]),
                np.zeros((self.scene.model.nbody, 6)),
                np.array(self.state["position"]),
            )
        request = {"kind": "step", "command": self.u.tolist()}
        if not self.n:
            t = i * self.case["dt"]
            c = 0.006 * smooth(t, 0.2, 0.6) * (1 - smooth(t, 0.9, 1.3))
            request["plates"] = [[-0.04 + c, 0, 0], [0.04 - c, 0, 0]]
        self.send(request)
        reply = self.worker.receive()
        self.state = reply["state"]
        peak = float(np.linalg.norm(np.asarray(reply["wrench"])[..., :3], axis=-1).max())
        self.audit["rigid_contact_probe_peak_n"] = max(
            self.audit.get("rigid_contact_probe_peak_n", 0.0), peak
        )
        return np.asarray(self.state["vertices"])

    def close(self):
        self.worker.close()
