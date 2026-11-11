"""Generate a report exclusively from locally recorded native experiments."""

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def report(root):
    root = Path(root)
    rows = []
    groups = defaultdict(list)
    for p in sorted(root.rglob("result.json")):
        r = json.loads(p.read_text())
        r["directory"] = str(p.parent.relative_to(root))
        rows.append(r)
        groups[(r["case"]["family"], r["engine"])].append(r)
    lines = [
        "# 扩展物理实验实测报告",
        "",
        "数据来源：本目录各次原生仿真的 `result.json` 和 `trajectory.npz`。任务失败、数值无效和接触力核算不通过分别记录；没有运行的配置不计入分母。",
        "",
        "| 实验 | 引擎 | 已记录 | 数值有效 | 任务成功 | 力核算通过 | 异常/翻转 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for (family, engine), rs in sorted(groups.items()):
        lines.append(
            f"| {family} | {engine} | {len(rs)} | {sum(bool(r.get('numerically_valid')) for r in rs)} | {sum(bool(r.get('task_success')) for r in rs)} | {sum(r.get('contact_force_validated', r.get('force_validated')) is True for r in rs)} | {sum(r['status'] in ('error', 'inverted', 'interrupted') for r in rs)} |"
        )
    lines += [
        "",
        "数值有效表示已完成相应状态校验；插销触发过载属于任务停止。力数据只有通过独立动量核算才可用于定量比较。所有软体质量从实际四面体体积计算；网格细化保留粗网格边界。",
        "",
        "原文公开了协议和部分参数，没有公开完整场景源码及冻结轨迹。本项目依据公开协议独立实现，几何补全、引擎版本和硬件差异见 `docs/full-experiments.md`，这些数据不等同于原文复现值。",
    ]
    errors = [r for r in rows if r.get("error")]
    if errors:
        lines += ["", "## 异常记录", ""] + [
            f"- `{r['directory']}`：{r['error'].splitlines()[-1]}" for r in errors
        ]
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        families = sorted({r["case"]["family"] for r in rows})
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
                        y = (a["centroid"][:, 2] - a["centroid"][0, 2]) * 1000
                        label = "Vertex centroid lift (mm)"
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
                name = family + ".png"
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
