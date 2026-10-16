# Genesis CUDA 环境部署

本项目基础及早期扩展实验使用 Genesis 1.4.3、PyTorch 2.8.0、CUDA 和 float64。与原文的 Genesis 1.4.1 有版本差异。以下命令在仓库根目录执行。

2026-10-09 补跑改用独立的 Genesis 1.4.1 / Quadrants 1.3.0 环境，固定依赖见 `requirements/genesis-recovery.lock`。原 1.4.3 环境与历史结果保留。两种版本的实验不能当作同一批次。

## 安装与检查

需要 Python 3.11、uv 和可用 NVIDIA GPU。先确认宿主驱动可用，再创建独立环境；不要改写已有 Conda 环境。

```bash
nvidia-smi
uv venv --python 3.11 .venv-genesis
uv pip install --python .venv-genesis/bin/python -r requirements/genesis.lock
.venv-genesis/bin/python -c 'import genesis as gs, torch; print(gs.__version__, torch.__version__); gs.init(backend=gs.cuda, precision="64", logging_level="warning"); print(gs.device)'
```

`requirements/genesis.lock` 固定当前 Linux x86_64 / Python 3.11 的完整依赖闭包。首次下载包含大型 CUDA/PyTorch 包，需要预留磁盘空间。不要只安装 `genesis-world` 后假设已有 PyTorch 版本兼容；本项目曾遇到 PyTorch 2.7 的接触接口索引类型错误。

现有本机 `.venv-genesis` 使用 Conda Python 的系统包可见模式，但新增包位于项目覆盖环境；完整独立复跑使用上述命令。

补跑版本的独立安装命令：

```bash
uv venv --python 3.11 .venv-genesis-recovery
uv pip install --python .venv-genesis-recovery/bin/python -r requirements/genesis-recovery.lock
PYTHONPATH=src .venv-genesis-recovery/bin/python -c 'import genesis as gs, importlib.metadata as m; print(gs.__version__, m.version("quadrants")); gs.init(backend=gs.cuda, precision="64", logging_level="warning")'
PYTHONPATH=src .venv-genesis-recovery/bin/python -m physics_benchmark.extended.suite rigid --engine genesis --output results/my-genesis141-rigid
```

本机为节约磁盘复用了原环境的已安装依赖，并在新的项目覆盖环境中安装 1.4.1 和 Quadrants 1.3.0；通过依赖闭包检查后生成上述锁文件。若从零部署，按锁文件安装即可，不需要创建本机的 `.pth` 路径。

## 运行

```bash
.venv-genesis/bin/physics-bench run --engine genesis
.venv-genesis/bin/python -m physics_benchmark.extended.suite rigid --engine genesis --output results/my-genesis-rigid
.venv-genesis/bin/python -m physics_benchmark.extended.suite soft --engine genesis --output results/my-genesis-soft
.venv-genesis/bin/python -m physics_benchmark.extended.suite tuning --engine genesis --output results/my-genesis-tuning
.venv-genesis/bin/python -m physics_benchmark.extended.suite throughput --engine genesis --output results/my-genesis-throughput
```

基础实验 18/18 组已完成。软体使用隐式 FEM/SAP，网格注入仅在构造期间生效，随后回读节点与单元；没有修改已安装的 Genesis 文件。共享 E/ν 不代表材料模型已经校准。

## 已知限制与验收

在本机 Genesis 1.4.3 / Quadrants 1.3.3 / 驱动 570.211.01 组合中，密集扫掠构建出现 `CUDA_ERROR_INVALID_PTX`。原生标量求解分支与 MuJoCo 兼容选项的独立诊断仍出现该错误。不能把这一环境故障解释为扫掠任务失败或引擎物理准确性结论；更换隔离版本后须重新验收并记录依赖。

1.4.1 / Quadrants 1.3.3 的诊断扫掠已完成 12.5 s 仿真，送入托盘 10/15 个物体，力核算未通过。随后依照 1.4.1 的包依赖要求改为 Quadrants 1.3.0，正式补跑重新执行整个 Genesis 矩阵；不能沿用该诊断作为正式版本的结果。

部分复杂接触场景未通过动量核算。结果中 `contact_force_validated` 或 `force_validated` 不是 true 时，不发布定量载荷比较。软体翻转保留失败帧，不能补齐轨迹。

吞吐独占实验 GPU 队列，计时前后同步，排除预热，并检验批量/单环境轨迹一致性。内存字段只表示记录的分配器口径，不等于整卡峰值。详见 [完整实验说明](full-experiments.md)。
