# 单物体实验：滑动方块

task04 当前范围为四种引擎的滑动方块，验证摩擦力和运动轨迹。
支持独立选择引擎、无界面计算或实时三维窗口，完成后保存相同格式的测试结果。
方块下落与单铰链保留已有入口，未纳入本次新增验收；完整扩展补跑仍暂停。

## 实验参数

使用 `configs/baseline.json`：质量 0.1 kg、边长 0.04 m、初速度 1 m/s、摩擦系数 0.4、
重力加速度 9.81 m/s²、时长 0.6 s。初始方块底面位于地面，不预先静置。
每引擎使用 2 ms 和 1 ms 两种步长，各重建场景独立重复三次，共六组。
这些参数由本项目选定，不是原文数值的精确复现。

| 引擎选项 | 执行方式 | 精度 | 本机环境 |
|---|---|---|---|
| `mujoco-cpu` | MuJoCo CPU | float64 | `.venv` |
| `mujoco-warp` | 直接 MuJoCo-Warp CUDA | float32 | `.venv-warp` |
| `genesis` | Genesis CUDA | float64 | `.venv-genesis` |
| `physx` | Isaac Sim / PhysX CPU TGS | float32 | `.venv` + Docker |

任务中的“Newton / MuJoCo-Warp”沿用已验证的直接 MuJoCo-Warp 后端，未增加 Newton 包装层。
各引擎的接触模型和求解参数并不完全等价，具体版本和导入回读见每次结果中的
`environment.json` 与各组 `imported.json`。安装见四份 [部署说明](../README.md)。

## 四引擎无界面命令

以下均在仓库根目录执行。每次自动生成新结果目录并打印报告路径；可以逐个执行。

```bash
# PhysX：使用已有的 Isaac Sim 镜像，--pull=never
.venv/bin/physics-bench run --engine physx --scene slide --headless

# MuJoCo-Warp：需要 CUDA
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene slide --headless

# MuJoCo CPU
.venv/bin/physics-bench run --engine mujoco-cpu --scene slide --headless

# Genesis：需要 CUDA
.venv-genesis/bin/physics-bench run --engine genesis --scene slide --headless
```

省略 `--headless` 也是无界面运行。默认生成结果曲线；`--no-plots` 仅关闭结果绘图。
`--config 路径` 可更换参数，`--repeats N` 可调整重复数。
需要固定输出位置时加 `--output results/新目录`，已存在目录会被拒绝，防止覆盖。

## 四引擎有界面命令

有界面模式需要可用的桌面显示服务和 OpenGL。在桌面终端执行以下命令；
远程无显示会话使用无界面模式。下面每个引擎执行两种步长各一次，便于观看。
改为 `--repeats 3` 即执行完整六组。

```bash
.venv/bin/physics-bench run --engine physx --scene slide --viewer --repeats 1
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene slide --viewer --repeats 1
.venv/bin/physics-bench run --engine mujoco-cpu --scene slide --viewer --repeats 1
.venv-genesis/bin/physics-bench run --engine genesis --scene slide --viewer --repeats 1
```

窗口使用统一的 MuJoCo 被动渲染器，实时接收**所选物理引擎**每步实际算出的位置、姿态和速度。
例如选择 PhysX 时，滑块物理计算仍由容器内 PhysX 完成，宿主窗口只显示测量状态；
无需向容器转发 X11，也不启动 Isaac Sim 的编辑器。
渲染模型与物理模型独立，不对渲染模型调用 `mj_step`，鼠标交互不影响实验。
窗口叠加显示引擎名、步长、时间、X位置、X速度与X接触力，支持鼠标旋转和缩放。

`--viewer-speed 0.2` 默认以五倍慢速观看，物理步长、初始条件和采样保持原值。
首次构建或 CUDA 编译期间，终端显示运行状态；收到首个物理测量步后才创建窗口并开始播放。
四引擎的显示窗口统一运行于独立进程，避免显示同步拖慢采样读取；
Genesis 还借此隔离其离屏 EGL 上下文与桌面窗口资源。
独立显示进程可合并积压显示帧，原始物理采样完整保存，最终显示状态仍单独核对。
结束后默认保持两秒，`--viewer-hold 5` 可延长；每组结束自动关闭，再开启下一组。
关闭正在计算的窗口或按 Ctrl+C 会中断整批，保存已采集数据与部分报告，退出码为 130。
完整物理步骤结束后关闭保持中的窗口视为正常结束。
界面模式增加显示与等待时间，运行耗时不用于性能比较。

## 查看结果与跨引擎对比

每个引擎独立输出后，使用打印出的四个目录汇总。例如本次实际验收目录：

```bash
.venv/bin/physics-bench compare \
  results/task04-slide-20261010/bilingual/physx \
  results/task04-slide-20261010/bilingual/mujoco-warp \
  results/task04-slide-20261010/bilingual/mujoco-cpu \
  results/task04-slide-20261010/bilingual/genesis \
  --output results/task04-slide-20261010/bilingual/comparison
```

对比要求配置完全相同、引擎不同；保留全部重复和失败。
第一次重复用于报告与叠图，全部通过运行用于均值、总体标准差、最小值和最大值统计。
标准差不代表随机实验的置信区间。

| 文件 | 内容 |
|---|---|
| `report.md` | 通过记录、首次重复的主要中英文指标与结果曲线 |
| `metrics_bilingual.md` | 所有重复的中英文指标名称、单位、状态、数值 |
| `metrics_bilingual.csv` | 双语表头、名称、单位说明、原始数值及双语值显示；UTF-8 BOM |
| `metric_stats_bilingual.csv` | 双语均值、标准差、极值、通过次数与有效数值次数 |
| `metric_definitions.json` / `.md` | 英文字段与中英文指标名称、单位符号和中英文单位说明 |
| `slide.png` | X位移、X速度、摩擦力与法向力、高度、摩擦系数、俯视轨迹 |
| `runs.json` / `summary.csv` | 单引擎运行记录 / 英文指标；对比目录保留全部状态于 summary.csv |
| `slide/dt_*/repeat_*/raw.csv` | 单引擎逐物理步原始状态、力、冲量、校验残差及参考轨迹 |
| `slide/dt_*/repeat_*/viewer.json` | 成功界面运行的显示帧数、速度、最终显示状态 |
| `config.json` / `environment.json` | 单引擎完整参数、实际软件硬件与源码指纹 |
| `sources.json` | 对比报告的来源目录、版本与实现差异 |

出现数值非有限、MuJoCo 警告、参数回读失败或动量残差超过 5×10⁻⁶ N·s 时，记录失败；
保留部分原始采样和异常信息。失败运行不进入通过运行的指标统计。空值表示未测得，不填零。

## 摩擦与轨迹指标口径 / Friction and trajectory metrics

主要中英文指标包括设定及实测摩擦系数、平均摩擦力、平均法向力、平均X减速度、
停止时间与距离、停止距离偏差、最大与均方根X轨迹误差、侧向偏移、质心抬升、
穿透深度、全程X接触冲量及动量残差。

- 滑动段窗口：首次接触后排除 40 ms 启动阶段，步初水平速度须大于 0.01 m/s。
  平均力与减速度包含窗口内离地步的零接触力，避免仅统计接触步造成条件平均偏高。
- 实测等效摩擦系数：窗口内法向力大于 10⁻⁹ N 的步上，
  `Σ(√(Fx²+Fy²)×dt) / Σ(Fz×dt)`；没有有效接触时为未测得。
  曲线只画有接触的有效系数，离地时不把系数画为零。
- 平均X减速度：同一滑动段内 `−Δvx/dt` 的平均；摩擦方向用水平力与步初水平速度的点积核查。
- 停止时间：`|vx| < 0.001 m/s` 且之后所有已记录采样均满足阈值的首个时刻；
  停止距离取该时刻的X位移。“质心静置时间”另用三轴线速度模长判定。
- 理想库仑参考：刚性水平面纯平移，`a=μg`、`v=max(v₀−at,0)`、
  `x=v₀t−at²/2`，停止后位移保持。当前理想停止时间 0.254842 s、停止距离 0.127421 m。
  参考不含转动、接触启动或软接触，轨迹偏差不直接作为不同引擎的准确性排名。
- PhysX 接触力由法向与摩擦原生冲量合成后除以步长；其余引擎采样原生接触力。
  动量校验含重力，误差单位为 N·s。峰值力受步长和接触模型影响。

验收结果见 [task04 实测记录](validation-task04.md)。


## 中英文汇总 / Bilingual results

所有新运行与 `compare` 输出均提供中英文指标名称、单位说明和状态。
例如：`停止距离 / Stopping distance`，单位 `m`（`米 / metre`）；
`实测等效摩擦系数 / Measured effective friction coefficient`，单位 `1`（`无量纲 / dimensionless`）。
数字使用通用阿拉伯数字；CSV的数值列保持原始数值精度，另设双语显示列表示
`是 / Yes`、`否 / No`、`未测得 / Not measured`，缺失数值列留空。

兼容文件 `metrics_zh.md`、`metrics_zh.csv` 和 `metric_stats_zh.csv` 继续生成，内容也加入英文名称与单位说明。
指标字段和英文机器汇总 `summary.csv` 保持原格式。
本次新版报告根据原24组实测重新导出，原始配置、采样、指标、运行状态及历史目录均保留。
再导出的来源和SHA-256校验见 `results/task04-slide-20261010/bilingual/export_manifest.json`。
