"""Compare nominal insertion against the same motion without contact, on CPU."""

import argparse
import json
from pathlib import Path
from xml.etree import ElementTree as ET

import mujoco as mj
import numpy as np

from physics_benchmark.extended.model import build, rotation
from physics_benchmark.extended.rigid import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    summary = []
    for clearance in (0.0001, 0.0005):
        for contact in (True, False):
            scene = build(
                {"family": "insertion", "clearance": clearance, "offset": 0, "tilt_deg": 0}
            )
            scene.case.update(diagnostic="contact" if contact else "no_contact")
            if not contact:
                root = ET.fromstring(scene.xml)
                ET.SubElement(root.find("option"), "flag", contact="disable")
                scene.xml = ET.tostring(root, encoding="unicode")
                model = mj.MjModel.from_xml_string(scene.xml)
                data = mj.MjData(model)
                data.qpos[:] = scene.data.qpos
                data.qvel[:] = scene.data.qvel
                mj.mj_forward(model, data)
                scene.model, scene.data = model, data
            path = args.output / f"clearance-{clearance:g}-{scene.case['diagnostic']}"
            result = run(scene, "mujoco", path)
            with np.load(path / "trajectory.npz") as a:
                h = scene.model.body("hand").id
                index = np.minimum(
                    np.rint(a["time"] / scene.reference["dt"]).astype(int),
                    len(scene.reference["hand"]) - 1,
                )
                deviation = a["position"][:, h] - scene.reference["hand"][index]
                orientation_error = np.array(
                    [
                        np.linalg.norm(rotation(q) - target)
                        for q, target in zip(
                            a["quaternion"][:, h], scene.reference["hand_rotation"][index]
                        )
                    ]
                )
                summary.append(
                    {
                        "clearance_m": clearance,
                        "contact_enabled": contact,
                        "status": result["status"],
                        "task_success": result["task_success"],
                        "final_depth_m": result.get("final_insertion_depth_m"),
                        "max_lateral_tracking_error_m": float(
                            np.linalg.norm(deviation[:, :2], axis=1).max()
                        ),
                        "max_orientation_matrix_error": float(orientation_error.max()),
                    }
                )
    (args.output / "audit.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
