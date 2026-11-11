"""Headless scientific plots of raw, unsmoothed samples."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .metrics import column, states


def plot_scene(scene: str, runs: list[dict], output: Path, include_net_force=True):
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
