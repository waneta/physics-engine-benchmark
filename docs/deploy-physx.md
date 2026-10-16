# Isaac Sim / PhysX 环境部署

本项目复用本机 `nvcr.io/nvidia/isaac-sim:6.0.1` 镜像，通过 JSON 管道驱动原生 PhysX。刚体使用 CPU TGS、float32；软体使用 GPU TetMesh。宿主无需安装 Isaac Sim 或 Isaac Lab。

## 前提与检查

需要可用 NVIDIA GPU、Docker、NVIDIA Container Toolkit、现有 Isaac Sim 镜像及仓库 CPU Python 环境。以下命令在仓库根目录执行。

```bash
nvidia-smi
docker info
docker image inspect nvcr.io/nvidia/isaac-sim:6.0.1 --format '{{.Id}}'
uv sync --locked --python 3.11
.venv/bin/physics-bench doctor
```

本机已验证镜像 ID 为 `sha256:783444c706538aa76cf5126e911ddc5e618779e6105305ad4af4260362a30aa9`。镜像需预先可用；适配器使用 `--pull=never`，不会隐式下载。容器以只读方式挂载仓库，结果由宿主进程保存。

## 运行

```bash
.venv/bin/physics-bench run --engine physx
.venv/bin/physics-bench extended rigid --engine physx --output results/my-physx-rigid
.venv/bin/physics-bench extended soft --engine physx --output results/my-physx-soft
.venv/bin/physics-bench extended tuning --engine physx --output results/my-physx-tuning
```

若使用另一已有镜像，设置 `PHYSICS_BENCH_ISAAC_IMAGE`；更换版本后需要重新验证接口和实验。

```bash
PHYSICS_BENCH_ISAAC_IMAGE=nvcr.io/nvidia/isaac-sim:6.0.1 \
  .venv/bin/physics-bench run --engine physx
```

启动时会创建名字以 `physics-bench-` 开头的容器。Ctrl+C 或连接失效后仅清理本次创建的容器，不处理其他服务。原生日志保存在 `.cache/logs/`；各结果记录实际镜像 ID、USD 场景和参数回读。

## 故障定位与验收

- `permission denied ... docker.sock`：当前执行会话不能访问 Docker；在具有相应权限的宿主终端重试。不要把它解释为物理失败。
- `I/O operation on closed file`：早期批次存在失效连接复用问题。当前适配器会使错误连接失效，下一试验创建新工作进程；旧冻结源码仍保留旧行为，应使用新批次验证修复。
- 软体节点翻转：记录第一次翻转并停止，不能补齐为成功轨迹。

刚体接触力必须包含接触报告的法向冲量及 tensor 接口的摩擦冲量。软体刚体探针返回零不代表软体载荷为零；未完成独立力校验的软体反力发布为 `null`。

本项目没有可与 Warp/Genesis GPU 批量吞吐直接比较的 PhysX 性能入口。详见 [多引擎说明](multi-engine.md) 和 [完整实验说明](full-experiments.md)。
