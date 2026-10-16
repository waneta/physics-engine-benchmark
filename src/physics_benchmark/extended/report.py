"""Generate a report exclusively from locally recorded native experiments."""

import csv
import json
import os
from collections import defaultdict
from pathlib import Path

import numpy as np


def read_results(inputs, root):
    """Count the latest attempt per trial; retain superseded attempts as history."""
    latest = {}
    ranks = {}
    history = []
    for directory in inputs:
        for p in sorted(Path(directory).rglob("result.json")):
            r = json.loads(p.read_text())
            r["directory"] = os.path.relpath(p.parent, root)
            trial = p.parent.parent if p.parent.name.startswith("attempt-") else p.parent
            key = str(trial.resolve())
            rank = int(p.parent.name.split("-")[1]) if p.parent.name.startswith("attempt-") else 0
            if key in latest:
                if rank < ranks[key]:
                    history.append(r)
                    continue
                history.append(latest[key])
            latest[key] = r
            ranks[key] = rank
    return list(latest.values()), history


def report(root, inputs=None):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    inputs = [Path(p) for p in inputs] if inputs else [root]
    rows, history = read_results(inputs, root)
    groups = defaultdict(list)
    for r in rows:
        family = r["case"]["family"]
        if r["case"].get("phase"):
            family += "/" + r["case"]["phase"]
        groups[(family, r["engine"])].append(r)
    lines = [
        "# 扩展物理实验实测报告",
        "",
        "数据来源：下列批次各次原生仿真的 `result.json` 和 `trajectory.npz`。任务失败、数值无效和接触力核算不通过分别记录；未运行配置列为缺失。恢复重试只统计最后一次，旧尝试仍保留。",
        "",
    ]
    lines += [f"- [{os.path.relpath(p, root)}]({os.path.relpath(p, root)}/)" for p in inputs]
    reused = [r for r in rows if r.get("provenance")]
    if reused:
        observations = {r["provenance"]["source_result"] for r in reused}
        lines += [
            "",
            (
                f"本批次 {len(reused)} 条记录沿用 {len(observations)} 次历史观测；不是新增独立重复。"
                "每条 result.json 的 provenance 保留原始结果 SHA256、配置、源码摘要与环境路径。"
                "计数按矩阵用途展示，汇总统计时不得把同一次观测的多个用途当作独立样本。"
                "完整映射见 [reuse-index.json](reuse-index.json)。"
            ),
        ]
        (root / "reuse-index.json").write_text(
            json.dumps([{"directory": r["directory"], **r["provenance"]} for r in reused], indent=2)
        )
    lines += ["", "## 计划覆盖", "", "| 批次 | 已记录 / 计划 | 缺失 |", "|---|---:|---:|"]
    recorded = {}
    for r in rows:
        p = (root / r["directory"]).resolve()
        if p.name.startswith("attempt-"):
            p = p.parent
        recorded.setdefault(str(p.parent), set()).add(r["case"].get("id", p.name))
    missing = 0
    pending_jobs = []
    for source in inputs:
        for p in sorted(source.rglob("manifest.json")):
            manifest = json.loads(p.read_text())
            if "cases" not in manifest:
                continue
            planned = {c["id"] for c in manifest["cases"]}
            actual = recorded.get(str(p.parent.resolve()), set())
            absent = len(planned - actual)
            missing += absent
            lines.append(
                f"| {os.path.relpath(p.parent, root)} | {len(planned & actual)} / {len(planned)} | {absent} |"
            )
        status_path = source / "status.json"
        if status_path.exists():
            status = json.loads(status_path.read_text())
            pending = [
                key + ": " + item["state"]
                for key, item in status["jobs"].items()
                if item["state"] != "completed"
            ]
            if pending:
                pending_jobs.extend(os.path.relpath(source, root) + "/" + p for p in pending)
    if pending_jobs:
        lines += ["", "运行器尚未完成的批次：" + "；".join(pending_jobs) + "。"]
    lines += [
        "",
        f"已生成计划中的缺失结果：{missing}；历史尝试：{len(history)}。尚未生成计划的后续批次不在该缺失数内，请同时检查运行器状态。",
        "",
        "## 数值与任务结果",
        "",
        "| 实验 | 引擎 | 已记录 | 数值有效 | 任务成功 | 力核算通过 | 异常/翻转 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for (family, engine), rs in sorted(groups.items()):
        if family == "throughput":
            continue
        lines.append(
            f"| {family} | {engine} | {len(rs)} | {sum(bool(r.get('numerically_valid')) for r in rs)} | {sum(bool(r.get('task_success')) for r in rs)} | {sum(r.get('contact_force_validated', r.get('force_validated')) is True for r in rs)} | {sum(r['status'] in ('error', 'inverted', 'interrupted') for r in rs)} |"
        )
    lines += [
        "",
        "数值有效表示已完成相应状态校验；插销触发过载属于任务停止。力数据只有通过独立动量核算才可用于定量比较。所有软体质量从实际四面体体积计算；网格细化保留粗网格边界。",
        "",
        "原文公开了协议和部分参数，没有公开完整场景源码及冻结轨迹。本项目依据公开协议独立实现，几何补全、引擎版本和硬件差异见 `docs/full-experiments.md`，这些数据不等同于原文复现值。",
    ]
    selections = {}
    for source in inputs:
        for p in sorted(source.rglob("selection.json")):
            if "transfer-selection" in p.parts:
                continue
            selections[p.parent.name] = json.loads(p.read_text())["candidate"]
    if selections:
        lines += [
            "",
            "## 冻结控制器与迁移",
            "",
            "训练选中："
            + "；".join(f"{e}: `{c}`" for e, c in sorted(selections.items()))
            + "。预留数据不参与选择。",
            "",
            "| 控制器 | 测试引擎 | 成功 / 已记录 | 数值无效 | 平均归一化力矩平方 |",
            "|---|---|---:|---:|---:|",
        ]
        transfer = defaultdict(list)
        for r in rows:
            if r["case"].get("phase") in ("heldout", "transfer"):
                label = r["case"]["controller"]
                if r["case"]["phase"] == "heldout":
                    label = "本引擎预留/" + label
                transfer[(label, r["engine"])].append(r)
        for (controller, engine), rs in sorted(transfer.items()):
            effort = [
                r["normalized_squared_arm_effort"]
                for r in rs
                if r.get("numerically_valid") and "normalized_squared_arm_effort" in r
            ]
            mean = f"{np.mean(effort):.6g}" if effort else "—"
            lines.append(
                f"| {controller} | {engine} | {sum(bool(r.get('task_success')) for r in rs)} / {len(rs)} | {sum(not r.get('numerically_valid', False) for r in rs)} | {mean} |"
            )
    soft = [r for r in rows if r["case"]["family"].startswith("soft_")]
    if soft:
        lines += [
            "",
            "## 软体步长、网格与力阈值",
            "",
            "| 引擎 | 实验 | dt (µs) | 节点 | 指令力 (N) | SAP | 状态 | 保持段质心抬升 (mm) | 压缩反力 (N) |",
            "|---|---|---:|---:|---:|---:|---|---:|---:|",
        ]
        for r in soft:
            c = r["case"]
            lift = r.get("hold_com_lift_m")
            force = r.get("force_n")
            lines.append(
                f"| {r['engine']} | {c['id']} | {c['dt'] * 1e6:g} | {r.get('audit', {}).get('vertex_count', '—')} | {c.get('finger_force', '—')} | {c.get('sap_iterations', 5) if r['engine'] == 'genesis' else '—'} | {r['status']} | {format(lift * 1000, '.4g') if lift is not None else '—'} | {format(force, '.4g') if force is not None else '—'} |"
            )
    throughput = [r for r in rows if r["case"]["family"] == "throughput"]
    if throughput:
        lines += [
            "",
            "## 吞吐实测",
            "",
            "仅轨迹校验通过的结果可比较速度。三次计时的范围不代表置信区间，OOM 是本机容量限制。",
            "",
            "| 引擎 | 环境数 | 状态 | 轨迹校验 | 中位秒数 | 世界步/秒 |",
            "|---|---:|---|---|---:|---:|",
        ]
        for r in throughput:
            valid = r.get("trajectory_validated", False)
            seconds = format(r["median_seconds"], ".6g") if valid else "—"
            speed = format(r["world_steps_per_second"], ".6g") if valid else "—"
            lines.append(
                f"| {r['engine']} | {r['batch']} | {r['status']} | {valid} | {seconds} | {speed} |"
            )
    speed_groups = defaultdict(list)
    for r in rows:
        if r["case"].get("phase") == "speed":
            speed_groups[(r["engine"], r["case"]["push_duration"])].append(r)
    if speed_groups:
        import mujoco as mj

        lines += [
            "",
            "## 固定控制器速度扫描",
            "",
            "手部高度偏差从原生位姿计算，相对初始高度；范围跨三种布局，不是置信区间。",
            "",
            "| 引擎 | 推送时长 (s) | 放置成功 / 已记录 | 数值无效 | 峰值高度偏差范围 (mm) |",
            "|---|---:|---:|---:|---:|",
        ]
        for (engine, duration), rs in sorted(speed_groups.items()):
            peaks = []
            for r in rs:
                directory = root / r["directory"]
                if not r.get("numerically_valid"):
                    continue
                model = mj.MjModel.from_xml_path(str(directory / "scene.xml"))
                with np.load(directory / "trajectory.npz") as data:
                    z = data["position"][:, model.body("hand").id, 2]
                    peaks.append(float(np.max(abs(z - z[0]))) * 1000)
            span = f"{min(peaks):.4g}–{max(peaks):.4g}" if peaks else "—"
            lines.append(
                f"| {engine} | {duration:g} | {sum(bool(r.get('task_success')) for r in rs)} / {len(rs)} | {sum(not r.get('numerically_valid', False) for r in rs)} | {span} |"
            )
    reference_groups = defaultdict(set)
    reference_engines = defaultdict(set)
    for r in rows:
        ref = r.get("reference_sha256") or r.get("audit", {}).get("reference_sha256")
        if ref:
            c = {k: v for k, v in r["case"].items() if k not in ("dt", "repeat", "id")}
            key = json.dumps(c, sort_keys=True)
            reference_groups[key].add(ref)
            reference_engines[key].add(r["engine"])
    paired = {
        key: values for key, values in reference_groups.items() if len(reference_engines[key]) > 1
    }
    mismatches = [key for key, values in paired.items() if len(values) != 1]
    lines += [
        "",
        "## 参考轨迹一致性",
        "",
        f"在两个及以上引擎运行的 {len(paired)} 个配置中，参考摘要不一致：{len(mismatches)}。这只检查共同参考输入，不证明输出轨迹一致。",
    ]
    if mismatches:
        lines += [f"- `{case}`" for case in mismatches]
    errors = [r for r in rows if r.get("error")]
    if errors:
        lines += ["", "## 异常记录", ""] + [
            f"- `{r['directory']}`：{r['error'].splitlines()[-1]}" for r in errors
        ]
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        families = sorted({f for f, _ in groups if f != "throughput"})
        for family in families:
            fig, ax = plt.subplots(figsize=(8, 4))
            drawn = False
            for (f, engine), rs in sorted(groups.items()):
                if f != family:
                    continue
                selected = next(
                    (
                        r
                        for r in rs
                        if (root / r["directory"] / "trajectory.npz").exists()
                        and r.get("samples", 0) > 1
                    ),
                    None,
                )
                if selected is None:
                    continue
                with np.load(root / selected["directory"] / "trajectory.npz") as a:
                    if "centroid" in a:
                        center = a["com"] if "com" in a else a["centroid"]
                        y = (center[:, 2] - center[0, 2]) * 1000
                        label = (
                            "Center of mass lift (mm)"
                            if "com" in a
                            else "Vertex centroid lift (mm)"
                        )
                    elif "command" in a and a["command"].shape[1]:
                        refpath = root / selected["directory"] / "reference.npz"
                        with np.load(refpath) as ref:
                            idx = np.minimum(
                                np.rint(a["time"] / float(ref["dt"])).astype(int), len(ref["q"]) - 1
                            )
                            y = np.sqrt(np.mean((a["q"][:, :7] - ref["q"][idx, :7]) ** 2, axis=1))
                            label = "Arm joint RMS error (rad)"
                    else:
                        y = a["q"][:, 0]
                        label = "First body x (m)"
                    ax.plot(a["time"], y, label=engine + " / " + selected["status"])
                    drawn = True
            if drawn:
                ax.set(xlabel="Time (s)", ylabel=label, title=family)
                ax.grid(alpha=0.25)
                ax.legend()
                fig.tight_layout()
                name = family.replace("/", "-") + ".png"
                fig.savefig(root / name, dpi=150)
                lines += ["", f"![{family}]({name})"]
            plt.close(fig)
    except ImportError:
        lines += ["", "当前环境缺少 Matplotlib，未生成图表。"]
    fields = (
        "directory",
        "engine",
        "family",
        "status",
        "numerically_valid",
        "task_success",
        "samples",
        "wall_seconds",
        "contact_force_validated",
        "hold_lift_m",
        "joint_rmse_rad",
        "passed_objects",
        "objects_in_tray",
        "final_insertion_depth_m",
    )
    with (root / "summary.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow(
                {k: (r["case"]["family"] if k == "family" else r.get(k)) for k in fields}
            )
    (root / "report.md").write_text("\n".join(lines) + "\n")
