"""Audit this batch's physics samples, GUI equivalence and historical preservation."""
import csv
import hashlib
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parent
repo = root.parents[1]
manifest = json.loads((root / "manifest.json").read_text())
config = json.loads((repo / "configs/baseline.json").read_text())
engines = ("physx", "mujoco-warp", "mujoco-cpu", "genesis")
groups = {
    "position_m": [f"qpos{i}_{edge}" for i in range(3) for edge in ("start", "end")],
    "quaternion": [f"qpos{i}_{edge}" for i in range(3, 7) for edge in ("start", "end")],
    "velocity_m_s": [f"qvel{i}_{edge}" for i in range(3) for edge in ("start", "end")],
    "angular_velocity_rad_s": [f"qvel{i}_{edge}" for i in range(3, 6) for edge in ("start", "end")],
    "force_n": [f"contact_f{axis}_n" for axis in "xyz"],
    "impulse_ns": [f"contact_j{axis}_ns" for axis in "xyz"],
}
limits = manifest["gui_absolute_limits"]


def read_rows(directory):
    with (directory / "raw.csv").open() as f:
        rows = [{k: float(v) for k, v in row.items()} for row in csv.DictReader(f)]
    assert rows and all(math.isfinite(v) for row in rows for v in row.values())
    return rows


headless_steps = gui_steps = 0
gui_checks, overview = [], []
for engine in engines:
    headless = root / manifest["accepted_result_paths"][engine]
    viewer = root / manifest.get("accepted_viewer_paths", {}).get(engine, "viewer-" + engine)
    assert json.loads((headless / "config.json").read_text()) == config
    assert json.loads((viewer / "config.json").read_text()) == config
    viewer_source = manifest["viewer_source_sha256_by_engine"][engine]
    for base, expected in ((headless, manifest["headless_source_sha256"]),
                           (viewer, viewer_source)):
        environment = json.loads((base / "environment.json").read_text())
        assert all(environment["source_sha256"][p] == digest
                   for p, digest in expected.items() if p.endswith(".py"))
    runs = json.loads((headless / "runs.json").read_text())
    gui_runs = json.loads((viewer / "runs.json").read_text())
    expected = {(dt, repeat) for dt in config["timesteps_s"]["drop"] for repeat in range(3)}
    assert len(runs) == 6 and {(r["dt_s"], r["repeat"]) for r in runs} == expected
    assert len(gui_runs) == 2
    assert {(r["dt_s"], r["repeat"]) for r in gui_runs} == {(dt, 0) for dt in config["timesteps_s"]["drop"]}
    for base, records in ((headless, runs), (viewer, gui_runs)):
        for run in records:
            assert run["scene"] == "drop" and run["status"] == "passed"
            directory = base / run["directory"]
            assert json.loads((directory / "imported.json").read_text())["validation"] == "passed"
            rows = read_rows(directory)
            dt = run["dt_s"]
            assert len(rows) == round(config["durations_s"]["drop"] / dt)
            assert abs(rows[-1]["t_end_s"] - config["durations_s"]["drop"]) < 1e-12
            assert all(abs(row["t_end_s"] - (i + 1) * dt) < 1e-12 for i, row in enumerate(rows))
            assert max(row["momentum_residual_ns"] for row in rows) <= config["momentum_tolerance_ns"]
            m = run["metrics"]
            assert m["settled_within_duration"] and m["rigid_settled_time_s"] is not None
            assert m["rest_observation_duration_s"] > 0
            assert m["final_linear_speed_m_s"] < config["stop_speed_m_s"]
            assert m["final_angular_speed_rad_s"] < m["settling_angular_speed_threshold_rad_s"]
            assert m["first_contact_s"] < m["rigid_settled_time_s"]
            assert m["impulse_window_complete"] and m["mean_tail_normal_force_n"] > 0
            assert all(v is None or not isinstance(v, (int, float)) or math.isfinite(v) for v in m.values())
            if base == headless:
                headless_steps += len(rows)
            else:
                gui_steps += len(rows)
    for run in runs:
        if run["repeat"] != 0:
            continue
        gui_run = next(r for r in gui_runs if r["dt_s"] == run["dt_s"])
        rows = read_rows(headless / run["directory"])
        gui_dir = viewer / gui_run["directory"]
        gui_rows = read_rows(gui_dir)
        assert len(rows) == len(gui_rows) and rows[0].keys() == gui_rows[0].keys()
        differences = {
            group: max(abs(a[k] - b[k]) for a, b in zip(rows, gui_rows) for k in keys)
            for group, keys in groups.items()
        }
        display = json.loads((gui_dir / "viewer.json").read_text())
        assert display["display_process_exit_code"] == 0
        pose_error = max(abs(display["final_display_qpos"][i] - gui_rows[-1][f"qpos{i}_end"]) for i in range(7))
        settle_error = abs(run["metrics"]["rigid_settled_time_s"] - gui_run["metrics"]["rigid_settled_time_s"])
        passed = all(differences[k] <= limits[k] for k in groups)
        passed &= display["frames"] > 0 and pose_error < 1e-12 and settle_error <= run["dt_s"]
        check = dict(engine=engine, dt_s=run["dt_s"], steps=len(rows), frames=display["frames"],
                     all_numeric_columns_identical=all(a == b for a, b in zip(rows, gui_rows)),
                     max_difference=differences, final_display_pose_error=pose_error,
                     settling_time_difference_s=settle_error, passed=passed)
        gui_checks.append(check)
    overview.append(dict(engine=engine, headless_passed=6, gui_passed=2, settled_runs=8))

historical_changes = [p for p, expected in manifest["historical_result_sha256"].items()
                      if hashlib.sha256((repo / p).read_bytes()).hexdigest() != expected]
source_changes = [p for p, expected in manifest["source_sha256"].items()
                  if hashlib.sha256((repo / p).read_bytes()).hexdigest() != expected]
regression_base = root / manifest.get("regression_result_path", "regression-cpu")
regression = json.loads((regression_base / "runs.json").read_text())
assert len(regression) == 18 and all(r["status"] == "passed" for r in regression)
slide_regression = []
for run in regression:
    if run["scene"] != "slide" or run["repeat"] != 0:
        continue
    new = read_rows(regression_base / run["directory"])
    old = read_rows(repo / "results/task04-slide-rerun-20261010-1818/mujoco-cpu" / run["directory"])
    identical = new == old
    slide_regression.append(dict(dt_s=run["dt_s"], all_numeric_columns_identical=identical))
    assert identical
with (root / "comparison/summary.csv").open() as f:
    comparison = list(csv.DictReader(f))
assert len(comparison) == 24 and all(r["status"] == "passed" for r in comparison)
assert headless_steps == 18000 and gui_steps == 6000
result = dict(
    passed=all(r["passed"] for r in gui_checks) and not historical_changes and not source_changes,
    headless_runs=24, gui_runs=8, headless_steps=headless_steps, gui_steps=gui_steps,
    overview=overview, gui_absolute_limits=limits, viewer_equivalence=gui_checks,
    preserved_historical_files=len(manifest["historical_result_sha256"]),
    historical_changes=historical_changes, source_changes=source_changes,
    cpu_regression_passed=18, slide_regression=slide_regression,
)
(root / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False))
assert result["passed"], "Inspect audit.json for failed GUI equivalence or modified historical files"
