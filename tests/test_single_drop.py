import copy
import csv
import json
from argparse import Namespace
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from physics_benchmark.cli import run_suite
from physics_benchmark.metrics import measure
from physics_benchmark.reporting import (
    METRIC_NAMES_EN,
    METRICS,
    drop_report_lines,
    write_chinese_metrics,
)
from physics_benchmark.scenes import load_config
from physics_benchmark.simulation import simulate
from physics_benchmark.viewer import LiveViewer, ProcessViewer, _display_process


@pytest.fixture(scope="module")
def cfg():
    return load_config(Path("configs/baseline.json"))


@pytest.fixture(scope="module")
def drop_rows(cfg):
    return simulate("drop", cfg, 0.001).rows


@pytest.mark.parametrize("dt", [0.002, 0.001])
def test_drop_reference_impact_support_and_full_rigid_settling(cfg, dt):
    rows = simulate("drop", cfg, dt).rows
    m = measure("drop", cfg, rows)
    assert abs(m["first_contact_time_error_s"]) <= dt
    assert m["preimpact_vertical_velocity_m_s"] == pytest.approx(
        -cfg["gravity_m_s2"] * m["first_contact_s"], abs=1e-10
    )
    assert m["ideal_impact_vertical_velocity_m_s"] < -2.5
    assert m["max_free_fall_height_error_m"] == pytest.approx(
        cfg["gravity_m_s2"] * dt * m["first_contact_s"] / 2, abs=1e-11
    )
    assert m["max_free_fall_velocity_error_m_s"] < 1e-10
    assert m["peak_rebound_vertical_velocity_m_s"] > 0
    assert m["settled_within_duration"]
    assert m["rigid_settled_time_s"] >= m["settled_time_s"]
    assert m["rest_observation_duration_s"] == pytest.approx(1 - m["rigid_settled_time_s"])
    assert m["tail_support_weight_ratio"] == pytest.approx(1, abs=1e-5)
    assert m["total_contact_jz_ns"] == pytest.approx(0.981, abs=1e-8)
    assert m["final_com_height_m"] == pytest.approx(0.02, abs=1e-4)
    assert m["final_linear_speed_m_s"] < cfg["stop_speed_m_s"]
    assert m["max_horizontal_displacement_m"] < 1e-8
    assert all(not r["free_fall_sample"] for r in rows if r["t_end_s"] > m["first_contact_s"])
    assert set(m) - {"scene"} <= METRICS.keys()
    assert METRICS.keys() == METRIC_NAMES_EN.keys()


def test_partial_drop_distinguishes_no_contact_and_no_settling(cfg, drop_rows):
    m = measure("drop", cfg, copy.deepcopy(drop_rows[:100]))
    assert m["first_contact_s"] is None
    for key in (
        "preimpact_vertical_velocity_m_s",
        "first_contact_time_error_s",
        "peak_rebound_vertical_velocity_m_s",
        "mean_tail_normal_force_n",
        "tail_support_weight_ratio",
        "rigid_settled_time_s",
        "rest_observation_duration_s",
    ):
        assert m[key] is None
    assert not m["settled_within_duration"]
    m = measure("drop", cfg, copy.deepcopy(drop_rows[:270]))
    assert m["first_contact_s"] is not None
    assert m["rigid_settled_time_s"] is None
    assert m["mean_tail_normal_force_n"] is None


def test_rotating_or_unsupported_body_is_not_rigidly_settled(cfg, drop_rows):
    rotating = copy.deepcopy(drop_rows)
    for row in rotating[-10:]:
        row["qvel3_start"] = row["qvel3_end"] = 1
    m = measure("drop", cfg, rotating)
    assert m["settled_time_s"] is not None
    assert not m["settled_within_duration"]
    assert m["rigid_settled_time_s"] is None
    unsupported = copy.deepcopy(drop_rows)
    unsupported[-1]["contact_fz_n"] = 0
    assert not measure("drop", cfg, unsupported)["settled_within_duration"]


def test_tail_average_includes_contact_free_samples(cfg, drop_rows):
    rows = copy.deepcopy(drop_rows)
    weight = cfg["cube_mass_kg"] * cfg["gravity_m_s2"]
    for i, row in enumerate(rows[-40:]):
        row["contact_fz_n"] = 0 if i % 2 == 0 else 2 * weight
    m = measure("drop", cfg, rows)
    assert m["mean_tail_normal_force_n"] == pytest.approx(weight, abs=1e-12)
    assert m["tail_support_weight_ratio"] == pytest.approx(1, abs=1e-12)


def test_drop_observer_shows_vertical_measurements_and_leaves_physics_unchanged(cfg, drop_rows):
    texts = []
    observer = LiveViewer("drop", cfg, 0.001, speed=1e9, hold=0)
    observer.handle = SimpleNamespace(
        is_running=lambda: True,
        lock=nullcontext,
        sync=lambda **kwargs: None,
        set_texts=lambda text: texts.append(text),
    )
    observed = simulate("drop", cfg, 0.001, on_sample=observer)
    # The fixture may have derived fields; compare before measuring both trajectories.
    baseline = simulate("drop", cfg, 0.001)
    assert observed.rows == baseline.rows
    assert "drop" in texts[-1][2]
    assert "z=" in texts[-1][3] and "vz=" in texts[-1][3] and "Fz=" in texts[-1][3]
    assert " m/s" in texts[-1][3]
    np.testing.assert_array_equal(
        observer.data.qpos, [observed.rows[-1][f"qpos{i}_end"] for i in range(7)]
    )


def test_drop_camera_covers_release_and_ground(cfg, monkeypatch):
    import mujoco.viewer

    camera = SimpleNamespace(lookat=np.zeros(3), distance=0, azimuth=0, elevation=0)
    handle = SimpleNamespace(
        cam=camera, lock=nullcontext, sync=lambda: None, set_texts=lambda *args: None
    )
    monkeypatch.setattr(mujoco.viewer, "launch_passive", lambda *args, **kwargs: handle)
    viewer = LiveViewer("drop", cfg, 0.001)
    viewer._open()
    assert camera.lookat[2] == pytest.approx(cfg["drop_height_m"] / 2)
    assert camera.distance >= 3 * cfg["drop_height_m"]


def test_drop_bilingual_export_preserves_missing_and_unsettled_values(cfg, drop_rows, tmp_path):
    m = measure("drop", cfg, copy.deepcopy(drop_rows[:100]))
    records = [
        {
            "engine": "mujoco-cpu",
            "scene": "drop",
            "dt_s": 0.001,
            "repeat": 0,
            "status": "passed",
            "metrics": m,
        }
    ]
    write_chinese_metrics(tmp_path, records, cfg)
    with (tmp_path / "metrics_bilingual.csv").open(encoding="utf-8-sig") as stream:
        rows = {r["指标字段 / Metric key"]: r for r in csv.DictReader(stream)}
    assert rows["rigid_settled_time_s"]["数值 / Value"] == ""
    assert rows["settled_within_duration"]["数值显示 / Display value"] == "否 / No"
    assert (
        rows["preimpact_vertical_velocity_m_s"]["单位说明 / Unit description"]
        == "米每秒 / metre per second"
    )
    report = "\n".join(drop_report_lines(records, cfg))
    assert "Rigid-body settling time" in report
    assert "未测得 / Not measured" in report and "否 / No" in report


def test_drop_cli_saves_raw_reference_and_bilingual_report(tmp_path):
    output = tmp_path / "drop"
    args = Namespace(
        config=Path("configs/baseline.json"), repeats=1, output=output, scene="drop", no_plots=True
    )
    assert run_suite(args) == 0
    runs = json.loads((output / "runs.json").read_text())
    assert len(runs) == 2 and all(r["metrics"]["settled_within_duration"] for r in runs)
    assert "Cube drop, impact and settling" in (output / "report.md").read_text()
    for run in runs:
        with (output / run["directory"] / "raw.csv").open() as stream:
            rows = list(csv.DictReader(stream))
        assert len(rows) == run["metrics"]["steps"]
        assert "free_fall_sample" in rows[0]


def test_display_backlog_coalesces_samples_and_preserves_audit_and_finish(monkeypatch):
    samples, sent, finished, closed = [], [], [], []
    messages = [{"kind": "sample", "row": {"t_end_s": i / 10}} for i in range(1, 4)] + [
        {"kind": "audit"},
        {"kind": "finish"},
    ]

    class Viewer:
        handle = SimpleNamespace(is_running=lambda: True)

        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            closed.append(True)

        def _open(self):
            pass

        def __call__(self, row):
            samples.append(row)

        def audit(self):
            return {"final_sample": samples[-1]}

        def finish(self):
            finished.append(True)

    monkeypatch.setattr("physics_benchmark.viewer.LiveViewer", Viewer)

    def send(message):
        if message["kind"] == "finished":
            assert closed == [True]
        sent.append(message)

    connection = SimpleNamespace(
        poll=lambda *args: bool(messages),
        recv=lambda: messages.pop(0),
        send=send,
        close=lambda: None,
    )
    _display_process(connection, "drop", {}, 0.001, "physx", 0)
    assert samples == [{"t_end_s": 0.3}]
    assert [r["kind"] for r in sent] == ["ready", "audit", "finished"]
    assert sent[1]["data"]["final_sample"] == samples[-1]
    assert sent[1]["data"]["coalesced_display_samples"] == 2
    assert finished == [True]


def test_display_process_failed_exit_is_not_counted_as_success(cfg):
    observer = ProcessViewer("drop", cfg, 0.001)
    observer.process = SimpleNamespace(
        is_alive=lambda: False,
        join=lambda **kwargs: None,
        exitcode=1,
    )
    observer.connection = SimpleNamespace(close=lambda: None)
    with pytest.raises(RuntimeError, match="exit code 1"):
        observer.__exit__(None, None, None)
    assert observer.exit_code == 1


def test_live_viewer_waits_for_its_render_thread_before_returning(cfg):
    order = []
    viewer = LiveViewer("drop", cfg, 0.001)
    viewer.handle = SimpleNamespace(close=lambda: order.append("close"))
    viewer.render_threads = [
        SimpleNamespace(
            join=lambda **kwargs: order.append("join"),
            is_alive=lambda: False,
        )
    ]
    viewer.__exit__(None, None, None)
    assert order == ["close", "join"]
