# 我做这个实验对比
## 任务
'/home/datamesh/github_waneta/physics-engine-benchmark/.talisman/dev_docs/2026-10/机器人仿真物理引擎对比 — MuJoCo‑Warp  Genesis  PhysX 1.md'
我也想测试这实验对比，应该怎么做？

## 2026-10-08归档
可以。**建议先复现三个基础刚体实验，再加入机械臂和 GPU 性能测试。** 这样每一步都能确认配置是否正确。

我读了这份[实验文档](</home/datamesh/github_waneta/physics-engine-benchmark/.talisman/dev_docs/2026-10/机器人仿真物理引擎对比 — MuJoCo‑Warp  Genesis  PhysX 1.md>)，也检查了当前仓库：目前只有文档，没有可直接运行的 benchmark 代码。

**1. 先确定复现目标**

有两种目标，准备工作不同：

- **复现原文数值**：需要作者的场景资产、完整参数、控制器、代码版本和力测量实现。当前转载丢失了部分公式和参数，不能仅凭它精确复现。
- **在自己的机器上做同类对比**：可以自行搭建统一测试框架，记录与原文的配置差异。这是目前可以开始的路线。

**2. 先跑通 CPU 基线**

当前环境是 Ubuntu 22.04、约 32GB 内存，有 `uv`；但 `nvidia-smi` 报告无法与 NVIDIA 驱动通信。**MuJoCo CPU 可以先做，GPU 实验需要先确认显卡及驱动可用。**

可以先建立独立环境：

```bash
cd /home/datamesh/github_waneta/physics-engine-benchmark

uv venv --python 3.12 .venv-mujoco
uv pip install --python .venv-mujoco/bin/python mujoco numpy matplotlib

.venv-mujoco/bin/python -c \
  "import mujoco; print(mujoco.__version__)"
```

这是环境检查，尚未运行实验。安装成功后记录依赖版本；正式复现时，再按作者版本锁定。

**3. 第一轮只做这三个场景**

| 场景 | 文档中的设置 | 要比较的指标 |
|---|---|---|
| 滑块停止 | 100g、边长4cm；步长2ms和1ms | 停止距离、质心高度、接触力和冲量 |
| 方块下落 | 同一方块，质心高度35cm，运行1s；步长1ms和2ms | 高度、速度、穿透深度、碰撞冲量、静置时间 |
| 单铰链摆动 | 1kg、长30cm、宽4cm，初始角0.5rad；0.1–0.2s施加0.2N·m | 角度和角速度、相对参考ODE的误差 |

滑块的初速度、摩擦系数等仍需从完整配置确认；自行选择时应明确标记。

先在 MuJoCo CPU 中实现，再把**相同的场景定义**接到其他引擎。每次导入后，回读质量、惯量、关节轴、阻尼和 `armature`，不能只检查源文件。

**4. 再逐个加入引擎**

建议顺序是：

**MuJoCo CPU → MuJoCo‑Warp → Genesis → Isaac Sim/PhysX**

其中原文的 Newton 测试通过 MuJoCo‑Warp 求解器运行；直接使用 MuJoCo‑Warp 可作为起步，但需标记这个实现差异。[MuJoCo‑Warp 官方仓库](https://github.com/google-deepmind/mujoco_warp)、[Newton 安装说明](https://github.com/newton-physics/newton/blob/main/docs/guide/installation.rst)。

各引擎使用独立环境。Genesis 按官方流程先安装匹配平台的 PyTorch，再安装 `genesis-world`。[Genesis 官方说明](https://genesis-world.readthedocs.io/en/latest/)。

注意：**原文刚体 PhysX 使用 Isaac Sim 的 CPU TGS 配置；GPU 吞吐实验只比较 MuJoCo‑Warp 和 Genesis。** 不应把它们合并成一组速度排名。

**5. 统一输出和比较方法**

每个场景至少独立重跑3次，并增加步长减半的对照。保存：

- 完整配置、软件版本和硬件信息。
- 每个物理步的位姿、速度、接触力或冲量。
- 失败原因和原始数据。
- 汇总指标及叠加曲线。

尤其要统一力的坐标系、作用对象和采样时刻。若引擎返回冲量，换算单步平均力时用 `F = J / Δt`，并保留原始冲量。**峰值力必须和固定时间窗口内的总冲量一起比较**，否则步长变化可能造成误判。

这三个场景验证通过后，再做 Panda 无接触运动、统一力矩控制器、推物和抓取，最后加入软体实验。吞吐测试单独进行：关闭渲染、排除编译和预热、计时前后同步 GPU，并报告总环境步数/秒和显存占用。

对这个仓库，合适的第一个里程碑是：**跑通三个 MuJoCo CPU 场景，导出原始数据和曲线，再接入第二个引擎。**

## 2026-10-08 实施与验收

已将上文的第一个里程碑实现并在本机跑通：三个 MuJoCo CPU 基础场景，
每场景两种步长、每组独立重复三次，共 18/18 组通过；14 项测试通过。

新增内容：`src/physics_benchmark/`、`configs/baseline.json`、`tests/`、
`pyproject.toml` 和 `uv.lock`。完整使用说明见 `docs/benchmark.md`，
实测指标及环境见 `docs/validation-2026-10-08.md`。

```bash
# 当前环境已安装，可直接运行；每次创建新的结果目录
.venv/bin/physics-bench run

# 只跑一个场景
.venv/bin/physics-bench run --scene drop --repeats 3
```

本次结果入口：`results/task01-cpu-baseline/report.md`，包含三张步长对照曲线。
原始数据、每次指标、参数回读、配置、环境和重复性记录均已保存。
同一配置三次重复的数值采样完全一致。

1 ms 下滑块停止距离约 126.960 mm；下落峰值接触力约 53.441 N，
40 ms 竖直接触冲量约 0.30341047 N·s；铰链最大角误差约 0.083903°，
0.5 ms 时约 0.041896°。

环境更新：当前 GPU 可识别为 RTX 4090 D，驱动 570.211.01。
本次 MuJoCo 3.15.0 / CPU / float64，和转载文档中的版本不同；
原文缺失参数已显式标注自选，不能将此结果宣称为原文精确复现。
MuJoCo-Warp、Genesis、PhysX、机械臂、GPU 吞吐和软体实验仍属于后续阶段。


### 2026-10-08 Ctrl+C 中断处理修复

用户输出中的 `^C` / `KeyboardInterrupt` 表示收到终端中断；
堆栈停在 `data.warning` 的检查行不等于引擎报告了物理错误。

已补充：启动打印输出目录；仿真或指标阶段中断时保存当前原始采样，
将本次标记为 `interrupted`，保存 `interruption.json`，停止后续运行，
生成明确标注不完整的部分报告并返回 130。中断时跳过绘图，不输出异常堆栈。
正常运行依然完成全部 18 组并生成曲线。目前没有断点续跑功能。

验收：17 项测试、Ruff 检查、默认 18/18 组实验通过；
真实 SIGINT 子进程检查通过（退出 130、无堆栈、已有数据和部分报告保留）。
正常回归报告：`results/20261008T073238Z-98f91469/report.md`。

`run` 默认为无窗口批量计算，不会弹出三维仿真窗口。
