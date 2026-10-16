# task04 滑动方块验收记录

验收日期：2026-10-10（Asia/Shanghai）。当前任务只调整并验收滑动方块。

## 完成情况

- 四引擎无界面正式实验：24/24 组通过，每引擎两步长各三次独立重复，共10800物理步。
- 最终代码的三维界面验证：8/8 组通过，每引擎两步长各一次，共3600物理步。
- `pytest -q`：65项通过；`ruff check src tests scripts` 与 `git diff --check` 通过。
- 原有 MuJoCo CPU 三场景18/18组回归通过，数据保存在 `results/task04-slide-20261010/regression-cpu/`。
- 四引擎命令、参数、指标口径与输出格式见 [使用说明](single-slide.md)。

正式数据与中英文对比 / Bilingual results：[对比报告](../results/task04-slide-20261010/bilingual/comparison/report.md)、[中英文指标 / Bilingual metrics](../results/task04-slide-20261010/bilingual/comparison/metrics_bilingual.md)、[重复统计 / Repeat statistics](../results/task04-slide-20261010/bilingual/comparison/metric_stats_bilingual.csv)。

## 实际环境

- NVIDIA GeForce RTX 4090 D，显存24564 MiB，驱动570.211.01；桌面DISPLAY=:1。
- MuJoCo CPU 3.15.0；MuJoCo-Warp 3.15.0 / Warp 1.16.0，直接CUDA float32后端。
- Genesis 1.4.3 / Quadrants 1.3.3 / PyTorch 2.8.0，CUDA float64；本批次使用原 `.venv-genesis`，不混入1.4.1补跑环境。
- Isaac Sim 6.0.1 / PhysX CPU TGS、float32。镜像ID：`sha256:783444c706538aa76cf5126e911ddc5e618779e6105305ad4af4260362a30aa9`。
- 参数、软件包、代码指纹及模型回读分别保存于各引擎 `environment.json` 和各组 `imported.json`。

## 主要对比结果 / Key comparison results

以下为首次重复。全部重复和有效值数量保存在双语CSV；平均力包含滑动测量段内离地步的零力。
设定摩擦系数为0.4，理想停止距离127.420999 mm、理想停止时间0.254842 s。

| 引擎 / Engine | 步长 / Timestep (ms) | 实测摩擦系数 / Measured friction coefficient (1) | 平均摩擦力 / Mean sliding friction force (N) | 停止时间 / Stopping time (s) | 停止距离 / Stopping distance (mm) | 距离偏差 / Distance deviation (%) | 最大动量残差 / Maximum momentum residual (N·s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| PhysX（CPU TGS） | 2 | 0.39999987 | 0.39239991 | 0.256 | 126.424491 | -0.782059 | 5.10705e-08 |
| PhysX（CPU TGS） | 1 | 0.39999987 | 0.39239991 | 0.255 | 126.917973 | -0.394775 | 5.82886e-08 |
| MuJoCo-Warp CUDA | 2 | 0.39829974 | 0.38504517 | 0.260 | 126.459196 | -0.754823 | 9.25658e-08 |
| MuJoCo-Warp CUDA | 1 | 0.39927878 | 0.38086028 | 0.262 | 126.960471 | -0.361422 | 1.51856e-07 |
| MuJoCo CPU | 2 | 0.39829983 | 0.38504551 | 0.260 | 126.459227 | -0.754799 | 5.69567e-14 |
| MuJoCo CPU | 1 | 0.39927873 | 0.38085928 | 0.262 | 126.960411 | -0.361469 | 1.4617e-09 |
| Genesis CUDA | 2 | 0.39852328 | 0.39082509 | 0.260 | 126.452747 | -0.759884 | 5.72049e-14 |
| Genesis CUDA | 1 | 0.39898212 | 0.39134924 | 0.262 | 126.960671 | -0.361266 | 2.87214e-14 |

四引擎在本配置下的实测摩擦系数接近0.4，所有正式运行的滑动段摩擦力均与运动反向，动量残差均小于5×10⁻⁶ N·s。
步长减半后，停止距离更接近理想参考。MuJoCo CPU和Warp结果接近，接触初期存在小幅抬升与力波动；PhysX的硬接触曲线更平稳，Genesis的接触响应也有自身差异。
这些差异涉及接触模型、离散积分、参数与精度，不据此给出准确性或性能排名。

![四引擎摩擦与轨迹](../results/task04-slide-20261010/bilingual/comparison/slide.png)

## 界面与无界面逐步核对

界面使用所选引擎的真实测量状态，显示模型不执行物理步进。Genesis的窗口用spawn独立进程隔离EGL与GLFW，构建及清理均已通过。

最终界面结果目录：

- `final/viewer-final-mujoco-cpu/`
- `final/viewer-final-mujoco-warp/`
- `final/viewer-genesis-isolated/`
- `final/viewer-final-physx/`

目录均位于 `results/task04-slide-20261010/`。首次界面观察采用0.2倍速，最终CPU/Warp/PhysX窗口生命周期复核采用1倍速；物理dt不随显示速度改变。
各组 `viewer.json` 保存实际显示帧数及最终显示位置；[逐步核对结果](../results/task04-slide-20261010/final/viewer_equivalence.json)保存每项最大差值。

核对容差在最终复核前设定：位置1×10⁻⁶ m、四元数分量1×10⁻⁶、线速度1×10⁻⁴ m/s、角速度1×10⁻³ rad/s、接触力1×10⁻³ N、冲量1×10⁻⁶ N·s，停止时间差不超过一个物理步。
CPU、Genesis、PhysX界面与无界面各步数值逐列一致；Warp的float32 GPU归约有微小重复差异，界面核对全部在上述容差内。不声称GPU逐位确定。

## 保留的诊断与边界

- 首次PhysX批次 `results/task04-slide-20261010/physx/` 为5/6通过；首组容器应用初始化后被系统Killed，无采样。之后复用恢复的工作进程正常运行，正式 `final/physx/` 六组全部通过。日志不能单独证明终止原因。
- Genesis同进程窗口诊断分别保存于 `final/viewer-genesis/`、`final/viewer-genesis-lazy/`、`final/viewer-genesis-glfix/`；存在EGL初始化或清理错误，即使已采满物理步也标记失败。采用独立显示进程后两步长全部通过，未修改已安装引擎或吞掉清理异常。
- 单元测试覆盖理想参考、零摩擦、测量窗口、离地步统计、渲染状态隔离、窗口关闭与独立显示进程失败时保留物理采样。
- GUI需要桌面及OpenGL；默认无界面不启动实时窗口。PhysX仍在只读挂载仓库的已有容器中运行，宿主保存结果。
- 本次未调整下落或单铰链实验，也未恢复用户暂停的完整扩展补跑；CPU三场景运行仅用于回归。


## 补充信息验收：中英文展示（2026-10-10）

根据任务补充信息完善展示层：全部39种基础指标的名称均提供中文与可读英文，
覆盖滑块、下落及铰链；单位字典说明SI符号、计数、布尔值和无量纲量。
报告、CSV、指标字典和滑块曲线提供中英文对照；数字保留原值，缺失值和布尔值提供双语显示。

新版四引擎报告位于 `results/task04-slide-20261010/bilingual/comparison/`，
各引擎六组报告位于同级对应引擎目录。此次只重新导出先前的24组实测数据，未重新运行物理引擎。
原目录全部文件的SHA-256校验一致，新目录的原始CSV、运行记录、配置、环境和指标JSON也与来源逐字节一致；
来源、文件校验和导出代码指纹保存在 [导出清单](../results/task04-slide-20261010/bilingual/export_manifest.json)。

数值精度、失败剔除统计、英文名称、单位与双语布尔值展示均通过已有测试中的导出校验。
物理计算及实测结论保持原样，完整扩展补跑继续暂停。


## 本任务重新实测（2026-10-10）

用户要求重新运行滑动方块，已在新目录完成24/24组正式无界面及8/8组界面验证。
本页上述历史实测记录保留；新批次见 [重新实测验收](validation-task04-rerun-20261010.md)
及 [本轮中英文汇总](../results/task04-slide-rerun-20261010-1818/comparison/report.md)。
