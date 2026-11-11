# mujoco-warp 基础实验报告

运行通过：6/6；已记录 6 组。这是一套独立实现，不是原文数值的精确复现。
所有计划实验均已执行。

全部配置见 config.json，环境与代码指纹见 environment.json。每组目录包含 scene.xml、imported.json、raw.csv 和 metrics.json；失败时另存 failure.json，中断时另存 interruption.json；保留已采集数据。

| 场景 | dt (ms) | 重复 | 状态 | 主要指标 |
|---|---:|---:|---|---|
| slide | 2 | 1 | passed | 峰值接触力 10.531670 N；最终位移 126.448587 mm |
| slide | 2 | 2 | passed | 峰值接触力 10.531702 N；最终位移 126.448646 mm |
| slide | 2 | 3 | passed | 峰值接触力 10.531702 N；最终位移 126.448646 mm |
| slide | 1 | 1 | passed | 峰值接触力 9.532951 N；最终位移 126.962036 mm |
| slide | 1 | 2 | passed | 峰值接触力 9.532980 N；最终位移 126.962081 mm |
| slide | 1 | 3 | passed | 峰值接触力 9.532980 N；最终位移 126.962081 mm |

## 重复性

每次重建模型和数据，不加入随机扰动；重复编号不是随机种子。检查每列相对第一次运行的最大绝对差，详见 repeatability.json。未使用重复次数估计统计置信区间。

- slide / 2 ms：3/3 次通过；所有数值列完全一致：False。
- slide / 1 ms：3/3 次通过；所有数值列完全一致：False。

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

![slide](slide.png)


这是单引擎场景报告；跨引擎对照使用 compare 命令，并核查 imported.json 中的实现差异。当前采样带有 Python 与导出开销，不报告引擎吞吐量。


## 滑动方块：摩擦与运动轨迹

表中为第一次重复；全部重复、中文名称、单位与统计见 [中文指标明细](metrics_zh.md)、[CSV](metrics_zh.csv)、[统计CSV](metric_stats_zh.csv)。

| 引擎 | 步长(ms) | 状态 | 实测等效摩擦系数 (1) | 稳定滑动平均摩擦力 (N) | 稳定滑动平均X减速度 (m/s²) | 停止时间 (s) | 停止距离 (m) | 停止距离相对理想值偏差 (%) | 相对理想轨迹最大X位移误差 (m) | 最大动量平衡残差 (N·s) |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MuJoCo-Warp（直接 CUDA） | 2 | 通过 | 0.398299767 | 0.784899804 | 7.84900807 | 0.26 | 0.126459196 | -0.754822814 | 0.000972869161 | 9.25658415e-08 |
| MuJoCo-Warp（直接 CUDA） | 1 | 通过 | 0.399278744 | 0.823901979 | 8.23899946 | 0.262 | 0.126960427 | -0.361457229 | 0.000482127346 | 1.48115227e-07 |

稳定滑动测量窗口：首次接触之后排除启动阶段 40 ms；步初水平速度 > 0.01 m/s，且法向力 > 1e-9 N。
实测等效摩擦系数 = Σ(水平接触力模长×dt) / Σ(法向力×dt)，平均摩擦力和平均X减速度使用同一窗口；无有效窗口时为未测得。
理想参考为水平刚性平面上的纯平移库仑模型：a=μg，v=max(v₀−at,0)，x=v₀t−at²/2（停止后保持）；不含接触启动、转动或软接触，轨迹误差用于观察模型差异。
停止时间使用|vx|低于配置阈值且此后所有采样保持低于阈值的首个时刻；停止距离取该时刻X位移。所有指标仅覆盖已记录时长。
