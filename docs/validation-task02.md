# task02 验收记录：2026-10-08

剩余三个引擎均已接入并实测：MuJoCo-Warp、Genesis、Isaac Sim/PhysX 各 18/18 组通过；
另重新运行 MuJoCo CPU 18/18 组，共 72 组、64,800 个物理步。22 项 pytest 测试与 Ruff 检查通过。
每个引擎覆盖三个场景、每场景两个步长、每组独立重复三次。通过表示运行与测量校验通过，不代表实物准确性排名。

完整叠图、逐组指标及来源：[四引擎报告](../results/task02-comparison/report.md)。
环境安装与复跑命令：[多引擎说明](multi-engine.md)。results/ 不入 Git，本文保留关键数字以供查阅。

## 1 ms 下的第一轮重复

| 引擎 | 滑块停止距离 (mm) | 下落峰值合力 (N) | 下落 40 ms Jz (N s) | 最大穿透 (mm) | 铰链最大角误差 (°) |
|---|---:|---:|---:|---:|---:|
| MuJoCo CPU | 126.960411 | 53.441377 | 0.30341047 | 7.567368 | 0.083903 |
| MuJoCo-Warp | 126.960427 | 53.440929 | 0.30340982 | 7.567287 | 0.083899 |
| Genesis | 126.960671 | 53.441377 | 0.30341047 | 7.567368 | 0.083903 |
| Isaac Sim / PhysX | 126.917973 | 255.058203 | 0.29331836 | 0.302228 | 0.084013 |

MuJoCo CPU、Warp 和 Genesis 的下落与铰链输出接近；滑块停止距离接近，但瞬态接触力与质心高度有差异。
Genesis 的滑块接触合力较平滑，MuJoCo CPU/Warp 出现明显瞬态波动，完整曲线已保留。
PhysX 下落峰值从 2 ms 的约 127.53 N 增加至 1 ms 的约 255.06 N，而 40 ms 接触冲量只从约 0.29234 变为 0.29332 N s。
这是必须同时看步长、峰值、冲量及接触模型的例子；不能仅凭峰值或穿透大小给引擎排名。

## 校验与重复性

所有自由体逐步动量残差均低于共同容差 5e-6 N s。各引擎所有组中的最大值：

| 引擎 | 最大动量残差 (N s) | 结果目录 |
|---|---:|---|
| MuJoCo CPU | 1.46170299e-09 | [task02-cpu](../results/task02-cpu/report.md) |
| MuJoCo-Warp | 2.15792418e-07 | [task02-warp-validated](../results/task02-warp-validated/report.md) |
| Genesis | 5.86457966e-14 | [task02-genesis](../results/task02-genesis/report.md) |
| Isaac Sim / PhysX | 5.82886485e-08 | [task02-physx](../results/task02-physx/report.md) |

每组导入校验包含质量、惯量、质心、初始状态及关节/接触设置的回读。PhysX 保存实际 USD；Warp 额外回读 GPU 数组。
各引擎铰链角误差均低于 0.15°，步长由 1 ms 减半后误差约减半；力矩冲量均为 0.02 N m s。
CPU、Genesis、PhysX 的三次重复逐列完全一致。Warp 滑块两种步长存在微小差异：
最大 x 位移样本差约 4.47e-8 m，最大合力样本差约 3.79e-5 N；下落和铰链重复完全一致。
这些结论只适用于本次配置、版本和设备，不构成一般确定性保证或置信区间。

## 环境及实现边界

本机 RTX 4090 D，驱动 570.211.01。MuJoCo / MuJoCo-Warp 3.15.0、Warp 1.16.0；
Genesis 1.4.3、PyTorch 2.8.0；Isaac Sim 本地 6.0.1 镜像，内部 VERSION 为 6.0.1-rc.7+release.42383.32955d8d.gl。
版本固定在 uv.lock、requirements/warp.lock、requirements/genesis.lock，并在运行结果中保存实际环境和代码指纹。
可选依赖锁文件由已安装依赖闭包生成，验证过依赖版本约束；不包含 Genesis 初期复用环境中无关的 IsaacLab/RL 包。
没有修改原 Conda 环境、系统驱动或其他运行中的容器。

Warp 使用直接 CUDA 后端，与原文 Newton 包装路径有差异。Genesis 为 CUDA float64；Warp 为 float32。
PhysX 为 CPU TGS / float32，硬接触无法与 solref/solimp 一一对应；不是 GPU PhysX 性能测试。
未覆盖 Panda、软体和吞吐量，未取得作者完整资产和配置，因此不宣称原文精确复现。

## 调试失败记录

以下试跑失败均保留；最终 72 组是修复后完整执行的四套实验，不是从试跑中挑选成功样本。

- [PhysX 初始化失败](../results/20261008T083959Z-81ca84f6/report.md)：Isaac Sim 6 的 stage 绑定与旧接口不同，改用 World 创建的物理视图。
- [PhysX 动量失败](../results/20261008T094452Z-37e99092/report.md)：接触事件只有法向冲量；补上原生摩擦冲量后通过，不改大容差。
- [Genesis 接触接口失败](../results/20261008T092719Z-aca13888/report.md)：PyTorch 2.7 的 gather 不接受该索引类型；升级至 2.8.0 后通过。

## 可复查产物

各组目录包含 raw.csv、imported.json、metrics.json、scene.xml；PhysX 另有 scene.usda。
各引擎目录包含 config.json、environment.json、runs.json、repeatability.json、summary.csv 与曲线。
跨引擎目录包含统一 summary.csv、sources.json 和三张叠图，已检查图像显示。
