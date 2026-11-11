"""Record an exact command and its exit status for this experimental batch."""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import shlex

root = Path(__file__).resolve().parent
label, *command = sys.argv[1:]
manifest = root / "rerun_manifest.json"
data = json.loads(manifest.read_text())
record = {
    "label": label,
    "command": shlex.join(command),
    "started_at": datetime.now(timezone.utc).isoformat(),
    "log": label + ".log",
    "status": "running",
}
data["commands"].append(record)
manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
with (root / record["log"]).open("w") as log:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        log.write(line)
        log.flush()
        print(line, end="", flush=True)
    code = process.wait()
data = json.loads(manifest.read_text())
data["commands"][-1].update(
    finished_at=datetime.now(timezone.utc).isoformat(),
    exit_code=code,
    status="finished" if code == 0 else "failed",
)
manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
raise SystemExit(code)
