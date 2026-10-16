"""Evidence reuse must retain failed physics and reject incompatible native runs."""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "run_recovery", Path(__file__).resolve().parents[1] / "scripts/run_recovery.py"
)
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)

ASSET = "configs/assets/panda/source.xml"
CONTROLLER = "src/physics_benchmark/extended/rigid.py"
HASHES = {ASSET: "asset", CONTROLLER: "fixed"}
VERSIONS = {"genesis-world": "1.4.1", "quadrants": "1.3.0"}


def record(tmp_path, family="push", status="completed"):
    source = tmp_path / "history"
    trial = source / "original"
    trial.mkdir(parents=True)
    case = {"id": "original", "family": family, "dt": 0.001, "repeat": 0}
    row = {
        "case": case,
        "engine": "genesis",
        "status": status,
        "task_success": False,
        "contact_force_validated": False,
        "max_momentum_residual_ns": {"object": 0.04},
    }
    manifest = {"engine": "genesis", "cases": [case], "source_hashes": HASHES}
    environment = {"packages": VERSIONS}
    (source / "manifest.json").write_text(json.dumps(manifest))
    (source / "environment.json").write_text(json.dumps(environment))
    (trial / "result.json").write_text(json.dumps(row))
    (trial / "trajectory.npz").write_bytes(b"raw native observations")
    return source, row, manifest, environment


def test_reuse_preserves_force_failure_and_original_evidence(tmp_path):
    source, row, _, _ = record(tmp_path)
    original = (source / "original/result.json").read_bytes()
    # A held-out/transfer label does not change the physical observation.
    case = {
        "id": "transfer-new",
        "family": "push",
        "phase": "transfer",
        "controller": "p1-d1-t3",
        "kp_scale": 1,
        "kd_scale": 1,
        "push_duration": 3,
    }
    stage = tmp_path / "transfer"
    recovery.seed_stage(stage, "genesis", [case], [source], VERSIONS, HASHES)
    result = json.loads((stage / "transfer-new/result.json").read_text())
    assert not result["task_success"] and not result["contact_force_validated"]
    assert result["max_momentum_residual_ns"] == row["max_momentum_residual_ns"]
    assert result["provenance"]["source_case"] == row["case"]
    assert result["provenance"]["source_sha256"] == hashlib.sha256(original).hexdigest()
    assert (source / "original/result.json").read_bytes() == original
    assert (stage / "transfer-new/trajectory.npz").is_symlink()


@pytest.mark.parametrize("change", ["version", "asset", "insertion", "error", "repeat"])
def test_reuse_rejects_wrong_version_asset_controller_or_execution(tmp_path, change):
    _, row, manifest, environment = record(tmp_path, family="insertion")
    case = row["case"].copy()
    if change == "version":
        environment["packages"] = {**VERSIONS, "genesis-world": "1.4.3"}
    elif change == "asset":
        manifest["source_hashes"] = {**HASHES, ASSET: "different"}
    elif change == "insertion":
        manifest["source_hashes"] = {**HASHES, CONTROLLER: "before-fix"}
    elif change == "error":
        row["status"] = "error"
    elif change == "repeat":
        case["repeat"] = 1
    assert not recovery.compatible(row, manifest, environment, case, VERSIONS, HASHES)


def test_latest_failed_attempt_does_not_reuse_old_success(tmp_path):
    source, row, _, _ = record(tmp_path)
    retry = source / "original/attempt-0001"
    retry.mkdir()
    (retry / "result.json").write_text(json.dumps(dict(row, status="error")))
    (retry / "trajectory.npz").write_bytes(b"partial")
    stage = tmp_path / "new"
    recovery.seed_stage(stage, "genesis", [row["case"]], [source], VERSIONS, HASHES)
    assert not (stage / "original/result.json").exists()
