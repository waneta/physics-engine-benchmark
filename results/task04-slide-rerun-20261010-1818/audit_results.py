"""Validate this batch, its GUI samples and preservation of historical results."""
import csv
import hashlib
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parent
repo = root.parents[1]
manifest = json.loads((root / "rerun_manifest.json").read_text())
engines = ("physx", "mujoco-warp", "mujoco-cpu", "genesis")
config = json.loads((repo / "configs/baseline.json").read_text())
groups = {
    "position_m": [f"qpos{i}_{edge}" for i in range(3) for edge in ("start", "end")],
    "quaternion": [f"qpos{i}_{edge}" for i in range(3, 7) for edge in ("start", "end")],
    "velocity_m_s": [f"qvel{i}_{edge}" for i in range(3) for edge in ("start", "end")],
    "angular_velocity_rad_s": [f"qvel{i}_{edge}" for i in range(3, 6) for edge in ("start", "end")],
    "force_n": ["contact_fx_n", "contact_fy_n", "contact_fz_n"],
    "impulse_ns": ["contact_jx_ns", "contact_jy_ns", "contact_jz_ns"],
}
limits = manifest["comparison_absolute_limits"]


def read_rows(directory):
    with (directory / "raw.csv").open() as stream:
        rows = [{key: float(value) for key, value in row.items()} for row in csv.DictReader(stream)]
    assert rows and all(math.isfinite(v) for row in rows for v in row.values())
    return rows


def compare_rows(first, second):
    assert len(first) == len(second)
    assert first[0].keys() == second[0].keys()
    differences = {
        group: max(abs(a[key] - b[key]) for a, b in zip(first, second) for key in keys)
        for group, keys in groups.items()
    }
    identical = all(a == b for a, b in zip(first, second))
    passed = all(differences[group] <= limits[group] for group in groups)
    return dict(max_difference=differences, all_numeric_columns_identical=identical, within_limits=passed)


headless_steps = gui_steps = 0
gui_checks, historical_checks, overview = [], [], []
for engine in engines:
    headless = root / manifest["accepted_result_paths"][engine]
    viewer = root / ("viewer-" + engine)
    assert json.loads((headless / "config.json").read_text()) == config
    assert json.loads((viewer / "config.json").read_text()) == config
    runs = json.loads((headless / "runs.json").read_text())
    gui_runs = json.loads((viewer / "runs.json").read_text())
    expected = {(dt, repeat) for dt in config["timesteps_s"]["slide"] for repeat in range(3)}
    assert {(r["dt_s"], r["repeat"]) for r in runs} == expected
    assert len(runs) == 6 and all(r["status"] == "passed" and r["scene"] == "slide" for r in runs)
    assert len(gui_runs) == 2 and all(r["status"] == "passed" and r["scene"] == "slide" for r in gui_runs)
    assert {(r["dt_s"], r["repeat"]) for r in gui_runs} == {(dt, 0) for dt in config["timesteps_s"]["slide"]}
    for run in runs:
        rows = read_rows(headless / run["directory"])
        dt = run["dt_s"]
        assert len(rows) == round(config["durations_s"]["slide"] / dt)
        assert abs(rows[-1]["t_end_s"] - config["durations_s"]["slide"]) < 1e-12
        assert max(row["momentum_residual_ns"] for row in rows) <= config["momentum_tolerance_ns"]
        assert run["metrics"]["friction_opposes_motion"]
        headless_steps += len(rows)
        if run["repeat"]:
            continue
        old_dir = repo / "results/task04-slide-20261010/final" / engine / run["directory"]
        historical = compare_rows(rows, read_rows(old_dir))
        historical_checks.append(dict(engine=engine, dt_s=dt, **historical))
        gui_run = next(r for r in gui_runs if r["dt_s"] == dt)
        gui_dir = viewer / gui_run["directory"]
        gui_rows = read_rows(gui_dir)
        gui_steps += len(gui_rows)
        check = compare_rows(rows, gui_rows)
        audit = json.loads((gui_dir / "viewer.json").read_text())
        pose_error = max(abs(audit["final_display_qpos"][i] - gui_rows[-1][f"qpos{i}_end"]) for i in range(7))
        assert audit["frames"] > 0 and pose_error < 1e-12
        stop_time_difference = abs(run["metrics"]["stop_time_s"] - gui_run["metrics"]["stop_time_s"])
        check.update(engine=engine, dt_s=dt, steps=len(rows), frames=audit["frames"],
                     final_display_pose_error=pose_error, stop_time_difference_s=stop_time_difference)
        check["passed"] = check["within_limits"] and stop_time_difference <= dt
        gui_checks.append(check)
        assert check["passed"], check
    overview.append(dict(engine=engine, passed=6, gui_passed=2))

for path, expected_hash in manifest["historical_result_sha256"].items():
    assert hashlib.sha256((repo / path).read_bytes()).hexdigest() == expected_hash, path
for path, expected_hash in manifest["source_sha256"].items():
    assert hashlib.sha256((repo / path).read_bytes()).hexdigest() == expected_hash, path
assert headless_steps == 10800 and gui_steps == 3600
result = dict(
    passed=True, headless_runs=24, gui_runs=8, headless_steps=headless_steps, gui_steps=gui_steps,
    overview=overview, comparison_absolute_limits=limits, viewer_equivalence=gui_checks,
    previous_to_current_sample_comparison=historical_checks,
    preserved_historical_files=len(manifest["historical_result_sha256"]),
    source_files_unchanged=True,
)
(root / "audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k not in ("viewer_equivalence", "previous_to_current_sample_comparison")}, ensure_ascii=False))
