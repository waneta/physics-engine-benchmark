"""Headless scientific plots of raw, unsmoothed samples."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .metrics import column, states


def plot_scene(scene: str, runs: list[dict], output: Path, include_net_force=True):
    if scene == "slide":
        return plot_slide(runs, output)
    if scene == "drop":
        return plot_drop(runs, output, include_net_force)
    fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
    axes = axes.ravel()
    colors = {
        "mujoco-cpu": "#2878b5",
        "mujoco-warp": "#df7a18",
        "genesis": "#33945e",
        "physx": "#aa4b99",
    }
    largest_dt = max((r["dt_s"] for r in runs), default=0)
    reference_plotted = False
    for run in runs:
        if run["repeat"] != 0 or run["status"] != "passed":
            continue
        rows = run["rows"]
        t = np.r_[0, column(rows, "t_end_s")]
        tf = column(rows, "t_start_s")
        label = f"{run.get('engine', 'mujoco-cpu')} {run['dt_s'] * 1000:g} ms"
        style = {
            "color": colors[run.get("engine", "mujoco-cpu")],
            "linestyle": "-" if run["dt_s"] == largest_dt else "--",
        }
        if scene == "hinge":
            theta = states(rows, "qpos0")
            ref = np.r_[
                rows[0]["reference_angle_start_rad"], column(rows, "reference_angle_end_rad")
            ]
            axes[0].plot(t, theta, label=label, **style)
            if not reference_plotted:
                axes[0].plot(t, ref, "k:", alpha=0.8, linewidth=1, label="ODE reference")
                reference_plotted = True
            axes[1].plot(t, states(rows, "qvel0"), label=label, **style)
            axes[2].plot(t, (theta - ref) * 180 / np.pi, label=label, **style)
            axes[3].step(tf, column(rows, "applied_torque_nm"), where="post", label=label, **style)
            titles = [
                "Angle (rad); dotted = independent ODE",
                "Angular velocity (rad/s)",
                "Angle error vs ODE (deg)",
                "Applied torque (N m)",
            ]
        else:
            axes[0].plot(
                t,
                states(rows, "qpos0" if scene == "slide" else "qpos2") * 1000,
                label=label,
                **style,
            )
            axes[1].plot(
                t, states(rows, "qvel0" if scene == "slide" else "qvel2"), label=label, **style
            )
            axes[2].step(
                tf, column(rows, "contact_force_norm_n"), where="post", label=label, **style
            )
            if scene == "drop" and include_net_force:
                axes[2].step(
                    tf,
                    column(rows, "net_fz_n"),
                    where="post",
                    linestyle=":",
                    color=style["color"],
                    alpha=0.6,
                    label=label + " net z",
                )
            axes[3].plot(
                t,
                states(rows, "qpos2") * 1000
                if scene == "slide"
                else np.r_[rows[0]["penetration_start_m"], column(rows, "penetration_end_m")]
                * 1000,
                label=label,
                **style,
            )
            titles = [
                "Displacement x (mm)" if scene == "slide" else "COM height (mm)",
                "Velocity x (m/s)" if scene == "slide" else "Velocity z (m/s)",
                "Contact / net force (N)"
                if scene == "drop" and include_net_force
                else "Contact resultant (N)",
                "COM height (mm)" if scene == "slide" else "Lowest-vertex penetration (mm)",
            ]
        for ax, title in zip(axes, titles):
            ax.set_title(title)
    for ax in axes:
        ax.set_xlabel("Time (s)")
        ax.grid(alpha=0.25)
        if ax.lines:
            ax.legend(fontsize=8)
    fig.suptitle(f"{scene} — first repeat, raw samples")
    fig.savefig(output / f"{scene}.png", dpi=160)
    plt.close(fig)


def plot_slide(runs, output):
    from matplotlib import font_manager

    chinese_font = next(
        (f.name for f in font_manager.fontManager.ttflist if "Noto Sans CJK" in f.name), None
    )
    with plt.rc_context(
        {"font.family": chinese_font or "DejaVu Sans", "axes.unicode_minus": False}
    ):
        fig, axes = plt.subplots(2, 3, figsize=(16, 8), constrained_layout=True)
        axes = axes.ravel()
        colors = {
            "mujoco-cpu": "#2878b5",
            "mujoco-warp": "#df7a18",
            "genesis": "#33945e",
            "physx": "#aa4b99",
        }
        largest_dt = max((r["dt_s"] for r in runs), default=0)
        reference_plotted = False
        for run in runs:
            if run["repeat"] != 0 or run["status"] != "passed":
                continue
            rows = run["rows"]
            t = np.r_[0, column(rows, "t_end_s")]
            tf = column(rows, "t_start_s")
            engine = run.get("engine", "mujoco-cpu")
            label = f"{engine} {run['dt_s'] * 1000:g} ms"
            style = {
                "color": colors[engine],
                "linestyle": "-" if run["dt_s"] == largest_dt else "--",
            }
            x = states(rows, "qpos0") - rows[0]["qpos0_start"]
            y = states(rows, "qpos1") - rows[0]["qpos1_start"]
            axes[0].plot(t, x * 1000, label=label, **style)
            axes[1].plot(t, states(rows, "qvel0"), label=label, **style)
            tangent = np.hypot(column(rows, "contact_fx_n"), column(rows, "contact_fy_n"))
            normal = column(rows, "contact_fz_n")
            axes[2].step(tf, tangent, where="post", label=label + " Ft", **style)
            axes[2].step(
                tf,
                normal,
                where="post",
                label=label + " Fn",
                color=colors[engine],
                linestyle=":",
                alpha=0.7,
            )
            axes[3].plot(t, states(rows, "qpos2") * 1000, label=label, **style)
            if "friction_metric_sample" in rows[0]:
                mask = column(rows, "friction_metric_sample").astype(bool) & (normal > 1e-9)
                ratio = np.where(mask, column(rows, "effective_friction_coefficient"), np.nan)
                axes[4].plot(tf, ratio, label=label, **style)
            axes[5].plot(x * 1000, y * 1000, label=label, **style)
            if not reference_plotted and "reference_displacement_end_m" in rows[0]:
                axes[0].plot(
                    t,
                    np.r_[0, column(rows, "reference_displacement_end_m")] * 1000,
                    "k:",
                    label="理想库仑 / Ideal Coulomb",
                )
                axes[1].plot(
                    t,
                    np.r_[rows[0]["qvel0_start"], column(rows, "reference_velocity_end_m_s")],
                    "k:",
                    label="理想库仑 / Ideal Coulomb",
                )
                reference_plotted = True
        titles = [
            "X位移 / X displacement (mm)",
            "X速度 / X velocity (m/s)",
            "摩擦力 Ft / 法向力 Fn (N)\nFriction force / Normal force",
            "质心高度 / COM height (mm)",
            "滑动段实测摩擦系数\nMeasured friction coefficient (无量纲 / dimensionless)",
            "俯视运动轨迹 / Top-view trajectory (mm)",
        ]
        for i, (ax, title) in enumerate(zip(axes, titles)):
            ax.set_title(title, fontsize=11)
            ax.set_xlabel("X位移 / X displacement (mm)" if i == 5 else "时间 / Time (s)")
            ax.grid(alpha=0.25)
            if ax.lines:
                ax.legend(fontsize=7, loc="upper right" if i == 2 else "best")
        axes[5].set_ylabel("Y位移 / Y displacement (mm)")
        axes[5].set_aspect("equal", adjustable="datalim")
        fig.suptitle(
            "滑动方块 / Sliding cube：首次重复 / First repeat；实线/虚线区分步长 / Line styles distinguish timesteps"
        )
        fig.savefig(output / "slide.png", dpi=160)
        plt.close(fig)


def plot_drop(runs, output, include_net_force=True):
    from matplotlib import font_manager

    chinese_font = next(
        (f.name for f in font_manager.fontManager.ttflist if "Noto Sans CJK" in f.name), None
    )
    with plt.rc_context(
        {"font.family": chinese_font or "DejaVu Sans", "axes.unicode_minus": False}
    ):
        fig, axes = plt.subplots(2, 3, figsize=(16, 8), constrained_layout=True)
        axes = axes.ravel()
        colors = {
            "mujoco-cpu": "#2878b5",
            "mujoco-warp": "#df7a18",
            "genesis": "#33945e",
            "physx": "#aa4b99",
        }
        largest_dt = max((r["dt_s"] for r in runs), default=0)
        reference_plotted = False
        for run in runs:
            if run["repeat"] != 0 or run["status"] != "passed":
                continue
            rows = run["rows"]
            t = np.r_[0, column(rows, "t_end_s")]
            tf = column(rows, "t_start_s")
            engine = run.get("engine", "mujoco-cpu")
            label = f"{engine} {run['dt_s'] * 1000:g} ms"
            style = {
                "color": colors[engine],
                "linestyle": "-" if run["dt_s"] == largest_dt else "--",
            }
            axes[0].plot(t, states(rows, "qpos2") * 1000, label=label, **style)
            axes[1].plot(t, states(rows, "qvel2"), label=label, **style)
            axes[2].step(tf, column(rows, "contact_fz_n"), where="post", label=label, **style)
            if include_net_force:
                axes[2].step(
                    tf,
                    column(rows, "net_fz_n"),
                    where="post",
                    color=colors[engine],
                    linestyle=":",
                    alpha=0.6,
                    label=label + " net z",
                )
            penetration = np.r_[rows[0]["penetration_start_m"], column(rows, "penetration_end_m")]
            axes[3].plot(t, penetration * 1000, label=label, **style)
            speed = np.linalg.norm(
                np.column_stack([states(rows, f"qvel{i}") for i in range(3)]), axis=1
            )
            angular = np.linalg.norm(
                np.column_stack([states(rows, f"qvel{i}") for i in range(3, 6)]), axis=1
            )
            axes[4].plot(t, speed, label=label, **style)
            axes[5].plot(t, angular, label=label, **style)
            if not reference_plotted and "free_fall_sample" in rows[0]:
                mask = np.r_[True, column(rows, "free_fall_sample").astype(bool)]
                reference_height = np.r_[
                    rows[0]["qpos2_start"], column(rows, "free_fall_reference_height_end_m")
                ]
                reference_velocity = np.r_[0, column(rows, "free_fall_reference_velocity_end_m_s")]
                axes[0].plot(
                    t[mask], reference_height[mask] * 1000, "k:", label="自由落体 / Free fall"
                )
                axes[1].plot(t[mask], reference_velocity[mask], "k:", label="自由落体 / Free fall")
                reference_plotted = True
        titles = [
            "质心高度 / COM height (mm)",
            "竖直速度 / Vertical velocity (m/s)",
            "法向接触力 / Normal contact force (N)",
            "最低顶点穿透 / Lowest-vertex penetration (mm)",
            "质心线速度模长 / COM linear speed (m/s)",
            "角速度模长 / Angular speed (rad/s)",
        ]
        for i, (ax, title) in enumerate(zip(axes, titles)):
            ax.set_title(title, fontsize=11)
            ax.set_xlabel("时间 / Time (s)")
            ax.grid(alpha=0.25)
            if ax.lines:
                ax.legend(fontsize=7, loc="upper right" if i in (2, 3) else "best")
        fig.suptitle(
            "立方体下落、碰撞、静置 / Cube drop, impact and settling：首次重复 / First repeat"
        )
        fig.savefig(output / "drop.png", dpi=160)
        plt.close(fig)
