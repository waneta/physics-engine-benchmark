# 立方体下落碰撞静置：本轮执行与验收 / Cube drop batch acceptance

四引擎已独立实测，正式 **24/24 无界面、8/8 界面通过**。

[四引擎双语对比](comparison/report.md) · [双语明细](comparison/metrics_bilingual.md) · [明细CSV](comparison/metrics_bilingual.csv) · [统计CSV](comparison/metric_stats_bilingual.csv) · [自动审计](audit.json) · [命令与源码指纹](manifest.json)

## 参数与覆盖 / Parameters and coverage

本轮从静止释放质量 0.1 kg、边长 0.04 m 的立方体，质心初始高度 0.35 m，底面离地 0.33 m。
重力 9.81 m/s²、摩擦系数 0.4、记录时长 1 s；步长 2 ms 和 1 ms。
理想接触时间 0.259380584 s、理想接触前速度 −2.544523531 m/s。
配置沿用 `configs/baseline.json`，四引擎各独立重建场景，无界面每步长三次，界面每步长一次。

| 引擎 / Engine | 无界面 / Headless | 最终界面 / Final GUI | 单引擎结果 / Results |
|---|---:|---:|---|
| PhysX / Isaac Sim CPU TGS | 6/6 | 2/2 | [无界面 / Headless](physx/report.md) · [界面 / GUI](viewer-final-physx/report.md) |
| MuJoCo-Warp CUDA | 6/6 | 2/2 | [无界面 / Headless](mujoco-warp/report.md) · [界面 / GUI](viewer-final-mujoco-warp/report.md) |
| MuJoCo CPU | 6/6 | 2/2 | [无界面 / Headless](mujoco-cpu/report.md) · [界面 / GUI](viewer-final-mujoco-cpu/report.md) |
| Genesis CUDA | 6/6 | 2/2 | [无界面 / Headless](genesis/report.md) · [界面 / GUI](viewer-final-genesis/report.md) |

## 主要测量 / Main measurements

首次重复；完整重复与统计见上方双语文件。

| 引擎 / Engine | 步长 / Timestep (ms) | 首次接触 / First contact (s) | 峰值法向力 / Peak normal force (N) | 最大穿透 / Maximum penetration (m) | 刚体静置 / Rigid-body settling (s) | 静置后观察 / Rest observation (s) | 末段支撑力/重力 / Tail support/weight (1) |
|---|---:|---:|---:|---:|---:|---:|---:|
| PhysX / Isaac Sim CPU TGS | 2 | 0.258 | 127.527893 | 1.20823339e-08 | 0.26 | 0.74 | 1.0000001 |
| PhysX / Isaac Sim CPU TGS | 1 | 0.259 | 255.058203 | 0.000302227661 | 0.26 | 0.74 | 1.00000005 |
| MuJoCo-Warp CUDA | 2 | 0.26 | 58.2575302 | 0.00874086356 | 0.36 | 0.64 | 1.0000001 |
| MuJoCo-Warp CUDA | 1 | 0.259 | 53.4409294 | 0.00756728704 | 0.364 | 0.636 | 1.00000009 |
| MuJoCo CPU | 2 | 0.26 | 58.2571948 | 0.00874060957 | 0.36 | 0.64 | 1 |
| MuJoCo CPU | 1 | 0.259 | 53.441377 | 0.00756736771 | 0.364 | 0.636 | 1 |
| Genesis CUDA | 2 | 0.26 | 58.2571948 | 0.00874060957 | 0.36 | 0.64 | 1 |
| Genesis CUDA | 1 | 0.259 | 53.441377 | 0.00756736771 | 0.364 | 0.636 | 1 |

全部正式运行均在 1 s 内满足刚体静置判定，末段平均支撑力约为重力 0.981 N。
本轮 PhysX 静置时间为 0.260 s，其他三个后端为 0.360/0.364 s。
当前软接触路径的最大穿透约 7.57–8.74 mm，PhysX 最大穿透约 0–0.302 mm；
PhysX 的法向峰值力随步长减半由约 127.53 N 增至 255.06 N。
这些差异反映当前求解器、接触模型、偏置、材料参数与时间离散，不能据此给出引擎准确性排名。
回弹指标是接触后最大向上速度，不作为材料恢复系数估计；本轮未进行吞吐或图形性能比较。

## 验证 / Validation

- 正式无界面 24/24 组通过，18000 个物理步；最终界面 8/8 组通过，6000 个物理步。
- 质量、惯量、初始状态等模型回读通过，原始数据有限，接触力/冲量与动量一致性通过；容差为 `5e-6 N·s`。
- 32 组均满足静置判定：线速度 <0.001 m/s，角速度×立方体半对角线 <0.001 m/s，前一步法向支撑力 >1e-9 N；此后全部记录状态持续满足。静置后观察时长另列。
- 最终八组界面与各自无界面首次重复逐步对比，所有数值列完全一致；最终显示姿态误差为零，显示进程退出码均为 0。
- 界面预设绝对容差：位置 1e-6 m、四元数 1e-6、线速度 1e-4 m/s、角速度 1e-3 rad/s、力 1e-3 N、冲量 1e-6 N·s；静置时间差不超过一个步长。本轮全部差异为零，不代表所有 GPU 场景逐位确定。
- 双语汇总包含 768 条指标明细、256 条分组统计；本场景 32 种指标，全局字典 56 种。统计仅使用通过记录，缺失值不填零。
- `pytest -q`：77 passed in 5.05s；`ruff check src tests scripts` 通过。CPU 默认三场景回归 18/18 组通过；滑块原始数值与上轮对应首次重复完全一致。
- 1130 个历史滑块文件 SHA-256 校验一致，最终源码与配置指纹校验通过。

## 本轮实际命令 / Executed commands

在仓库根目录依次执行；目录已经存在，重新实验须换新目录或省略 `--output`。

```bash
.venv/bin/physics-bench run --engine physx --scene drop --headless --repeats 3 --output results/task04-drop-20261010/physx
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene drop --headless --repeats 3 --output results/task04-drop-20261010/mujoco-warp
.venv/bin/physics-bench run --engine mujoco-cpu --scene drop --headless --repeats 3 --output results/task04-drop-20261010/mujoco-cpu
.venv-genesis/bin/physics-bench run --engine genesis --scene drop --headless --repeats 3 --output results/task04-drop-20261010/genesis
.venv/bin/physics-bench run --engine physx --scene drop --viewer --repeats 1 --output results/task04-drop-20261010/viewer-final-physx
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene drop --viewer --repeats 1 --output results/task04-drop-20261010/viewer-final-mujoco-warp
.venv/bin/physics-bench run --engine mujoco-cpu --scene drop --viewer --repeats 1 --output results/task04-drop-20261010/viewer-final-mujoco-cpu
.venv-genesis/bin/physics-bench run --engine genesis --scene drop --viewer --repeats 1 --output results/task04-drop-20261010/viewer-final-genesis
.venv/bin/physics-bench compare results/task04-drop-20261010/physx results/task04-drop-20261010/mujoco-warp results/task04-drop-20261010/mujoco-cpu results/task04-drop-20261010/genesis --output results/task04-drop-20261010/comparison
```

汇总读取四个无界面结果，不重新执行物理仿真。常用命令见 [下落实验使用说明](../../docs/single-drop.md)。

CPU 三场景回归：

```bash
.venv/bin/physics-bench run --engine mujoco-cpu --scene all --headless --repeats 3 --output results/task04-drop-20261010/regression-cpu-final
```

## 显示修复与保留诊断 / Display fixes and retained diagnostics

首次同进程显示导致 PhysX/Warp 采样很慢；两次主动中断、部分采样及日志保存在
`viewer-physx/`、`viewer-mujoco-warp/`。之后改为全部引擎使用 spawn 独立显示进程，
合并积压显示消息并核对最终姿态，原始逐步物理采样全部保留。

中间尝试还发现窗口清理时 `GLXBadContext`。旧入口没有检查显示子进程退出码，
其运行记录的 passed 只能表明采样完成，不能作为本轮界面验收。
现已等待 MuJoCo 渲染线程销毁窗口，再回传完成；父进程检查并保存显示进程退出码，异常则记录失败。
最终四个引擎全部重新验证，只有 `viewer-final-*` 纳入正式界面结果。
中间 `viewer-physx-isolated/`、`viewer-mujoco-warp-isolated/`、`viewer-mujoco-cpu/`、`viewer-genesis/`
均保留作为诊断，未混入汇总。最终日志无 `GLXBadContext` 或异常堆栈。
CPU 最终日志仍有 X11 `NV-GLX` 扩展缺失提示，八组均实际绘制并正常退出；未据此推断显卡渲染路径或修改驱动。

独立显示窗口展示测量状态，采用统一 MuJoCo 模型且不执行物理步进。
显示可能跳过中间帧；逐步真实数据应查看原始 CSV。
`viewer-physx/window.png` 是早期诊断截图，不是最终验收截图。

## 来源与范围 / Provenance and scope

各引擎 `environment.json`、每组 `imported.json` 保存实际环境与模型回读。
无界面源版本记录于 manifest 的 `headless_source_sha256`，最终界面为 `viewer_source_sha256_by_engine`。
两阶段之间只修改显示生命周期与入口；配置、后端物理采样及下落指标未改变。
中间诊断源码指纹也保留，不能用当前 Git 提交号替代未提交源码指纹。
本次完成下落碰撞静置；单铰链新增界面验收和此前暂停的完整扩展补跑未执行。
