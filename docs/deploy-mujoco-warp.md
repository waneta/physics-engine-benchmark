# MuJoCo-Warp CUDA 环境部署

本项目直接调用 MuJoCo-Warp 3.15.0，使用 Warp 1.16.0、CUDA 和 float32。该路径与原文的 Newton 包装路径不同；Newton/VBD 软体使用另一独立环境。

## 前提与安装

以下命令在仓库根目录执行。需要可用 NVIDIA GPU、驱动、Python 3.11 和 uv。本机验收使用 RTX 4090 D、驱动 570.211.01。

```bash
nvidia-smi
uv venv --python 3.11 .venv-warp
uv pip install --python .venv-warp/bin/python -r requirements/warp.lock
.venv-warp/bin/python -c 'import mujoco_warp, warp; print(mujoco_warp.__version__, warp.__version__); warp.init(); print(warp.get_device("cuda:0"))'
```

锁文件包含本项目的可编辑安装。不要随意升级 Warp；新版本的 CUDA 驱动要求可能不同。若 GPU 在隔离执行会话不可见，先在宿主终端执行 `nvidia-smi`，确认是会话限制还是宿主故障。

## 运行

```bash
.venv-warp/bin/physics-bench run --engine mujoco-warp
.venv-warp/bin/python -m physics_benchmark.extended.suite rigid --engine mujoco-warp --output results/my-warp-rigid
.venv-warp/bin/python -m physics_benchmark.extended.suite soft --engine mujoco-warp --output results/my-warp-soft
.venv-warp/bin/python -m physics_benchmark.extended.suite tuning --engine mujoco-warp --output results/my-warp-tuning
.venv-warp/bin/python -m physics_benchmark.extended.suite throughput --engine mujoco-warp --output results/my-warp-throughput
```

首次运行会编译 CUDA kernel，缓存写入项目 `.cache/warp/`。准确性实验包含逐步 GPU 回读，不可用其墙钟时间排名；吞吐入口另行预热、同步计时并验证轨迹。

## 验收与限制

基础实验已完成 18/18 组。复杂接触中的动量残差必须逐场景核查：`numerically_valid=true` 不能代替 `contact_force_validated=true`。没有合格训练候选时记录 `no_eligible_candidate`，不能放宽力校验门槛以选出控制器。

默认吞吐规模为 1、128、8192、32768、131072 环境。显存不足或轨迹校验失败必须保留，不发布估算速度。查看结果目录中的 `environment.json`、`audit`、`result.json` 和原始轨迹；完整约定见 [完整实验说明](full-experiments.md)。
