# 完整扩展实验

基础滑块、落体和铰链之外，本项目现提供碰撞链、Panda 开环/跟踪、抓放、堆叠、通道推物、密集扫掠、插销装配、软体、控制器调参及 GPU 吞吐的原生求解器实现。实验是否成功以实际结果文件为准；命令存在、进程退出和数值有效分别检查。

## 运行入口

沿用已有环境，单独运行一个引擎：

```bash
.venv/bin/physics-bench extended rigid --engine mujoco --output results/my-rigid-cpu
.venv-warp/bin/python -m physics_benchmark.extended.suite rigid --engine mujoco-warp --output results/my-rigid-warp
.venv-genesis/bin/python -m physics_benchmark.extended.suite rigid --engine genesis --output results/my-rigid-genesis
.venv/bin/physics-bench extended rigid --engine physx --output results/my-rigid-physx
```

`--family grasp` 等参数可以筛选场景；`--case-index 0` 选择筛选后矩阵的一个配置；`--plan-only` 查看计划。现有基础命令 `physics-bench run` 保留。

完成所有矩阵的统一入口：

```bash
.venv/bin/python scripts/run_full_experiments.py --output results/my-full-suite
# 同一个输出目录恢复。使用首次运行冻结的源码，保留已完成结果和中断目录。
.venv/bin/python scripts/run_full_experiments.py --output results/my-full-suite --resume
```

运行器先复制源码和资产到输出目录的 `source/`，各子进程通过 `PYTHONPATH` 使用该快照。刚体和调参允许不同引擎并行；软体 GPU 路径依次运行；全部准确性实验结束后，吞吐独占本运行器的 GPU 任务队列。外部程序仍可能占用 GPU，性能测试时应保持相同负载条件。`status.json`、`logs/` 和每次试验的 `progress.json` 可用于查看进度。

输出路径必须是新目录。`--resume` 要求相同配置和源码摘要；不完整的刚体/软体试验写入新的 `attempt-*`，不会覆盖原始记录。明确记录为 `error` 的试验不会自动重试。修改代码后应创建新批次。

## 实验矩阵

| 类别 | 每个引擎的配置 | 原生路径 |
|---|---|---|
| 碰撞链 | 球、立方体、三棱柱；1/0.5 ms，各重复 3 次 | MuJoCo CPU、直接 MuJoCo-Warp、Genesis、Isaac PhysX CPU TGS |
| Panda 开环 | 0.5 s，共同初始偏置力矩及两次关节脉冲；两种步长、3 次重复 | 同上 |
| Panda 跟踪 | 2.5 s 七关节五次曲线；两种步长、3 次重复 | 同上 |
| 抓放 | 40 mm、100 g 方块，居中/偏置 8 mm；3 次重复 | 同上 |
| 堆叠 | 放置偏置 0/16/20/22 mm，加两种边缘扰动；3 次重复 | 同上 |
| 通道推物 | 3 方块，80/90 mm 通道，后方方块偏移 0/±1 mm；两种步长、3 次重复 | 同上 |
| 密集扫掠 | 220 mm 挡板、15 物体、45° 导向件、15 mm 下坡与托盘；12.5 s、3 次重复 | 同上 |
| 插销装配 | 64 面销与倒角孔；径向间隙 0.1/0.25/0.5 mm，居中/偏移/倾斜，3 次重复；困难配置增加接触引导 | 同上 |
| 软体 | 压缩重复/半步长、1/1.1/1.5/2 N 抓取、2 N 网格与步长敏感性 | CPU flex、直接 Warp flex、Genesis FEM/SAP、PhysX GPU TetMesh、Newton MJWarp/VBD |
| 调参和预留验证 | 27 候选 × 3 训练布局，基线/选中控制器 × 6 预留布局 | 四个刚体引擎 |
| 固定控制器速度扫描 | 0.75/1/1.5/2/3 s × 3 布局 | 四个刚体引擎 |
| 吞吐 | CPU 1 环境；Warp/Genesis 1/128/8192/32768/131072 环境；预热后 3 次计时 | CPU、CUDA；不把 PhysX 的跨容器诊断时间加入 GPU 吞吐排名 |

完整计划为每个刚体引擎 111 次，每个调参引擎 108 次（包括速度扫描和预留验证），每条软体路径 12 次，Genesis 另加 1 次独立收敛/力诊断，吞吐 11 个规模。GPU 大规模配置若出现显存不足，会保留异常，不把缺失数据替换为估计速度。

## 资产与控制一致性

Panda 来自 [MuJoCo Menagerie 固定版本](https://github.com/google-deepmind/mujoco_menagerie/tree/822c2d8f877dd166c5b7d3c9f7e3c3b6589473b7/franka_emika_panda)，源文件、Apache-2.0 许可证、下载地址和 SHA256 在 `configs/assets/panda/`。保留 11 个刚体的质量、质心和完整惯量。为隔离实验，只保留解析指垫和试验附件的碰撞体。

全部控制轨迹及无载前馈由 MuJoCo 3.15.0 生成并缓存为同一份数据。Newton 运行环境使用 3.11 时也读取 3.15 的冻结轨迹。每次记录保存参考数据及摘要；生成前馈时禁用物体接触与限位反力，避免把某个引擎的抓取接触载荷写入公共控制器。

控制频率固定 1 kHz；0.5 ms 物理步保持两步同一指令。原生位置驱动、关节阻尼、摩擦损耗和 armature 关闭，使用共同 PD 参数、前馈和力矩上限。手指为两个独立关节，不用焊接、传送或隐藏约束完成抓取。插销使用有界笛卡尔阻抗；引导修正由接触力/力矩产生，不读取孔中心来决定修正方向。

刚体导入检查包含质量、质心、惯量和五组原生 FK；位置容差 10 µm、旋转矩阵 Frobenius 容差 1e-4、关节坐标容差 1e-5。逐步保存原生关节坐标与刚体位姿，再用规范模型复核 FK。自由物体使用原生接触力与动量变化交叉核算，冲量残差阈值 5e-6 N·s。

## 软体约定

球半径 30 mm、密度 1000 kg/m³、E=20 kPa、ν=0.3、摩擦系数 0.5。共享粗网格 125 顶点/384 四面体；边中点细化后 729/3072。细化不重新投影为更圆的球，两个网格体积和质量相同，质量约 0.1050491235 kg。节点质量按四面体体积分摊。

CPU/Warp 默认 50 µs，PhysX/Genesis 1 ms，Newton VBD 0.5 ms。2 N 灵敏度配置为粗网格原步长、半步长、四分之一步长，细网格半步长、四分之一步长。每个物理步检查非有限节点和单元有向体积，首次翻转即停止；记录失败帧及前面的有效数据，不补齐轨迹。5 ms 保存几何，保留顶点均值和体积质量加权质心，完整覆盖 1.9–2.2 s 才报告保持期抬升。

Genesis 使用 float64 隐式线性共旋 FEM 和原文主实验的 5 次 SAP 迭代；50 次迭代仅用于单独的压缩收敛/力诊断。当前版本没有公开四面体数组 morph，本项目通过局部、构造期间生效的 `FEMEntity.sample` 注入共享网格，随后读取完整节点/单元进行校验，隐式 FEM 的 Newton 迭代固定为 10，PCG 为 100，Rayleigh 阻尼固定为零并记录为与作者默认阻尼的差异；没有修改已安装引擎文件。与原文的 Genesis 内部重网格路径有差异。

PhysX 软体使用 Isaac Sim GPU tensor pipeline，原生 TetMesh，检查节点置换和单元连通性；刚体实验仍用 CPU TGS。该版本的 GPU kinematic-target setter 未实现，因此压缩使用规定的压板位姿更新。原生刚体 contact-report 不等于软体载荷；未通过软体力核算时发布值为 `null`，不会把零探针结果当成零载荷。

Newton 使用官方 `SolverCoupledProxy` 的 lagged 模式，将 MuJoCo-Warp 刚体与 VBD 节点求解连接；明确设置每个 shape 的接触阻尼为 0.2。没有改为 Isaac Lab 前端或用刚体球代替软体球。

MuJoCo 3.15 对直接定义的 flex 在零阻尼下发出“没有被动力”编译提示，但实际弹性刚度与恢复力非零，已用单元测试验证。运行期数值警告仍按失败处理。材料本构和求解器不同，共同 E/ν 不代表已完成材料标定。

## 调参与计时

候选集合：Kp 比例 0.5/1/2，Kd 比例 0.7/1/1.4，推送时间 2/3/4 s。所有 81 条训练结果齐全才选择；任何一条数值或接触力校验失败，该候选不可选。按成功布局数、通过物体数、截断到目标的最小物体进度、归一化力矩平方、距基线距离和候选编号排序。预留布局从不参与排序；`selection.json` 保存选择结果。

吞吐使用相同的七关节完整轨迹。Warp 控制器在 CUDA kernel 内运行，Genesis 使用 GPU 张量，不在计时区间逐步回传状态。先预热完整轨迹，再复位，GPU 同步后开始/结束计时；包括控制与原生调度开销。检查批内一致性、复位重复性，并以五个时间点与同引擎单环境轨迹对照。记录三个时间样本、步/秒、精度和内存统计口径，不能把框架分配器峰值解释成整卡峰值。

## 输出与差异

刚体：`scene.xml`、PhysX 的 `scene.usda`、`case.json`、`reference.npz`、`trajectory.npz`、`result.json`。轨迹含时间、广义坐标/速度、所有刚体位姿、原生接触扳手、控制输入和 FK 误差。软体另外保存 `mesh.npz`、节点轨迹、单元体积检查、质量加权质心及未经验证的原生力诊断。各批次保存源码摘要和环境，报告可重新生成：

```bash
.venv/bin/physics-bench extended report --output results/my-full-suite
```

本项目依据[作者公开原文](https://mandarobotics.com/blog/comparing-physics-engines/index.html)和其链接的实验协议独立实现。作者完整场景源码及冻结参考轨迹未公开；不能声称逐值复现。推物的绝对位置、扫掠布局与轨迹、插销阻抗/引导增益和桌面尺寸是明确的实现选择；本机为 RTX 4090 D，驱动、精度、Isaac/Genesis/MuJoCo 版本与作者环境不同。常规重复在同进程中重新创建原生场景，未等同于作者部分实验的全新进程重复。高刚度力峰值、过载或软体翻转不能单独证明哪个引擎更准确。

### 跨引擎冻结控制器迁移

四个引擎分别完成训练后，加载各自 `selection.json` 并从 81 条训练记录重新计算选择，验证证据一致。将基线与所有选中控制器去重后，逐一在四个引擎、六个预留布局运行。同一控制器被多个引擎选中时共享测试结果，保存 `selected_by` 来源。除本引擎预留验证外，新增 24–120 次交叉迁移试验，具体数量取决于独立选出的控制器数量。

```bash
.venv/bin/python scripts/run_full_experiments.py --scope transfer \
  --selection-root results/full-rigid-tuning-v3/tuning --output results/my-transfer
```

多批次汇总会读取计划和最新尝试，避免恢复试验重复计数：

```bash
.venv/bin/physics-bench extended report --output results/my-comparison \
  --input results/full-rigid-tuning-v3 --input results/full-soft-v1 \
  --input results/my-transfer
```

恢复使用输出目录里的冻结源码，已完成结果不重跑；修改实现后选择新目录。应用退出或执行会话被终止可能中断后台进程，`status.json` 的 running 不是进程仍存活的证明，应结合进程和 `progress.json` 的更新时间检查。

候选全部未通过训练有效性门槛时，选择结果为空，不放宽动量残差阈值。新运行器会保留 `no_eligible_candidate` 和基线预留验证；迁移仍测试其他引擎选出的控制器。早期冻结批次可能在同一条件下以异常退出，原始错误保留，迁移程序可从齐全的训练记录重新核算“无合格候选”。

### 故障修复后的补跑

`scripts/run_recovery.py` 将 PhysX 容器串行执行，软体与 PhysX 不重叠，CUDA 实验互斥；准确性矩阵结束后才执行吞吐。所有 20 个作业从启动时即写入 `status.json`，区分 queued、running、completed 和 error。作业 completed 表示运行命令结束，物理验收仍需检查每次的状态和力核算。

```bash
.venv/bin/python scripts/run_recovery.py --output results/my-recovery \
  --genesis-python .venv-genesis-recovery/bin/python \
  --input results/full-rigid-tuning-v3 --input results/full-soft-v1 \
  --input results/recovery-20261009-cpu-insertion \
  --input results/recovery-20261009-warp-insertion
# 恢复时保留相同参数并添加 --resume；引擎版本也必须相同。
```

复用要求相同物理配置、重复编号、关键依赖版本与 Panda 资产。插销还要求修复后的控制器源码一致。仅在本次已审阅的迁移范围内复用其余旧场景，历史源码和原始 force gate 保留在 `provenance`；不是任意源码版本都等价的通用缓存。明确的运行错误不复用，翻转和过载作为已观察的失效保留。吞吐全部重新计时。旧数据通过文件软链接保留，结果 JSON 另外写入新目录，不修改原件。

同一历史观测可用于配置相同的基线、预留或迁移用途，但不是新独立重复。报告列出复用数量和 `reuse-index.json`，统计推断不得重复计入这些观测。未经力核算的旧数据仍未经力核算，不因复用而变为有效载荷。

插销现在在有界笛卡尔阻抗中增加冗余关节的零空间姿态反馈。原控制器在无接触时也会漂移，不能将之前的过载直接归为引擎问题。无接触控制审计见 `scripts/audit_insertion.py`，修复前的 30 组插销结果不参与新批次。
