"""Display measured engine states in an isolated, render-only MJCF viewer."""

import math
import multiprocessing
import os
import threading
import time
import traceback

import mujoco
import numpy as np

from .scenes import build_model


def validate_viewer_options(speed, hold):
    if not math.isfinite(speed) or speed <= 0:
        raise ValueError("--viewer-speed must be finite and > 0")
    if not math.isfinite(hold) or hold < 0:
        raise ValueError("--viewer-hold must be finite and >= 0")
    if os.name == "posix" and not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
        raise ValueError("--viewer 需要桌面显示服务；无界面运行请省略 --viewer")


class LiveViewer:
    """Never step the display model or share simulation arrays with the renderer.

    All four backends supply the same measured SI state. Mouse/viewer edits only
    affect this disposable display model, never the engine under measurement.
    """

    def __init__(self, scene, cfg, dt, speed=0.2, hold=2.0, engine="mujoco-cpu"):
        self.model, self.data, _, _ = build_model(scene, cfg, dt)
        self.scene = scene
        self.engine, self.dt = engine, dt
        self.speed, self.hold = speed, hold
        self.duration = cfg["durations_s"][scene]
        self.started = None
        self.last_frame = 0.0
        self.frames = 0
        self.handle = None
        self.render_threads = []

    def __enter__(self):
        return self

    def _open(self):
        # Genesis builds an EGL offscreen context even with show_viewer=False.
        # Initialize its physics scene first, before opening a GLFW/GLX window.
        import mujoco.viewer

        existing_threads = set(threading.enumerate())
        self.handle = mujoco.viewer.launch_passive(
            self.model, self.data, show_left_ui=False, show_right_ui=False
        )
        # MuJoCo launches a daemon render thread; finish its destroy() before GLFW atexit.
        self.render_threads = [
            thread
            for thread in threading.enumerate()
            if thread not in existing_threads and thread.name.endswith("(_launch_internal)")
        ]
        with self.handle.lock():
            self.handle.cam.lookat[:] = self.data.xpos[self.model.body("object").id]
            self.handle.cam.lookat[0] += 0.05
            self.handle.cam.distance = 0.45
            self.handle.cam.azimuth = 135
            self.handle.cam.elevation = -25
            if self.scene == "drop":
                height = self.data.qpos[2]
                self.handle.cam.lookat[:] = [self.data.qpos[0], self.data.qpos[1], height / 2]
                self.handle.cam.distance = max(0.45, 3 * height)
            self.model.geom_rgba[self.model.geom("object_geom").id] = [0.15, 0.6, 0.95, 1]
            self.model.vis.headlight.ambient[:] = 0.5
        self.handle.sync()
        self.handle.set_texts(
            (None, None, f"{self.engine} | dt={self.dt * 1000:g} ms", "Preparing...")
        )

    def __call__(self, row):
        if self.handle is None:
            self._open()
        if not self.handle.is_running():
            raise KeyboardInterrupt("viewer closed")
        now = time.monotonic()
        if self.started is None:
            # Start pacing at the first measured step, after engine compilation.
            self.started = now - row["t_end_s"] / self.speed
        delay = self.started + row["t_end_s"] / self.speed - now
        if delay > 0:
            time.sleep(delay)
        now = time.monotonic()
        if now - self.last_frame < 1 / 30 and row["t_end_s"] < self.duration - 1e-12:
            return
        with self.handle.lock():
            self.data.qpos[:] = [row[f"qpos{i}_end"] for i in range(self.model.nq)]
            self.data.qvel[:] = [row[f"qvel{i}_end"] for i in range(self.model.nv)]
            self.data.time = row["t_end_s"]
            mujoco.mj_forward(self.model, self.data)
        # Disable copying UI edits into the render model (camera interaction still works).
        self.handle.sync(state_only=True)
        if hasattr(self.handle, "set_texts"):
            axis, component = ("z", 2) if self.scene == "drop" else ("x", 0)
            self.handle.set_texts(
                (
                    None,
                    None,
                    f"{self.engine} | {self.scene} | dt={self.dt * 1000:g} ms",
                    (
                        f"t={row['t_end_s']:.3f} s\n"
                        f"{axis}={row[f'qpos{component}_end']:.5f} m\n"
                        f"v{axis}={row[f'qvel{component}_end']:.4f} m/s\n"
                        f"F{axis}={row[f'contact_f{axis}_n']:.4f} N"
                    ),
                )
            )
        self.frames += 1
        self.last_frame = now

    def finish(self):
        end = time.monotonic() + self.hold
        while time.monotonic() < end and self.handle.is_running():
            self.handle.sync(state_only=True)
            time.sleep(min(0.03, max(0, end - time.monotonic())))

    def __exit__(self, exc_type, *_):
        if self.handle is not None:
            self.handle.close()
        for thread in self.render_threads:
            thread.join(timeout=5)
            if thread.is_alive() and exc_type is None:
                raise RuntimeError("MuJoCo display thread did not finish shutdown")

    def audit(self):
        return {
            "mode": "live_measured_states",
            "renderer": "MuJoCo passive viewer; isolated display model, no mj_step",
            "frames": self.frames,
            "speed": self.speed,
            "hold_s": self.hold,
            "final_display_qpos": np.asarray(self.data.qpos).tolist(),
        }


def _display_process(connection, scene, cfg, dt, engine, hold):
    """Own the GLFW context outside Genesis's EGL process; no engine imports here."""
    try:
        finished = False
        with LiveViewer(scene, cfg, dt, speed=1e9, hold=hold, engine=engine) as viewer:
            viewer._open()
            connection.send({"kind": "ready"})
            pending = None
            coalesced = 0
            while viewer.handle.is_running():
                if pending is None:
                    if not connection.poll(0.02):
                        continue
                    message = connection.recv()
                else:
                    message, pending = pending, None
                if message["kind"] == "sample":
                    # Display the newest queued measurement. Control messages remain ordered,
                    # so an audit always observes the final sample preceding its request.
                    while connection.poll():
                        newer = connection.recv()
                        if newer["kind"] != "sample":
                            pending = newer
                            break
                        message = newer
                        coalesced += 1
                    viewer(message["row"])
                elif message["kind"] == "audit":
                    connection.send(
                        {
                            "kind": "audit",
                            "data": {
                                **viewer.audit(),
                                "coalesced_display_samples": coalesced,
                            },
                        }
                    )
                elif message["kind"] == "finish":
                    viewer.finish()
                    finished = True
                    break
                elif message["kind"] == "close":
                    return
            if not finished:
                connection.send({"kind": "closed"})
        if finished:
            connection.send({"kind": "finished"})
    except KeyboardInterrupt:
        connection.send({"kind": "closed"})
    except Exception:  # noqa: BLE001 - forward any renderer failure to the parent audit
        connection.send({"kind": "error", "error": traceback.format_exc()})
    finally:
        connection.close()


class ProcessViewer:
    """Render measured states in a spawned process with isolated GL resources."""

    def __init__(self, scene, cfg, dt, speed=0.2, hold=2.0, engine="genesis"):
        self.spec = (scene, cfg, dt, engine, hold)
        self.speed, self.hold, self.duration = speed, hold, cfg["durations_s"][scene]
        self.process = None
        self.started = None
        self.last_frame = 0.0
        self.finished = False
        self.exit_code = None

    def __enter__(self):
        return self

    def _receive(self, expected, timeout=60):
        if not self.connection.poll(timeout):
            raise RuntimeError("独立显示进程响应超时")
        try:
            message = self.connection.recv()
        except EOFError as exc:
            raise RuntimeError("独立显示进程意外退出") from exc
        if message["kind"] == "closed":
            raise KeyboardInterrupt("viewer closed")
        if message["kind"] == "error":
            raise RuntimeError(message["error"])
        if message["kind"] != expected:
            raise RuntimeError(f"Unexpected viewer message: {message['kind']}")
        return message

    def __call__(self, row):
        if self.process is None:
            context = multiprocessing.get_context("spawn")
            self.connection, child = context.Pipe()
            self.process = context.Process(target=_display_process, args=(child, *self.spec))
            self.process.start()
            child.close()
            self._receive("ready")
        if self.connection.poll():
            self._receive("ready")  # closed/error is propagated immediately
        if not self.process.is_alive():
            raise RuntimeError("独立显示进程意外退出")
        now = time.monotonic()
        if self.started is None:
            self.started = now - row["t_end_s"] / self.speed
        delay = self.started + row["t_end_s"] / self.speed - now
        if delay > 0:
            time.sleep(delay)
        now = time.monotonic()
        if now - self.last_frame >= 1 / 30 or row["t_end_s"] >= self.duration - 1e-12:
            self.connection.send({"kind": "sample", "row": row})
            self.last_frame = now

    def audit(self):
        self.connection.send({"kind": "audit"})
        audit = self._receive("audit")["data"]
        audit.update(speed=self.speed, rendering_process="spawned, isolated display process")
        return audit

    def finish(self):
        self.connection.send({"kind": "finish"})
        self._receive("finished", timeout=self.hold + 30)
        self.finished = True

    def __exit__(self, exc_type, *_):
        if self.process is not None:
            if self.process.is_alive() and not self.finished:
                try:
                    self.connection.send({"kind": "close"})
                except (BrokenPipeError, EOFError, OSError):
                    pass
            self.process.join(timeout=10)
            if self.process.is_alive():
                self.process.terminate()
                self.process.join(timeout=3)
            self.connection.close()
            self.exit_code = self.process.exitcode
            if self.exit_code != 0 and exc_type is None:
                raise RuntimeError(f"Display process failed shutdown: exit code {self.exit_code}")
