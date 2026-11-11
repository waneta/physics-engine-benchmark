"""Explicit experiment matrices and resumable execution with immutable trial directories."""

import argparse
import hashlib
import itertools
import json
import sys
import traceback
from pathlib import Path

ENGINES = ("mujoco", "mujoco-warp", "genesis", "physx")


def rigid_cases():
    cases = []

    def add(family, variants, dt=(0.001,), repeats=3):
        for variant, step, repeat in itertools.product(variants, dt, range(repeats)):
            case = dict(family=family, dt=step, repeat=repeat, **variant)
            case["id"] = (
                family
                + "-"
                + hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest()[:12]
            )
            cases.append(case)

    for family in ("collision_chain", "panda_open_loop", "panda_tracking"):
        add(family, [{}], (0.001, 0.0005))
    add("grasp", [{"offset": v} for v in (0, 0.008)])
    add(
        "stack",
        [{"offset": v} for v in (0, 0.016, 0.020, 0.022)]
        + [{"offset": 0.020, "perturb_x": v, "perturb_y": -v} for v in (-0.001, 0.001)],
    )
    add(
        "push",
        [{"width": w, "rear_y": y} for w, y in itertools.product((0.09, 0.08), (0, -0.001, 0.001))],
        (0.001, 0.0005),
    )
    add("sweep", [{}])
    add(
        "insertion",
        [
            {"clearance": c, "offset": o, "tilt_deg": a}
            for c, (o, a) in itertools.product(
                (0.0001, 0.00025, 0.0005), ((0, 0), (0.00025, 0), (0, 1))
            )
        ],
    )
    add("insertion", [{"clearance": 0.0001, "tilt_deg": 1, "guided": True}])
    return cases


def tuning_cases():
    out = []
    for kp, kd, duration in itertools.product((0.5, 1, 2), (0.7, 1, 1.4), (2, 3, 4)):
        candidate = f"p{kp:g}-d{kd:g}-t{duration:g}"
        for i, y in enumerate((-0.002, 0, 0.002)):
            out.append(
                {
                    "id": f"train-{candidate}-{i}",
                    "family": "push",
                    "dt": 0.001,
                    "repeat": 0,
                    "phase": "train",
                    "candidate": candidate,
                    "kp_scale": kp,
                    "kd_scale": kd,
                    "push_duration": duration,
                    "width": 0.09,
                    "rear_y": y,
                }
            )
    for duration, i in itertools.product((3, 2, 1.5, 1, 0.75), range(3)):
        out.append(
            {
                "id": f"speed-{duration:g}-{i}",
                "family": "push",
                "dt": 0.001,
                "repeat": 0,
                "phase": "speed",
                "push_duration": duration,
                "width": 0.09,
                "rear_y": (-0.002, 0, 0.002)[i],
            }
        )
    return out


def select(results):
    groups = {}
    for r in results:
        c = r["case"]
        if c.get("phase") == "train":
            groups.setdefault(c["candidate"], []).append(r)
    if len(groups) != 27 or any(len(g) != 3 for g in groups.values()):
        raise ValueError("All 81 scheduled training results are required before selection")
    candidates = []
    for name, rs in groups.items():
        if not all(r.get("numerically_valid") and r.get("contact_force_validated") for r in rs):
            continue
        c = rs[0]["case"]
        distance = abs(c["kp_scale"] - 1) + abs(c["kd_scale"] - 1) + abs(c["push_duration"] - 3)
        key = (
            -sum(r["task_success"] for r in rs),
            -sum(r["passed_objects"] for r in rs),
            -sum(r["minimum_capped_goal_progress_m"] for r in rs) / 3,
            sum(r["normalized_squared_arm_effort"] for r in rs) / 3,
            distance,
            name,
        )
        candidates.append((key, c))
    if not candidates:
        raise ValueError("No candidate passed all three training validity gates")
    return min(candidates, key=lambda x: x[0])[1]


def heldout_cases(selected):
    out = []
    for mode in ("baseline", "selected"):
        for i, (width, y) in enumerate(
            [(0.09, y) for y in (-0.003, -0.001, 0.001, 0.003)]
            + [(0.08, y) for y in (-0.001, 0.001)]
        ):
            c = {
                "id": f"heldout-{mode}-{i}",
                "family": "push",
                "dt": 0.001,
                "repeat": 0,
                "phase": "heldout",
                "controller": mode,
                "width": width,
                "rear_y": y,
            }
            if mode == "selected":
                c.update({k: selected[k] for k in ("kp_scale", "kd_scale", "push_duration")})
            out.append(c)
    return out


def source_hashes():
    root = Path(__file__).resolve().parents[3]
    paths = list((root / "src/physics_benchmark").rglob("*.py")) + [
        root / "scripts/isaac_extended_worker.py",
        root / "scripts/isaac_worker.py",
        root / "configs/assets/panda/source.xml",
    ]
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
        if p.exists()
    }


def transfer_cases(selection_root):
    """Freeze all training selections, then evaluate each unique controller everywhere."""
    controllers = {"p1-d1-t3": {"kp_scale": 1, "kd_scale": 1, "push_duration": 3}}
    origins = {"p1-d1-t3": ["baseline"]}
    evidence = {}
    for engine in ENGINES:
        directory = Path(selection_root) / engine
        # Recompute from training records only; never trust a selection without its evidence.
        training = json.loads((directory / "results.json").read_text())
        digest = hashlib.sha256((directory / "results.json").read_bytes()).hexdigest()
        try:
            selected = select(training)
        except ValueError as exc:
            if str(exc) != "No candidate passed all three training validity gates":
                raise
            evidence[engine] = {"candidate": None, "reason": str(exc), "training_sha256": digest}
            continue
        saved = directory / "selection.json"
        if saved.exists() and json.loads(saved.read_text()) != selected:
            raise ValueError(f"Selection disagrees with frozen training records: {engine}")
        name = selected["candidate"]
        controllers[name] = {k: selected[k] for k in ("kp_scale", "kd_scale", "push_duration")}
        origins.setdefault(name, []).append(engine)
        evidence[engine] = {
            "candidate": name,
            "training_sha256": digest,
        }
    cases = []
    for name, controller in sorted(controllers.items()):
        for c in heldout_cases(controller):
            if c["controller"] != "selected":
                continue
            c.update(
                id=f"transfer-{name}-{c['id'].rsplit('-', 1)[1]}",
                phase="transfer",
                controller=name,
                selected_by=origins[name],
            )
            cases.append(c)
    return cases, evidence


def execute(cases, engine, output, resume=False):
    from .model import build
    from .rigid import run

    output = Path(output)
    manifest = {"schema": 1, "engine": engine, "cases": cases, "source_hashes": source_hashes()}
    if output.exists():
        if not resume:
            raise FileExistsError(f"{output} exists; choose a new output or --resume")
        previous = json.loads((output / "manifest.json").read_text())
        if previous != manifest:
            raise ValueError(
                "Resume requires identical cases, engine and source hashes; choose a new output after code changes"
            )
    else:
        output.mkdir(parents=True)
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2))
        from ..cli import environment

        (output / "environment.json").write_text(json.dumps(environment(engine), indent=2))
    results = []
    for i, case in enumerate(cases):
        trial = output / case["id"]
        result_file = trial / "result.json"
        attempts = sorted(trial.glob("attempt-*/result.json")) if trial.exists() else []
        if attempts:
            result_file = attempts[-1]
        if (
            result_file.exists()
            and json.loads(result_file.read_text()).get("status") != "interrupted"
        ):
            r = json.loads(result_file.read_text())
        else:
            if trial.exists():
                trial = trial / f"attempt-{len(list(trial.glob('attempt-*'))) + 1:04d}"
                result_file = trial / "result.json"
            print(f"[{i + 1}/{len(cases)}] {engine}: {case['id']}", flush=True)
            try:
                r = run(build(case), engine, trial)
            except KeyboardInterrupt:
                raise
            except Exception as e:  # noqa: BLE001 - retain native failures as auditable results
                trial.mkdir(parents=True, exist_ok=True)
                r = {
                    "case": case,
                    "engine": engine,
                    "status": "error",
                    "error": str(e),
                    "numerically_valid": False,
                    "task_success": False,
                }
                (trial / "error.txt").write_text(traceback.format_exc())
                result_file.write_text(json.dumps(r, indent=2))
            print(
                f"  {r['status']}; task_success={r['task_success']}; error={r.get('error')}",
                flush=True,
            )
        results.append(r)
        (output / "results.json").write_text(json.dumps(results, indent=2))
        if r["status"] == "interrupted":
            raise KeyboardInterrupt
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Extended article experiments. Run each engine in its own environment."
    )
    parser.add_argument(
        "scope", choices=("rigid", "tuning", "transfer", "soft", "throughput", "report")
    )
    parser.add_argument("--engine", choices=ENGINES + ("newton-vbd",), default="mujoco")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--family", action="append")
    parser.add_argument("--case-index", type=int)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--selection-root", type=Path)
    parser.add_argument(
        "--input", type=Path, action="append", help="Result roots to combine for report"
    )
    args = parser.parse_args(argv)
    if args.scope == "report":
        from .report import report

        report(args.output, args.input)
        return 0
    if args.scope in ("soft", "throughput"):
        from importlib import import_module

        return import_module("." + args.scope, __package__).main(args)
    evidence = None
    if args.scope == "transfer":
        if args.selection_root is None:
            parser.error(
                "transfer requires --selection-root pointing to the four engine tuning directories"
            )
        cases, evidence = transfer_cases(args.selection_root)
    else:
        cases = rigid_cases() if args.scope == "rigid" else tuning_cases()
    if args.family:
        cases = [c for c in cases if c["family"] in args.family]
    if args.case_index is not None:
        cases = [cases[args.case_index]]
    if args.plan_only:
        print(json.dumps(cases, indent=2))
        return 0
    try:
        results = execute(cases, args.engine, args.output, args.resume)
        if evidence is not None:
            (args.output / "selection-evidence.json").write_text(json.dumps(evidence, indent=2))
        if args.scope == "tuning" and args.case_index is None:
            try:
                choice = select(results)
            except ValueError as exc:
                if str(exc) != "No candidate passed all three training validity gates":
                    raise
                choice = {
                    "candidate": None,
                    "selection_status": "no_eligible_candidate",
                    "reason": str(exc),
                }
            (args.output / "selection.json").write_text(json.dumps(choice, indent=2))
            validation = (
                heldout_cases(choice)
                if choice["candidate"] is not None
                else [
                    c
                    for c in heldout_cases({"kp_scale": 1, "kd_scale": 1, "push_duration": 3})
                    if c["controller"] == "baseline"
                ]
            )
            results += execute(
                validation,
                args.engine,
                args.output / "heldout",
                args.resume and (args.output / "heldout").exists(),
            )
        from .report import report

        report(args.output)
        return 1 if any(r["status"] in ("error", "interrupted") for r in results) else 0
    except KeyboardInterrupt:
        print("Interrupted. Completed trials and the current prefix are retained.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
