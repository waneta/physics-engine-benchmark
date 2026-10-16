# repo memory

- 当前已验证四引擎的三个基础场景，各 18 组；不是作者数值精确复现。
- 参数与来源在 configs/baseline.json；uv.lock 及 requirements/*.lock 锁定依赖。
- 力的坐标、作用对象和时间步必须对齐；以方块线动量残差检查采样。
- 使用有限截面刚体摆 ODE 参考，不能用质点单摆惯量替代。
- 仿真输出创建新目录并保留失败，不覆盖旧结果；results/ 不入 Git。
- 2026-10-08 已验证 RTX 4090 D / 570.211.01 上的 Warp 1.16 与 Genesis 1.4.3 CUDA 后端。
- Genesis 接触接口使用 PyTorch 2.8；不要复用旧版 2.7 的 gather 行为。
- 用户选择 Isaac Sim/PhysX 路径。本地镜像 nvcr.io/nvidia/isaac-sim:6.0.1 可用，使用 CPU TGS。
- PhysX 接触报告只含法向冲量，需另加 tensor friction impulse；使用 World 的现有物理视图。
- Warp 滑块重复有微小差异，不能把全部 GPU 实验称为逐位确定。

已验证命令：`.venv/bin/physics-bench run`、`.venv/bin/pytest -q`、
`.venv/bin/ruff check src tests scripts`；多引擎命令见 docs/multi-engine.md。
本次对比入口：results/task02-comparison/report.md；验收记录：docs/validation-task02.md。

- 2026-10-09 插销原笛卡尔控制在无接触时漂移，已补零空间姿态反馈；修复前插销不得混入新矩阵。
- 单次复用观测可能用于多个矩阵用途，provenance保存原始SHA与环境；不能当作独立重复或清除力核算失败。
- Genesis 1.4.1 要求 Quadrants 1.3.0，隔离补跑锁为 requirements/genesis-recovery.lock；旧1.4.3结果保留。
- 宿主Popen即使start_new_session也在会话切换时退出。长跑用临时用户级 systemd 服务托管，串行PhysX和软体，准确性完成后才测吞吐。


- task04 滑块入口为 `run --scene slide`，`--headless`默认，`--viewer`实时显示测量状态。
- Genesis 1.4.3 的离屏 EGL 与同进程 MuJoCo GLFW 窗口在构建/清理时冲突；显示改用 spawn 独立进程，不能吞掉清理错误冒充通过。
- 平均摩擦力必须包含滑动测量窗口内离地步的零接触力；等效μ按有接触步积分Ft/Fn，不能仅平均接触步的力后与mg比较。
- 中文指标文件为 metrics_zh.csv/md、metric_stats_zh.csv、metric_definitions.json；库仑参考用于模型差异观察，不是准确性排名。


- task04补充要求中英文并列，优先使用 metrics_bilingual.md/csv 和 metric_stats_bilingual.csv；旧metrics_zh文件名继续生成。
- 双语导出使用已有24组滑块结果，来源及原文件SHA-256保存在 results/task04-slide-20261010/bilingual/export_manifest.json；数值与历史结果不可因翻译而改动。


- task04 下落入口为 `run --scene drop`；四引擎逐个选择 `--headless` 或 `--viewer`，命令见 docs/single-drop.md；本轮24/24无界面、8/8界面验收见 docs/validation-task04-drop.md。
- 下落刚体静置必须包含COM线速度、角速度×半对角线及原生法向支撑；记录持续满足至采样末尾的起点与观察时长，不把原COM静置时间当作完整刚体静置。
- 四引擎统一spawn显示进程，只显示真实测量状态、不步进；积压显示帧可合并，原始物理步骤全部保留。
- MuJoCo被动显示线程是daemon，关闭后须等待窗口destroy再回传finished；父进程检查退出码，GLX清理失败不能凭采样passed算作界面验收。viewer.json保存最终显示姿态及显示退出码。
- 本轮GUI与headless逐步数值完全一致；这只是当前下落批次结果，不扩大为全部GPU场景的逐位确定性保证。
