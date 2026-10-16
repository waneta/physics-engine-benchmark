# 单物体实验使用

完整参数、指标口径、中英文文件格式和汇总命令见 [使用说明](../../../docs/single-slide.md)。
四引擎实测与对比见 [验收记录](../../../docs/validation-task04.md)。

以下在仓库根目录执行，每次自动创建新结果目录。

## 无界面

```bash
.venv/bin/physics-bench run --engine physx --scene slide --headless
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene slide --headless
.venv/bin/physics-bench run --engine mujoco-cpu --scene slide --headless
.venv-genesis/bin/physics-bench run --engine genesis --scene slide --headless
```

## 有界面

```bash
.venv/bin/physics-bench run --engine physx --scene slide --viewer --repeats 1
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene slide --viewer --repeats 1
.venv/bin/physics-bench run --engine mujoco-cpu --scene slide --viewer --repeats 1
.venv-genesis/bin/physics-bench run --engine genesis --scene slide --viewer --repeats 1
```

默认无界面每引擎两步长各三重复；以上界面命令为各一次。
界面使用统一渲染器显示所选引擎的实时测量状态，默认0.2倍速，物理步长保持原值。
四引擎的窗口都运行于独立进程，隔离显示资源并避免积压显示帧拖慢采样。
需要桌面与 OpenGL；关闭计算中的窗口或 Ctrl+C 保存部分数据并中断。

本次正式对比报告：
[四引擎滑块结果](../../../results/task04-slide-20261010/bilingual/comparison/report.md)。
打开各输出的 `report.md`、`metrics_bilingual.md`、`metrics_bilingual.csv` 和 `metric_stats_bilingual.csv`
查看中英文名称、单位说明、数值及重复统计。

## 立方体下落、碰撞、静置

参数、测量口径、完整输出说明见 [下落使用说明](../../../docs/single-drop.md)。
无界面两步长各三重复；有界面命令为各一次，自动保存新目录。

```bash
# 无界面：逐个引擎执行
.venv/bin/physics-bench run --engine physx --scene drop --headless
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene drop --headless
.venv/bin/physics-bench run --engine mujoco-cpu --scene drop --headless
.venv-genesis/bin/physics-bench run --engine genesis --scene drop --headless

# 有界面：逐个引擎执行
.venv/bin/physics-bench run --engine physx --scene drop --viewer --repeats 1
.venv-warp/bin/physics-bench run --engine mujoco-warp --scene drop --viewer --repeats 1
.venv/bin/physics-bench run --engine mujoco-cpu --scene drop --viewer --repeats 1
.venv-genesis/bin/physics-bench run --engine genesis --scene drop --viewer --repeats 1
```

窗口显示 Z 高度、Z 速度及法向接触力，镜头覆盖释放位置和地面。
下落中英文报告另列碰撞时间、回弹、穿透、末段支撑力、包含转动的刚体静置时间及最终速度。

使用四次运行打印出的结果目录汇总，输出目录须尚不存在：

```bash
.venv/bin/physics-bench compare PhysX结果目录 Warp结果目录 CPU结果目录 Genesis结果目录 --output results/新的下落汇总目录
```

本轮结果：[四引擎下落中英文对比](../../../results/task04-drop-20261010/comparison/report.md)。
实测与界面核对见 [下落验收记录](../../../docs/validation-task04-drop.md)。
