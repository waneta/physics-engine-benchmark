# 中英文指标明细 / Bilingual metric details

全部重复与失败见 metrics_bilingual.csv；按引擎/步长的通过运行统计见 metric_stats_bilingual.csv。
标准差为总体标准差（ddof=0），重复不加随机扰动，不用于估计置信区间。
空值表示未测得 / Not measured；布尔值为是 / Yes、否 / No；无量纲 / dimensionless的单位为1。
失败指标仅供诊断，不进入通过运行的统计。CSV数值列保留原始数值精度，显示列采用9位有效数字。
完整名称与单位说明见 [指标字典 / Metric dictionary](metric_definitions.md)。

| 引擎 / Engine | 场景 / Scene | 步长 / Timestep (ms) | 重复 / Repeat | 状态 / Status | 指标名称 / Metric name | 单位 / Unit | 数值 / Value |
|---|---|---:|---:|---|---|---|---:|
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 仿真步长 / Simulation timestep | s (秒 / second) | 0.002 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 物理步数 / Physics steps | 步 (步 / step) | 500 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force | N (牛顿 / newton) | 58.2571948 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 峰值法向接触力 / Peak normal contact force | N (牛顿 / newton) | 58.2571948 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 最大穿透深度 / Maximum penetration depth | m (米 / metre) | 0.00874060957 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 首次接触时间 / First contact time | s (秒 / second) | 0.26 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 质心静置时间 / COM settling time | s (秒 / second) | 0.36 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 最大动量平衡残差 / Maximum momentum balance residual | N·s (牛顿秒 / newton second) | 5.86498037e-14 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 最大接触力核算误差 / Maximum contact force accounting error | N (牛顿 / newton) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 窗口接触冲量X / Window contact impulse X | N·s (牛顿秒 / newton second) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 窗口接触冲量Y / Window contact impulse Y | N·s (牛顿秒 / newton second) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 窗口接触冲量Z / Window contact impulse Z | N·s (牛顿秒 / newton second) | 0.305547386 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 接触冲量窗口完整 / Contact impulse window complete | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 最低质心高度 / Minimum COM height | m (米 / metre) | 0.0112593904 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 理想首次接触时间 / Ideal first contact time | s (秒 / second) | 0.259380584 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 首次接触时间相对理想值偏差 / First contact time deviation from ideal | s (秒 / second) | 0.000619415796 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 首次接触步初竖直速度 / Vertical velocity at start of first contact step | m/s (米每秒 / metre per second) | -2.5506 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 理想碰撞前竖直速度 / Ideal preimpact vertical velocity | m/s (米每秒 / metre per second) | -2.54452353 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 接触后最大向上速度 / Peak upward velocity after contact | m/s (米每秒 / metre per second) | 0.337265512 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 自由落体段最大高度误差 / Maximum free-fall height error | m (米 / metre) | 0.0025506 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 自由落体段最大竖直速度误差 / Maximum free-fall vertical velocity error | m/s (米每秒 / metre per second) | 3.55271368e-15 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 最终质心高度 / Final COM height | m (米 / metre) | 0.0199726992 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 最终质心线速度模长 / Final COM linear speed | m/s (米每秒 / metre per second) | 1.02069338e-14 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 最终角速度模长 / Final angular speed | rad/s (弧度每秒 / radian per second) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 刚体静置时间 / Rigid-body settling time | s (秒 / second) | 0.36 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 静置后观察时长 / Observation duration after settling | s (秒 / second) | 0.64 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 记录时长内刚体已静置 / Rigid body settled within recorded duration | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 静置角速度阈值 / Settling angular speed threshold | rad/s (弧度每秒 / radian per second) | 0.0288675135 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 末段平均法向接触力 / Mean normal contact force in final window | N (牛顿 / newton) | 0.981 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 末段平均支撑力与重力比 / Final-window mean support force to weight ratio | 1 (无量纲 / dimensionless) | 1 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 最大水平偏移 / Maximum horizontal displacement | m (米 / metre) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 2 | 1 | 通过 / Passed | 全程Z接触冲量 / Total contact impulse Z | N·s (牛顿秒 / newton second) | 0.981 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 仿真步长 / Simulation timestep | s (秒 / second) | 0.001 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 物理步数 / Physics steps | 步 (步 / step) | 1000 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 峰值接触合力 / Peak resultant contact force | N (牛顿 / newton) | 53.441377 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 峰值法向接触力 / Peak normal contact force | N (牛顿 / newton) | 53.441377 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 最大穿透深度 / Maximum penetration depth | m (米 / metre) | 0.00756736771 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 首次接触时间 / First contact time | s (秒 / second) | 0.259 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 质心静置时间 / COM settling time | s (秒 / second) | 0.364 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 最大动量平衡残差 / Maximum momentum balance residual | N·s (牛顿秒 / newton second) | 2.99293229e-14 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 最大接触力核算误差 / Maximum contact force accounting error | N (牛顿 / newton) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 窗口接触冲量X / Window contact impulse X | N·s (牛顿秒 / newton second) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 窗口接触冲量Y / Window contact impulse Y | N·s (牛顿秒 / newton second) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 窗口接触冲量Z / Window contact impulse Z | N·s (牛顿秒 / newton second) | 0.303410467 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 接触冲量窗口完整 / Contact impulse window complete | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 最低质心高度 / Minimum COM height | m (米 / metre) | 0.0124326323 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 理想首次接触时间 / Ideal first contact time | s (秒 / second) | 0.259380584 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 首次接触时间相对理想值偏差 / First contact time deviation from ideal | s (秒 / second) | -0.000380584204 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 首次接触步初竖直速度 / Vertical velocity at start of first contact step | m/s (米每秒 / metre per second) | -2.54079 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 理想碰撞前竖直速度 / Ideal preimpact vertical velocity | m/s (米每秒 / metre per second) | -2.54452353 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 接触后最大向上速度 / Peak upward velocity after contact | m/s (米每秒 / metre per second) | 0.284654009 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 自由落体段最大高度误差 / Maximum free-fall height error | m (米 / metre) | 0.001270395 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 自由落体段最大竖直速度误差 / Maximum free-fall vertical velocity error | m/s (米每秒 / metre per second) | 8.8817842e-15 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 最终质心高度 / Final COM height | m (米 / metre) | 0.0199726992 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 最终质心线速度模长 / Final COM linear speed | m/s (米每秒 / metre per second) | 6.1178594e-16 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 最终角速度模长 / Final angular speed | rad/s (弧度每秒 / radian per second) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 刚体静置时间 / Rigid-body settling time | s (秒 / second) | 0.364 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 静置后观察时长 / Observation duration after settling | s (秒 / second) | 0.636 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 记录时长内刚体已静置 / Rigid body settled within recorded duration | 布尔 (布尔值 / boolean) | 是 / Yes |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 静置角速度阈值 / Settling angular speed threshold | rad/s (弧度每秒 / radian per second) | 0.0288675135 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 末段平均法向接触力 / Mean normal contact force in final window | N (牛顿 / newton) | 0.981 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 末段平均支撑力与重力比 / Final-window mean support force to weight ratio | 1 (无量纲 / dimensionless) | 1 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 最大水平偏移 / Maximum horizontal displacement | m (米 / metre) | 0 |
| MuJoCo CPU | 方块下落 / Cube drop | 1 | 1 | 通过 / Passed | 全程Z接触冲量 / Total contact impulse Z | N·s (牛顿秒 / newton second) | 0.981 |

滑动段测量窗口：首次接触之后排除启动阶段 40 ms；步初水平速度 > 0.01 m/s。平均力与减速度包含离地步的零接触力。
实测等效摩擦系数 = Σ(水平接触力模长×dt) / Σ(法向力×dt)，系数仅使用窗口内法向力 > 1e-9 N 的接触步；无有效接触时为未测得。
理想参考为水平刚性平面上的纯平移库仑模型：a=μg，v=max(v₀−at,0)，x=v₀t−at²/2（停止后保持）；不含接触启动、转动或软接触，轨迹误差用于观察模型差异。
停止时间使用|vx|低于配置阈值且此后所有采样保持低于阈值的首个时刻；停止距离取该时刻X位移。所有指标仅覆盖已记录时长。
