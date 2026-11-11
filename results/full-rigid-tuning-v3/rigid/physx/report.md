# 扩展物理实验实测报告

数据来源：本目录各次原生仿真的 `result.json` 和 `trajectory.npz`。任务失败、数值无效和接触力核算不通过分别记录；没有运行的配置不计入分母。

| 实验 | 引擎 | 已记录 | 数值有效 | 任务成功 | 力核算通过 | 异常/翻转 |
|---|---|---:|---:|---:|---:|---:|
| collision_chain | physx | 6 | 6 | 6 | 6 | 0 |
| grasp | physx | 6 | 6 | 6 | 6 | 0 |
| insertion | physx | 30 | 0 | 0 | 0 | 30 |
| panda_open_loop | physx | 6 | 6 | 6 | 0 | 0 |
| panda_tracking | physx | 6 | 6 | 6 | 0 | 0 |
| push | physx | 36 | 0 | 0 | 0 | 36 |
| stack | physx | 18 | 17 | 12 | 17 | 1 |
| sweep | physx | 3 | 0 | 0 | 0 | 3 |

数值有效表示已完成相应状态校验；插销触发过载属于任务停止。力数据只有通过独立动量核算才可用于定量比较。所有软体质量从实际四面体体积计算；网格细化保留粗网格边界。

原文公开了协议和部分参数，没有公开完整场景源码及冻结轨迹。本项目依据公开协议独立实现，几何补全、引擎版本和硬件差异见 `docs/full-experiments.md`，这些数据不等同于原文复现值。

## 异常记录

- `insertion-095882702afc`：I/O operation on closed file.
- `insertion-14e6bb0e9d3b`：I/O operation on closed file.
- `insertion-18da234be164`：I/O operation on closed file.
- `insertion-37175dec0b01`：I/O operation on closed file.
- `insertion-386d95ac7e0a`：I/O operation on closed file.
- `insertion-42e1d7f6f4f1`：I/O operation on closed file.
- `insertion-47a67b3b0d61`：I/O operation on closed file.
- `insertion-483c23124b40`：I/O operation on closed file.
- `insertion-5413d38ab6bf`：I/O operation on closed file.
- `insertion-5472deab52a7`：I/O operation on closed file.
- `insertion-68f21330c871`：I/O operation on closed file.
- `insertion-6ca0603e7187`：I/O operation on closed file.
- `insertion-70215a73a006`：I/O operation on closed file.
- `insertion-75386d156c0a`：I/O operation on closed file.
- `insertion-7fb0c438a828`：I/O operation on closed file.
- `insertion-8a9b3722f3b3`：I/O operation on closed file.
- `insertion-8c2a7186844f`：I/O operation on closed file.
- `insertion-8e56623a1fdd`：I/O operation on closed file.
- `insertion-957abd9ccd58`：I/O operation on closed file.
- `insertion-a2e8669cfe34`：I/O operation on closed file.
- `insertion-a50da9682978`：I/O operation on closed file.
- `insertion-aac36139cb78`：I/O operation on closed file.
- `insertion-b9f97ad974b1`：I/O operation on closed file.
- `insertion-cb31ec5b7cf1`：I/O operation on closed file.
- `insertion-cbef3637ecbb`：I/O operation on closed file.
- `insertion-ce5e90767957`：I/O operation on closed file.
- `insertion-d48bf8be9ebb`：I/O operation on closed file.
- `insertion-e30c0c0ab219`：I/O operation on closed file.
- `insertion-ea58ee4b82b9`：I/O operation on closed file.
- `insertion-fbe18b5c1654`：I/O operation on closed file.
- `push-040b6acb5ce8`：I/O operation on closed file.
- `push-05b606e18966`：I/O operation on closed file.
- `push-072103986bc2`：I/O operation on closed file.
- `push-12255620c8d0`：I/O operation on closed file.
- `push-278ddbc4209f`：I/O operation on closed file.
- `push-3b01d3ab60b8`：I/O operation on closed file.
- `push-3b1bb08c77d3`：I/O operation on closed file.
- `push-4cd12fb7a122`：I/O operation on closed file.
- `push-503d09560c12`：I/O operation on closed file.
- `push-62ec297f64f9`：I/O operation on closed file.
- `push-687378cb6ab8`：I/O operation on closed file.
- `push-6ecd44229ed6`：I/O operation on closed file.
- `push-7311eb035f71`：I/O operation on closed file.
- `push-7ab979f32354`：I/O operation on closed file.
- `push-7b6f982c0e5f`：I/O operation on closed file.
- `push-845d30f5f2aa`：I/O operation on closed file.
- `push-8848601ece70`：I/O operation on closed file.
- `push-8d379b126f4e`：I/O operation on closed file.
- `push-8e74d193afde`：I/O operation on closed file.
- `push-94cccfcec2b9`：I/O operation on closed file.
- `push-96caf5a40261`：I/O operation on closed file.
- `push-96ccdc35e6c4`：I/O operation on closed file.
- `push-9dde4881a363`：I/O operation on closed file.
- `push-a3136d589283`：I/O operation on closed file.
- `push-a715fd77a7d2`：I/O operation on closed file.
- `push-bf866ada1b95`：I/O operation on closed file.
- `push-c40e9a866a39`：I/O operation on closed file.
- `push-c8a50d929a26`：I/O operation on closed file.
- `push-d1b5075ccdeb`：I/O operation on closed file.
- `push-d6892b8092c9`：I/O operation on closed file.
- `push-eb388fee8cf6`：I/O operation on closed file.
- `push-ee03c962029d`：I/O operation on closed file.
- `push-f7c9528c13ab`：I/O operation on closed file.
- `push-f956b06100d6`：I/O operation on closed file.
- `push-f9df6ca1c65a`：I/O operation on closed file.
- `push-fa3582cd1d2d`：I/O operation on closed file.
- `stack-48203d3b5208`：I/O operation on closed file.
- `sweep-58afcc89a59b`：I/O operation on closed file.
- `sweep-cf7399b17d6d`：I/O operation on closed file.
- `sweep-e700dae8e99f`：I/O operation on closed file.

![collision_chain](collision_chain.png)

![grasp](grasp.png)

![panda_open_loop](panda_open_loop.png)

![panda_tracking](panda_tracking.png)

![stack](stack.png)
