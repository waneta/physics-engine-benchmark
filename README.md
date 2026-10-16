# Physics Engine Benchmark

从三个基础刚体场景开始，建立可复查的机器人仿真物理引擎对比实验。
支持 **MuJoCo CPU、MuJoCo-Warp CUDA、Genesis CUDA、Isaac Sim/PhysX CPU TGS**，
统一测试滑块停止、方块下落、单铰链摆动。
每个引擎默认执行 3 个场景 × 2 种步长 × 3 次独立重复，共 18 组。

多引擎安装、版本及测量差异见 [使用说明](docs/multi-engine.md)，
实测结果见 [task02 验收记录](docs/validation-task02.md)。

独立部署文档：[MuJoCo CPU](docs/deploy-mujoco.md)、[MuJoCo-Warp](docs/deploy-mujoco-warp.md)、[Genesis](docs/deploy-genesis.md)、[Isaac Sim/PhysX](docs/deploy-physx.md)。

task04 滑动方块的四引擎**有界面/无界面命令、中英文摩擦与轨迹指标**见
[单物体滑块使用说明](docs/single-slide.md)，实测对比见 [task04 验收记录](docs/validation-task04.md)。

立方体下落、碰撞、静置的四引擎**有界面/无界面命令、中英文碰撞与静置指标**见
[单物体下落使用说明](docs/single-drop.md)，实测结果见 [下落实验验收](docs/validation-task04-drop.md)。

```bash
uv sync --locked --python 3.11
uv run --locked physics-bench doctor
uv run --locked physics-bench run
```

`run` 默认使用 MuJoCo CPU。已安装可选环境后，可分别执行：

```bash
.venv-warp/bin/physics-bench run --engine mujoco-warp
.venv-genesis/bin/physics-bench run --engine genesis
.venv/bin/physics-bench run --engine physx
```

PhysX 复用本地 Isaac Sim 6.0.1 Docker 镜像。各结果目录可用
`physics-bench compare DIR1 DIR2 ... --output 新目录` 生成叠加曲线和比较表。

默认是无窗口批量计算；加 `--viewer` 可用三维窗口实时显示所选引擎的测量状态，例如
`.venv/bin/physics-bench run --engine mujoco-cpu --scene slide --viewer --repeats 1`。
按 Ctrl+C 或关闭正在计算的窗口可中止实验，
已采集数据会保存，当前实验标记为 `interrupted`，并输出部分报告（退出码 130）。

输出目录自动创建在 `results/<UTC时间>-<唯一编号>/`，运行结束打印报告路径。
打开 `report.md` 查看指标和曲线，`summary.csv` 查看全部成功运行指标，
`runs.json` 查看成功及失败记录。修改 [configs/baseline.json](configs/baseline.json)
可以调整参数；输出会保存所用配置、MJCF、导入参数、软件与硬件信息。

```bash
# 只跑下落实验；显式路径必须尚不存在，防止覆盖旧数据
uv run --locked physics-bench run --scene drop --repeats 3 --output results/drop-check

# 验证
uv run --locked pytest -q
uv run --locked ruff check src tests scripts
```

实验参数的来源、力采样语义和文件格式见
[实验说明](docs/benchmark.md)。本实现包含明确标记的自选参数，
**不是原文数值的精确复现**。直接 MuJoCo-Warp 与原文 Newton 包装路径有差异；
机械臂、软体和 GPU 吞吐的覆盖及验收状态以扩展实验实测报告为准；基础命令的运行时间不用于性能排名。

## 完整扩展实验

机械臂、复杂接触、五条软体路径、控制器调参与 GPU 吞吐见 [完整实验说明](docs/full-experiments.md)。

```bash
.venv/bin/physics-bench extended rigid --engine mujoco --output results/my-panda-tests
.venv/bin/python scripts/run_full_experiments.py --output results/my-full-suite
```

统一运行器冻结源码，保存逐次结果，并支持 `--resume`。基础刚体命令仍为 `physics-bench run`。

2026-10-09 的故障修复、剩余范围与补跑入口见 [续跑验证记录](docs/validation-2026-10-09.md)。当前完整补跑保存在 `results/full-recovery-20261009/`，尚未验收完毕。
