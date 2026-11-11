# 中英文指标明细 / Bilingual metric details

全部重复与失败见 metrics_bilingual.csv；按引擎/步长的通过运行统计见 metric_stats_bilingual.csv。
标准差为总体标准差（ddof=0），重复不加随机扰动，不用于估计置信区间。
空值表示未测得 / Not measured；布尔值为是 / Yes、否 / No；无量纲 / dimensionless的单位为1。
失败指标仅供诊断，不进入通过运行的统计。CSV数值列保留原始数值精度，显示列采用9位有效数字。
完整名称与单位说明见 [指标字典 / Metric dictionary](metric_definitions.md)。

| 引擎 / Engine | 场景 / Scene | 步长 / Timestep (ms) | 重复 / Repeat | 状态 / Status | 指标名称 / Metric name | 单位 / Unit | 数值 / Value |
|---|---|---:|---:|---|---|---|---:|
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 仿真步长 / Simulation timestep | s (秒 / second) | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 物理步数 / Physics steps | 步 (步 / step) | 300 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force | N (牛顿 / newton) | 10.5316698 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 峰值法向接触力 / Peak normal contact force | N (牛顿 / newton) | 9.77840996 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 最大穿透深度 / Maximum penetration depth | m (米 / metre) | 0.000216020689 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 首次接触时间 / First contact time | s (秒 / second) | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 质心静置时间 / COM settling time | s (秒 / second) | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 最大动量平衡残差 / Maximum momentum balance residual | N·s (牛顿秒 / newton second) | 9.25658415e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 最大接触力核算误差 / Maximum contact force accounting error | N (牛顿 / newton) | 2.66560075e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 窗口接触冲量X / Window contact impulse X | N·s (牛顿秒 / newton second) | -0.0177374028 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 窗口接触冲量Y / Window contact impulse Y | N·s (牛顿秒 / newton second) | -8.78487505e-12 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 窗口接触冲量Z / Window contact impulse Z | N·s (牛顿秒 / newton second) | 0.0443435063 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 接触冲量窗口完整 / Contact impulse window complete | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 停止时间 / Stopping time | s (秒 / second) | 0.26 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 停止距离 / Stopping distance | m (米 / metre) | 0.126459196 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 最终X位移 / Final X displacement | m (米 / metre) | 0.126448587 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 最大质心抬升 / Maximum COM lift | m (米 / metre) | 0.000892068744 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 理想库仑停止距离 / Ideal Coulomb stopping distance | m (米 / metre) | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 设定摩擦系数 / Configured friction coefficient | 1 (无量纲 / dimensionless) | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 滑动段测量步数 / Sliding measurement steps | 步 (步 / step) | 106 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 滑动窗口内有接触步数 / Contact steps in sliding window | 步 (步 / step) | 52 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 滑动段平均摩擦力 / Mean sliding friction force | N (牛顿 / newton) | 0.385045168 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 滑动段平均法向力 / Mean sliding normal force | N (牛顿 / newton) | 0.966722112 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 实测等效摩擦系数 / Measured effective friction coefficient | 1 (无量纲 / dimensionless) | 0.398299742 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 滑动段平均X减速度 / Mean sliding X deceleration | m/s² (米每二次方秒 / metre per second squared) | 3.85045692 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 滑动段摩擦力反向 / Sliding friction opposes motion | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 全程X接触冲量 / Total contact impulse X | N·s (牛顿秒 / newton second) | -0.0999999449 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 相对理想轨迹最大X位移误差 / Maximum X displacement error vs ideal trajectory | m (米 / metre) | 0.000972869161 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 相对理想轨迹X位移均方根误差 / RMS X displacement error vs ideal trajectory | m (米 / metre) | 0.000847969499 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 相对理想轨迹最大X速度误差 / Maximum X velocity error vs ideal trajectory | m/s (米每秒 / metre per second) | 0.051871113 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 最大侧向偏移 / Maximum lateral displacement | m (米 / metre) | 1.2876356e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 理想库仑停止时间 / Ideal Coulomb stopping time | s (秒 / second) | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 1 | 通过 / Passed | 停止距离相对理想值偏差 / Stopping distance deviation from ideal | % (百分比 / percent) | -0.754822814 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 仿真步长 / Simulation timestep | s (秒 / second) | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 物理步数 / Physics steps | 步 (步 / step) | 300 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force | N (牛顿 / newton) | 10.5316698 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 峰值法向接触力 / Peak normal contact force | N (牛顿 / newton) | 9.77840996 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 最大穿透深度 / Maximum penetration depth | m (米 / metre) | 0.000216020689 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 首次接触时间 / First contact time | s (秒 / second) | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 质心静置时间 / COM settling time | s (秒 / second) | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 最大动量平衡残差 / Maximum momentum balance residual | N·s (牛顿秒 / newton second) | 9.25658415e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 最大接触力核算误差 / Maximum contact force accounting error | N (牛顿 / newton) | 2.66560075e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 窗口接触冲量X / Window contact impulse X | N·s (牛顿秒 / newton second) | -0.0177374028 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 窗口接触冲量Y / Window contact impulse Y | N·s (牛顿秒 / newton second) | -8.78487505e-12 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 窗口接触冲量Z / Window contact impulse Z | N·s (牛顿秒 / newton second) | 0.0443435063 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 接触冲量窗口完整 / Contact impulse window complete | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 停止时间 / Stopping time | s (秒 / second) | 0.26 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 停止距离 / Stopping distance | m (米 / metre) | 0.126459196 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 最终X位移 / Final X displacement | m (米 / metre) | 0.126448587 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 最大质心抬升 / Maximum COM lift | m (米 / metre) | 0.000892068744 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 理想库仑停止距离 / Ideal Coulomb stopping distance | m (米 / metre) | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 设定摩擦系数 / Configured friction coefficient | 1 (无量纲 / dimensionless) | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 滑动段测量步数 / Sliding measurement steps | 步 (步 / step) | 106 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 滑动窗口内有接触步数 / Contact steps in sliding window | 步 (步 / step) | 52 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 滑动段平均摩擦力 / Mean sliding friction force | N (牛顿 / newton) | 0.385045168 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 滑动段平均法向力 / Mean sliding normal force | N (牛顿 / newton) | 0.966722112 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 实测等效摩擦系数 / Measured effective friction coefficient | 1 (无量纲 / dimensionless) | 0.398299742 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 滑动段平均X减速度 / Mean sliding X deceleration | m/s² (米每二次方秒 / metre per second squared) | 3.85045692 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 滑动段摩擦力反向 / Sliding friction opposes motion | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 全程X接触冲量 / Total contact impulse X | N·s (牛顿秒 / newton second) | -0.0999999449 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 相对理想轨迹最大X位移误差 / Maximum X displacement error vs ideal trajectory | m (米 / metre) | 0.000972869161 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 相对理想轨迹X位移均方根误差 / RMS X displacement error vs ideal trajectory | m (米 / metre) | 0.000847969499 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 相对理想轨迹最大X速度误差 / Maximum X velocity error vs ideal trajectory | m/s (米每秒 / metre per second) | 0.051871113 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 最大侧向偏移 / Maximum lateral displacement | m (米 / metre) | 1.2876356e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 理想库仑停止时间 / Ideal Coulomb stopping time | s (秒 / second) | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 2 | 通过 / Passed | 停止距离相对理想值偏差 / Stopping distance deviation from ideal | % (百分比 / percent) | -0.754822814 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 仿真步长 / Simulation timestep | s (秒 / second) | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 物理步数 / Physics steps | 步 (步 / step) | 300 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force | N (牛顿 / newton) | 10.5316698 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 峰值法向接触力 / Peak normal contact force | N (牛顿 / newton) | 9.77840996 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 最大穿透深度 / Maximum penetration depth | m (米 / metre) | 0.000216020689 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 首次接触时间 / First contact time | s (秒 / second) | 0.002 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 质心静置时间 / COM settling time | s (秒 / second) | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 最大动量平衡残差 / Maximum momentum balance residual | N·s (牛顿秒 / newton second) | 9.25658415e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 最大接触力核算误差 / Maximum contact force accounting error | N (牛顿 / newton) | 2.66560075e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 窗口接触冲量X / Window contact impulse X | N·s (牛顿秒 / newton second) | -0.0177374028 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 窗口接触冲量Y / Window contact impulse Y | N·s (牛顿秒 / newton second) | -8.78487505e-12 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 窗口接触冲量Z / Window contact impulse Z | N·s (牛顿秒 / newton second) | 0.0443435063 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 接触冲量窗口完整 / Contact impulse window complete | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 停止时间 / Stopping time | s (秒 / second) | 0.26 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 停止距离 / Stopping distance | m (米 / metre) | 0.126459196 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 最终X位移 / Final X displacement | m (米 / metre) | 0.126448587 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 最大质心抬升 / Maximum COM lift | m (米 / metre) | 0.000892068744 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 理想库仑停止距离 / Ideal Coulomb stopping distance | m (米 / metre) | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 设定摩擦系数 / Configured friction coefficient | 1 (无量纲 / dimensionless) | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 滑动段测量步数 / Sliding measurement steps | 步 (步 / step) | 106 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 滑动窗口内有接触步数 / Contact steps in sliding window | 步 (步 / step) | 52 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 滑动段平均摩擦力 / Mean sliding friction force | N (牛顿 / newton) | 0.385045168 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 滑动段平均法向力 / Mean sliding normal force | N (牛顿 / newton) | 0.966722112 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 实测等效摩擦系数 / Measured effective friction coefficient | 1 (无量纲 / dimensionless) | 0.398299742 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 滑动段平均X减速度 / Mean sliding X deceleration | m/s² (米每二次方秒 / metre per second squared) | 3.85045692 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 滑动段摩擦力反向 / Sliding friction opposes motion | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 全程X接触冲量 / Total contact impulse X | N·s (牛顿秒 / newton second) | -0.099999945 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 相对理想轨迹最大X位移误差 / Maximum X displacement error vs ideal trajectory | m (米 / metre) | 0.000972869161 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 相对理想轨迹X位移均方根误差 / RMS X displacement error vs ideal trajectory | m (米 / metre) | 0.000847969499 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 相对理想轨迹最大X速度误差 / Maximum X velocity error vs ideal trajectory | m/s (米每秒 / metre per second) | 0.051871113 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 最大侧向偏移 / Maximum lateral displacement | m (米 / metre) | 1.2876356e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 理想库仑停止时间 / Ideal Coulomb stopping time | s (秒 / second) | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 2 | 3 | 通过 / Passed | 停止距离相对理想值偏差 / Stopping distance deviation from ideal | % (百分比 / percent) | -0.754822814 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 仿真步长 / Simulation timestep | s (秒 / second) | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 物理步数 / Physics steps | 步 (步 / step) | 600 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force | N (牛顿 / newton) | 9.53297962 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 峰值法向接触力 / Peak normal contact force | N (牛顿 / newton) | 8.85114932 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 最大穿透深度 / Maximum penetration depth | m (米 / metre) | 0.000118393635 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 首次接触时间 / First contact time | s (秒 / second) | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 质心静置时间 / COM settling time | s (秒 / second) | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 最大动量平衡残差 / Maximum momentum balance residual | N·s (牛顿秒 / newton second) | 1.51856231e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 最大接触力核算误差 / Maximum contact force accounting error | N (牛顿 / newton) | 2.68220901e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 窗口接触冲量X / Window contact impulse X | N·s (牛顿秒 / newton second) | -0.0183370035 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 窗口接触冲量Y / Window contact impulse Y | N·s (牛顿秒 / newton second) | -4.87443903e-10 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 窗口接触冲量Z / Window contact impulse Z | N·s (牛顿秒 / newton second) | 0.0458425078 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 接触冲量窗口完整 / Contact impulse window complete | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 停止时间 / Stopping time | s (秒 / second) | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 停止距离 / Stopping distance | m (米 / metre) | 0.126960471 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 最终X位移 / Final X displacement | m (米 / metre) | 0.126962081 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 最大质心抬升 / Maximum COM lift | m (米 / metre) | 0.000374212414 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 理想库仑停止距离 / Ideal Coulomb stopping distance | m (米 / metre) | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 设定摩擦系数 / Configured friction coefficient | 1 (无量纲 / dimensionless) | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 滑动段测量步数 / Sliding measurement steps | 步 (步 / step) | 212 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 滑动窗口内有接触步数 / Contact steps in sliding window | 步 (步 / step) | 98 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 滑动段平均摩擦力 / Mean sliding friction force | N (牛顿 / newton) | 0.380860283 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 滑动段平均法向力 / Mean sliding normal force | N (牛顿 / newton) | 0.953870572 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 实测等效摩擦系数 / Measured effective friction coefficient | 1 (无量纲 / dimensionless) | 0.399278785 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 滑动段平均X减速度 / Mean sliding X deceleration | m/s² (米每二次方秒 / metre per second squared) | 3.80859251 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 滑动段摩擦力反向 / Sliding friction opposes motion | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 全程X接触冲量 / Total contact impulse X | N·s (牛顿秒 / newton second) | -0.100000175 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 相对理想轨迹最大X位移误差 / Maximum X displacement error vs ideal trajectory | m (米 / metre) | 0.000482082642 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 相对理想轨迹X位移均方根误差 / RMS X displacement error vs ideal trajectory | m (米 / metre) | 0.000401247131 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 相对理想轨迹最大X速度误差 / Maximum X velocity error vs ideal trajectory | m/s (米每秒 / metre per second) | 0.0296640083 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 最大侧向偏移 / Maximum lateral displacement | m (米 / metre) | 2.02004209e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 理想库仑停止时间 / Ideal Coulomb stopping time | s (秒 / second) | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 1 | 通过 / Passed | 停止距离相对理想值偏差 / Stopping distance deviation from ideal | % (百分比 / percent) | -0.361422145 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 仿真步长 / Simulation timestep | s (秒 / second) | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 物理步数 / Physics steps | 步 (步 / step) | 600 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force | N (牛顿 / newton) | 9.53297962 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 峰值法向接触力 / Peak normal contact force | N (牛顿 / newton) | 8.85114932 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 最大穿透深度 / Maximum penetration depth | m (米 / metre) | 0.000118396815 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 首次接触时间 / First contact time | s (秒 / second) | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 质心静置时间 / COM settling time | s (秒 / second) | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 最大动量平衡残差 / Maximum momentum balance residual | N·s (牛顿秒 / newton second) | 1.57019866e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 最大接触力核算误差 / Maximum contact force accounting error | N (牛顿 / newton) | 2.66560075e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 窗口接触冲量X / Window contact impulse X | N·s (牛顿秒 / newton second) | -0.0183370035 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 窗口接触冲量Y / Window contact impulse Y | N·s (牛顿秒 / newton second) | -4.87443903e-10 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 窗口接触冲量Z / Window contact impulse Z | N·s (牛顿秒 / newton second) | 0.0458425078 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 接触冲量窗口完整 / Contact impulse window complete | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 停止时间 / Stopping time | s (秒 / second) | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 停止距离 / Stopping distance | m (米 / metre) | 0.126960456 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 最终X位移 / Final X displacement | m (米 / metre) | 0.126962066 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 最大质心抬升 / Maximum COM lift | m (米 / metre) | 0.000374212414 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 理想库仑停止距离 / Ideal Coulomb stopping distance | m (米 / metre) | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 设定摩擦系数 / Configured friction coefficient | 1 (无量纲 / dimensionless) | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 滑动段测量步数 / Sliding measurement steps | 步 (步 / step) | 212 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 滑动窗口内有接触步数 / Contact steps in sliding window | 步 (步 / step) | 98 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 滑动段平均摩擦力 / Mean sliding friction force | N (牛顿 / newton) | 0.380860351 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 滑动段平均法向力 / Mean sliding normal force | N (牛顿 / newton) | 0.953870778 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 实测等效摩擦系数 / Measured effective friction coefficient | 1 (无量纲 / dimensionless) | 0.39927877 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 滑动段平均X减速度 / Mean sliding X deceleration | m/s² (米每二次方秒 / metre per second squared) | 3.80859321 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 滑动段摩擦力反向 / Sliding friction opposes motion | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 全程X接触冲量 / Total contact impulse X | N·s (牛顿秒 / newton second) | -0.100000175 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 相对理想轨迹最大X位移误差 / Maximum X displacement error vs ideal trajectory | m (米 / metre) | 0.000482097543 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 相对理想轨迹X位移均方根误差 / RMS X displacement error vs ideal trajectory | m (米 / metre) | 0.00040125831 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 相对理想轨迹最大X速度误差 / Maximum X velocity error vs ideal trajectory | m/s (米每秒 / metre per second) | 0.0296640083 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 最大侧向偏移 / Maximum lateral displacement | m (米 / metre) | 1.44763277e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 理想库仑停止时间 / Ideal Coulomb stopping time | s (秒 / second) | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 2 | 通过 / Passed | 停止距离相对理想值偏差 / Stopping distance deviation from ideal | % (百分比 / percent) | -0.36143384 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 仿真步长 / Simulation timestep | s (秒 / second) | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 物理步数 / Physics steps | 步 (步 / step) | 600 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force | N (牛顿 / newton) | 9.53297962 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 峰值法向接触力 / Peak normal contact force | N (牛顿 / newton) | 8.85114932 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 最大穿透深度 / Maximum penetration depth | m (米 / metre) | 0.000118396464 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 首次接触时间 / First contact time | s (秒 / second) | 0.001 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 质心静置时间 / COM settling time | s (秒 / second) | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 最大动量平衡残差 / Maximum momentum balance residual | N·s (牛顿秒 / newton second) | 1.55575221e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 最大接触力核算误差 / Maximum contact force accounting error | N (牛顿 / newton) | 4.53935451e-07 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 窗口接触冲量X / Window contact impulse X | N·s (牛顿秒 / newton second) | -0.0183370153 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 窗口接触冲量Y / Window contact impulse Y | N·s (牛顿秒 / newton second) | -4.87445751e-10 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 窗口接触冲量Z / Window contact impulse Z | N·s (牛顿秒 / newton second) | 0.0458425373 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 接触冲量窗口完整 / Contact impulse window complete | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 停止时间 / Stopping time | s (秒 / second) | 0.262 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 停止距离 / Stopping distance | m (米 / metre) | 0.126960441 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 最终X位移 / Final X displacement | m (米 / metre) | 0.126962051 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 最大质心抬升 / Maximum COM lift | m (米 / metre) | 0.000374212414 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 理想库仑停止距离 / Ideal Coulomb stopping distance | m (米 / metre) | 0.127420999 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 设定摩擦系数 / Configured friction coefficient | 1 (无量纲 / dimensionless) | 0.4 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 滑动段测量步数 / Sliding measurement steps | 步 (步 / step) | 212 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 滑动窗口内有接触步数 / Contact steps in sliding window | 步 (步 / step) | 98 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 滑动段平均摩擦力 / Mean sliding friction force | N (牛顿 / newton) | 0.380860431 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 滑动段平均法向力 / Mean sliding normal force | N (牛顿 / newton) | 0.953870985 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 实测等效摩擦系数 / Measured effective friction coefficient | 1 (无量纲 / dimensionless) | 0.399278768 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 滑动段平均X减速度 / Mean sliding X deceleration | m/s² (米每二次方秒 / metre per second squared) | 3.80859325 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 滑动段摩擦力反向 / Sliding friction opposes motion | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 全程X接触冲量 / Total contact impulse X | N·s (牛顿秒 / newton second) | -0.100000203 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 相对理想轨迹最大X位移误差 / Maximum X displacement error vs ideal trajectory | m (米 / metre) | 0.000482112444 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 相对理想轨迹X位移均方根误差 / RMS X displacement error vs ideal trajectory | m (米 / metre) | 0.000401268841 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 相对理想轨迹最大X速度误差 / Maximum X velocity error vs ideal trajectory | m/s (米每秒 / metre per second) | 0.0296640083 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 最大侧向偏移 / Maximum lateral displacement | m (米 / metre) | 2.07537063e-08 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 理想库仑停止时间 / Ideal Coulomb stopping time | s (秒 / second) | 0.254841998 |
| MuJoCo-Warp（直接 CUDA） | 滑动方块 / Sliding cube | 1 | 3 | 通过 / Passed | 停止距离相对理想值偏差 / Stopping distance deviation from ideal | % (百分比 / percent) | -0.361445534 |

滑动段测量窗口：首次接触之后排除启动阶段 40 ms；步初水平速度 > 0.01 m/s。平均力与减速度包含离地步的零接触力。
实测等效摩擦系数 = Σ(水平接触力模长×dt) / Σ(法向力×dt)，系数仅使用窗口内法向力 > 1e-9 N 的接触步；无有效接触时为未测得。
理想参考为水平刚性平面上的纯平移库仑模型：a=μg，v=max(v₀−at,0)，x=v₀t−at²/2（停止后保持）；不含接触启动、转动或软接触，轨迹误差用于观察模型差异。
停止时间使用|vx|低于配置阈值且此后所有采样保持低于阈值的首个时刻；停止距离取该时刻X位移。所有指标仅覆盖已记录时长。
