# MuJoCo CPU 环境部署

本项目的 CPU 基线使用 MuJoCo 3.15.0、float64、Euler 积分和 Newton 求解器。无需 GPU、Isaac Lab 或 Docker。以下命令在仓库根目录执行。

## 安装与检查

需要 Linux、Python 3.11 和 uv。依赖按仓库 `uv.lock` 安装到 `.venv`；不要安装到已有 Conda 环境。

```bash
uv sync --locked --python 3.11
.venv/bin/python -c 'import mujoco; print(mujoco.__version__)'
.venv/bin/physics-bench doctor
```

`doctor` 记录 GPU 检查失败不会影响 CPU 实验。本文命令只进行无窗口计算。

## 运行

```bash
# 三个基础场景、两个步长、三次重复；自动创建新的结果目录
.venv/bin/physics-bench run --engine mujoco-cpu

# 完整扩展刚体矩阵；显式目录必须不存在
.venv/bin/physics-bench extended rigid --engine mujoco --output results/my-cpu-rigid
.venv/bin/physics-bench extended soft --engine mujoco --output results/my-cpu-soft
.venv/bin/physics-bench extended tuning --engine mujoco --output results/my-cpu-tuning
.venv/bin/physics-bench extended throughput --engine mujoco --output results/my-cpu-throughput
```

基础入口的引擎名为 `mujoco-cpu`，扩展入口为 `mujoco`。软体细网格和很小的步长计算成本较高。

## 验证与结果

```bash
.venv/bin/pytest -q
.venv/bin/ruff check src tests scripts
```

基础实验查看 `report.md`、`runs.json` 和原始 CSV；扩展实验查看 `result.json`、`trajectory.npz`、导入审计和失败记录。任务成功、数值完成及接触力校验是独立字段。

CPU 可运行不代表 GPU 环境可运行。原文使用 MuJoCo 3.11.0，本项目主 CPU 环境为 3.15.0，不能声称精确复现原文数值。完整实验参数、冻结资产和控制器约定见 [完整实验说明](full-experiments.md)。
