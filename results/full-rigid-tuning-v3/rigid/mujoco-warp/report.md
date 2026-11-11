# 扩展物理实验实测报告

数据来源：本目录各次原生仿真的 `result.json` 和 `trajectory.npz`。任务失败、数值无效和接触力核算不通过分别记录；没有运行的配置不计入分母。

| 实验 | 引擎 | 已记录 | 数值有效 | 任务成功 | 力核算通过 | 异常/翻转 |
|---|---|---:|---:|---:|---:|---:|
| collision_chain | mujoco-warp | 6 | 6 | 6 | 3 | 0 |
| grasp | mujoco-warp | 6 | 6 | 6 | 0 | 0 |
| insertion | mujoco-warp | 30 | 30 | 0 | 0 | 0 |
| panda_open_loop | mujoco-warp | 6 | 6 | 6 | 0 | 0 |
| panda_tracking | mujoco-warp | 6 | 6 | 6 | 0 | 0 |
| push | mujoco-warp | 36 | 36 | 18 | 0 | 0 |
| stack | mujoco-warp | 18 | 18 | 12 | 0 | 0 |
| sweep | mujoco-warp | 3 | 3 | 0 | 0 | 0 |

数值有效表示已完成相应状态校验；插销触发过载属于任务停止。力数据只有通过独立动量核算才可用于定量比较。所有软体质量从实际四面体体积计算；网格细化保留粗网格边界。

原文公开了协议和部分参数，没有公开完整场景源码及冻结轨迹。本项目依据公开协议独立实现，几何补全、引擎版本和硬件差异见 `docs/full-experiments.md`，这些数据不等同于原文复现值。

![collision_chain](collision_chain.png)

![grasp](grasp.png)

![insertion](insertion.png)

![panda_open_loop](panda_open_loop.png)

![panda_tracking](panda_tracking.png)

![push](push.png)

![stack](stack.png)

![sweep](sweep.png)
