# 单物体实验：立方体下落、碰撞、静置 / Cube drop, impact and settling

四个引擎均支持逐个验证、有界面或无界面，并保存原始物理采样、中英文指标、重复统计与曲线。
场景选项为 `--scene drop`，不需要先执行滑动方块。下面命令在仓库根目录运行。

## 参数与测量 / Parameters and measurements

沿用 `configs/baseline.json`：质量 0.1 kg、边长 0.04 m，质心初始高度 0.35 m，
从静止开始，重力 9.81 m/s²，地面摩擦系数 0.4，时长 1 s。
0.35 m 是质心高度，底面离地 0.33 m。平放刚体的理想接触时间约 0.259381 s，
理想接触前竖直速度约 −2.544524 m/s；实际结果受积分、接触偏置及接触模型影响。
每引擎两种步长 2 ms、1 ms，各重建场景重复三次，共六组。

| 引擎 / Engine | 命令选项 / Option | 执行方式 / Execution | 环境 / Environment |
|---|---|---|---|
| PhysX | `physx` | Isaac Sim / PhysX CPU TGS，float32 | `.venv` + 已有 Docker 镜像 |
| Newton / MuJoCo-Warp | `mujoco-warp` | 直接 MuJoCo-Warp CUDA，float32 | `.venv-warp` |
| MuJoCo CPU | `mujoco-cpu` | CPU，float64 | `.venv` |
| Genesis | `genesis` | CUDA，float64 | `.venv-genesis` |

Newton / MuJoCo-Warp 沿用直接 MuJoCo-Warp 路径；安装方法见 [四引擎部署文档](../README.md)。
MuJoCo/Warp 使用已配置的软接触，Genesis 使用其原生接触模型，PhysX 使用硬接触。
这些参数由项目选定；峰值力、穿透及回弹的差异不能直接当作准确性排名。

## 无界面：每引擎一条命令 / Headless commands

以下输出目录须尚不存在。新一轮可将 `01` 改为 `02`；也可省略 `--output` 自动生成新目录。

```bash
.venv/bin/physics-bench run --engine physx --scene drop --headless --output results/drop-physx-01
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene drop --headless --output results/drop-warp-01
.venv/bin/physics-bench run --engine mujoco-cpu --scene drop --headless --output results/drop-cpu-01
.venv-genesis/bin/physics-bench run --engine genesis --scene drop --headless --output results/drop-genesis-01
```

默认每引擎六组；`--repeats N` 可修改重复数，`--config 路径` 可换配置。
PhysX 使用已有镜像，`--pull=never`，仓库只读挂载，结果由宿主写入。

## 有界面：每引擎一条命令 / GUI commands

下面两种步长各执行一次，自动保存新结果目录；改成 `--repeats 3` 即完整六组。

```bash
.venv/bin/physics-bench run --engine physx --scene drop --viewer --repeats 1
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene drop --viewer --repeats 1
.venv/bin/physics-bench run --engine mujoco-cpu --scene drop --viewer --repeats 1
.venv-genesis/bin/physics-bench run --engine genesis --scene drop --viewer --repeats 1
```

需要桌面显示和 OpenGL。窗口显示所选引擎的真实测量状态，镜头覆盖释放高度到地面，
文字显示时间、Z 高度（m）、Z 速度（m/s）和 Z 接触力（N）。
统一渲染模型不执行物理步进；四个引擎的窗口都使用独立进程。
显示隔离避免 GUI 同步拖慢采样，Genesis 还借此隔离 EGL/GLFW。
显示进程合并积压帧、显示最新测量状态；物理逐步采样全部保存在原始 CSV，最终显示姿态另行核对。
默认 `--viewer-speed 0.2` 五倍慢速，`--viewer-hold 2` 结束保持两秒；物理步长和采样不变。
收到首个物理步后才开窗口，CUDA 编译或容器初始化期间请看终端状态。
按 Ctrl+C 或关闭正在计算的窗口会保存部分数据及中断记录，停止后续组，退出码 130。
渲染增加的时间不用于性能比较。

## 最后汇总 / Compare saved results

先完成四个独立引擎，再运行一条汇总命令。汇总读取已有数据，不重新运行物理引擎。
四个输入必须使用完全相同的配置和实验覆盖。

```bash
.venv/bin/physics-bench compare \
  results/drop-physx-01 \
  results/drop-warp-01 \
  results/drop-cpu-01 \
  results/drop-genesis-01 \
  --output results/drop-comparison-01
```

| 文件 / File | 内容 / Contents |
|---|---|
| `report.md` | 中英文碰撞及静置表、测量定义与曲线 |
| `metrics_bilingual.md` / `.csv` | 各次指标名称、英文名称、单位、状态和完整数值 |
| `metric_stats_bilingual.csv` | 仅通过运行的均值、总体标准差、极值与有效值次数 |
| `metric_definitions.md` / `.json` | 中英文名称与单位字典 |
| `drop.png` | 高度、竖直速度、法向力、穿透、线速度和角速度六幅曲线 |
| `drop/dt_*/repeat_*/raw.csv` | 单引擎逐步状态、接触力、冲量及参考自由落体采样 |
| `drop/dt_*/repeat_*/viewer.json` | 有界面显示帧数、播放速度、最终显示姿态及显示进程退出码 |
| `runs.json` / `summary.csv` | 单引擎运行记录 / 机器可读指标；对比汇总保留失败状态 |
| `config.json` / `environment.json` | 单引擎配置、环境和源码指纹 |
| `imported.json` / `sources.json` | 各组模型回读 / 对比的来源与版本 |

表和曲线用首次重复，统计用全部通过重复；失败及中断仍保留，未测得为空而不是零。
CSV 数值列保持原始精度，显示列采用双语布尔值和缺失值说明。

## 指标口径 / Metric definitions

- 自由落体参考：`z=h₀−gt²/2`、`vz=−gt`，只在首次接触前计算误差。原始采样包含对应参考值与有效段标记。
- 首次接触：接触合力大于 `1e-9 N` 的首个步初时间；碰撞前竖直速度取同一步初 `vz`。
- 回弹：首次接触之后所有记录状态中的最大正向竖直速度；不据此估计材料恢复系数。
- 穿透：按实际姿态计算最低顶点相对地面深度，包含步初和步末；峰值力不平滑。
- 刚体静置：质心线速度小于 `0.001 m/s`，角速度乘半对角线也小于 `0.001 m/s`，
  前一步法向支撑力大于 `1e-9 N`，并要求此后全部记录状态持续满足。本配置角速度阈值约 `0.0288675 rad/s`。
- 原 `质心静置时间 / COM settling time` 只检查三轴线速度，继续保留；
  新 `刚体静置时间 / Rigid-body settling time` 包含转动与支撑，另存静置后观察时长。
- 末段平均支撑力：最后 40 ms 的法向力时间平均，包含零接触力步骤，窗口须全部位于首次接触之后。
  平均力除以重力 `mg=0.981 N` 得到支撑力与重力比。
- 动量平衡：接触冲量与重力共同核算，最大允许残差 `5e-6 N·s`。
  PhysX 力由原生法向和摩擦冲量除以步长获得。

运行“通过”表示参数、有限性、引擎警告和动量校验通过；“记录时长内刚体已静置”是独立布尔指标。
仿真结束仍在运动时，静置时间为未测得，报告不能宣称已经静止。
结论只覆盖记录时长，静置后观察时长用于说明持续观察了多久。
界面运行还检查窗口资源正常关闭与显示进程退出码；退出错误会记录失败并保留采样。

本轮实测目录为 `results/task04-drop-20261010/`；完成记录见 [下落实验验收](validation-task04-drop.md)。
