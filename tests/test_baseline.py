import copy
import json
from argparse import Namespace
from pathlib import Path

import mujoco
import numpy as np
import pytest

from physics_benchmark.cli import run_suite
from physics_benchmark.metrics import column, hinge_reference, measure, sustained_time
from physics_benchmark.scenes import build_model, load_config
from physics_benchmark.simulation import contact_force_world, cube_penetration, simulate


@pytest.fixture(scope="module")
def cfg():
    return load_config(Path("configs/baseline.json"))


@pytest.mark.parametrize("scene", ["slide", "drop", "hinge"])
def test_imported_physical_parameters(cfg, scene):
    model, data, imported, _ = build_model(scene, cfg, 0.001)
    assert imported["validation"] == "passed"
    assert not model.dof_armature.any()
    if scene == "hinge":
        # Initial acceleration must use the finite-width rod inertia about its pivot.
        inertia = cfg["hinge_mass_kg"] * (
            cfg["hinge_length_m"] ** 2 / 3 + cfg["hinge_width_m"] ** 2 / 12
        )
        expected = (
            -cfg["hinge_mass_kg"]
            * cfg["gravity_m_s2"]
            * cfg["hinge_length_m"]
            / 2
            * np.sin(0.5)
            / inertia
        )
        assert data.qacc[0] == pytest.approx(expected, abs=1e-10)


def test_drop_free_fall_and_contact_momentum(cfg):
    run = simulate("drop", cfg, 0.001)
    m = measure("drop", cfg, run.rows)
    before_contact = [r for r in run.rows if r["t_end_s"] < 0.2]
    for row in before_contact:
        t, dt = row["t_end_s"], 0.001
        assert row["qvel2_end"] == pytest.approx(-cfg["gravity_m_s2"] * t, abs=1e-11)
        # Semi-implicit Euler's discrete free-fall trajectory.
        assert row["qpos2_end"] == pytest.approx(
            cfg["drop_height_m"] - cfg["gravity_m_s2"] * t * (t + dt) / 2, abs=1e-11
        )
        assert row["contact_force_norm_n"] == 0
    assert m["first_contact_s"] == pytest.approx(m["ideal_first_contact_s"], abs=0.002)
    assert m["max_momentum_residual_ns"] < cfg["momentum_tolerance_ns"]
    assert m["max_constraint_force_error_n"] < 1e-8
    assert run.rows[-1]["contact_fz_n"] == pytest.approx(0.981, abs=1e-5)
    assert m["settled_time_s"] is not None
    assert m["impulse_window_complete"]
    assert m["window_contact_jz_ns"] > 0.25


def test_force_action_reaction(cfg):
    model, data, _, _ = build_model("drop", cfg, 0.001)
    for _ in range(1000):
        mujoco.mj_step(model, data)
    force = contact_force_world(model, data, model.body("object").id)
    floor = contact_force_world(model, data, 0)
    np.testing.assert_allclose(force + floor, 0, atol=1e-12)
    assert force[2] == pytest.approx(0.981, abs=1e-5)


def test_rotated_cube_penetration():
    qpos = np.array([0, 0, 0.02, np.cos(np.pi / 8), 0, np.sin(np.pi / 8), 0])
    assert cube_penetration(qpos, 0.04) == pytest.approx(0.02 * (np.sqrt(2) - 1))


def test_slide_stops_and_force_opposes_motion(cfg):
    run = simulate("slide", cfg, 0.001)
    metrics = measure("slide", cfg, run.rows)
    assert metrics["stop_time_s"] is not None
    assert metrics["stop_distance_m"] == pytest.approx(
        metrics["ideal_coulomb_distance_m"], abs=0.004
    )
    assert metrics["max_momentum_residual_ns"] < cfg["momentum_tolerance_ns"]
    moving = [r for r in run.rows if r["qvel0_start"] > 0.1]
    assert sum(r["contact_jx_ns"] for r in moving) < 0


def test_hinge_ode_and_timestep_refinement(cfg):
    errors = []
    for dt in (0.001, 0.0005):
        run = simulate("hinge", cfg, dt)
        m = measure("hinge", cfg, run.rows)
        assert m["torque_impulse_nms"] == pytest.approx(0.02, abs=1e-14)
        assert max(column(run.rows, "contacts")) == 0
        errors.append(m["max_angle_error_rad"])
    assert errors[0] < np.deg2rad(0.15)
    assert errors[1] < 0.6 * errors[0]
    times = np.linspace(0, 1, 101)
    np.testing.assert_allclose(
        hinge_reference(cfg, times), hinge_reference(cfg, times, max_step=0.000025), atol=1e-10
    )


def test_independent_repeats(cfg):
    a, b = simulate("slide", cfg, 0.002), simulate("slide", cfg, 0.002)
    assert a.rows == b.rows


def test_settled_means_stays_below_threshold():
    times = np.arange(5) * 0.1
    assert sustained_time(times, np.array([True, False, True, False, True])) == 0.4
    assert sustained_time(times, np.zeros(5, dtype=bool)) is None


def test_invalid_configuration_rejects_misaligned_pulse(cfg, tmp_path):
    broken = copy.deepcopy(cfg)
    broken["pulse_start_s"] = 0.1001
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(broken))
    with pytest.raises(ValueError, match="align"):
        load_config(path)


def test_partial_impulse_window_is_not_reported_as_complete(cfg):
    run = simulate("drop", cfg, 0.001)
    m = measure("drop", cfg, run.rows[:270])
    assert m["first_contact_s"] is not None
    assert not m["impulse_window_complete"]
    assert m["window_contact_jz_ns"] is None


def test_cli_exports_and_refuses_overwrite(tmp_path):
    output = tmp_path / "run"
    args = Namespace(
        config=Path("configs/baseline.json"), repeats=1, output=output, scene="slide", no_plots=True
    )
    assert run_suite(args) == 0
    assert len(json.loads((output / "runs.json").read_text())) == 2
    assert (output / "report.md").exists()
    assert len(list(output.rglob("raw.csv"))) == 2
    assert len(list(output.rglob("imported.json"))) == 2
    with pytest.raises(FileExistsError):
        run_suite(args)


def test_failed_run_retains_partial_samples(tmp_path, monkeypatch):
    def failing_simulation(scene, cfg, dt, rows):
        rows.append({"step": 0, "t_start_s": 0.0, "t_end_s": dt})
        raise RuntimeError("deliberate instrumentation failure")

    monkeypatch.setattr("physics_benchmark.cli.simulate", failing_simulation)
    output = tmp_path / "failed"
    args = Namespace(
        config=Path("configs/baseline.json"), repeats=1, output=output, scene="slide", no_plots=True
    )
    assert run_suite(args) == 1
    records = json.loads((output / "runs.json").read_text())
    assert all(r["status"] == "failed" for r in records)
    assert len(list(output.rglob("raw.csv"))) == 2
    assert len(list(output.rglob("failure.json"))) == 2
    assert "deliberate instrumentation failure" in (output / "report.md").read_text()


@pytest.mark.parametrize("interrupt_call", [1, 2])
def test_ctrl_c_retains_partial_report_and_stops_runs(
    tmp_path, monkeypatch, capsys, interrupt_call
):
    calls = 0

    def interrupted_simulation(scene, cfg, dt, rows):
        nonlocal calls
        calls += 1
        if calls == interrupt_call:
            rows.append({"step": 0, "t_start_s": 0.0, "t_end_s": dt})
            raise KeyboardInterrupt
        return simulate(scene, cfg, dt, rows)

    monkeypatch.setattr("physics_benchmark.cli.simulate", interrupted_simulation)
    output = tmp_path / "interrupted"
    args = Namespace(
        config=Path("configs/baseline.json"),
        repeats=3,
        output=output,
        scene="all",
        no_plots=False,
    )
    assert run_suite(args) == 130
    assert calls == interrupt_call
    records = json.loads((output / "runs.json").read_text())
    assert [r["status"] for r in records] == ["passed"] * (interrupt_call - 1) + ["interrupted"]
    partial = output / records[-1]["directory"]
    assert (partial / "raw.csv").read_text().splitlines() == [
        "step,t_start_s,t_end_s",
        "0,0.0,0.002",
    ]
    assert json.loads((partial / "interruption.json").read_text())["samples"] == 1
    assert not (partial / "failure.json").exists()
    assert not list(output.glob("*.png"))
    report = (output / "report.md").read_text()
    assert f"运行通过：{interrupt_call - 1}/18" in report
    assert "本次运行已中断，报告不完整" in report
    if interrupt_call > 1:
        assert (output / "summary.csv").exists()
    captured = capsys.readouterr()
    assert str(output.resolve()) in captured.out
    assert "Interrupted (Ctrl+C)" in captured.err
    assert "Traceback" not in captured.err


def test_ctrl_c_during_startup_has_no_traceback(monkeypatch, capsys):
    from physics_benchmark.cli import main

    def interrupted_environment():
        raise KeyboardInterrupt

    monkeypatch.setattr("physics_benchmark.cli.environment", interrupted_environment)
    monkeypatch.setattr("sys.argv", ["physics-bench", "doctor"])
    assert main() == 130
    assert "Traceback" not in capsys.readouterr().err
