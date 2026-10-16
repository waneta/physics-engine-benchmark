# 基础刚体实验说明

本文描述最初的 CPU 基线和公共测量约定。task02 已扩展多引擎适配，
安装、运行方式及接触模型差异见 [多引擎说明](multi-engine.md)。

## 本阶段验收范围

落实 task01 归档提出的第一个里程碑：可重复运行三个 MuJoCo CPU 场景，
保存原始状态、力、冲量、参数回读、软硬件版本和曲线，建立后续引擎的校验依据。
不把三个场景的自建实现称作整篇研究复现，不将 CPU 采样脚本耗时当作性能排名。

## 参数及来源

| 参数 | 本实现 | 来源 / 假设 |
|---|---|---|
| 立方体 | 0.1 kg，边长 0.04 m | 转载文档 |
| 滑块初速度 / 滑动摩擦 | 1 m/s / 0.4 | 原文转载未给出，自选；理想距离约 127.421 mm |
| 滑块时长 / 步长 | 0.6 s / 2、1 ms | 文档展示窗口及步长 |
| 下落初始质心高度 | 0.35 m | 转载文档；底面离地 0.33 m |
| 下落时长 / 步长 | 1 s / 2、1 ms | 转载文档 |
| 铰链连杆 | 1 kg，长 0.3 m，方形截面 0.04 × 0.04 m | 长、宽、质量来自文档；方形截面是本实现假设 |
| 铰链初角 / 初角速度 | 0.5 rad / 0 rad/s | 转载文档 |
| 力矩脉冲 | [0.1, 0.2) s，0.2 N·m | 转载文档；边界明确按半开区间 |
| 铰链时长 / 步长 | 1 s / 1、0.5 ms | 文档误差对照窗口与步长 |
| 重力 | 世界坐标 -z，9.81 m/s² | 与文档支撑力一致 |
| solref | (0.01, 1) | 下落实验已说明；滑块沿用是自选 |
| solimp | (0.9, 0.95, 0.001, 0.5, 2) | 显式自选，不声称作者配置 |
| 接触 / 积分 / 求解器 | condim=3，elliptic，Euler，Newton，100 次迭代 | 显式自选，tolerance=1e-10 |
| 阻尼 / armature / 关节摩擦损耗 | 均为 0 | 无驱动、无预静置；扭转与滚动摩擦为 0 |

实际版本以 `uv.lock` 和每次的 `environment.json` 为准；不假定等于转载文档中的版本。
配置文件会逐条保存上述假设。调参得到相近数字，不能证明恢复了作者的完整配置。
源文章：https://mandarobotics.com/blog/comparing-physics-engines/index.html
（本次网络读取失败，研究参数依据仓库中的转载文档；部分公式缺失。）

## 运行

在仓库根目录执行：

```bash
uv sync --locked --python 3.11
uv run --locked physics-bench doctor
uv run --locked physics-bench run
uv run --locked physics-bench run --scene hinge --repeats 3 --output results/hinge-check
```

也可直接使用 `.venv/bin/physics-bench run`，避免运行时重复解析环境。
无须显示器、窗口系统或 GPU。`--no-plots` 可关闭绘图，`--config <路径>` 可指定另一份 JSON。
程序拒绝覆盖任何已有输出目录；若实验失败，保留已经采集的行、异常及配置，
继续其他运行并在最终返回非零退出码。

`run` 是无窗口批量计算，不会弹出三维仿真界面。启动时打印 `Output:`，
完成后打印 `Report:`；正常运行请等待命令返回。
在实验仿真或指标计算过程中按 Ctrl+C，会停止后续实验、将当前实验标记为
`interrupted`，保存已采集的 `raw.csv` 与 `interruption.json`，
并导出标明未完成的部分报告。中断时跳过绘图，退出码为 130。
初始化阶段中断可能尚未生成报告，可检查已打印的输出目录。
重复运行会新建实验目录，目前不支持断点续跑。

每次运行独立重建模型与数据。当前场景无随机输入，因此 repeat 是重复编号，
并非随机种子。相同结果仅说明此场景、版本与设备上的重复性，不能外推到 GPU 或多物体接触。
三次重复不构成成功率或置信区间估计。

## 导入校验

质量、局部质心、体坐标惯性张量、铰链轴、初始质心位置、阻尼、armature、
frictionloss 均从编译后的模型校验。惯量通过主轴旋转还原到体坐标，
避免将排列变化误判为惯量不一致。回读还保存几何尺寸、碰撞掩码、表面参数、
关节位置和限位标记、求解器设置、初始广义位置和速度。

铰链绕 y 轴旋转，竖直向下为零角。有限截面均匀连杆的支点惯量为
`I = m * (L²/3 + W²/12)`，参考方程为
`I * θ'' = τ(t) - m*g*L/2*sin(θ)`。
独立 RK4 使用不超过 50 μs 的子步，并在脉冲边界切段。
这是高精度数值 ODE 参考，不是闭式解析解，也不是实物真值。
测试将参考步长再减半验证参考误差足够小。

## 力、冲量及时间语义

每行 CSV 对应 `[t_start_s, t_end_s]`；先保存起始状态，调用 `mj_step1/mj_step2`，
再保存终止状态并读取本次求解器的接触力。
在读取力之前不调用下一次 `mj_forward`，以免覆盖刚施加在该时间步上的力。
该采样方式针对本实现固定使用的 Euler 积分器。

`mj_contactForce` 返回接触坐标系力；用接触坐标轴矩阵的转置转换到世界坐标系，
按目标物体是 geom1 还是 geom2 调整符号，再将作用于目标物体的全部接触力求和。
这是合力矢量的模，不是逐接触点力模长的总和。

- `contact_f{x,y,z}_n`：作用于方块的世界坐标接触力，不含重力。
- `contact_j{x,y,z}_ns`：上述力乘 dt。MuJoCo 原生输出的是力，冲量为派生值。
- `net_fz_n`：包含重力的竖直净力，供下落图对照。
- `momentum_residual_ns`：`||m*(v_end-v_start)-(F_contact+m*g)*dt||`。
- `constraint_force_error_n`：接触合力与原生广义约束力前三项的差。

自由立方体质心与自由关节原点重合，qvel 前三项是世界坐标线速度，
因此可以直接做线动量校验。默认动量残差容差 `5e-6 N·s`，超出则标记失败；
该校验不适用于直接忽略支点约束反力的铰链，所以铰链使用 ODE 对照。

官方 API 和步进语义依据：
[MuJoCo simulation](https://mujoco.readthedocs.io/en/stable/programming/simulation.html)、
[mj_contactForce](https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html#mj-contactforce)。

## 指标定义

- 停止时刻：滑块 x 向速度绝对值从此在剩余记录中持续小于 1 mm/s；停止距离取该采样。
  另存最终位移，防止两种定义混用；未停止记 null。
- 静置时刻：首次接触后，质心线速度模从此持续小于 1 mm/s；不包含角速度条件。
- 穿透深度：按实际旋转求方块最低顶点，取其低于 z=0 平面的深度。
- 峰值力：逐步原始接触合力模长的最大值，不平滑。
- 窗口冲量：从首次非零接触力开始积分 40 ms，逐轴报告接触冲量；不含重力。
  非整步窗口的末步按重叠时间积分；仿真结束前窗口不完整记 null。
- 铰链：报告角度最大/RMS误差、角速度最大误差、施加力矩的时间积分。
- 重复性：相对首个成功重复，逐 CSV 数值列计算最大绝对差。只有一次成功则为 null。

## 输出目录

```text
results/<run>/
  config.json             完整输入与假设
  environment.json        依赖、平台、CPU/GPU、Git 状态、代码/锁文件指纹
  runs.json               每次运行状态、异常摘要及目录
  summary.csv             所有成功运行指标；单位写入列名
  repeatability.json      各列重复差异（单位沿用相应列）
  report.md               指标与曲线入口
  slide.png / drop.png / hinge.png
  <scene>/dt_<seconds>/repeat_<index>/
    scene.xml             MuJoCo/Genesis 的输入模型；PhysX 的共同场景参考
    scene.usda            PhysX 实际创建的 USD 场景（仅 PhysX）
    imported.json         导入后的参数回读
    raw.csv               全部物理步，含起止位置/速度和本步力/冲量
    metrics.json          单次指标
    failure.json          仅在失败时生成；保留堆栈和已采样行数
    interruption.json     用户中断时生成；记录已采样行数
```

自由体 `qpos0..6` 依次为 x、y、z、qw、qx、qy、qz；
`qvel0..2` 为世界坐标线速度，`qvel3..5` 为物体局部角速度。
铰链 `qpos0` 为角度，`qvel0` 为角速度。
所有量使用 SI 单位。图中为首次重复的原始曲线；三次重复的数据均完整保存。
`results/` 和虚拟环境被 Git 忽略，运行结果不会自动提交。

## 后续阶段

task02 已将三个场景接入 MuJoCo-Warp、Genesis、Isaac Sim/PhysX，详见 [验收记录](validation-task02.md)。
直接 MuJoCo-Warp 与作者的 Newton/MuJoCo-Warp 路径仍需明确区分。
刚体 PhysX 使用 Isaac Sim CPU TGS 对照，不能混入 GPU 吞吐排名。

1. 接入 Panda 时先校验资产与无接触运动，再统一显式力矩控制器、推物和抓取。
2. GPU 吞吐单独实现：关闭渲染，排除编译与预热，计时前后同步 GPU，
   记录总环境步/秒、显存、精度、batch 大小。当前诊断采样循环不能用于这个排名。
3. 软体测试需要另外验证材料、网格、耦合与力测量；不从刚体成功外推。

2026-10-08 现场检查已可识别 RTX 4090 D / 驱动 570.211.01。
task02 已在该设备验证 Warp 与 Genesis CUDA 后端，更新了旧归档的 GPU 不可用结论。
