# 单物体实验
## 概述
基于之前做的实验的基础上，改下测试的细节。
01 单物体（Single Objects）
验证摩擦力与运动轨迹。

01 Single objects
Validating friction & trajectories

## 任务

1.四种引擎，分别验证单物体的摩擦力与运动轨迹。
可以单个引擎进行验证，有界面和无界面两种选择，然后出测试结果。
PhysX
Newton / MuJoCo‑Warp
MuJoCo CPU
Genesis

单物体实验
1.滑动方块实验
2.立方体下落碰撞静置
3.单铰链测试

先完成单物体实验，滑动方块实验
下面四种引擎有界面和无界面命令，然后出测试结果。
PhysX
Newton / MuJoCo‑Warp
MuJoCo CPU
Genesis

可以一个一个引擎进行验证，然后出测试结果。最后汇总结果。进行对比。
汇总结果。各种指标名称，单位，值等，最好都有中文来表示。

2.补充信息
汇总结果，各种指标名称，单位，值等，最好都有中文和英文一起来表示。


## 验收记录（2026-10-10）

已完成本任务优先范围：单物体滑动方块实验。

- 四引擎支持逐个选择无界面计算或有界面观察，命令见 [单物体使用](task04_单物体使用.md) 和 [正式使用说明](../../../docs/single-slide.md)。
- 正式无界面24/24组通过：每引擎2 ms、1 ms各三次独立重复；最终界面8/8组通过。
- 新增中文摩擦系数、平均摩擦力、法向力、减速度、停止时间/距离、理想轨迹误差、动量残差及重复统计，均包含单位与实际值。
- CPU、Genesis、PhysX的有界面/无界面逐步数据一致；Warp微小float32差异在预设容差内。
- Genesis显示进程隔离已修复EGL冲突，先前诊断失败全部保留；PhysX首次容器启动失败也保留，正式重跑六组全部通过。
- 65项测试、Ruff及差异空白检查通过；CPU原三场景18/18组回归通过。
- 汇总报告：[四引擎滑块对比](../../../results/task04-slide-20261010/final/comparison/report.md)；环境、指标与限制详见 [验收实测记录](../../../docs/validation-task04.md)。

Newton / MuJoCo-Warp采用此前已验证的直接MuJoCo-Warp CUDA路径。
界面统一显示实际物理引擎的测量状态；Genesis窗口独立进程运行。
本次未调整下落、单铰链实验，未恢复已暂停的完整扩展补跑。


## 补充信息验收：中英文汇总（2026-10-10）

已完成第2条补充信息：报告、指标明细、重复统计、单位字典与滑块曲线均加入中英文对照。
例如“停止距离 / Stopping distance”，单位“m（米 / metre）”；
布尔值“是 / Yes、否 / No”，空值“未测得 / Not measured”。
数字使用通用阿拉伯数字，CSV原始数值列保留原精度。

- 双语指标目录覆盖39种基础指标；本次24组滑块实测导出792条明细、264条分组统计。
- [新版四引擎报告](../../../results/task04-slide-20261010/bilingual/comparison/report.md)
- [中英文指标明细](../../../results/task04-slide-20261010/bilingual/comparison/metrics_bilingual.md)
- [双语CSV](../../../results/task04-slide-20261010/bilingual/comparison/metrics_bilingual.csv)
- [双语统计CSV](../../../results/task04-slide-20261010/bilingual/comparison/metric_stats_bilingual.csv)
- [中英文指标与单位字典](../../../results/task04-slide-20261010/bilingual/comparison/metric_definitions.md)

仅根据已有实测重新导出展示，原始数据、配置、环境、指标JSON及历史结果均保留，
SHA-256校验全部一致，新旧对比summary.csv数值完全一致。
来源和导出代码指纹见 `bilingual/export_manifest.json`。
65项测试及Ruff检查通过；使用说明与验收文档已更新。


## 重新实测验收（2026-10-10 18:41:08，Asia/Shanghai）

按用户要求重新计算滑动方块：四引擎、两步长各三重复，正式24/24组通过；界面8/8组通过。
配置和物理代码沿用，所有界面采样差异在预设容差内，534个历史结果文件校验一致。
新增中英文792条指标明细、264条统计，65项测试及Ruff通过。
PhysX首轮末组超时、随后初始化中断均保留，最终新批次六组全部通过。

- [本轮四引擎中英文汇总](../../../results/task04-slide-rerun-20261010-1818/comparison/report.md)
- [执行命令、诊断和全部结果入口](../../../results/task04-slide-rerun-20261010-1818/report.md)
- [本轮验收记录](../../../docs/validation-task04-rerun-20261010.md)

本轮只重新计算滑动方块；其余实验继续保持暂停状态。


## 第4条验收：立方体下落碰撞静置（2026-10-10 19:45:08，Asia/Shanghai）

按用户请求继续立方体下落、碰撞、静置，四个引擎均可逐个选择有界面或无界面，一条命令生成各自结果，最后一条 compare 命令汇总。

- 新批次正式无界面24/24组通过：两步长2 ms、1 ms各三重复；最终界面8/8组通过。
- 32组均在1 s记录内达到包含转动及地面支撑的刚体静置；新增自由落体参考、碰撞步初速度、向上速度、末段支撑及静置后观察时长。
- 本轮最终八组界面/无界面原始数值完全一致，显示进程退出码均为0；全局字典56种，本场景32种指标，双语768条明细、256条统计。
- 修复显示同步拖慢采样及GLX清理错误；所有中断和中间诊断保留，只有 viewer-final-* 用于本轮界面验收。
- 77项测试、Ruff通过；CPU默认三场景18/18组回归通过，滑块对应首次重复原始数值一致；1130个历史滑块文件SHA-256不变。
- [四引擎双语汇总](../../../results/task04-drop-20261010/comparison/report.md)
- [逐引擎有界面、无界面及最终汇总命令](../../../docs/single-drop.md)
- [本轮执行、诊断和来源](../../../results/task04-drop-20261010/report.md) · [验收实测记录](../../../docs/validation-task04-drop.md)

本次只继续下落碰撞静置；单铰链新增验证留待后续，完整扩展补跑继续保持暂停。
