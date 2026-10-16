"""Compare audited run directories without hiding failures or changing raw data."""

import csv
import json
import os
from pathlib import Path

from .scenes import SCENES


def load_results(paths):
    datasets, engines = [], set()
    for path in paths:
        path = Path(path).resolve()
        cfg = json.loads((path / "config.json").read_text())
        env = json.loads((path / "environment.json").read_text())
        engine = env["engine"]
        if engine in engines:
            raise ValueError(f"Duplicate engine: {engine}")
        engines.add(engine)
        if datasets and cfg != datasets[0]["config"]:
            raise ValueError(f"Configuration mismatch: {path}")
        records = json.loads((path / "runs.json").read_text())
        for run in records:
            run["engine"] = engine
            run["rows"] = []
            if run["status"] == "passed" and run["repeat"] == 0:
                with (path / run["directory"] / "raw.csv").open() as stream:
                    run["rows"] = [
                        {k: float(v) for k, v in row.items()} for row in csv.DictReader(stream)
                    ]
        datasets.append({"path": path, "config": cfg, "environment": env, "records": records})
    if len(datasets) < 2:
        raise ValueError("At least two distinct engines are required")
    return datasets


def compare(args):
    from .cli import write_csv, write_json
    from .plotting import plot_scene

    datasets = load_results(args.inputs)
    output = args.output
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "config.json", datasets[0]["config"])
    records = [r for data in datasets for r in data["records"]]
    from .reporting import (
        SCENE_NAMES,
        STATUS_NAMES,
        drop_report_lines,
        metric_title,
        slide_report_lines,
        write_chinese_metrics,
    )

    write_chinese_metrics(output, records, datasets[0]["config"])
    write_csv(
        output / "summary.csv",
        [
            dict(
                engine=r["engine"],
                scene=r["scene"],
                dt_s=r["dt_s"],
                repeat=r["repeat"],
                status=r["status"],
                error=r.get("error", ""),
                **{k: v for k, v in r.get("metrics", {}).items() if k not in ("scene", "dt_s")},
            )
            for r in records
        ],
    )
    manifest = []
    lines = [
        f"# {len(datasets)} 引擎基础场景对比 / Multi-engine baseline comparison",
        "",
        "相同 SI 配置；保留全部重复与失败。表中为第一次重复，完整指标见 summary.csv。",
        "当前实验测量物理响应，不测吞吐量；峰值力依赖步长及接触模型，不能单独作为准确性排名。",
        "",
        "| 引擎 / Engine | 精度 / Precision | 通过 / 记录 (Passed / Recorded) | 来源 / Source |",
        "|---|---|---:|---|",
    ]
    complete = True
    expected_coverage = {(r["scene"], r["dt_s"], r["repeat"]) for r in records}
    for data in datasets:
        env, runs = data["environment"], data["records"]
        source = os.path.relpath(data["path"], output)
        passed = sum(r["status"] == "passed" for r in runs)
        coverage = {(r["scene"], r["dt_s"], r["repeat"]) for r in runs}
        complete &= bool(runs) and passed == len(runs) and coverage == expected_coverage
        lines.append(
            f"| {env['engine']} | {env['precision']} | {passed}/{len(runs)} | [报告 / Report]({source}/report.md) |"
        )
        imports = []
        for run in runs:
            file = data["path"] / run["directory"] / "imported.json"
            if file.exists():
                imported = json.loads(file.read_text())
                imports.append(
                    {
                        k: v
                        for k, v in imported.items()
                        if k
                        in (
                            "engine_version",
                            "warp_version",
                            "isaac_sim_version",
                            "container_image",
                            "container_image_id",
                            "implementation_difference",
                            "execution_path",
                            "force_source",
                        )
                    }
                )
                break
        manifest.append(
            {
                "engine": env["engine"],
                "source": str(data["path"]),
                "runtime": imports,
                "environment": env,
            }
        )
    write_json(output / "sources.json", manifest)
    lines += [
        "",
        "实现差异与精确版本见 sources.json 及各组 imported.json。",
        "MuJoCo-Warp 为直接 CUDA 后端；Genesis 为 CUDA float64；PhysX 为 Isaac Sim CPU TGS，",
        "使用原生接触冲量除以步长。PhysX 的硬接触没有与 solref/solimp 一一对应的参数。",
        "铰链参考为独立非线性 ODE 的 RK4 数值解。",
        "",
    ]
    columns = {
        "slide": [
            "stop_distance_m",
            "stop_time_s",
            "window_contact_jx_ns",
            "max_momentum_residual_ns",
        ],
        "drop": [
            "peak_contact_force_n",
            "max_penetration_m",
            "window_contact_jz_ns",
            "max_momentum_residual_ns",
        ],
        "hinge": [
            "max_angle_error_rad",
            "rms_angle_error_rad",
            "torque_impulse_nms",
        ],
    }
    for scene in SCENES:
        selected = [r for r in records if r["scene"] == scene]
        if not selected:
            continue
        lines += [
            f"## {SCENE_NAMES[scene]}",
            "",
            "| 引擎 / Engine | 步长 / Timestep (ms) | 状态 / Status | "
            + " | ".join(metric_title(key) for key in columns[scene])
            + " |",
            "|---|---:|---|" + "---:|" * len(columns[scene]),
        ]
        for run in selected:
            if run["repeat"] != 0:
                continue
            values = [run.get("metrics", {}).get(key) for key in columns[scene]]
            numbers = ["—" if value is None else f"{value:.7g}" for value in values]
            lines.append(
                f"| {run['engine']} | {run['dt_s'] * 1000:g} | {STATUS_NAMES[run['status']]} | "
                + " | ".join(numbers)
                + " |"
            )
        plot_scene(scene, selected, output, include_net_force=False)
        lines += ["", f"![{scene}]({scene}.png)", ""]
    if not complete:
        lines += ["", "**结果不完整：存在失败运行或各引擎实验覆盖范围不同。**", ""]
    lines += slide_report_lines(records, datasets[0]["config"])
    lines += drop_report_lines(records, datasets[0]["config"])
    (output / "report.md").write_text("\n".join(lines))
    print(f"Comparison: {(output / 'report.md').resolve()}")
    return 0 if complete else 1
