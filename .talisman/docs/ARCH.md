# ARCH

输入：`configs/baseline.json` 中的 SI 单位参数、步长、时长和来源假设。

| 模块 | 文件 | 职责 |
|---|---|---|
| 场景 | src/physics_benchmark/scenes.py | 校验配置、生成 MJCF、导入后核验 |
| 仿真 | src/physics_benchmark/simulation.py | 独立重建模型、同步采样力与起止状态 |
| 适配 | src/physics_benchmark/backends/ | Warp CUDA、Genesis CUDA、PhysX 容器客户端 |
| 采样 | src/physics_benchmark/sampling.py | 统一 SI 行格式、原生冲量和动量残差 |
| PhysX 进程 | scripts/isaac_worker.py | Isaac Sim USD 场景、原生 tensor 与接触接口 |
| 度量 | src/physics_benchmark/metrics.py | 物理指标、独立 ODE 参考 |
| 绘图 | src/physics_benchmark/plotting.py | 无窗口原始数据步长对照图 |
| 入口 | src/physics_benchmark/cli.py | 重复运行、环境记录、失败审计、报告 |
| 对比 | src/physics_benchmark/comparison.py | 校验输入配置、保留失败、跨引擎叠图 |

数据流：配置 → MJCF（PhysX 为 USD）→ 独立引擎状态 → 原始 CSV → 指标/重复性统计/曲线。
输出到新的 `results/` 子目录，禁止覆盖旧结果。
各后端使用独立 Python 环境；PhysX 复用本地 Isaac Sim 镜像，通过 stdin/stdout JSON 与宿主通信。
仓库只读挂载，结果由宿主写入；原生法向与摩擦冲量均保留。
可选后端只在选中时导入。共享 SI 参数和测量语义，明确记录接触模型与数值精度差异。

扩展实验由 `extended/model.py` 生成统一 Panda 和工装，固定 MuJoCo 3.15 逆动力学参考后交给各原生后端。`rigid.py` 负责 1 kHz 控制、参数/FK 校验和逐步记录；`soft*.py` 对接五条四面体路径；`suite.py` 定义刚体、训练、预留与交叉迁移矩阵。`throughput.py` 在独立进程内预热、同步计时及验证批量轨迹；`report.py` 从最新尝试生成覆盖与结果报告。`scripts/run_full_experiments.py` 冻结源码和资产，分配环境并保存运行状态，准确性任务结束后才启动吞吐。


task04 在各基础后端逐步采样后调用只读观察回调。`viewer.py` 用独立 MJCF 模型显示
测量状态，不步进显示模型；Genesis 使用 spawn 显示进程隔离 EGL/GLFW 生命周期。
`reporting.py` 维护中文名称与单位，生成逐次指标及仅通过运行的分组统计；
滑块曲线展示库仑参考、水平摩擦力、法向力与轨迹，仍保存原始 SI 采样。


双语展示由 `reporting.py` 的英文名称和单位字典集中定义，输出
`metrics_bilingual.md/csv`、`metric_stats_bilingual.csv`、`metric_definitions.json/md`。
兼容的 `metrics_zh.*` 仍生成，CSV原始数值与显示值分列，统计计算与物理采样保持原样。

单物体下落扩展沿用相同后端与观察回调。`drop_metrics` 从真实采样测量自由落体、
首次碰撞、向上速度、末段支撑及刚体静置；原质心静置指标保留，新判定增加角速度
乘半对角线的表面速度界限及法向支撑。`drop_report_lines` 输出碰撞/静置双语表，
`plot_drop` 绘制六幅曲线。显示相机覆盖释放点到地面，叠加Z高度、Z速度和Z接触力。

四引擎显示统一使用 spawn 子进程，避免宿主 GUI 同步拖慢实际采样。
显示子进程可合并连续积压测量消息，并保留 audit/finish 的顺序，核对最终姿态；
物理步骤的原始状态、力和冲量仍全部保存在宿主，未合并物理采样。

显示关闭时等待本次 MuJoCo daemon 渲染线程完成窗口销毁，再发送 finished 回执；
父进程检查子进程退出码，并保存到 viewer.json。渲染线程超时或非零退出均记录失败，
防止完整物理采样掩盖 GLX 清理错误。
