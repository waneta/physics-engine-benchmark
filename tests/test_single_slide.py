import copy
import csv
import json
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from physics_benchmark.metrics import coulomb_reference, measure
from physics_benchmark.reporting import write_chinese_metrics
from physics_benchmark.scenes import load_config
from physics_benchmark.simulation import simulate
from physics_benchmark.viewer import LiveViewer, ProcessViewer, validate_viewer_options


@pytest.fixture
def cfg():
    return load_config(Path("configs/baseline.json"))


def test_coulomb_reference_stops_and_handles_zero_friction(cfg):
    stop = cfg["slide_speed_m_s"] / (cfg["sliding_friction"] * cfg["gravity_m_s2"])
    x, v = coulomb_reference(cfg, np.array([0, stop / 2, stop, 2 * stop]))
    distance = cfg["slide_speed_m_s"] * stop / 2
    np.testing.assert_allclose(x, [0, 0.75 * distance, distance, distance])
    np.testing.assert_allclose(v, [1, 0.5, 0, 0])
    cfg["sliding_friction"] = 0
    x, v = coulomb_reference(cfg, np.array([0, 1, 2]))
    np.testing.assert_allclose(x, [0, 1, 2])
    np.testing.assert_allclose(v, 1)


def test_measured_friction_uses_normal_force_and_excludes_startup(cfg):
    run = simulate("slide", cfg, 0.001)
    metrics = measure("slide", cfg, run.rows)
    assert metrics["friction_opposes_motion"]
    assert metrics["effective_friction_coefficient"] == pytest.approx(0.4, abs=0.002)
    assert metrics["mean_normal_force_n"] == pytest.approx(0.1 * 9.81, rel=0.05)
    assert metrics["mean_friction_force_n"] == pytest.approx(
        metrics["effective_friction_coefficient"] * metrics["mean_normal_force_n"], abs=1e-9
    )
    assert metrics["mean_deceleration_m_s2"] == pytest.approx(
        metrics["mean_friction_force_n"] / cfg["cube_mass_kg"], abs=1e-7
    )
    assert metrics["friction_contact_samples"] < metrics["friction_measurement_samples"]
    assert metrics["total_contact_jx_ns"] == pytest.approx(-0.1, abs=1e-5)
    assert metrics["max_displacement_error_m"] < 0.004
    assert metrics["max_lateral_displacement_m"] < 1e-8
    assert all(not r["friction_metric_sample"] for r in run.rows if r["t_start_s"] < 0.04)
    # The friction estimate must not include even an extreme instrumentation error at startup.
    changed = copy.deepcopy(run.rows)
    changed[0]["contact_fx_n"] = -1e5
    assert measure("slide", cfg, changed)["effective_friction_coefficient"] == pytest.approx(
        metrics["effective_friction_coefficient"]
    )


def test_no_stable_sliding_window_reports_null(cfg):
    run = simulate("slide", cfg, 0.001)
    m = measure("slide", cfg, run.rows[:20])
    assert m["friction_measurement_samples"] == 0
    for key in (
        "effective_friction_coefficient",
        "mean_friction_force_n",
        "friction_opposes_motion",
    ):
        assert m[key] is None
    assert m["stop_time_s"] is None


def test_display_model_is_independent_and_observer_leaves_physics_unchanged(cfg):
    viewer = LiveViewer("slide", cfg, 0.001, speed=1e9, hold=0)
    viewer.handle = SimpleNamespace(
        is_running=lambda: True, lock=nullcontext, sync=lambda **kwargs: None
    )
    baseline = simulate("slide", cfg, 0.001)
    observed = simulate("slide", cfg, 0.001, on_sample=viewer)
    assert observed.rows == baseline.rows
    np.testing.assert_allclose(
        viewer.data.qpos, [baseline.rows[-1][f"qpos{i}_end"] for i in range(7)]
    )
    assert viewer.frames > 0
    assert measure("slide", cfg, observed.rows) == measure("slide", cfg, baseline.rows)


def test_closing_viewer_preserves_last_measured_sample(cfg):
    viewer = LiveViewer("slide", cfg, 0.001)
    viewer.handle = SimpleNamespace(is_running=lambda: False)
    rows = []
    with pytest.raises(KeyboardInterrupt):
        simulate("slide", cfg, 0.001, rows, on_sample=viewer)
    assert len(rows) == 1
    assert rows[0]["t_end_s"] == 0.001


@pytest.mark.parametrize("kind,exception", [("closed", KeyboardInterrupt), ("error", RuntimeError)])
def test_display_process_failure_preserves_physical_samples(cfg, kind, exception):
    observer = ProcessViewer("slide", cfg, 0.001)
    observer.process = SimpleNamespace(is_alive=lambda: True)
    observer.connection = SimpleNamespace(
        poll=lambda *args: True, recv=lambda: {"kind": kind, "error": "renderer failed"}
    )
    rows = []
    with pytest.raises(exception):
        simulate("slide", cfg, 0.001, rows, on_sample=observer)
    assert len(rows) == 1
    assert rows[0]["t_end_s"] == 0.001
    assert np.isfinite(rows[0]["qpos0_end"])


@pytest.mark.parametrize("speed,hold", [(0, 0), (float("nan"), 0), (1, -1), (1, float("inf"))])
def test_viewer_rejects_invalid_timing(speed, hold):
    with pytest.raises(ValueError):
        validate_viewer_options(speed, hold)


def test_chinese_stats_exclude_failed_measurements_and_keep_status(cfg, tmp_path):
    metrics = measure("slide", cfg, simulate("slide", cfg, 0.001).rows)
    base = {"engine": "mujoco-cpu", "scene": "slide", "dt_s": 0.001}
    records = [
        {**base, "repeat": 0, "status": "passed", "metrics": metrics},
        {**base, "repeat": 1, "status": "failed", "metrics": {"stop_distance_m": 999}},
        {**base, "repeat": 2, "status": "interrupted", "error": "cancelled"},
    ]
    write_chinese_metrics(tmp_path, records, cfg)
    with (tmp_path / "metric_stats_zh.csv").open(encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    distance = next(r for r in rows if r["指标字段"] == "stop_distance_m")
    assert float(distance["平均值"]) == metrics["stop_distance_m"]
    assert distance["通过次数"] == "1"
    assert distance["记录次数"] == "3"
    assert distance["标准差"] == "0.0"
    with (tmp_path / "metrics_zh.csv").open(encoding="utf-8-sig") as stream:
        assert {r["状态"] for r in csv.DictReader(stream)} == {
            "通过 / Passed",
            "失败 / Failed",
            "中断 / Interrupted",
        }
    definitions = json.loads((tmp_path / "metric_definitions.json").read_text())
    assert definitions["stop_distance_m"] == {
        "名称": "停止距离",
        "name_en": "Stopping distance",
        "单位": "m",
        "unit_name_zh": "米",
        "unit_name_en": "metre",
    }
    with (tmp_path / "metrics_bilingual.csv").open(encoding="utf-8-sig") as stream:
        bilingual = list(csv.DictReader(stream))
    passed_distance = next(
        r
        for r in bilingual
        if r["指标字段 / Metric key"] == "stop_distance_m" and r["状态 / Status"] == "通过 / Passed"
    )
    assert passed_distance["指标名称（英文） / Metric name (English)"] == "Stopping distance"
    assert passed_distance["单位说明 / Unit description"] == "米 / metre"
    assert float(passed_distance["数值 / Value"]) == metrics["stop_distance_m"]
    direction = next(
        r for r in bilingual if r["指标字段 / Metric key"] == "friction_opposes_motion"
    )
    assert direction["数值显示 / Display value"] == "是 / Yes"
    with (tmp_path / "metric_stats_bilingual.csv").open(encoding="utf-8-sig") as stream:
        stats = next(
            r for r in csv.DictReader(stream) if r["指标字段 / Metric key"] == "stop_distance_m"
        )
    assert float(stats["平均值 / Mean"]) == metrics["stop_distance_m"]
    assert stats["有效数值次数 / Valid values"] == "1"
    assert "Stopping distance" in (tmp_path / "metrics_bilingual.md").read_text()
