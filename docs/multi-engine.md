# 多引擎实验

三个场景沿用 [baseline.json](../configs/baseline.json)：滑块停止、方块下落、带力矩脉冲的单铰链摆动。
每个引擎默认运行 3 个场景 × 2 个步长 × 3 次独立重复，共 18 组。
这是基础刚体实验；未实施 Panda、软体或吞吐量测试，不宣称精确复现转载原文。

## 环境与运行

不同引擎使用不同 Python 环境。以下安装命令在仓库根目录执行；CPU 环境沿用 uv.lock。
可选引擎的 requirements/*.lock 固定本次 Linux x86_64 / Python 3.11 的依赖版本。
Genesis 与 PyTorch 的 CUDA 依赖较大，需要数 GB 下载和额外磁盘空间。

```bash
uv sync --locked --python 3.11

uv venv --python 3.11 .venv-warp
uv pip install --python .venv-warp/bin/python -r requirements/warp.lock

uv venv --python 3.11 .venv-genesis
uv pip install --python .venv-genesis/bin/python -r requirements/genesis.lock

.venv/bin/physics-bench run --engine mujoco-cpu
.venv-warp/bin/physics-bench run --engine mujoco-warp
.venv-genesis/bin/physics-bench run --engine genesis
.venv/bin/physics-bench run --engine physx
```

本机 Genesis 环境最初复用了 `env_IsaacLaunch` 的 Python 3.11 与系统包，
新增或升级依赖均安装在项目 `.venv-genesis`，没有改写原 Conda 环境。
复跑建议使用上面的独立环境命令；锁文件只包含所需依赖的闭包，不包含原 Conda 中无关的 IsaacLab/RL 包。
各次运行的 environment.json 保存实际可见的全部包版本。

PhysX 使用本地 `nvcr.io/nvidia/isaac-sim:6.0.1` 镜像，需要 Docker 和 NVIDIA Container Toolkit。
适配器使用 `--pull=never`，不会隐式下载镜像；仓库只读挂载到容器，结果由宿主进程写入。
没有安装 IsaacLab，因为三个基础场景只需要 Isaac Sim 自带的 PhysX 与 USD API。

```bash
docker image inspect nvcr.io/nvidia/isaac-sim:6.0.1
# 有其他已验证镜像时可覆盖；不同版本的 API 未保证兼容
PHYSICS_BENCH_ISAAC_IMAGE=nvcr.io/nvidia/isaac-sim:6.0.1 \
  .venv/bin/physics-bench run --engine physx
```

本次镜像 ID 为 `sha256:783444c706538aa76cf5126e911ddc5e618779e6105305ad4af4260362a30aa9`；
镜像内 VERSION 为 `6.0.1-rc.7+release.42383.32955d8d.gl`。
实际 image ID、容器版本和执行路径同时记录到每组 imported.json。

## 实现差异

| 引擎 | 实测路径 | 数值精度 | 接触测量 |
|---|---|---|---|
| MuJoCo CPU 3.15.0 | CPU Euler / Newton / 椭圆摩擦锥 | float64 | mj_contactForce 转世界坐标 |
| MuJoCo-Warp 3.15.0、Warp 1.16.0 | CUDA，直接调用 MuJoCo-Warp | float32 | contact_force(world frame) |
| Genesis 1.4.3 | CUDA Euler / Newton / 椭圆摩擦锥 | float64 | get_contacts 中目标 link 的 force_a / force_b |
| PhysX / Isaac Sim 6.0.1 | CPU TGS，100 次位置迭代、1 次速度迭代 | float32 | 接触事件法向冲量 + tensor friction impulse |

Warp 1.16 支持本机 570 驱动；不可随意升级到要求 CUDA 13 驱动的 Warp 版本。
Genesis 的接触接口要求 PyTorch 2.8；2.7 的 gather 索引类型错误已在试跑中暴露，因此锁定 2.8.0。
Genesis 导入器可能添加默认 armature，适配器显式置零并回读；没有以默认值代替配置。

PhysX 在带 GPU 的 Isaac Sim 容器中启动，但刚体求解明确使用 CPU TGS。
硬接触采用 contact offset 1 mm、rest offset 0、恢复系数 0、静/动摩擦系数 0.4；关闭睡眠、阻尼和稳定化。
这些参数不等价于 MuJoCo/Genesis 的 solref、solimp，因而不同峰值力和穿透不能直接判定谁更准确。
PhysX 接触报告仅给出法向冲量，必须另取摩擦冲量；缺失摩擦时会被动量校验拒绝。

所有适配器均回读质量、惯量、质心、初始状态和关键接触/关节参数。
自由体的接触总力为世界坐标合力，包含摩擦；数据没有由速度差反推接触力。
逐步检查 `m*(v_end-v_start) - J_contact - m*g*dt`，默认容差为 `5e-6 N s`。
铰链用独立非线性 ODE 的 RK4 解计算角误差；力矩脉冲严格按步边界施加。

## 输出与对比

每次运行创建新目录，拒绝覆盖既有结果。每组保存 raw.csv、metrics.json、imported.json 和统一场景的 scene.xml；
PhysX 额外保存实际创建的 scene.usda，XML 仅作共同场景参考，并非容器直接加载的模型。
容器诊断日志保存在 `.cache/logs/physics-bench-*.log`。

```bash
.venv/bin/physics-bench compare \
  results/task02-cpu results/task02-warp-validated \
  results/task02-genesis results/task02-physx \
  --output results/task02-comparison
```

compare 要求各输入 config.json 完全一致，拒绝重复引擎；保留失败指标与错误。
各引擎覆盖不一致或存在失败时返回 1，并在报告标明不完整。
表格和曲线采用每组第一次重复，全部重复见 summary.csv；重复性见各引擎 repeatability.json。
曲线未经平滑，同色表示同一引擎，实线/虚线表示两个步长。
40 ms 冲量从各自首次非零接触力开始积分，包含接触力，不包含重力。

当前逐步 GPU 回读、Python、JSON 通信与文件导出开销均存在，不使用这些运行时间给引擎作性能排名。
Ctrl+C 会保存已收到的原始采样与部分报告；PhysX 会关闭本次创建的容器，不影响其他容器。

## 验证

```bash
.venv/bin/pytest -q
.venv/bin/ruff check src tests scripts
```

实际实验结果、失败修复记录和观察结论见 [task02 验收记录](validation-task02.md)。

接口依据官方安装包源码，并对照 [MuJoCo-Warp API](https://mujoco.readthedocs.io/en/stable/mjwarp/api.html)、
[Genesis 安装说明](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/installation.html)
及镜像内 `omni.physics.tensors`、`isaacsim.core` API。
