# mujoco-warp 基础实验报告

运行通过：2/2；已记录 2 组。这是一套独立实现，不是原文数值的精确复现。
所有计划实验均已执行。

全部配置见 config.json，环境与代码指纹见 environment.json。每组目录包含 scene.xml、imported.json、raw.csv 和 metrics.json；失败时另存 failure.json，中断时另存 interruption.json；保留已采集数据。

| 场景 | dt (ms) | 重复 | 状态 | 主要指标 |
|---|---:|---:|---|---|
| drop | 2 | 1 | passed | 峰值接触力 58.257530 N；最大穿透 8.740864 mm |
| drop | 1 | 1 | passed | 峰值接触力 53.440929 N；最大穿透 7.567287 mm |

## 重复性

每次重建模型和数据，不加入随机扰动；重复编号不是随机种子。检查每列相对第一次运行的最大绝对差，详见 repeatability.json。未使用重复次数估计统计置信区间。

- drop / 2 ms：1/1 次通过；所有数值列完全一致：None。
- drop / 1 ms：1/1 次通过；所有数值列完全一致：None。

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

这是单引擎场景报告；跨引擎对照使用 compare 命令，并核查 imported.json 中的实现差异。当前采样带有 Python 与导出开销，不报告引擎吞吐量。
