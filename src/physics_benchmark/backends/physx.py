"""Isaac Sim worker in the user's local container; no host simulator installation."""

import atexit
import json
import os
import queue
import subprocess
import threading
from pathlib import Path
from uuid import uuid4

import numpy as np

from ..sampling import make_row
from ..scenes import scene_xml
from ..simulation import Run

_worker = None


class Worker:
    def __init__(self, script="isaac_worker.py"):
        self.image = os.environ.get("PHYSICS_BENCH_ISAAC_IMAGE", "nvcr.io/nvidia/isaac-sim:6.0.1")
        self.name = "physics-bench-" + uuid4().hex[:12]
        self.closed = False
        self.image_id = subprocess.check_output(
            ["docker", "image", "inspect", self.image, "--format", "{{.Id}}"], text=True, timeout=15
        ).strip()
        root = Path(__file__).resolve().parents[3]
        logdir = root / ".cache/logs"
        logdir.mkdir(parents=True, exist_ok=True)
        self.log = (logdir / f"{self.name}.log").open("w")
        self.messages = queue.Queue()
        self.process = subprocess.Popen(
            [
                "docker",
                "run",
                "--rm",
                "--pull=never",
                "-i",
                "--gpus",
                "all",
                "--name",
                self.name,
                "-e",
                "ACCEPT_EULA=Y",
                "-v",
                f"{root}:/workspace:ro",
                "-w",
                "/workspace",
                "--entrypoint",
                "/isaac-sim/python.sh",
                self.image,
                "-u",
                f"/workspace/scripts/{script}",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()
        atexit.register(self.close)
        try:
            if self.receive()["kind"] != "ready":
                raise RuntimeError("Isaac worker did not initialize")
        except BaseException:
            self.close()
            raise

    def _read(self):
        try:
            for line in self.process.stdout:
                if line.startswith("PHYSICS_BENCH:"):
                    self.messages.put(json.loads(line[len("PHYSICS_BENCH:") :]))
                else:
                    self.log.write(line)
                    self.log.flush()
        finally:
            self.messages.put(
                {"kind": "error", "error": "Isaac worker exited; see " + self.log.name}
            )

    def receive(self):
        try:
            message = self.messages.get(timeout=180)
        except queue.Empty as exc:
            self.close()
            raise RuntimeError("Isaac worker timed out; see " + self.log.name) from exc
        if message["kind"] == "error":
            self.close()
            raise RuntimeError(message["error"])
        return message

    def send(self, message):
        """A failed protocol connection must never be reused by a later trial."""
        if self.closed or self.process.poll() is not None or self.process.stdin.closed:
            self.close()
            raise RuntimeError("Isaac worker connection is closed; see " + self.log.name)
        try:
            self.process.stdin.write(json.dumps(message) + "\n")
            self.process.stdin.flush()
        except (OSError, ValueError):
            self.close()
            raise

    def close(self):
        if self.closed:
            return
        self.closed = True
        atexit.unregister(self.close)
        # Cleanup failures are diagnostics, not replacements for the native error.
        self.cleanup_errors = []
        if self.process.poll() is None:
            if not self.process.stdin.closed:
                try:
                    self.process.stdin.close()
                except OSError as exc:
                    self.cleanup_errors.append(str(exc))
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                try:
                    stopped = subprocess.run(
                        ["docker", "stop", "--time", "5", self.name],
                        capture_output=True,
                        text=True,
                        timeout=15,
                        check=False,
                    )
                    if stopped.returncode:
                        self.cleanup_errors.append(stopped.stderr.strip())
                except (OSError, subprocess.TimeoutExpired) as exc:
                    self.cleanup_errors.append(str(exc))
                try:
                    self.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait(timeout=10)
        self.reader.join(timeout=2)
        if not self.reader.is_alive():
            if self.cleanup_errors:
                self.log.write("\nCleanup diagnostics: " + repr(self.cleanup_errors) + "\n")
            self.log.close()


def simulate(scene, cfg, dt, rows=None, on_sample=None):
    global _worker
    rows = [] if rows is None else rows
    if (
        _worker is None
        or _worker.closed
        or _worker.process.poll() is not None
        or _worker.process.stdin.closed
    ):
        _worker = Worker()
    imported = None
    try:
        _worker.send({"scene": scene, "config": cfg, "dt": dt})
        while True:
            message = _worker.receive()
            if message["kind"] == "imported":
                imported = message["data"]
                imported["container_image"] = _worker.image
                imported["container_image_id"] = _worker.image_id
            elif message["kind"] == "sample":
                impulse = np.array(message["impulse"])
                rows.append(
                    make_row(
                        scene,
                        cfg,
                        dt,
                        message["step"],
                        message["q_before"],
                        message["v_before"],
                        message["q_after"],
                        message["v_after"],
                        impulse / dt,
                        message["contacts"],
                        message["torque"],
                        native_impulse=impulse,
                    )
                )
                for component in ("normal", "friction"):
                    for i, axis in enumerate("xyz"):
                        rows[-1][f"{component}_j{axis}_ns"] = message[component + "_impulse"][i]
                if on_sample is not None:
                    on_sample(rows[-1])
            elif message["kind"] == "done":
                break
    except BaseException:
        _worker.close()
        _worker = None
        raise
    if imported is None or len(rows) != round(cfg["durations_s"][scene] / dt):
        raise RuntimeError("Incomplete PhysX worker output")
    return Run(rows, imported, scene_xml(scene, cfg, dt))
