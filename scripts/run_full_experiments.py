"""Freeze source code, then run the full matrix in isolated engine environments.

Accuracy jobs may overlap; throughput starts only after all accuracy jobs finish.
Each output is immutable. --resume reuses the frozen source snapshot.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENVS = {
    "mujoco": ".venv",
    "physx": ".venv",
    "mujoco-warp": ".venv-warp",
    "genesis": ".venv-genesis",
    "newton-vbd": ".venv-newton",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--scope", choices=("rigid", "soft", "tuning", "transfer", "throughput"), action="append"
    )
    parser.add_argument("--engine", choices=tuple(ENVS), action="append")
    parser.add_argument("--selection-root", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    scopes = args.scope or ["rigid", "soft", "tuning", "transfer", "throughput"]
    engines = args.engine or list(ENVS)
    output.mkdir(parents=True, exist_ok=args.resume)
    snapshot = output / "source"
    if not snapshot.exists():
        for dirname in ("src", "configs", "scripts", "requirements"):
            shutil.copytree(
                ROOT / dirname,
                snapshot / dirname,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
        (snapshot / ".venv").symlink_to(ROOT / ".venv", target_is_directory=True)
        (output / "request.json").write_text(
            json.dumps({"scopes": scopes, "engines": engines}, indent=2)
        )
    elif json.loads((output / "request.json").read_text()) != {
        "scopes": scopes,
        "engines": engines,
    }:
        raise ValueError("Resume requires the same requested scopes and engines")
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(snapshot / "src")
    environment["PYTHONUNBUFFERED"] = "1"
    environment["MPLCONFIGDIR"] = str(ROOT / ".cache/matplotlib")
    logdir = output / "logs"
    logdir.mkdir(exist_ok=True)
    lock = threading.Lock()
    jobs = {}
    status_file = output / "status.json"
    if args.resume and status_file.exists():
        jobs = json.loads(status_file.read_text()).get("jobs", {})

    def save():
        payload = {"pid": os.getpid(), "updated_at": datetime.now(UTC).isoformat(), "jobs": jobs}
        temporary = status_file.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, indent=2))
        temporary.replace(status_file)

    def job(scope, engine):
        key = f"{scope}/{engine}"
        path = output / scope / engine
        with lock:
            if jobs.get(key, {}).get("state") == "completed":
                return 0
            jobs[key] = {"state": "running", "started_at": datetime.now(UTC).isoformat()}
            save()
        command = [
            str(ROOT / ENVS[engine] / "bin/python"),
            "-u",
            "-m",
            "physics_benchmark.extended.suite",
            scope,
            "--engine",
            engine,
            "--output",
            str(path),
        ]
        if scope == "transfer":
            command.extend(["--selection-root", str(output / "transfer-selection")])
        if path.exists():
            command.append("--resume")
        with (logdir / f"{scope}-{engine}.log").open("a") as log:
            process = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
            )
        with lock:
            jobs[key].update(
                state="completed" if process.returncode == 0 else "error",
                exit_code=process.returncode,
                finished_at=datetime.now(UTC).isoformat(),
            )
            save()
        print(key, jobs[key]["state"], flush=True)
        return process.returncode

    def cpu_accuracy():
        if "mujoco" in engines:
            for scope in scopes:
                if scope not in ("throughput", "transfer"):
                    job(scope, "mujoco")

    with ThreadPoolExecutor(max_workers=4) as pool:
        cpu = pool.submit(cpu_accuracy)
        for scope in ("rigid", "tuning"):
            if scope in scopes:
                futures = [
                    pool.submit(job, scope, e) for e in engines if e not in ("mujoco", "newton-vbd")
                ]
                for future in futures:
                    future.result()
        if "soft" in scopes:
            # FEM builds and dense flex solvers have substantial memory requirements.
            for engine in engines:
                if engine != "mujoco":
                    job("soft", engine)
        cpu.result()
        if "transfer" in scopes:
            selection_root = args.selection_root or output / "tuning"
            frozen_selection = output / "transfer-selection"
            if not frozen_selection.exists():
                for engine in ENVS:
                    if engine == "newton-vbd":
                        continue
                    destination = frozen_selection / engine
                    destination.mkdir(parents=True)
                    for name in ("results.json", "selection.json"):
                        source = selection_root / engine / name
                        if name == "results.json" or source.exists():
                            shutil.copy2(source, destination / name)
            futures = [pool.submit(job, "transfer", e) for e in engines if e != "newton-vbd"]
            for future in futures:
                future.result()
    if "throughput" in scopes:
        for engine in engines:
            if engine in ("mujoco", "mujoco-warp", "genesis"):
                job("throughput", engine)
    command = [
        str(ROOT / ".venv/bin/python"),
        "-m",
        "physics_benchmark.extended.suite",
        "report",
        "--output",
        str(output),
    ]
    subprocess.run(command, cwd=ROOT, env=environment, check=True)
    with lock:
        save()
    return int(any(j["state"] != "completed" for j in jobs.values()))


if __name__ == "__main__":
    sys.exit(main())
