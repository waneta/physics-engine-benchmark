# 扩展物理实验实测报告

数据来源：下列批次各次原生仿真的 `result.json` 和 `trajectory.npz`。任务失败、数值无效和接触力核算不通过分别记录；未运行配置列为缺失。恢复重试只统计最后一次，旧尝试仍保留。

- [.](./)

## 计划覆盖

| 批次 | 已记录 / 计划 | 缺失 |
|---|---:|---:|
| . | 111 / 111 | 0 |

已生成计划中的缺失结果：0；历史尝试：0。尚未生成计划的后续批次不在该缺失数内，请同时检查运行器状态。

## 数值与任务结果

| 实验 | 引擎 | 已记录 | 数值有效 | 任务成功 | 力核算通过 | 异常/翻转 |
|---|---|---:|---:|---:|---:|---:|
| collision_chain | genesis | 6 | 6 | 6 | 6 | 0 |
| grasp | genesis | 6 | 6 | 6 | 0 | 0 |
| insertion | genesis | 30 | 30 | 24 | 0 | 0 |
| panda_open_loop | genesis | 6 | 6 | 6 | 0 | 0 |
| panda_tracking | genesis | 6 | 6 | 6 | 0 | 0 |
| push | genesis | 36 | 36 | 9 | 0 | 0 |
| stack | genesis | 18 | 18 | 12 | 18 | 0 |
| sweep | genesis | 3 | 3 | 0 | 0 | 0 |

数值有效表示已完成相应状态校验；插销触发过载属于任务停止。力数据只有通过独立动量核算才可用于定量比较。所有软体质量从实际四面体体积计算；网格细化保留粗网格边界。

原文公开了协议和部分参数，没有公开完整场景源码及冻结轨迹。本项目依据公开协议独立实现，几何补全、引擎版本和硬件差异见 `docs/full-experiments.md`，这些数据不等同于原文复现值。

## 参考轨迹一致性

在两个及以上引擎运行的 0 个配置中，参考摘要不一致：0。这只检查共同参考输入，不证明输出轨迹一致。

![collision_chain](collision_chain.png)

![grasp](grasp.png)

![insertion](insertion.png)

![panda_open_loop](panda_open_loop.png)

![panda_tracking](panda_tracking.png)

![push](push.png)

![stack](stack.png)

![sweep](sweep.png)
