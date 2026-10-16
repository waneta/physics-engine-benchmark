"""Run isolated repeats, retain failures, and export auditable results."""

import argparse
import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import numpy as np

from .backends import ENGINES, load_backend
from .metrics import column, measure
from .scenes import SCENES, load_config, scene_xml
from .simulation import simulate


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def write_csv(path, rows):
    if not rows:
        return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def command_output(args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=15, check=False)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"error": str(exc)}


def environment(engine="mujoco-cpu"):
    cpu = "unknown"
    memory = "unknown"
    if Path("/proc/cpuinfo").exists():
        cpu = next(
            (
                line.split(":", 1)[1].strip()
                for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")
            ),
            cpu,
        )
    if Path("/proc/meminfo").exists():
        memory = Path("/proc/meminfo").read_text().splitlines()[0]
    root = Path(__file__).resolve().parents[2]
    sources = sorted(Path(__file__).parent.rglob("*.py")) + sorted((root / "scripts").glob("*.py"))
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "schema_version": 1,
        "engine": engine,
        "precision": "float32" if engine in ("mujoco-warp", "physx") else "float64",
        "rendering": False,
        "python": sys.version,
        "platform": platform.platform(),
        "cpu": cpu,
        "logical_cpus": os.cpu_count(),
        "memory": memory,
        # Resolve overlay packages using import precedence, not the last duplicate found.
        "packages": {
            name: importlib.metadata.version(name)
            for name in sorted({d.metadata["Name"] for d in importlib.metadata.distributions()})
        },
        "gpu": command_output(
            ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"]
        ),
        "git_commit": command_output(["git", "rev-parse", "HEAD"]),
        "git_status": command_output(["git", "status", "--short"]),
        "source_sha256": {
            str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources
        },
        "lock_sha256": hashlib.sha256(Path("uv.lock").read_bytes()).hexdigest()
        if Path("uv.lock").exists()
        else None,
    }


def write_report(output, records, repeatability, cfg, plots, planned_runs, engine="mujoco-cpu"):
    from .reporting import SCENE_NAMES, STATUS_NAMES, format_value

    passed = sum(r["status"] == "passed" for r in records)
    lines = [
        f"# {engine} 基础实验报告 / Baseline experiment report",
        "",
        (
            f"运行通过：{passed}/{planned_runs}；已记录 {len(records)} 组。"
            "这是一套独立实现，不是原文数值的精确复现。"
        ),
        "本次运行已中断，报告不完整；其余实验未执行。"
        if any(r["status"] == "interrupted" for r in records) or len(records) < planned_runs
        else "所有计划实验均已执行。",
        "",
        (
            "全部配置见 config.json，环境与代码指纹见 environment.json。"
            "每组目录包含 scene.xml、imported.json、raw.csv 和 metrics.json；"
            "失败时另存 failure.json，中断时另存 interruption.json；保留已采集数据。"
        ),
        "",
        "| 场景 / Scene | 步长 / Timestep (ms) | 重复 / Repeat | 状态 / Status | 主要指标 / Key metrics |",
        "|---|---:|---:|---|---|",
    ]
    for r in records:
        m = r.get("metrics", {})
        if "max_angle_error_rad" in m:
            detail = (
                f"最大角误差 / Maximum angle error {m['max_angle_error_rad'] * 180 / np.pi:.6f}°"
            )
        elif "peak_contact_force_n" in m:
            detail = (
                f"峰值接触合力 / Peak resultant contact force {m['peak_contact_force_n']:.6f} N"
            )
            if r["scene"] == "slide":
                detail += (
                    f"；最终X位移 / Final X displacement {m['final_displacement_m'] * 1000:.6f} mm"
                )
            else:
                detail += f"；最大穿透 / Maximum penetration {m['max_penetration_m'] * 1000:.6f} mm"
        else:
            detail = r.get("error", "无指标").replace("|", "/").replace("\n", " ")
        lines.append(
            f"| {SCENE_NAMES[r['scene']]} | {r['dt_s'] * 1000:g} | {r['repeat'] + 1} | "
            f"{STATUS_NAMES[r['status']]} | {detail} |"
        )
    lines += [
        "",
        "## 重复性 / Repeatability",
        "",
        (
            "每次重建模型和数据，不加入随机扰动；重复编号不是随机种子。"
            "检查每列相对第一次运行的最大绝对差，详见 repeatability.json。"
            "未使用重复次数估计统计置信区间。"
        ),
        "",
    ]
    for group in repeatability:
        lines.append(
            f"- {group['scene']} / {group['dt_s'] * 1000:g} ms："
            f"{group['successful_repeats']}/{group['requested_repeats']} 次通过；"
            f"所有数值列完全一致 / All numeric samples identical："
            f"{format_value(group['all_numeric_samples_identical'])}。"
        )
    lines += [
        "",
        "## 采样约定",
        "",
        (
            "raw.csv 每行对应 [t_start_s, t_end_s]。qpos/qvel 的 start/end 是物理步两端状态；"
            "contact_f* 是本步求解器施加在目标物体上的世界坐标力，contact_j*=contact_f*×dt。"
            "原生测量类型与接口见 imported.json（PhysX 原生冲量，其余引擎原生力）。SI 单位；"
            "自由体 qpos=[x,y,z,qw,qx,qy,qz]，"
            "qvel 前三项是世界坐标线速度、后三项是局部角速度；铰链为角度/角速度。"
        ),
        "",
        (
            f"冲量窗口从首次非零接触力开始，长度 {cfg['impulse_window_s'] * 1000:g} ms；"
            "window_contact_j* 是接触冲量，不含重力。窗口不完整时记 null。"
            "峰值力未经平滑；net_fz_n 包含重力。静置只针对质心线速度，"
            "要求此后全部已记录采样低于阈值，不代表仿真时长以外仍然静止。"
        ),
        "",
        "## 配置假设",
        "",
    ]
    lines += [f"- {a}" for a in cfg["provenance"]["assumptions"]]
    if plots:
        lines += ["", "## 步长对照曲线", ""]
        for scene in SCENES:
            if (output / f"{scene}.png").exists():
                lines += [f"![{scene}]({scene}.png)", ""]
    lines += [
        "",
        (
            "这是单引擎场景报告；跨引擎对照使用 compare 命令，并核查 imported.json 中的实现差异。"
            "当前采样带有 Python 与导出开销，不报告引擎吞吐量。"
        ),
        "",
    ]
    from .reporting import drop_report_lines, slide_report_lines

    lines += slide_report_lines(records, cfg)
    lines += drop_report_lines(records, cfg)
    (output / "report.md").write_text("\n".join(lines))


def run_suite(args):
    cfg = load_config(args.config)
    engine = getattr(args, "engine", "mujoco-cpu")
    simulate_fn = simulate if engine == "mujoco-cpu" else load_backend(engine).simulate
    viewer_enabled = getattr(args, "viewer", False)
    if viewer_enabled:
        from .viewer import ProcessViewer, validate_viewer_options

        validate_viewer_options(args.viewer_speed, args.viewer_hold)
        viewer_class = ProcessViewer
    if args.repeats < 1:
        raise ValueError("--repeats must be >= 1")
    output = args.output or Path("results") / (
        datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    )
    output.mkdir(parents=True, exist_ok=False)
    print(f"Output: {output.resolve()}", flush=True)
    write_json(output / "config.json", cfg)
    env = environment(engine)
    env.update(
        rendering=viewer_enabled,
        viewer="live measured states in isolated MuJoCo display model" if viewer_enabled else None,
    )
    write_json(output / "environment.json", env)
    scenes = SCENES if args.scene == "all" else (args.scene,)
    planned_runs = sum(len(cfg["timesteps_s"][s]) for s in scenes) * args.repeats
    records, metrics_rows, repeatability = [], [], []
    interrupted = False
    try:
        for scene in scenes:
            for dt in cfg["timesteps_s"][scene]:
                for repeat in range(args.repeats):
                    directory = output / scene / f"dt_{dt:.12g}" / f"repeat_{repeat:02d}"
                    directory.mkdir(parents=True)
                    (directory / "scene.xml").write_text(scene_xml(scene, cfg, dt))
                    record = {
                        "engine": engine,
                        "scene": scene,
                        "dt_s": dt,
                        "repeat": repeat,
                        "status": "failed",
                        "directory": str(directory.relative_to(output)),
                    }
                    rows = []
                    try:
                        print(
                            f"Running {engine}: {scene} dt={dt:g} repeat={repeat + 1}", flush=True
                        )
                        if viewer_enabled:
                            with viewer_class(
                                scene, cfg, dt, args.viewer_speed, args.viewer_hold, engine=engine
                            ) as viewer:
                                run = simulate_fn(scene, cfg, dt, rows, on_sample=viewer)
                                viewer_audit = viewer.audit()
                                write_json(directory / "viewer.json", viewer_audit)
                                viewer.finish()
                            viewer_audit["display_process_exit_code"] = viewer.exit_code
                            write_json(directory / "viewer.json", viewer_audit)
                        else:
                            run = simulate_fn(scene, cfg, dt, rows)
                        if "scene_usda" in run.imported:
                            (directory / "scene.usda").write_text(run.imported.pop("scene_usda"))
                        write_json(directory / "imported.json", run.imported)
                        metrics = measure(scene, cfg, rows)
                        record["metrics"] = metrics
                        write_json(directory / "metrics.json", metrics)
                        if (
                            metrics.get("max_momentum_residual_ns", 0)
                            > cfg["momentum_tolerance_ns"]
                        ):
                            raise RuntimeError(
                                "momentum-balance tolerance exceeded; inspect raw.csv"
                            )
                        record["status"] = "passed"
                    except KeyboardInterrupt:
                        record["status"] = "interrupted"
                        record["error"] = "KeyboardInterrupt: cancelled by user"
                        write_json(
                            directory / "interruption.json", {**record, "samples": len(rows)}
                        )
                        raise
                    except Exception as exc:  # noqa: BLE001 - retain any engine/metric failure
                        record["error"] = f"{type(exc).__name__}: {exc}"
                        write_json(
                            directory / "failure.json",
                            {**record, "traceback": traceback.format_exc(), "samples": len(rows)},
                        )
                    finally:
                        write_csv(directory / "raw.csv", rows)
                        records.append({**record, "rows": rows})
                        if record["status"] == "passed":
                            metrics_rows.append(
                                {"engine": engine, "repeat": repeat, **record["metrics"]}
                            )
                        write_json(
                            output / "runs.json",
                            [{k: v for k, v in r.items() if k != "rows"} for r in records],
                        )
                        print(
                            f"{scene:5} dt={dt:g} repeat={repeat + 1}: {record['status']}",
                            flush=True,
                        )
    except KeyboardInterrupt:
        interrupted = True
        print(
            "Interrupted (Ctrl+C). Saving partial results; remaining runs cancelled.",
            file=sys.stderr,
            flush=True,
        )
    for scene in scenes:
        for dt in cfg["timesteps_s"][scene]:
            successful = [
                r
                for r in records
                if r["scene"] == scene and r["dt_s"] == dt and r["status"] == "passed"
            ]
            differences = {}
            if len(successful) > 1:
                base = successful[0]["rows"]
                for key in base[0]:
                    differences[key] = max(
                        float(np.max(np.abs(column(r["rows"], key) - column(base, key))))
                        for r in successful[1:]
                    )
            repeatability.append(
                {
                    "scene": scene,
                    "dt_s": dt,
                    "successful_repeats": len(successful),
                    "requested_repeats": args.repeats,
                    "max_abs_difference_by_column": differences,
                    "all_numeric_samples_identical": all(v == 0 for v in differences.values())
                    if differences
                    else None,
                }
            )
    write_csv(output / "summary.csv", metrics_rows)
    from .reporting import write_chinese_metrics

    write_chinese_metrics(output, records, cfg)
    write_json(output / "repeatability.json", repeatability)
    # Persist the numerical report before optional plotting, which can also be interrupted.
    write_report(output, records, repeatability, cfg, False, planned_runs, engine)
    print(f"Report: {(output / 'report.md').resolve()}", flush=True)
    if not args.no_plots and not interrupted:
        from .plotting import plot_scene

        for scene in sorted({r["scene"] for r in records}):
            plot_scene(scene, [r for r in records if r["scene"] == scene], output)
        write_report(output, records, repeatability, cfg, True, planned_runs, engine)
    if interrupted:
        return 130
    return 0 if all(r["status"] == "passed" for r in records) else 1


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "extended":
        from .extended.suite import main as extended_main

        return extended_main(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser(
        "extended", help="Run Panda, contact tasks, soft bodies, tuning and GPU throughput"
    )
    sub.add_parser("doctor", help="Print software and hardware information")
    run = sub.add_parser("run", help="Run an engine's baselines and timestep comparisons")
    run.add_argument("--engine", choices=ENGINES, default="mujoco-cpu")
    run.add_argument("--config", type=Path, default=Path("configs/baseline.json"))
    run.add_argument("--scene", choices=("all", *SCENES), default="all")
    run.add_argument("--repeats", type=int, default=3)
    run.add_argument("--output", type=Path, help="New output directory; existing paths are refused")
    run.add_argument("--no-plots", action="store_true")
    display = run.add_mutually_exclusive_group()
    display.add_argument("--viewer", action="store_true", help="三维窗口显示所选引擎的实时测量状态")
    display.add_argument("--headless", action="store_true", help="无界面计算（默认）")
    run.add_argument(
        "--viewer-speed", type=float, default=0.2, help="播放速度，默认0.2倍；不改变dt"
    )
    run.add_argument("--viewer-hold", type=float, default=2.0, help="完成后保持窗口的秒数，默认2")
    comparison = sub.add_parser("compare", help="Compare existing result directories")
    comparison.add_argument("inputs", type=Path, nargs="+")
    comparison.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            print(json.dumps(environment(), indent=2, ensure_ascii=False))
            return 0
        if args.command == "compare":
            from .comparison import compare

            return compare(args)
        return run_suite(args)
    except KeyboardInterrupt:
        print(
            "Interrupted (Ctrl+C). Check the output directory printed above for saved results.",
            file=sys.stderr,
        )
        return 130
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
