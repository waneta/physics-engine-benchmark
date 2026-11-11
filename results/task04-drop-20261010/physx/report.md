# physx 基础实验报告 / Baseline experiment report

运行通过：6/6；已记录 6 组。这是一套独立实现，不是原文数值的精确复现。
所有计划实验均已执行。

全部配置见 config.json，环境与代码指纹见 environment.json。每组目录包含 scene.xml、imported.json、raw.csv 和 metrics.json；失败时另存 failure.json，中断时另存 interruption.json；保留已采集数据。

| 场景 / Scene | 步长 / Timestep (ms) | 重复 / Repeat | 状态 / Status | 主要指标 / Key metrics |
|---|---:|---:|---|---|
| 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force 127.527900 N；最大穿透 / Maximum penetration 0.000012 mm |
| 方块下落 / Cube drop | 2 | 2 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force 127.527900 N；最大穿透 / Maximum penetration 0.000012 mm |
| 方块下落 / Cube drop | 2 | 3 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force 127.527900 N；最大穿透 / Maximum penetration 0.000012 mm |
| 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force 255.058203 N；最大穿透 / Maximum penetration 0.302228 mm |
| 方块下落 / Cube drop | 1 | 2 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force 255.058203 N；最大穿透 / Maximum penetration 0.302228 mm |
| 方块下落 / Cube drop | 1 | 3 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force 255.058203 N；最大穿透 / Maximum penetration 0.302228 mm |

## 重复性 / Repeatability

每次重建模型和数据，不加入随机扰动；重复编号不是随机种子。检查每列相对第一次运行的最大绝对差，详见 repeatability.json。未使用重复次数估计统计置信区间。

- drop / 2 ms：3/3 次通过；所有数值列完全一致 / All numeric samples identical：是 / Yes。
- drop / 1 ms：3/3 次通过；所有数值列完全一致 / All numeric samples identical：是 / Yes。

## 采样约定

raw.csv 每行对应 [t_start_s, t_end_s]。qpos/qvel 的 start/end 是物理步两端状态；contact_f* 是本步求解器施加在目标物体上的世界坐标力，contact_j*=contact_f*×dt。原生测量类型与接口见 imported.json（PhysX 原生冲量，其余引擎原生力）。SI 单位；自由体 qpos=[x,y,z,qw,qx,qy,qz]，qvel 前三项是世界坐标线速度、后三项是局部角速度；铰链为角度/角速度。

冲量窗口从首次非零接触力开始，长度 40 ms；window_contact_j* 是接触冲量，不含重力。窗口不完整时记 null。峰值力未经平滑；net_fz_n 包含重力。静置只针对质心线速度，要求此后全部已记录采样低于阈值，不代表仿真时长以外仍然静止。

## 配置假设

- slide_speed_m_s=1 and sliding_friction=0.4 are selected locally; the clipping omits them
- hinge is a uniform rectangular prism with square 4 cm cross-section
- Euler integrator, Newton solver, elliptic cone, condim=3 and solimp are explicit local choices
- solref=(0.01,1) is stated for drop; using it for slide is a local choice
- no torsional/rolling friction, joint damping, armature, or pre-settling
- installed engine version is locked in uv.lock, not assumed equal to the article

## 步长对照曲线

![drop](drop.png)


这是单引擎场景报告；跨引擎对照使用 compare 命令，并核查 imported.json 中的实现差异。当前采样带有 Python 与导出开销，不报告引擎吞吐量。


## 立方体下落、碰撞、静置 / Cube drop, impact and settling

首次重复 / First repeat；全部重复与统计见 [双语明细](metrics_bilingual.md)、[CSV](metrics_bilingual.csv)、[统计CSV](metric_stats_bilingual.csv)。

### 碰撞响应 / Impact response

| 引擎 / Engine | 步长 / Timestep (ms) | 状态 / Status | 首次接触时间 / First contact time (s) | 首次接触时间相对理想值偏差 / First contact time deviation from ideal (s) | 首次接触步初竖直速度 / Vertical velocity at start of first contact step (m/s) | 接触后最大向上速度 / Peak upward velocity after contact (m/s) | 峰值法向接触力 / Peak normal contact force (N) | 最大穿透深度 / Maximum penetration depth (m) | 最大动量平衡残差 / Maximum momentum balance residual (N·s) |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| PhysX（Isaac Sim CPU TGS） | 2 | 通过 / Passed | 0.258 | -0.0013805842 | -2.53097558 | 4.58310145e-09 | 127.527893 | 1.20823339e-08 | 1.40164555e-08 |
| PhysX（Isaac Sim CPU TGS） | 1 | 通过 / Passed | 0.259 | -0.000380584204 | -2.54078412 | 0 | 255.058203 | 0.000302227661 | 4.96061517e-08 |

### 静置状态 / Settling state

| 引擎 / Engine | 步长 / Timestep (ms) | 状态 / Status | 刚体静置时间 / Rigid-body settling time (s) | 静置后观察时长 / Observation duration after settling (s) | 记录时长内刚体已静置 / Rigid body settled within recorded duration (boolean) | 最终质心高度 / Final COM height (m) | 最终质心线速度模长 / Final COM linear speed (m/s) | 最终角速度模长 / Final angular speed (rad/s) | 末段平均支撑力与重力比 / Final-window mean support force to weight ratio (1) |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| PhysX（Isaac Sim CPU TGS） | 2 | 通过 / Passed | 0.26 | 0.74 | 是 / Yes | 0.0200000051 | 8.60713628e-07 | 5.97454577e-06 | 1.0000001 |
| PhysX（Isaac Sim CPU TGS） | 1 | 通过 / Passed | 0.26 | 0.74 | 是 / Yes | 0.0199999958 | 4.73114187e-07 | 8.10296388e-06 | 1.00000005 |

理想自由落体 / Ideal free fall：质心初始高度 h₀、初速度0，z=h₀−gt²/2、vz=−gt；平放立方体首次接触参考 t=√(2(h₀−边长/2)/g)。参考只对无接触段比较；积分离散误差与接触偏置会影响首次接触时间。
首次接触用原生接触合力>1e-9 N的首个步初时间，碰撞前速度取该步初vz；最大向上速度取首次接触后所有已记录状态，不推算材料恢复系数。
刚体静置 / Rigid-body settling：质心线速度<0.001 m/s，角速度×立方体半对角线也低于该阈值，且前一步法向支撑力>1e-9 N，要求此后所有已记录状态持续满足。原质心静置时间仅检查线速度，继续保留。
末段支撑力为最后40 ms法向力的时间平均，该窗口须全部位于首次接触后；支撑力/重力比约为1表示平均支撑重力。
通过 / Passed表示参数、有限性和动量校验通过；是否已静置另列布尔指标。静置结论只覆盖记录时长，静置后观察时长另行保存；未测得不填零。
