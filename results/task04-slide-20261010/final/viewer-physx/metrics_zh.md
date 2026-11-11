# 中文指标明细

全部重复与失败见 metrics_zh.csv；按引擎/步长的通过运行统计见 metric_stats_zh.csv。
标准差为总体标准差（ddof=0），重复不加随机扰动，不用于估计置信区间。
空值表示未测得；无量纲单位为1。失败指标仅供诊断，不进入通过运行的统计。

| 引擎 | 场景 | 步长(ms) | 重复 | 状态 | 指标名称 | 单位 | 数值 |
|---|---|---:|---:|---|---|---|---:|
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 仿真步长 | s | 0.002 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 物理步数 | 步 | 300 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 峰值接触合力 | N | 1.05657078 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 峰值法向接触力 | N | 0.981094083 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 最大穿透深度 | m | 3.21252958e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 首次接触时间 | s | 0 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 质心静置时间 | s | 0.256 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 最大动量平衡残差 | N·s | 5.1070518e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 最大接触力核算误差 | N | 未测得 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量X | N·s | -0.0156959915 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量Y | N·s | 8.86919515e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量Z | N·s | 0.0392399923 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 停止时间 | s | 0.256 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 停止距离 | m | 0.126424491 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 最终X位移 | m | 0.126424491 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 最大质心抬升 | m | 3.27825546e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 滑动段测量步数 | 步 | 107 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 滑动窗口内有接触步数 | 步 | 107 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 滑动段平均摩擦力 | N | 0.392399915 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 滑动段平均法向力 | N | 0.981000113 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 实测等效摩擦系数 | 1 | 0.399999867 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 滑动段平均X减速度 | m/s² | 3.92400359 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 全程X接触冲量 | N·s | -0.100000034 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000996507575 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000843860393 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 9.466341e-06 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 最大侧向偏移 | m | 2.18749875e-07 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 1 | 通过 | 停止距离相对理想值偏差 | % | -0.782059145 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 仿真步长 | s | 0.001 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 物理步数 | 步 | 600 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 峰值接触合力 | N | 1.05657038 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 峰值法向接触力 | N | 0.98121482 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 最大穿透深度 | m | 3.21120926e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 首次接触时间 | s | 0 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 质心静置时间 | s | 0.255 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 最大动量平衡残差 | N·s | 5.82886485e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 最大接触力核算误差 | N | 未测得 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量X | N·s | -0.0156959917 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量Y | N·s | 3.57673681e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量Z | N·s | 0.0392399929 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 停止时间 | s | 0.255 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 停止距离 | m | 0.126917973 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 最终X位移 | m | 0.126917869 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 最大质心抬升 | m | 3.27825546e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 滑动段测量步数 | 步 | 213 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 滑动窗口内有接触步数 | 步 | 213 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 滑动段平均摩擦力 | N | 0.39239991 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 滑动段平均法向力 | N | 0.981000102 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 实测等效摩擦系数 | 1 | 0.399999867 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 滑动段平均X减速度 | m/s² | 3.92404867 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 全程X接触冲量 | N·s | -0.0999987984 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000503130128 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000425809125 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 1.18099351e-05 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 最大侧向偏移 | m | 5.67842804e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 1 | 通过 | 停止距离相对理想值偏差 | % | -0.394774663 |

滑动段测量窗口：首次接触之后排除启动阶段 40 ms；步初水平速度 > 0.01 m/s。平均力与减速度包含离地步的零接触力。
实测等效摩擦系数 = Σ(水平接触力模长×dt) / Σ(法向力×dt)，系数仅使用窗口内法向力 > 1e-9 N 的接触步；无有效接触时为未测得。
理想参考为水平刚性平面上的纯平移库仑模型：a=μg，v=max(v₀−at,0)，x=v₀t−at²/2（停止后保持）；不含接触启动、转动或软接触，轨迹误差用于观察模型差异。
停止时间使用|vx|低于配置阈值且此后所有采样保持低于阈值的首个时刻；停止距离取该时刻X位移。所有指标仅覆盖已记录时长。
