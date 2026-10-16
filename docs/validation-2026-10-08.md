# task01 CPU 基线验收（2026-10-08）

已完成 task01 归档中的第一个里程碑：三个 MuJoCo CPU 基础实验及其数据采集、指标和曲线。
尚未完成 MuJoCo-Warp、Genesis、PhysX 适配，不将本次结果称为完整跨引擎对比。

## 运行证据

- 18/18 组通过：三个场景 × 两种步长 × 三次独立重复，共 16200 个物理步。
- 同一配置三次重复的所有 CSV 数值列完全一致。
- 14 项 pytest 测试通过；Ruff 静态检查和格式检查通过。
- 三张曲线已查看，轴、图例、单位和步长对照正常。
- 方块实验最大每步动量残差约 1.462e-9 N·s，小于 5e-6 N·s 容差。

## 实际环境

- Python：3.11.0rc1 (main, Aug 12 2022, 10:02:14) [GCC 11.2.0]
- MuJoCo：3.15.0；NumPy：2.4.6；Matplotlib：3.11.2
- CPU：12th Gen Intel(R) Core(TM) i7-12700KF；逻辑 CPU：20；MemTotal:       32669132 kB
- GPU 检测：NVIDIA GeForce RTX 4090 D, 570.211.01, 24564 MiB
- 本次仿真使用 CPU / float64。GPU 检测成功不代表 GPU 仿真栈已验证。
- 原文记录的 MuJoCo 版本为 3.11.0；本次实际版本不同。缺失参数的自选值见配置 provenance。

## 实测结果（每组第一个重复）

| 场景 | 步长 | 结果 |
|---|---:|---|
| slide | 2 ms | 停止距离 126.459227 mm；最终位移 126.448590 mm；峰值力 10.531625 N |
| slide | 1 ms | 停止距离 126.960411 mm；最终位移 126.961965 mm；峰值力 9.532953 N |
| drop | 2 ms | 峰值力 58.257195 N；穿透 8.740610 mm；40 ms 竖直接触冲量 0.30554739 N·s |
| drop | 1 ms | 峰值力 53.441377 N；穿透 7.567368 mm；40 ms 竖直接触冲量 0.30341047 N·s |
| hinge | 1 ms | 相对 ODE 最大角误差 0.083903° |
| hinge | 0.5 ms | 相对 ODE 最大角误差 0.041897° |

停止距离取速度持续低于阈值的首个采样，最终位移取最后一帧；两者不同属于指标定义差异。
本次结果不能与原文数值直接当作相同配置比较，也不用于判断物理真实性。

## 结果入口

- [完整报告与曲线](../results/task01-cpu-baseline/report.md)
- [全部指标 CSV](../results/task01-cpu-baseline/summary.csv)
- [执行记录](../results/task01-cpu-baseline/runs.json)
- [重复性](../results/task01-cpu-baseline/repeatability.json)
- [使用说明及测量定义](benchmark.md)

原始结果保存在当前工作区，results/ 被 Git 忽略；分享或归档时需另行携带该目录。
报告里的源代码哈希记录生成时版本；生成后仅做了 import 排序，物理实现不变，14 项测试再次通过。

## 重新运行

```bash
.venv/bin/physics-bench run
.venv/bin/pytest -q
.venv/bin/ruff check src tests
```

安装时本地代理间歇性 TLS 超时，最终从清华 PyPI 镜像下载与 uv.lock 完全相同的 wheel，
逐一校验 SHA-256 后安装；`uv sync --locked --offline` 已通过。没有修改系统代理、驱动或全局 Python 环境。
