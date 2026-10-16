"""Bilingual metric names and units for individual and combined results."""

import csv
import json
from collections import defaultdict

import numpy as np

ENGINE_NAMES = {
    "mujoco-cpu": "MuJoCo CPU",
    "mujoco-warp": "MuJoCo-Warp（直接 CUDA）",
    "genesis": "Genesis CUDA",
    "physx": "PhysX（Isaac Sim CPU TGS）",
}
SCENE_NAMES = {
    "slide": "滑动方块 / Sliding cube",
    "drop": "方块下落 / Cube drop",
    "hinge": "单铰链 / Single hinge",
}
STATUS_NAMES = {
    "passed": "通过 / Passed",
    "failed": "失败 / Failed",
    "interrupted": "中断 / Interrupted",
}
# Unit 1 denotes dimensionless quantities; null denotes unavailable, never zero.
METRICS = {
    "dt_s": ("仿真步长", "s"),
    "steps": ("物理步数", "步"),
    "peak_contact_force_n": ("峰值接触合力", "N"),
    "peak_contact_fz_n": ("峰值法向接触力", "N"),
    "max_penetration_m": ("最大穿透深度", "m"),
    "first_contact_s": ("首次接触时间", "s"),
    "settled_time_s": ("质心静置时间", "s"),
    "max_momentum_residual_ns": ("最大动量平衡残差", "N·s"),
    "max_constraint_force_error_n": ("最大接触力核算误差", "N"),
    "window_contact_jx_ns": ("窗口接触冲量X", "N·s"),
    "window_contact_jy_ns": ("窗口接触冲量Y", "N·s"),
    "window_contact_jz_ns": ("窗口接触冲量Z", "N·s"),
    "impulse_window_complete": ("接触冲量窗口完整", "布尔"),
    "stop_time_s": ("停止时间", "s"),
    "stop_distance_m": ("停止距离", "m"),
    "final_displacement_m": ("最终X位移", "m"),
    "max_com_lift_m": ("最大质心抬升", "m"),
    "ideal_coulomb_distance_m": ("理想库仑停止距离", "m"),
    "configured_friction_coefficient": ("设定摩擦系数", "1"),
    "friction_measurement_samples": ("滑动段测量步数", "步"),
    "friction_contact_samples": ("滑动窗口内有接触步数", "步"),
    "mean_friction_force_n": ("滑动段平均摩擦力", "N"),
    "mean_normal_force_n": ("滑动段平均法向力", "N"),
    "effective_friction_coefficient": ("实测等效摩擦系数", "1"),
    "mean_deceleration_m_s2": ("滑动段平均X减速度", "m/s²"),
    "friction_opposes_motion": ("滑动段摩擦力反向", "布尔"),
    "total_contact_jx_ns": ("全程X接触冲量", "N·s"),
    "max_displacement_error_m": ("相对理想轨迹最大X位移误差", "m"),
    "rms_displacement_error_m": ("相对理想轨迹X位移均方根误差", "m"),
    "max_slide_velocity_error_m_s": ("相对理想轨迹最大X速度误差", "m/s"),
    "max_lateral_displacement_m": ("最大侧向偏移", "m"),
    "ideal_coulomb_stop_time_s": ("理想库仑停止时间", "s"),
    "stop_distance_error_percent": ("停止距离相对理想值偏差", "%"),
    "minimum_com_height_m": ("最低质心高度", "m"),
    "ideal_first_contact_s": ("理想首次接触时间", "s"),
    "first_contact_time_error_s": ("首次接触时间相对理想值偏差", "s"),
    "preimpact_vertical_velocity_m_s": ("首次接触步初竖直速度", "m/s"),
    "ideal_impact_vertical_velocity_m_s": ("理想碰撞前竖直速度", "m/s"),
    "peak_rebound_vertical_velocity_m_s": ("接触后最大向上速度", "m/s"),
    "max_free_fall_height_error_m": ("自由落体段最大高度误差", "m"),
    "max_free_fall_velocity_error_m_s": ("自由落体段最大竖直速度误差", "m/s"),
    "final_com_height_m": ("最终质心高度", "m"),
    "final_linear_speed_m_s": ("最终质心线速度模长", "m/s"),
    "final_angular_speed_rad_s": ("最终角速度模长", "rad/s"),
    "rigid_settled_time_s": ("刚体静置时间", "s"),
    "rest_observation_duration_s": ("静置后观察时长", "s"),
    "settled_within_duration": ("记录时长内刚体已静置", "布尔"),
    "settling_angular_speed_threshold_rad_s": ("静置角速度阈值", "rad/s"),
    "mean_tail_normal_force_n": ("末段平均法向接触力", "N"),
    "tail_support_weight_ratio": ("末段平均支撑力与重力比", "1"),
    "max_horizontal_displacement_m": ("最大水平偏移", "m"),
    "total_contact_jz_ns": ("全程Z接触冲量", "N·s"),
    "max_angle_error_rad": ("最大角度误差", "rad"),
    "rms_angle_error_rad": ("角度均方根误差", "rad"),
    "max_velocity_error_rad_s": ("最大角速度误差", "rad/s"),
    "torque_impulse_nms": ("力矩冲量", "N·m·s"),
}

METRIC_NAMES_EN = {
    "dt_s": "Simulation timestep",
    "steps": "Physics steps",
    "peak_contact_force_n": "Peak resultant contact force",
    "peak_contact_fz_n": "Peak normal contact force",
    "max_penetration_m": "Maximum penetration depth",
    "first_contact_s": "First contact time",
    "settled_time_s": "COM settling time",
    "max_momentum_residual_ns": "Maximum momentum balance residual",
    "max_constraint_force_error_n": "Maximum contact force accounting error",
    "window_contact_jx_ns": "Window contact impulse X",
    "window_contact_jy_ns": "Window contact impulse Y",
    "window_contact_jz_ns": "Window contact impulse Z",
    "impulse_window_complete": "Contact impulse window complete",
    "stop_time_s": "Stopping time",
    "stop_distance_m": "Stopping distance",
    "final_displacement_m": "Final X displacement",
    "max_com_lift_m": "Maximum COM lift",
    "ideal_coulomb_distance_m": "Ideal Coulomb stopping distance",
    "configured_friction_coefficient": "Configured friction coefficient",
    "friction_measurement_samples": "Sliding measurement steps",
    "friction_contact_samples": "Contact steps in sliding window",
    "mean_friction_force_n": "Mean sliding friction force",
    "mean_normal_force_n": "Mean sliding normal force",
    "effective_friction_coefficient": "Measured effective friction coefficient",
    "mean_deceleration_m_s2": "Mean sliding X deceleration",
    "friction_opposes_motion": "Sliding friction opposes motion",
    "total_contact_jx_ns": "Total contact impulse X",
    "max_displacement_error_m": "Maximum X displacement error vs ideal trajectory",
    "rms_displacement_error_m": "RMS X displacement error vs ideal trajectory",
    "max_slide_velocity_error_m_s": "Maximum X velocity error vs ideal trajectory",
    "max_lateral_displacement_m": "Maximum lateral displacement",
    "ideal_coulomb_stop_time_s": "Ideal Coulomb stopping time",
    "stop_distance_error_percent": "Stopping distance deviation from ideal",
    "minimum_com_height_m": "Minimum COM height",
    "ideal_first_contact_s": "Ideal first contact time",
    "first_contact_time_error_s": "First contact time deviation from ideal",
    "preimpact_vertical_velocity_m_s": "Vertical velocity at start of first contact step",
    "ideal_impact_vertical_velocity_m_s": "Ideal preimpact vertical velocity",
    "peak_rebound_vertical_velocity_m_s": "Peak upward velocity after contact",
    "max_free_fall_height_error_m": "Maximum free-fall height error",
    "max_free_fall_velocity_error_m_s": "Maximum free-fall vertical velocity error",
    "final_com_height_m": "Final COM height",
    "final_linear_speed_m_s": "Final COM linear speed",
    "final_angular_speed_rad_s": "Final angular speed",
    "rigid_settled_time_s": "Rigid-body settling time",
    "rest_observation_duration_s": "Observation duration after settling",
    "settled_within_duration": "Rigid body settled within recorded duration",
    "settling_angular_speed_threshold_rad_s": "Settling angular speed threshold",
    "mean_tail_normal_force_n": "Mean normal contact force in final window",
    "tail_support_weight_ratio": "Final-window mean support force to weight ratio",
    "max_horizontal_displacement_m": "Maximum horizontal displacement",
    "total_contact_jz_ns": "Total contact impulse Z",
    "max_angle_error_rad": "Maximum angle error",
    "rms_angle_error_rad": "RMS angle error",
    "max_velocity_error_rad_s": "Maximum angular velocity error",
    "torque_impulse_nms": "Torque impulse",
}
UNIT_NAMES = {
    "s": ("秒", "second"),
    "ms": ("毫秒", "millisecond"),
    "步": ("步", "step"),
    "N": ("牛顿", "newton"),
    "m": ("米", "metre"),
    "mm": ("毫米", "millimetre"),
    "N·s": ("牛顿秒", "newton second"),
    "布尔": ("布尔值", "boolean"),
    "1": ("无量纲", "dimensionless"),
    "m/s": ("米每秒", "metre per second"),
    "m/s²": ("米每二次方秒", "metre per second squared"),
    "%": ("百分比", "percent"),
    "rad": ("弧度", "radian"),
    "rad/s": ("弧度每秒", "radian per second"),
    "N·m·s": ("牛顿米秒", "newton metre second"),
}
FIELD_LABELS = {
    "引擎": "引擎 / Engine",
    "场景": "场景 / Scene",
    "步长(ms)": "步长 / Timestep (ms)",
    "重复编号": "重复编号 / Repeat",
    "状态": "状态 / Status",
    "指标名称": "指标名称（中文） / Metric name (Chinese)",
    "Metric name": "指标名称（英文） / Metric name (English)",
    "指标字段": "指标字段 / Metric key",
    "单位": "单位符号 / Unit symbol",
    "数值": "数值 / Value",
    "记录次数": "记录次数 / Recorded runs",
    "通过次数": "通过次数 / Passed runs",
    "有效数值次数": "有效数值次数 / Valid values",
    "平均值": "平均值 / Mean",
    "标准差": "标准差 / Standard deviation",
    "最小值": "最小值 / Minimum",
    "最大值": "最大值 / Maximum",
}


def unit_description(unit):
    return " / ".join(UNIT_NAMES[unit])


def metric_title(key):
    name, unit = METRICS[key]
    symbol = "step" if unit == "步" else "boolean" if unit == "布尔" else unit
    return f"{name} / {METRIC_NAMES_EN[key]} ({symbol})"


def format_value(value):
    if value is None:
        return "未测得 / Not measured"
    if isinstance(value, bool):
        return "是 / Yes" if value else "否 / No"
    return f"{value:.9g}"


def export_csv(path, rows, fields):
    # UTF-8 BOM allows Chinese headers to open correctly in desktop Excel.
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def export_bilingual_csv(path, rows, fields):
    export_csv(
        path,
        [{FIELD_LABELS.get(k, k): v for k, v in row.items()} for row in rows],
        [FIELD_LABELS.get(k, k) for k in fields],
    )


def write_chinese_metrics(output, records, cfg):
    rows, groups = [], defaultdict(list)
    definitions = {}
    for run in records:
        base = {
            "引擎": ENGINE_NAMES[run["engine"]],
            "场景": SCENE_NAMES[run["scene"]],
            "步长(ms)": run["dt_s"] * 1000,
            "重复编号": run["repeat"] + 1,
            "状态": STATUS_NAMES[run["status"]],
        }
        groups[run["engine"], run["scene"], run["dt_s"]].append(run)
        for key, value in run.get("metrics", {}).items():
            if key == "scene":
                continue
            name, unit = METRICS[key]
            definitions[key] = {
                "名称": name,
                "name_en": METRIC_NAMES_EN[key],
                "单位": unit,
                "unit_name_zh": UNIT_NAMES[unit][0],
                "unit_name_en": UNIT_NAMES[unit][1],
            }
            rows.append(
                {
                    **base,
                    "指标名称": name,
                    "Metric name": METRIC_NAMES_EN[key],
                    "指标字段": key,
                    "单位": unit,
                    "单位说明 / Unit description": unit_description(unit),
                    "数值": value,
                    "数值显示 / Display value": format_value(value),
                }
            )
        if not run.get("metrics"):
            rows.append(
                {
                    **base,
                    "指标名称": "运行错误",
                    "Metric name": "Run error",
                    "数值": run.get("error", "无采样 / No samples"),
                }
            )
    fields = [
        "引擎",
        "场景",
        "步长(ms)",
        "重复编号",
        "状态",
        "指标名称",
        "Metric name",
        "指标字段",
        "单位",
        "单位说明 / Unit description",
        "数值",
        "数值显示 / Display value",
    ]
    export_csv(output / "metrics_zh.csv", rows, fields)
    export_bilingual_csv(output / "metrics_bilingual.csv", rows, fields)
    stats = []
    for (engine, scene, dt), runs in groups.items():
        passed = [r for r in runs if r["status"] == "passed"]
        keys = dict.fromkeys(k for r in runs for k in r.get("metrics", {}) if k != "scene")
        for key in keys:
            name, unit = METRICS[key]
            values = [
                r["metrics"][key]
                for r in passed
                if r["metrics"].get(key) is not None and not isinstance(r["metrics"][key], bool)
            ]
            stats.append(
                {
                    "引擎": ENGINE_NAMES[engine],
                    "场景": SCENE_NAMES[scene],
                    "步长(ms)": dt * 1000,
                    "记录次数": len(runs),
                    "通过次数": len(passed),
                    "有效数值次数": len(values),
                    "指标名称": name,
                    "Metric name": METRIC_NAMES_EN[key],
                    "指标字段": key,
                    "单位": unit,
                    "单位说明 / Unit description": unit_description(unit),
                    "平均值": float(np.mean(values)) if values else None,
                    "标准差": float(np.std(values)) if values else None,
                    "最小值": min(values) if values else None,
                    "最大值": max(values) if values else None,
                }
            )
    stats_fields = [
        "引擎",
        "场景",
        "步长(ms)",
        "记录次数",
        "通过次数",
        "有效数值次数",
        "指标名称",
        "Metric name",
        "指标字段",
        "单位",
        "单位说明 / Unit description",
        "平均值",
        "标准差",
        "最小值",
        "最大值",
    ]
    export_csv(output / "metric_stats_zh.csv", stats, stats_fields)
    export_bilingual_csv(output / "metric_stats_bilingual.csv", stats, stats_fields)
    (output / "metric_definitions.json").write_text(
        json.dumps(definitions, indent=2, ensure_ascii=False) + "\n"
    )
    lines = [
        "# 中英文指标明细 / Bilingual metric details",
        "",
        "全部重复与失败见 metrics_bilingual.csv；按引擎/步长的通过运行统计见 metric_stats_bilingual.csv。",
        "标准差为总体标准差（ddof=0），重复不加随机扰动，不用于估计置信区间。",
        "空值表示未测得 / Not measured；布尔值为是 / Yes、否 / No；无量纲 / dimensionless的单位为1。",
        "失败指标仅供诊断，不进入通过运行的统计。CSV数值列保留原始数值精度，显示列采用9位有效数字。",
        "完整名称与单位说明见 [指标字典 / Metric dictionary](metric_definitions.md)。",
        "",
        "| 引擎 / Engine | 场景 / Scene | 步长 / Timestep (ms) | 重复 / Repeat | 状态 / Status | 指标名称 / Metric name | 单位 / Unit | 数值 / Value |",
        "|---|---|---:|---:|---|---|---|---:|",
    ]
    for row in rows:
        if row["指标名称"] == "运行错误":
            continue
        lines.append(
            f"| {row['引擎']} | {row['场景']} | {row['步长(ms)']:g} | {row['重复编号']} | "
            f"{row['状态']} | {row['指标名称']} / {row['Metric name']} | "
            f"{row['单位']} ({unit_description(row['单位'])}) | {format_value(row['数值'])} |"
        )
    lines += ["", *slide_notes(cfg), ""]
    (output / "metrics_zh.md").write_text("\n".join(lines))
    (output / "metrics_bilingual.md").write_text("\n".join(lines))
    glossary = [
        "# 指标字典 / Metric dictionary",
        "",
        "| 指标字段 / Metric key | 中文名称 / Chinese name | 英文名称 / English name | 单位符号 / Unit symbol | 单位说明 / Unit description |",
        "|---|---|---|---|---|",
    ]
    glossary += [
        f"| {k} | {d['名称']} | {d['name_en']} | {d['单位']} | {unit_description(d['单位'])} |"
        for k, d in definitions.items()
    ]
    (output / "metric_definitions.md").write_text("\n".join(glossary) + "\n")


def slide_notes(cfg):
    return [
        (
            "滑动段测量窗口：首次接触之后排除启动阶段 "
            f"{cfg['impulse_window_s'] * 1000:g} ms；步初水平速度 > "
            f"{10 * cfg['stop_speed_m_s']:g} m/s。平均力与减速度包含离地步的零接触力。"
        ),
        (
            "实测等效摩擦系数 = Σ(水平接触力模长×dt) / Σ(法向力×dt)，"
            "系数仅使用窗口内法向力 > 1e-9 N 的接触步；无有效接触时为未测得。"
        ),
        (
            "理想参考为水平刚性平面上的纯平移库仑模型：a=μg，"
            "v=max(v₀−at,0)，x=v₀t−at²/2（停止后保持）；"
            "不含接触启动、转动或软接触，轨迹误差用于观察模型差异。"
        ),
        (
            "停止时间使用|vx|低于配置阈值且此后所有采样保持低于阈值的首个时刻；"
            "停止距离取该时刻X位移。所有指标仅覆盖已记录时长。"
        ),
    ]


def slide_report_lines(records, cfg):
    selected = [r for r in records if r["scene"] == "slide" and r["repeat"] == 0]
    if not selected:
        return []
    keys = [
        "effective_friction_coefficient",
        "mean_friction_force_n",
        "mean_deceleration_m_s2",
        "stop_time_s",
        "stop_distance_m",
        "stop_distance_error_percent",
        "max_displacement_error_m",
        "max_momentum_residual_ns",
    ]
    lines = [
        "",
        "## 滑动方块：摩擦与运动轨迹 / Sliding cube: friction and trajectory",
        "",
        (
            "表中为第一次重复 / First repeat；全部重复、中英文名称、单位与统计见 "
            "[中英文指标明细 / Bilingual details](metrics_bilingual.md)、"
            "[CSV](metrics_bilingual.csv)、[统计 / Statistics CSV](metric_stats_bilingual.csv)。"
        ),
        "",
        "| 引擎 / Engine | 步长 / Timestep (ms) | 状态 / Status | "
        + " | ".join(metric_title(k) for k in keys)
        + " |",
        "|---|---:|---|" + "---:|" * len(keys),
    ]
    for r in selected:
        lines.append(
            f"| {ENGINE_NAMES[r['engine']]} | {r['dt_s'] * 1000:g} | {STATUS_NAMES[r['status']]} | "
            + " | ".join(format_value(r.get("metrics", {}).get(k)) for k in keys)
            + " |"
        )
    return [*lines, "", *slide_notes(cfg), ""]


def drop_report_lines(records, cfg):
    selected = [r for r in records if r["scene"] == "drop" and r["repeat"] == 0]
    if not selected:
        return []
    lines = [
        "",
        "## 立方体下落、碰撞、静置 / Cube drop, impact and settling",
        "",
        (
            "首次重复 / First repeat；全部重复与统计见 [双语明细](metrics_bilingual.md)、"
            "[CSV](metrics_bilingual.csv)、[统计CSV](metric_stats_bilingual.csv)。"
        ),
    ]
    for title, keys in (
        (
            "碰撞响应 / Impact response",
            [
                "first_contact_s",
                "first_contact_time_error_s",
                "preimpact_vertical_velocity_m_s",
                "peak_rebound_vertical_velocity_m_s",
                "peak_contact_fz_n",
                "max_penetration_m",
                "max_momentum_residual_ns",
            ],
        ),
        (
            "静置状态 / Settling state",
            [
                "rigid_settled_time_s",
                "rest_observation_duration_s",
                "settled_within_duration",
                "final_com_height_m",
                "final_linear_speed_m_s",
                "final_angular_speed_rad_s",
                "tail_support_weight_ratio",
            ],
        ),
    ):
        lines += [
            "",
            f"### {title}",
            "",
            "| 引擎 / Engine | 步长 / Timestep (ms) | 状态 / Status | "
            + " | ".join(metric_title(k) for k in keys)
            + " |",
            "|---|---:|---|" + "---:|" * len(keys),
        ]
        for run in selected:
            lines.append(
                f"| {ENGINE_NAMES[run['engine']]} | {run['dt_s'] * 1000:g} | "
                f"{STATUS_NAMES[run['status']]} | "
                + " | ".join(format_value(run.get("metrics", {}).get(k)) for k in keys)
                + " |"
            )
    return [
        *lines,
        "",
        (
            "理想自由落体 / Ideal free fall：质心初始高度 h₀、初速度0，"
            "z=h₀−gt²/2、vz=−gt；平放立方体首次接触参考 t=√(2(h₀−边长/2)/g)。"
            "参考只对无接触段比较；积分离散误差与接触偏置会影响首次接触时间。"
        ),
        (
            "首次接触用原生接触合力>1e-9 N的首个步初时间，碰撞前速度取该步初vz；"
            "最大向上速度取首次接触后所有已记录状态，不推算材料恢复系数。"
        ),
        (
            f"刚体静置 / Rigid-body settling：质心线速度<{cfg['stop_speed_m_s']:g} m/s，"
            "角速度×立方体半对角线也低于该阈值，且前一步法向支撑力>1e-9 N，"
            "要求此后所有已记录状态持续满足。原质心静置时间仅检查线速度，继续保留。"
        ),
        (
            f"末段支撑力为最后{cfg['impulse_window_s'] * 1000:g} ms法向力的时间平均，"
            "该窗口须全部位于首次接触后；支撑力/重力比约为1表示平均支撑重力。"
        ),
        (
            "通过 / Passed表示参数、有限性和动量校验通过；是否已静置另列布尔指标。"
            "静置结论只覆盖记录时长，静置后观察时长另行保存；未测得不填零。"
        ),
        "",
    ]
