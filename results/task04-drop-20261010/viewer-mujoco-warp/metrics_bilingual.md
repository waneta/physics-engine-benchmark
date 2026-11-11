# 中英文指标明细 / Bilingual metric details

全部重复与失败见 metrics_bilingual.csv；按引擎/步长的通过运行统计见 metric_stats_bilingual.csv。
标准差为总体标准差（ddof=0），重复不加随机扰动，不用于估计置信区间。
空值表示未测得 / Not measured；布尔值为是 / Yes、否 / No；无量纲 / dimensionless的单位为1。
失败指标仅供诊断，不进入通过运行的统计。CSV数值列保留原始数值精度，显示列采用9位有效数字。
完整名称与单位说明见 [指标字典 / Metric dictionary](metric_definitions.md)。

| 引擎 / Engine | 场景 / Scene | 步长 / Timestep (ms) | 重复 / Repeat | 状态 / Status | 指标名称 / Metric name | 单位 / Unit | 数值 / Value |
|---|---|---:|---:|---|---|---|---:|

滑动段测量窗口：首次接触之后排除启动阶段 40 ms；步初水平速度 > 0.01 m/s。平均力与减速度包含离地步的零接触力。
实测等效摩擦系数 = Σ(水平接触力模长×dt) / Σ(法向力×dt)，系数仅使用窗口内法向力 > 1e-9 N 的接触步；无有效接触时为未测得。
理想参考为水平刚性平面上的纯平移库仑模型：a=μg，v=max(v₀−at,0)，x=v₀t−at²/2（停止后保持）；不含接触启动、转动或软接触，轨迹误差用于观察模型差异。
停止时间使用|vx|低于配置阈值且此后所有采样保持低于阈值的首个时刻；停止距离取该时刻X位移。所有指标仅覆盖已记录时长。
