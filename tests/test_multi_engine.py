import io
import json
import queue
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from physics_benchmark.comparison import load_results
from physics_benchmark.sampling import make_row
from physics_benchmark.scenes import load_config


def test_environment_records_active_overlay_version(monkeypatch):
    from physics_benchmark import cli

    monkeypatch.setattr(
        cli.importlib.metadata,
        "distributions",
        lambda: [
            SimpleNamespace(metadata={"Name": "torch"}, version="2.8.0"),
            SimpleNamespace(metadata={"Name": "torch"}, version="2.7.0"),
        ],
    )
    monkeypatch.setattr(cli.importlib.metadata, "version", lambda name: "2.8.0")
    monkeypatch.setattr(cli, "command_output", lambda args: {})
    assert cli.environment("genesis")["packages"]["torch"] == "2.8.0"


def test_native_impulse_requires_friction_for_momentum_balance():
    cfg = load_config(Path("configs/baseline.json"))
    dt, mass = 0.002, cfg["cube_mass_kg"]
    normal = np.array([0, 0, mass * cfg["gravity_m_s2"] * dt])
    friction = np.array([-cfg["sliding_friction"] * normal[2], 0, 0])
    before = np.array([1, 0, 0, 0, 0, 0], dtype=float)
    after = before.copy()
    after[:3] += friction / mass
    q = [0, 0, 0.02, 1, 0, 0, 0]
    incomplete = make_row(
        "slide", cfg, dt, 0, q, before, q, after, normal / dt, 4, 0, native_impulse=normal
    )
    total = normal + friction
    complete = make_row(
        "slide", cfg, dt, 0, q, before, q, after, total / dt, 4, 0, native_impulse=total
    )
    assert incomplete["momentum_residual_ns"] > cfg["momentum_tolerance_ns"]
    assert complete["momentum_residual_ns"] < 1e-16
    assert complete["contact_jx_ns"] < 0
    assert complete["net_fz_n"] == pytest.approx(0)


def dataset(path, engine, cfg):
    path.mkdir()
    (path / "config.json").write_text(json.dumps(cfg))
    (path / "environment.json").write_text(json.dumps({"engine": engine}))
    (path / "runs.json").write_text(
        json.dumps(
            [
                {
                    "scene": "drop",
                    "repeat": 0,
                    "dt_s": 0.001,
                    "status": "failed",
                    "error": "native error",
                }
            ]
        )
    )
    return path


def test_comparison_rejects_mismatched_physics(tmp_path):
    first = dataset(tmp_path / "a", "mujoco-cpu", {"mass": 0.1})
    second = dataset(tmp_path / "b", "physx", {"mass": 1})
    with pytest.raises(ValueError, match="Configuration mismatch"):
        load_results([first, second])


def test_comparison_keeps_failed_runs(tmp_path):
    paths = [
        dataset(tmp_path / engine, engine, {"mass": 0.1}) for engine in ("mujoco-cpu", "physx")
    ]
    loaded = load_results(paths)
    assert all(data["records"][0]["status"] == "failed" for data in loaded)
    with pytest.raises(ValueError, match="Duplicate engine"):
        load_results([paths[0], paths[0]])


def test_nonfinite_native_sample_rejected():
    cfg = load_config(Path("configs/baseline.json"))
    with pytest.raises(RuntimeError, match="Nonfinite"):
        make_row("hinge", cfg, 0.001, 0, [0], [0], [np.nan], [0], [0] * 3, 0, 0)


def protocol_worker():
    from physics_benchmark.backends.physx import Worker

    worker = object.__new__(Worker)
    worker.closed = False
    worker.process = SimpleNamespace(stdin=io.StringIO(), poll=lambda: None)
    worker.log = SimpleNamespace(name="native.log")
    worker.messages = queue.Queue()
    worker.close = lambda: setattr(worker, "closed", True)
    return worker


def test_worker_invalidates_connection_on_native_error():
    worker = protocol_worker()
    worker.messages.put({"kind": "error", "error": "native initialization failed"})
    with pytest.raises(RuntimeError, match="native initialization failed"):
        worker.receive()
    assert worker.closed
    with pytest.raises(RuntimeError, match="connection is closed"):
        worker.send({"kind": "build"})


def test_worker_does_not_reuse_closed_stdin():
    worker = protocol_worker()
    worker.process.stdin.close()
    with pytest.raises(RuntimeError, match="connection is closed"):
        worker.send({"kind": "build"})
    assert worker.closed


def test_physx_restarts_after_failed_build(monkeypatch):
    from physics_benchmark.extended import physx

    created = []

    def factory(script):
        worker = protocol_worker()
        worker.image = "test-image"
        worker.image_id = "test-digest"
        worker.messages.put(
            {"kind": "error", "error": "build failed"}
            if not created
            else {"kind": "built", "audit": {}, "state": {}}
        )
        created.append(worker)
        return worker

    monkeypatch.setattr(physx, "_worker", None)
    monkeypatch.setattr(physx, "Worker", factory)
    monkeypatch.setattr(physx, "specification", lambda scene: {})
    scene = SimpleNamespace(model=None)
    with pytest.raises(RuntimeError, match="build failed"):
        physx.PhysX(scene)
    recovered = physx.PhysX(scene)
    assert len(created) == 2 and created[0].closed
    assert recovered.worker is created[1]
