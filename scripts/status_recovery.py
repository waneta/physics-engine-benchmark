"""Read live experiment coverage without importing or changing any simulator."""

import argparse
import json
import subprocess
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STATES = {
    "queued": "排队",
    "running": "运行",
    "completed": "结束",
    "error": "异常",
    "paused": "暂停",
    "interrupted": "中断",
}


def coverage(stage):
    manifest = stage / "manifest.json"
    if not manifest.exists():
        return "等待生成计划", ""
    cases = json.loads(manifest.read_text()).get("cases", [])
    rows = []
    for case in cases:
        trial = stage / case["id"]
        attempts = sorted(trial.glob("attempt-*/result.json"))
        file = attempts[-1] if attempts else trial / "result.json"
        if file.exists():
            try:
                rows.append(json.loads(file.read_text()))
            except json.JSONDecodeError:
                # A result may be in the middle of a write; read it on the next refresh.
                pass
    statuses = Counter(r["status"] for r in rows)
    details = []
    if statuses["error"]:
        details.append(f"异常{statuses['error']}")
    if statuses["inverted"]:
        details.append(f"翻转{statuses['inverted']}")
    heldout = stage / "heldout"
    if heldout.exists():
        count, _ = coverage(heldout)
        details.append(f"预留 {count}")
    return f"{len(rows)}/{len(cases)}", "; ".join(details)


def show(output, service):
    status = json.loads((output / "status.json").read_text())
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", service],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        live = result.stdout.strip() or "无法读取服务状态"
    except (OSError, subprocess.TimeoutExpired):
        live = "无法读取服务状态"
    print(datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S 上海时间"))
    print(f"后台服务: {live} ({service})")
    print(f"输出: {output}\n")
    print(f"{'任务':25} {'状态':4} {'已记录/计划':14} 备注")
    print("-" * 76)
    for key, value in status["jobs"].items():
        scope, engine = key.split("/")
        try:
            count, details = coverage(output / scope / engine)
        except (OSError, json.JSONDecodeError):
            count, details = "正在写入", "下一次刷新重读"
        print(f"{key:27} {STATES.get(value['state'], value['state']):4} {count:16} {details}")
    print("\nsoft=软体，transfer=控制器迁移，throughput=吞吐。")
    print("数量表示已记录配置，包含失败；结束表示作业退出，不代表物理验收全部通过。")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "results/full-recovery-20261009")
    parser.add_argument("--service", default="physics-bench-recovery-20261009.service")
    parser.add_argument("--watch", action="store_true", help="Refresh every five seconds")
    args = parser.parse_args()
    try:
        while True:
            if args.watch:
                print("\033[2J\033[H", end="", flush=True)
            show(args.output, args.service)
            if not args.watch:
                return 0
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n状态查看已退出，后台实验继续运行。")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
