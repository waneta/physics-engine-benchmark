"""Run the remaining engines sequentially, then check GUI display for each."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
relative = root.relative_to(Path.cwd())
runner = relative / "run_command.py"
environments = {
    "physx": ".venv",
    "mujoco-warp": ".venv-warp",
    "mujoco-cpu": ".venv",
    "genesis": ".venv-genesis",
}
for viewer, engines in (
    
    (True, ("physx", "mujoco-warp", "mujoco-cpu", "genesis")),
):
    for engine in engines:
        label = "viewer-physx-isolated" if engine == "physx" else "viewer-" + engine
        command = [
            sys.executable, str(runner), label,
            f"{environments[engine]}/bin/physics-bench", "run", "--engine", engine,
            "--scene", "drop", "--viewer" if viewer else "--headless",
            "--repeats", "1" if viewer else "3", "--output", str(relative / label),
        ]
        print(f"Starting {label}", flush=True)
        result = subprocess.run(command)
        if result.returncode:
            raise SystemExit(result.returncode)
