# 继续剩余物理引擎

## 任务
.talisman/dev_docs/2026-10/task01_我做这个实验对比.md 只完成了一部分，剩余的物理引擎测试。

## 2026-10-08 实施与验收

已完成 MuJoCo-Warp、Genesis、Isaac Sim/PhysX 接入和真实运行。
每个引擎运行滑块停止、方块下落、单铰链摆动，两个步长、三次独立重复，各 18/18 组通过。
加上重新运行的 MuJoCo CPU 基线，共 72/72 组、64,800 个物理步；22 项测试和 Ruff 检查通过。

- 四引擎对比报告：`results/task02-comparison/report.md`。
- 可复查数字、重复性及失败记录：`docs/validation-task02.md`。
- 安装、命令和实现差异：`docs/multi-engine.md`。
- 各引擎结果：`results/task02-cpu/`、`results/task02-warp-validated/`、`results/task02-genesis/`、`results/task02-physx/`。

按用户选择，PhysX 使用已有 Isaac Sim 6.0.1 镜像的 CPU TGS，没有改用独立原生 PhysX。
Warp 使用直接 MuJoCo-Warp CUDA；Genesis 1.4.3 使用 CUDA float64，PyTorch 固定 2.8.0。
物理参数回读、原生接触力/冲量和逐步动量校验均通过；PhysX 法向及摩擦冲量分别保留。
试跑中的初始化、摩擦测量和 PyTorch 兼容性失败均保留，最终结果来自修复后的完整实验。

1 ms 下落峰值合力：MuJoCo CPU 约 53.441 N、Warp 约 53.441 N、Genesis 约 53.441 N、PhysX 约 255.058 N。
必须结合 40 ms 冲量、步长和软/硬接触模型解释，不能据此单独作准确性排名。
CPU、Genesis、PhysX 三次重复逐列一致；Warp 滑块存在微小浮点差异，未隐藏。

仍未覆盖 Panda、软体和 GPU 吞吐；不是作者完整配置的精确复现。此次任务没有修改原 Conda 环境或系统驱动。

## 2026-10-09 扩展补跑进度（非最终验收）

已实现 Panda、复杂接触、五条软体路径、调参与吞吐矩阵。修复 PhysX 失效连接复用及插销控制器漂移；53 项测试、Ruff和CPU基础18组回归通过。CPU/Warp新刚体矩阵各111组记录，各78组任务成功，其中插销各30组、24组成功。

其余扩展矩阵在 `results/full-recovery-20261009/` 续跑，由用户级服务 `physics-bench-recovery-20261009.service` 托管。Genesis改用隔离1.4.1 / Quadrants1.3.0，全部重新运行；旧兼容观测保留provenance复用，不计作新独立重复。软体、迁移、吞吐及最终报告仍需完成，详见 `docs/validation-2026-10-09.md`。
