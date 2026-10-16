"""Protocol invariants: unloaded feedforward, physical meshes and unbiased selection."""

import copy
import json

import mujoco as mj
import numpy as np
import pytest

from physics_benchmark.extended.model import LIMIT, build
from physics_benchmark.extended.rigid import Controller, run
from physics_benchmark.extended.soft import MuJoCoSoft, mesh, volumes
from physics_benchmark.extended.suite import heldout_cases, rigid_cases, select, tuning_cases


@pytest.mark.parametrize(
    "family",
    [
        "collision_chain",
        "panda_open_loop",
        "panda_tracking",
        "grasp",
        "stack",
        "push",
        "sweep",
        "insertion",
    ],
)
def test_scene_compilation_and_frozen_reference(family):
    a = build({"family": family})
    b = build({"family": family})
    assert a.xml == b.xml
    assert a.reference.get("sha256") == b.reference.get("sha256")
    if a.controlled:
        assert a.reference["q"].shape[1] == a.controlled
        assert np.isfinite(a.reference["feedforward"]).all()
        np.testing.assert_array_equal(a.model.dof_armature, 0)
        np.testing.assert_array_equal(a.model.dof_damping, 0)


def test_frozen_feedforward_has_no_object_contact_load():
    a = build({"family": "grasp"})
    i = 1100
    m = copy.copy(a.model)
    m.opt.disableflags |= int(mj.mjtDisableBit.mjDSBL_CONTACT) | int(mj.mjtDisableBit.mjDSBL_LIMIT)
    d = mj.MjData(m)
    d.qpos[:] = a.data.qpos
    d.qpos[:9] = a.reference["q"][i]
    d.qvel[:9] = a.reference["v"][i]
    acceleration = np.gradient(a.reference["v"], a.reference["dt"], axis=0, edge_order=2)
    d.qacc[:9] = acceleration[i]
    mj.mj_inverse(m, d)
    np.testing.assert_allclose(a.reference["feedforward"][i], d.qfrc_inverse[:9], atol=1e-10)


def test_stack_offset_changes_placement_not_initial_cube():
    a = build({"family": "stack", "offset": 0})
    b = build({"family": "stack", "offset": 0.02})
    np.testing.assert_allclose(
        a.data.xpos[a.model.body("cube").id], b.data.xpos[b.model.body("cube").id]
    )
    assert not np.allclose(a.reference["q"], b.reference["q"])


def test_soft_refinement_preserves_volume_and_parent_boundary():
    coarse, ct, cm = mesh()
    fine, ft, fm = mesh(True)
    assert coarse.shape == (125, 3) and ct.shape == (384, 4)
    assert fine.shape == (729, 3) and ft.shape == (3072, 4)
    assert abs(cm.sum() - 0.10504912346763821) < 1e-14
    assert abs(cm.sum() - fm.sum()) < 1e-14
    np.testing.assert_allclose(
        np.sort(volumes(fine, ft)), np.sort(np.repeat(volumes(coarse, ct) / 8, 8)), rtol=1e-10
    )
    # Every new vertex is the midpoint of a coarse edge, never reprojected onto a sphere.
    coarse_edges = {
        tuple(sorted((int(a), int(b)))) for tet in ct for a in tet for b in tet if a != b
    }
    expected = {tuple((coarse[a] + coarse[b]) / 2) for a, b in coarse_edges}
    assert all(tuple(v) in expected for v in fine[len(coarse) :])


def test_flex_has_elastic_restoring_force_and_volume_lumped_mass():
    s = MuJoCoSoft({"family": "soft_compression", "dt": 0.00005}, "mujoco")
    s.data.qpos[6] = 0.001
    mj.mj_forward(s.model, s.data)
    assert np.linalg.norm(s.data.qfrc_passive) > 0.1
    ids = [s.model.body(f"ball_node_{i}").id for i in range(125)]
    np.testing.assert_allclose(s.model.body_mass[ids], s.masses)


def test_controller_same_at_matching_times_and_effort_caps():
    a = build({"family": "grasp", "dt": 0.001})
    b = build({"family": "grasp", "dt": 0.0005})
    q = a.data.qpos.copy()
    v = a.data.qvel.copy()
    forces = np.zeros((a.model.nbody, 6))
    poses = a.data.xpos.copy()
    u = Controller(a).command(700, q, v, forces, poses)
    other = Controller(b).command(1400, q, v, forces, poses)
    np.testing.assert_allclose(u, other)
    assert np.all(abs(u) <= LIMIT)


def test_insertion_controller_tracks_free_space_without_contact_support(tmp_path):
    scene = build({"family": "insertion", "clearance": 0.0001, "offset": 0, "tilt_deg": 0})
    scene.model.opt.disableflags |= int(mj.mjtDisableBit.mjDSBL_CONTACT)
    result = run(scene, "mujoco", tmp_path / "insertion")
    assert result["status"] == "completed" and result["task_success"]
    assert result["final_insertion_depth_m"] == pytest.approx(0.02, abs=1e-4)
    with np.load(tmp_path / "insertion/trajectory.npz") as a:
        hand = scene.model.body("hand").id
        index = np.rint(a["time"] / scene.reference["dt"]).astype(int)
        deviation = a["position"][:, hand] - scene.reference["hand"][index]
        assert np.linalg.norm(deviation[:, :2], axis=1).max() < 1e-4
        # Bounded Cartesian impedance permits transient vertical tracking lag.
        assert np.linalg.norm(deviation, axis=1).max() < 1e-3


def training_results():
    return [
        {
            "case": c,
            "numerically_valid": True,
            "contact_force_validated": True,
            "task_success": True,
            "passed_objects": 3,
            "minimum_capped_goal_progress_m": 0.1,
            "normalized_squared_arm_effort": 0.1,
        }
        for c in tuning_cases()
        if c["phase"] == "train"
    ]


def test_selection_requires_every_training_result_and_excludes_invalid():
    results = training_results()
    with pytest.raises(ValueError, match="81"):
        select(results[:-1])
    baseline = select(results)
    assert baseline["candidate"] == "p1-d1-t3"
    for r in results:
        if r["case"]["candidate"] == "p1-d1-t3":
            r["contact_force_validated"] = False
    assert select(results)["candidate"] != "p1-d1-t3"
    heldout = heldout_cases(baseline)
    assert len(heldout) == 12 and all(c["phase"] == "heldout" for c in heldout)
    # Held-out outcomes cannot influence selection, even with arbitrarily high scores.
    malicious = {"case": heldout[0], "task_success": True, "passed_objects": 999}
    assert select(results + [malicious]) == select(results)


def test_matrix_covers_full_rigid_protocol():
    plan = rigid_cases()
    assert len(plan) == 111
    assert len({c["id"] for c in plan}) == len(plan)
    assert {c["family"] for c in plan} == {
        "collision_chain",
        "panda_open_loop",
        "panda_tracking",
        "grasp",
        "stack",
        "push",
        "sweep",
        "insertion",
    }
    assert len([c for c in plan if c["family"] == "insertion" and not c.get("guided")]) == 27


def test_failure_retains_prefix_and_is_not_success(tmp_path, monkeypatch):
    from physics_benchmark.extended import rigid

    original = rigid.CPU.step
    counter = [0]

    def fail(self, command):
        counter[0] += 1
        if counter[0] == 10:
            raise RuntimeError("injected native failure")
        return original(self, command)

    monkeypatch.setattr(rigid.CPU, "step", fail)
    result = run(build({"family": "collision_chain"}), "mujoco", tmp_path / "trial")
    assert (
        result["status"] == "error"
        and not result["numerically_valid"]
        and not result["task_success"]
    )
    assert result["samples"] == 10
    assert (
        json.loads((tmp_path / "trial/result.json").read_text())["error"]
        == "injected native failure"
    )


def test_interrupt_retains_prefix(tmp_path, monkeypatch):
    from physics_benchmark.extended import rigid

    def interrupt(self, command):
        raise KeyboardInterrupt

    monkeypatch.setattr(rigid.CPU, "step", interrupt)
    result = run(build({"family": "collision_chain"}), "mujoco", tmp_path / "trial")
    assert result["status"] == "interrupted" and result["samples"] == 1
    assert (tmp_path / "trial/trajectory.npz").exists()


def test_cross_engine_transfer_freezes_training_selections(tmp_path):
    from physics_benchmark.extended.suite import ENGINES, transfer_cases

    for engine in ENGINES:
        directory = tmp_path / engine
        directory.mkdir()
        results = training_results()
        # One backend selects a genuinely different candidate using training evidence.
        if engine == "genesis":
            for r in results:
                if r["case"]["candidate"] == "p2-d1-t3":
                    r["normalized_squared_arm_effort"] = 0
        (directory / "results.json").write_text(json.dumps(results))
        (directory / "selection.json").write_text(json.dumps(select(results)))
    cases, evidence = transfer_cases(tmp_path)
    assert len(cases) == 12  # Two unique controllers, six layouts each.
    assert {c["controller"] for c in cases} == {"p1-d1-t3", "p2-d1-t3"}
    assert evidence["genesis"]["candidate"] == "p2-d1-t3"
    assert all(c["phase"] == "transfer" for c in cases)
    (tmp_path / "genesis/selection.json").write_text(json.dumps(select(training_results())))
    with pytest.raises(ValueError, match="disagrees"):
        transfer_cases(tmp_path)


def test_report_counts_latest_attempt_without_losing_history(tmp_path):
    from physics_benchmark.extended.report import read_results

    trial = tmp_path / "run" / "trial"
    (trial / "attempt-0001").mkdir(parents=True)
    original = {"case": {"id": "trial", "family": "push"}, "status": "interrupted"}
    (trial / "result.json").write_text(json.dumps(original))
    resumed = dict(original, status="completed")
    (trial / "attempt-0001/result.json").write_text(json.dumps(resumed))
    rows, history = read_results([tmp_path / "run"], tmp_path)
    assert len(rows) == len(history) == 1
    assert rows[0]["status"] == "completed"
    assert history[0]["status"] == "interrupted"


def test_transfer_retains_no_eligible_candidate_without_relaxing_force_gate(tmp_path):
    from physics_benchmark.extended.suite import ENGINES, transfer_cases

    for engine in ENGINES:
        directory = tmp_path / engine
        directory.mkdir()
        results = training_results()
        if engine == "mujoco-warp":
            for r in results:
                r["contact_force_validated"] = False
        (directory / "results.json").write_text(json.dumps(results))
    cases, evidence = transfer_cases(tmp_path)
    assert len(cases) == 6
    assert evidence["mujoco-warp"]["candidate"] is None
    assert all("mujoco-warp" not in c["selected_by"] for c in cases)
    (tmp_path / "mujoco-warp/results.json").write_text(json.dumps(training_results()[:-1]))
    with pytest.raises(ValueError, match="81"):
        transfer_cases(tmp_path)
