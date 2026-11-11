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
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 仿真步长 | s | 0.002 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 物理步数 | 步 | 300 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 峰值接触合力 | N | 1.05657078 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 峰值法向接触力 | N | 0.981094083 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 最大穿透深度 | m | 3.21252958e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 首次接触时间 | s | 0 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 质心静置时间 | s | 0.256 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 最大动量平衡残差 | N·s | 5.1070518e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 最大接触力核算误差 | N | 未测得 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量X | N·s | -0.0156959915 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量Y | N·s | 8.86919515e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量Z | N·s | 0.0392399923 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 停止时间 | s | 0.256 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 停止距离 | m | 0.126424491 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 最终X位移 | m | 0.126424491 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 最大质心抬升 | m | 3.27825546e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 滑动段测量步数 | 步 | 107 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 滑动窗口内有接触步数 | 步 | 107 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 滑动段平均摩擦力 | N | 0.392399915 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 滑动段平均法向力 | N | 0.981000113 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 实测等效摩擦系数 | 1 | 0.399999867 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 滑动段平均X减速度 | m/s² | 3.92400359 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 全程X接触冲量 | N·s | -0.100000034 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000996507575 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000843860393 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 9.466341e-06 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 最大侧向偏移 | m | 2.18749875e-07 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 2 | 通过 | 停止距离相对理想值偏差 | % | -0.782059145 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 仿真步长 | s | 0.002 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 物理步数 | 步 | 300 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 峰值接触合力 | N | 1.05657078 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 峰值法向接触力 | N | 0.981094083 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 最大穿透深度 | m | 3.21252958e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 首次接触时间 | s | 0 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 质心静置时间 | s | 0.256 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 最大动量平衡残差 | N·s | 5.1070518e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 最大接触力核算误差 | N | 未测得 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量X | N·s | -0.0156959915 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量Y | N·s | 8.86919515e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量Z | N·s | 0.0392399923 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 停止时间 | s | 0.256 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 停止距离 | m | 0.126424491 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 最终X位移 | m | 0.126424491 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 最大质心抬升 | m | 3.27825546e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 滑动段测量步数 | 步 | 107 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 滑动窗口内有接触步数 | 步 | 107 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 滑动段平均摩擦力 | N | 0.392399915 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 滑动段平均法向力 | N | 0.981000113 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 实测等效摩擦系数 | 1 | 0.399999867 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 滑动段平均X减速度 | m/s² | 3.92400359 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 全程X接触冲量 | N·s | -0.100000034 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000996507575 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000843860393 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 9.466341e-06 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 最大侧向偏移 | m | 2.18749875e-07 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 2 | 3 | 通过 | 停止距离相对理想值偏差 | % | -0.782059145 |
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
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 仿真步长 | s | 0.001 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 物理步数 | 步 | 600 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 峰值接触合力 | N | 1.05657038 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 峰值法向接触力 | N | 0.98121482 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 最大穿透深度 | m | 3.21120926e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 首次接触时间 | s | 0 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 质心静置时间 | s | 0.255 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 最大动量平衡残差 | N·s | 5.82886485e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 最大接触力核算误差 | N | 未测得 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量X | N·s | -0.0156959917 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量Y | N·s | 3.57673681e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量Z | N·s | 0.0392399929 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 停止时间 | s | 0.255 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 停止距离 | m | 0.126917973 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 最终X位移 | m | 0.126917869 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 最大质心抬升 | m | 3.27825546e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 滑动段测量步数 | 步 | 213 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 滑动窗口内有接触步数 | 步 | 213 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 滑动段平均摩擦力 | N | 0.39239991 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 滑动段平均法向力 | N | 0.981000102 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 实测等效摩擦系数 | 1 | 0.399999867 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 滑动段平均X减速度 | m/s² | 3.92404867 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 全程X接触冲量 | N·s | -0.0999987984 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000503130128 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000425809125 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 1.18099351e-05 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 最大侧向偏移 | m | 5.67842804e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 2 | 通过 | 停止距离相对理想值偏差 | % | -0.394774663 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 仿真步长 | s | 0.001 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 物理步数 | 步 | 600 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 峰值接触合力 | N | 1.05657038 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 峰值法向接触力 | N | 0.98121482 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 最大穿透深度 | m | 3.21120926e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 首次接触时间 | s | 0 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 质心静置时间 | s | 0.255 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 最大动量平衡残差 | N·s | 5.82886485e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 最大接触力核算误差 | N | 未测得 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量X | N·s | -0.0156959917 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量Y | N·s | 3.57673681e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量Z | N·s | 0.0392399929 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 停止时间 | s | 0.255 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 停止距离 | m | 0.126917973 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 最终X位移 | m | 0.126917869 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 最大质心抬升 | m | 3.27825546e-09 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 滑动段测量步数 | 步 | 213 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 滑动窗口内有接触步数 | 步 | 213 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 滑动段平均摩擦力 | N | 0.39239991 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 滑动段平均法向力 | N | 0.981000102 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 实测等效摩擦系数 | 1 | 0.399999867 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 滑动段平均X减速度 | m/s² | 3.92404867 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 全程X接触冲量 | N·s | -0.0999987984 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000503130128 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000425809125 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 1.18099351e-05 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 最大侧向偏移 | m | 5.67842804e-08 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| PhysX（Isaac Sim CPU TGS） | 滑动方块 | 1 | 3 | 通过 | 停止距离相对理想值偏差 | % | -0.394774663 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 仿真步长 | s | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 物理步数 | 步 | 300 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 峰值接触合力 | N | 10.5316698 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 峰值法向接触力 | N | 9.77840996 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 最大穿透深度 | m | 0.000216020689 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 首次接触时间 | s | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 最大动量平衡残差 | N·s | 9.25658415e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 最大接触力核算误差 | N | 2.66560075e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量X | N·s | -0.0177374028 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量Y | N·s | -8.78487505e-12 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量Z | N·s | 0.0443435063 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 停止时间 | s | 0.26 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 停止距离 | m | 0.126459196 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 最终X位移 | m | 0.126448587 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 最大质心抬升 | m | 0.000892068744 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 滑动段测量步数 | 步 | 106 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 滑动窗口内有接触步数 | 步 | 52 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 滑动段平均摩擦力 | N | 0.385045168 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 滑动段平均法向力 | N | 0.966722112 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 实测等效摩擦系数 | 1 | 0.398299742 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 滑动段平均X减速度 | m/s² | 3.85045692 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 全程X接触冲量 | N·s | -0.0999999449 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000972869161 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000847969499 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.051871113 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 最大侧向偏移 | m | 1.2876356e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 1 | 通过 | 停止距离相对理想值偏差 | % | -0.754822814 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 仿真步长 | s | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 物理步数 | 步 | 300 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 峰值接触合力 | N | 10.5316698 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 峰值法向接触力 | N | 9.77840996 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 最大穿透深度 | m | 0.000216020689 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 首次接触时间 | s | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 最大动量平衡残差 | N·s | 9.25658415e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 最大接触力核算误差 | N | 2.66560075e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量X | N·s | -0.0177374028 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量Y | N·s | -8.78487505e-12 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量Z | N·s | 0.0443435063 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 停止时间 | s | 0.26 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 停止距离 | m | 0.126459196 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 最终X位移 | m | 0.126448587 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 最大质心抬升 | m | 0.000892068744 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 滑动段测量步数 | 步 | 106 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 滑动窗口内有接触步数 | 步 | 52 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 滑动段平均摩擦力 | N | 0.385045168 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 滑动段平均法向力 | N | 0.966722112 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 实测等效摩擦系数 | 1 | 0.398299742 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 滑动段平均X减速度 | m/s² | 3.85045692 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 全程X接触冲量 | N·s | -0.0999999449 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000972869161 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000847969499 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.051871113 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 最大侧向偏移 | m | 1.2876356e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 2 | 通过 | 停止距离相对理想值偏差 | % | -0.754822814 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 仿真步长 | s | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 物理步数 | 步 | 300 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 峰值接触合力 | N | 10.5316698 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 峰值法向接触力 | N | 9.77840996 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 最大穿透深度 | m | 0.000216020689 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 首次接触时间 | s | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 最大动量平衡残差 | N·s | 9.25658415e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 最大接触力核算误差 | N | 2.66560075e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量X | N·s | -0.0177374028 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量Y | N·s | -8.78487505e-12 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量Z | N·s | 0.0443435063 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 停止时间 | s | 0.26 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 停止距离 | m | 0.126459196 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 最终X位移 | m | 0.126448587 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 最大质心抬升 | m | 0.000892068744 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 滑动段测量步数 | 步 | 106 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 滑动窗口内有接触步数 | 步 | 52 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 滑动段平均摩擦力 | N | 0.385045168 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 滑动段平均法向力 | N | 0.966722112 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 实测等效摩擦系数 | 1 | 0.398299742 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 滑动段平均X减速度 | m/s² | 3.85045692 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 全程X接触冲量 | N·s | -0.099999945 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000972869161 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000847969499 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.051871113 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 最大侧向偏移 | m | 1.2876356e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 2 | 3 | 通过 | 停止距离相对理想值偏差 | % | -0.754822814 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 仿真步长 | s | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 物理步数 | 步 | 600 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 峰值接触合力 | N | 9.53297962 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 峰值法向接触力 | N | 8.85114932 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 最大穿透深度 | m | 0.000118393635 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 首次接触时间 | s | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 最大动量平衡残差 | N·s | 1.51856231e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 最大接触力核算误差 | N | 2.68220901e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量X | N·s | -0.0183370035 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量Y | N·s | -4.87443903e-10 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量Z | N·s | 0.0458425078 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 停止时间 | s | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 停止距离 | m | 0.126960471 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 最终X位移 | m | 0.126962081 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 最大质心抬升 | m | 0.000374212414 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 滑动段测量步数 | 步 | 212 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 滑动窗口内有接触步数 | 步 | 98 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 滑动段平均摩擦力 | N | 0.380860283 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 滑动段平均法向力 | N | 0.953870572 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 实测等效摩擦系数 | 1 | 0.399278785 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 滑动段平均X减速度 | m/s² | 3.80859251 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 全程X接触冲量 | N·s | -0.100000175 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000482082642 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000401247131 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.0296640083 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 最大侧向偏移 | m | 2.02004209e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 1 | 通过 | 停止距离相对理想值偏差 | % | -0.361422145 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 仿真步长 | s | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 物理步数 | 步 | 600 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 峰值接触合力 | N | 9.53297962 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 峰值法向接触力 | N | 8.85114932 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 最大穿透深度 | m | 0.000118396815 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 首次接触时间 | s | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 最大动量平衡残差 | N·s | 1.57019866e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 最大接触力核算误差 | N | 2.66560075e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量X | N·s | -0.0183370035 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量Y | N·s | -4.87443903e-10 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量Z | N·s | 0.0458425078 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 停止时间 | s | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 停止距离 | m | 0.126960456 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 最终X位移 | m | 0.126962066 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 最大质心抬升 | m | 0.000374212414 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 滑动段测量步数 | 步 | 212 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 滑动窗口内有接触步数 | 步 | 98 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 滑动段平均摩擦力 | N | 0.380860351 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 滑动段平均法向力 | N | 0.953870778 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 实测等效摩擦系数 | 1 | 0.39927877 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 滑动段平均X减速度 | m/s² | 3.80859321 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 全程X接触冲量 | N·s | -0.100000175 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000482097543 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.00040125831 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.0296640083 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 最大侧向偏移 | m | 1.44763277e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 2 | 通过 | 停止距离相对理想值偏差 | % | -0.36143384 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 仿真步长 | s | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 物理步数 | 步 | 600 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 峰值接触合力 | N | 9.53297962 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 峰值法向接触力 | N | 8.85114932 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 最大穿透深度 | m | 0.000118396464 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 首次接触时间 | s | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 最大动量平衡残差 | N·s | 1.55575221e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 最大接触力核算误差 | N | 4.53935451e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量X | N·s | -0.0183370153 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量Y | N·s | -4.87445751e-10 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量Z | N·s | 0.0458425373 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 停止时间 | s | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 停止距离 | m | 0.126960441 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 最终X位移 | m | 0.126962051 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 最大质心抬升 | m | 0.000374212414 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 滑动段测量步数 | 步 | 212 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 滑动窗口内有接触步数 | 步 | 98 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 滑动段平均摩擦力 | N | 0.380860431 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 滑动段平均法向力 | N | 0.953870985 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 实测等效摩擦系数 | 1 | 0.399278768 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 滑动段平均X减速度 | m/s² | 3.80859325 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 全程X接触冲量 | N·s | -0.100000203 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000482112444 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000401268841 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.0296640083 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 最大侧向偏移 | m | 2.07537063e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 | 1 | 3 | 通过 | 停止距离相对理想值偏差 | % | -0.361445534 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 仿真步长 | s | 0.002 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 物理步数 | 步 | 300 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 峰值接触合力 | N | 10.5316246 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 峰值法向接触力 | N | 9.77836796 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 最大穿透深度 | m | 0.00021601579 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 首次接触时间 | s | 0.002 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 最大动量平衡残差 | N·s | 5.69567052e-14 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 最大接触力核算误差 | N | 0 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量X | N·s | -0.0177373764 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量Y | N·s | 4.34531871e-19 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量Z | N·s | 0.0443434409 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 停止时间 | s | 0.26 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 停止距离 | m | 0.126459227 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 最终X位移 | m | 0.12644859 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 最大质心抬升 | m | 0.000892068944 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 滑动段测量步数 | 步 | 106 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 滑动窗口内有接触步数 | 步 | 52 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 滑动段平均摩擦力 | N | 0.385045505 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 滑动段平均法向力 | N | 0.966722738 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 实测等效摩擦系数 | 1 | 0.398299833 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 滑动段平均X减速度 | m/s² | 3.85045505 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 全程X接触冲量 | N·s | -0.1 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000972839409 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000847953899 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.051871173 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 最大侧向偏移 | m | 1.98637315e-17 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo CPU | 滑动方块 | 2 | 1 | 通过 | 停止距离相对理想值偏差 | % | -0.754798693 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 仿真步长 | s | 0.002 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 物理步数 | 步 | 300 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 峰值接触合力 | N | 10.5316246 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 峰值法向接触力 | N | 9.77836796 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 最大穿透深度 | m | 0.00021601579 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 首次接触时间 | s | 0.002 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 最大动量平衡残差 | N·s | 5.69567052e-14 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 最大接触力核算误差 | N | 0 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量X | N·s | -0.0177373764 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量Y | N·s | 4.34531871e-19 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量Z | N·s | 0.0443434409 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 停止时间 | s | 0.26 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 停止距离 | m | 0.126459227 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 最终X位移 | m | 0.12644859 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 最大质心抬升 | m | 0.000892068944 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 滑动段测量步数 | 步 | 106 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 滑动窗口内有接触步数 | 步 | 52 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 滑动段平均摩擦力 | N | 0.385045505 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 滑动段平均法向力 | N | 0.966722738 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 实测等效摩擦系数 | 1 | 0.398299833 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 滑动段平均X减速度 | m/s² | 3.85045505 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 全程X接触冲量 | N·s | -0.1 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000972839409 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000847953899 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.051871173 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 最大侧向偏移 | m | 1.98637315e-17 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo CPU | 滑动方块 | 2 | 2 | 通过 | 停止距离相对理想值偏差 | % | -0.754798693 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 仿真步长 | s | 0.002 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 物理步数 | 步 | 300 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 峰值接触合力 | N | 10.5316246 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 峰值法向接触力 | N | 9.77836796 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 最大穿透深度 | m | 0.00021601579 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 首次接触时间 | s | 0.002 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 最大动量平衡残差 | N·s | 5.69567052e-14 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 最大接触力核算误差 | N | 0 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量X | N·s | -0.0177373764 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量Y | N·s | 4.34531871e-19 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量Z | N·s | 0.0443434409 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 停止时间 | s | 0.26 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 停止距离 | m | 0.126459227 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 最终X位移 | m | 0.12644859 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 最大质心抬升 | m | 0.000892068944 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 滑动段测量步数 | 步 | 106 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 滑动窗口内有接触步数 | 步 | 52 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 滑动段平均摩擦力 | N | 0.385045505 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 滑动段平均法向力 | N | 0.966722738 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 实测等效摩擦系数 | 1 | 0.398299833 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 滑动段平均X减速度 | m/s² | 3.85045505 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 全程X接触冲量 | N·s | -0.1 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000972839409 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000847953899 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.051871173 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 最大侧向偏移 | m | 1.98637315e-17 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo CPU | 滑动方块 | 2 | 3 | 通过 | 停止距离相对理想值偏差 | % | -0.754798693 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 仿真步长 | s | 0.001 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 物理步数 | 步 | 600 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 峰值接触合力 | N | 9.53295281 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 峰值法向接触力 | N | 8.85112448 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 最大穿透深度 | m | 0.000118383142 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 首次接触时间 | s | 0.001 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 最大动量平衡残差 | N·s | 1.46170299e-09 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 最大接触力核算误差 | N | 0 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量X | N·s | -0.0183370213 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量Y | N·s | 4.02008391e-20 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量Z | N·s | 0.0458425533 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 停止时间 | s | 0.262 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 停止距离 | m | 0.126960411 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 最终X位移 | m | 0.126961965 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 最大质心抬升 | m | 0.000374209017 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 滑动段测量步数 | 步 | 212 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 滑动窗口内有接触步数 | 步 | 98 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 滑动段平均摩擦力 | N | 0.380859276 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 滑动段平均法向力 | N | 0.953868193 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 实测等效摩擦系数 | 1 | 0.399278725 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 滑动段平均X减速度 | m/s² | 3.80859271 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 全程X接触冲量 | N·s | -0.100000001 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000482144149 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.00040131436 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.0296639915 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 最大侧向偏移 | m | 1.82767274e-17 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo CPU | 滑动方块 | 1 | 1 | 通过 | 停止距离相对理想值偏差 | % | -0.361469084 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 仿真步长 | s | 0.001 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 物理步数 | 步 | 600 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 峰值接触合力 | N | 9.53295281 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 峰值法向接触力 | N | 8.85112448 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 最大穿透深度 | m | 0.000118383142 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 首次接触时间 | s | 0.001 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 最大动量平衡残差 | N·s | 1.46170299e-09 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 最大接触力核算误差 | N | 0 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量X | N·s | -0.0183370213 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量Y | N·s | 4.02008391e-20 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量Z | N·s | 0.0458425533 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 停止时间 | s | 0.262 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 停止距离 | m | 0.126960411 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 最终X位移 | m | 0.126961965 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 最大质心抬升 | m | 0.000374209017 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 滑动段测量步数 | 步 | 212 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 滑动窗口内有接触步数 | 步 | 98 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 滑动段平均摩擦力 | N | 0.380859276 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 滑动段平均法向力 | N | 0.953868193 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 实测等效摩擦系数 | 1 | 0.399278725 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 滑动段平均X减速度 | m/s² | 3.80859271 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 全程X接触冲量 | N·s | -0.100000001 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000482144149 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.00040131436 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.0296639915 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 最大侧向偏移 | m | 1.82767274e-17 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo CPU | 滑动方块 | 1 | 2 | 通过 | 停止距离相对理想值偏差 | % | -0.361469084 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 仿真步长 | s | 0.001 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 物理步数 | 步 | 600 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 峰值接触合力 | N | 9.53295281 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 峰值法向接触力 | N | 8.85112448 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 最大穿透深度 | m | 0.000118383142 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 首次接触时间 | s | 0.001 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 质心静置时间 | s | 0.262 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 最大动量平衡残差 | N·s | 1.46170299e-09 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 最大接触力核算误差 | N | 0 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量X | N·s | -0.0183370213 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量Y | N·s | 4.02008391e-20 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量Z | N·s | 0.0458425533 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 停止时间 | s | 0.262 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 停止距离 | m | 0.126960411 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 最终X位移 | m | 0.126961965 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 最大质心抬升 | m | 0.000374209017 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 滑动段测量步数 | 步 | 212 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 滑动窗口内有接触步数 | 步 | 98 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 滑动段平均摩擦力 | N | 0.380859276 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 滑动段平均法向力 | N | 0.953868193 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 实测等效摩擦系数 | 1 | 0.399278725 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 滑动段平均X减速度 | m/s² | 3.80859271 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 全程X接触冲量 | N·s | -0.100000001 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000482144149 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.00040131436 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.0296639915 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 最大侧向偏移 | m | 1.82767274e-17 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| MuJoCo CPU | 滑动方块 | 1 | 3 | 通过 | 停止距离相对理想值偏差 | % | -0.361469084 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 仿真步长 | s | 0.002 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 物理步数 | 步 | 300 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 峰值接触合力 | N | 1.50194424 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 峰值法向接触力 | N | 1.39452022 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 最大穿透深度 | m | 8.37431237e-05 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 首次接触时间 | s | 0.002 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 质心静置时间 | s | 0.26 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 最大动量平衡残差 | N·s | 5.72049027e-14 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 最大接触力核算误差 | N | 0 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量X | N·s | -0.0165076625 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量Y | N·s | 9.37519367e-20 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 窗口接触冲量Z | N·s | 0.0412691562 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 停止时间 | s | 0.26 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 停止距离 | m | 0.126452747 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 最终X位移 | m | 0.126447003 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 最大质心抬升 | m | 0 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 滑动段测量步数 | 步 | 106 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 滑动窗口内有接触步数 | 步 | 106 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 滑动段平均摩擦力 | N | 0.39082509 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 滑动段平均法向力 | N | 0.980683221 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 实测等效摩擦系数 | 1 | 0.398523276 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 滑动段平均X减速度 | m/s² | 3.9082509 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 全程X接触冲量 | N·s | -0.1 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000979638872 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000825422115 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.007848 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 最大侧向偏移 | m | 6.50804063e-19 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| Genesis CUDA | 滑动方块 | 2 | 1 | 通过 | 停止距离相对理想值偏差 | % | -0.75988401 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 仿真步长 | s | 0.002 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 物理步数 | 步 | 300 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 峰值接触合力 | N | 1.50194424 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 峰值法向接触力 | N | 1.39452022 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 最大穿透深度 | m | 8.37431237e-05 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 首次接触时间 | s | 0.002 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 质心静置时间 | s | 0.26 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 最大动量平衡残差 | N·s | 5.72049027e-14 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 最大接触力核算误差 | N | 0 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量X | N·s | -0.0165076625 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量Y | N·s | 9.37519367e-20 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 窗口接触冲量Z | N·s | 0.0412691562 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 停止时间 | s | 0.26 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 停止距离 | m | 0.126452747 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 最终X位移 | m | 0.126447003 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 最大质心抬升 | m | 0 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 滑动段测量步数 | 步 | 106 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 滑动窗口内有接触步数 | 步 | 106 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 滑动段平均摩擦力 | N | 0.39082509 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 滑动段平均法向力 | N | 0.980683221 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 实测等效摩擦系数 | 1 | 0.398523276 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 滑动段平均X减速度 | m/s² | 3.9082509 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 全程X接触冲量 | N·s | -0.1 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000979638872 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000825422115 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.007848 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 最大侧向偏移 | m | 6.50804063e-19 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| Genesis CUDA | 滑动方块 | 2 | 2 | 通过 | 停止距离相对理想值偏差 | % | -0.75988401 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 仿真步长 | s | 0.002 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 物理步数 | 步 | 300 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 峰值接触合力 | N | 1.50194424 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 峰值法向接触力 | N | 1.39452022 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 最大穿透深度 | m | 8.37431237e-05 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 首次接触时间 | s | 0.002 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 质心静置时间 | s | 0.26 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 最大动量平衡残差 | N·s | 5.72049027e-14 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 最大接触力核算误差 | N | 0 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量X | N·s | -0.0165076625 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量Y | N·s | 9.37519367e-20 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 窗口接触冲量Z | N·s | 0.0412691562 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 停止时间 | s | 0.26 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 停止距离 | m | 0.126452747 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 最终X位移 | m | 0.126447003 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 最大质心抬升 | m | 0 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 滑动段测量步数 | 步 | 106 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 滑动窗口内有接触步数 | 步 | 106 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 滑动段平均摩擦力 | N | 0.39082509 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 滑动段平均法向力 | N | 0.980683221 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 实测等效摩擦系数 | 1 | 0.398523276 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 滑动段平均X减速度 | m/s² | 3.9082509 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 全程X接触冲量 | N·s | -0.1 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000979638872 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.000825422115 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.007848 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 最大侧向偏移 | m | 6.50804063e-19 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| Genesis CUDA | 滑动方块 | 2 | 3 | 通过 | 停止距离相对理想值偏差 | % | -0.75988401 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 仿真步长 | s | 0.001 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 物理步数 | 步 | 600 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 峰值接触合力 | N | 1.25469268 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 峰值法向接触力 | N | 1.1649529 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 最大穿透深度 | m | 4.86257859e-05 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 首次接触时间 | s | 0.001 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 质心静置时间 | s | 0.262 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 最大动量平衡残差 | N·s | 2.87213848e-14 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 最大接触力核算误差 | N | 0 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量X | N·s | -0.0160995003 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量Y | N·s | -2.61856761e-21 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 窗口接触冲量Z | N·s | 0.0402487507 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 停止时间 | s | 0.262 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 停止距离 | m | 0.126960671 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 最终X位移 | m | 0.126956148 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 最大质心抬升 | m | 0 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 滑动段测量步数 | 步 | 212 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 滑动窗口内有接触步数 | 步 | 212 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 滑动段平均摩擦力 | N | 0.391349236 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 滑动段平均法向力 | N | 0.980869098 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 实测等效摩擦系数 | 1 | 0.398982124 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 滑动段平均X减速度 | m/s² | 3.91349236 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 全程X接触冲量 | N·s | -0.1 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000482776014 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.00039636916 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.00572268205 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 最大侧向偏移 | m | 5.39301926e-20 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| Genesis CUDA | 滑动方块 | 1 | 1 | 通过 | 停止距离相对理想值偏差 | % | -0.361265674 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 仿真步长 | s | 0.001 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 物理步数 | 步 | 600 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 峰值接触合力 | N | 1.25469268 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 峰值法向接触力 | N | 1.1649529 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 最大穿透深度 | m | 4.86257859e-05 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 首次接触时间 | s | 0.001 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 质心静置时间 | s | 0.262 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 最大动量平衡残差 | N·s | 2.87213848e-14 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 最大接触力核算误差 | N | 0 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量X | N·s | -0.0160995003 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量Y | N·s | -2.61856761e-21 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 窗口接触冲量Z | N·s | 0.0402487507 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 停止时间 | s | 0.262 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 停止距离 | m | 0.126960671 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 最终X位移 | m | 0.126956148 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 最大质心抬升 | m | 0 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 滑动段测量步数 | 步 | 212 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 滑动窗口内有接触步数 | 步 | 212 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 滑动段平均摩擦力 | N | 0.391349236 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 滑动段平均法向力 | N | 0.980869098 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 实测等效摩擦系数 | 1 | 0.398982124 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 滑动段平均X减速度 | m/s² | 3.91349236 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 全程X接触冲量 | N·s | -0.1 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000482776014 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.00039636916 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.00572268205 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 最大侧向偏移 | m | 5.39301926e-20 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| Genesis CUDA | 滑动方块 | 1 | 2 | 通过 | 停止距离相对理想值偏差 | % | -0.361265674 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 仿真步长 | s | 0.001 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 物理步数 | 步 | 600 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 峰值接触合力 | N | 1.25469268 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 峰值法向接触力 | N | 1.1649529 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 最大穿透深度 | m | 4.86257859e-05 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 首次接触时间 | s | 0.001 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 质心静置时间 | s | 0.262 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 最大动量平衡残差 | N·s | 2.87213848e-14 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 最大接触力核算误差 | N | 0 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量X | N·s | -0.0160995003 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量Y | N·s | -2.61856761e-21 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 窗口接触冲量Z | N·s | 0.0402487507 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 接触冲量窗口完整 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 停止时间 | s | 0.262 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 停止距离 | m | 0.126960671 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 最终X位移 | m | 0.126956148 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 最大质心抬升 | m | 0 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 理想库仑停止距离 | m | 0.127420999 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 设定摩擦系数 | 1 | 0.4 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 滑动段测量步数 | 步 | 212 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 滑动窗口内有接触步数 | 步 | 212 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 滑动段平均摩擦力 | N | 0.391349236 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 滑动段平均法向力 | N | 0.980869098 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 实测等效摩擦系数 | 1 | 0.398982124 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 滑动段平均X减速度 | m/s² | 3.91349236 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 滑动段摩擦力反向 | 布尔 | 是 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 全程X接触冲量 | N·s | -0.1 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹最大X位移误差 | m | 0.000482776014 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹X位移均方根误差 | m | 0.00039636916 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 相对理想轨迹最大X速度误差 | m/s | 0.00572268205 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 最大侧向偏移 | m | 5.39301926e-20 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 理想库仑停止时间 | s | 0.254841998 |
| Genesis CUDA | 滑动方块 | 1 | 3 | 通过 | 停止距离相对理想值偏差 | % | -0.361265674 |

滑动段测量窗口：首次接触之后排除启动阶段 40 ms；步初水平速度 > 0.01 m/s。平均力与减速度包含离地步的零接触力。
实测等效摩擦系数 = Σ(水平接触力模长×dt) / Σ(法向力×dt)，系数仅使用窗口内法向力 > 1e-9 N 的接触步；无有效接触时为未测得。
理想参考为水平刚性平面上的纯平移库仑模型：a=μg，v=max(v₀−at,0)，x=v₀t−at²/2（停止后保持）；不含接触启动、转动或软接触，轨迹误差用于观察模型差异。
停止时间使用|vx|低于配置阈值且此后所有采样保持低于阈值的首个时刻；停止距离取该时刻X位移。所有指标仅覆盖已记录时长。
