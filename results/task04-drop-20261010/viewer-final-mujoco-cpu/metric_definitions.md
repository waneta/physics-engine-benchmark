# 指标字典 / Metric dictionary

| 指标字段 / Metric key | 中文名称 / Chinese name | 英文名称 / English name | 单位符号 / Unit symbol | 单位说明 / Unit description |
|---|---|---|---|---|
| dt_s | 仿真步长 | Simulation timestep | s | 秒 / second |
| steps | 物理步数 | Physics steps | 步 | 步 / step |
| peak_contact_force_n | 峰值接触合力 | Peak resultant contact force | N | 牛顿 / newton |
| peak_contact_fz_n | 峰值法向接触力 | Peak normal contact force | N | 牛顿 / newton |
| max_penetration_m | 最大穿透深度 | Maximum penetration depth | m | 米 / metre |
| first_contact_s | 首次接触时间 | First contact time | s | 秒 / second |
| settled_time_s | 质心静置时间 | COM settling time | s | 秒 / second |
| max_momentum_residual_ns | 最大动量平衡残差 | Maximum momentum balance residual | N·s | 牛顿秒 / newton second |
| max_constraint_force_error_n | 最大接触力核算误差 | Maximum contact force accounting error | N | 牛顿 / newton |
| window_contact_jx_ns | 窗口接触冲量X | Window contact impulse X | N·s | 牛顿秒 / newton second |
| window_contact_jy_ns | 窗口接触冲量Y | Window contact impulse Y | N·s | 牛顿秒 / newton second |
| window_contact_jz_ns | 窗口接触冲量Z | Window contact impulse Z | N·s | 牛顿秒 / newton second |
| impulse_window_complete | 接触冲量窗口完整 | Contact impulse window complete | 布尔 | 布尔值 / boolean |
| minimum_com_height_m | 最低质心高度 | Minimum COM height | m | 米 / metre |
| ideal_first_contact_s | 理想首次接触时间 | Ideal first contact time | s | 秒 / second |
| first_contact_time_error_s | 首次接触时间相对理想值偏差 | First contact time deviation from ideal | s | 秒 / second |
| preimpact_vertical_velocity_m_s | 首次接触步初竖直速度 | Vertical velocity at start of first contact step | m/s | 米每秒 / metre per second |
| ideal_impact_vertical_velocity_m_s | 理想碰撞前竖直速度 | Ideal preimpact vertical velocity | m/s | 米每秒 / metre per second |
| peak_rebound_vertical_velocity_m_s | 接触后最大向上速度 | Peak upward velocity after contact | m/s | 米每秒 / metre per second |
| max_free_fall_height_error_m | 自由落体段最大高度误差 | Maximum free-fall height error | m | 米 / metre |
| max_free_fall_velocity_error_m_s | 自由落体段最大竖直速度误差 | Maximum free-fall vertical velocity error | m/s | 米每秒 / metre per second |
| final_com_height_m | 最终质心高度 | Final COM height | m | 米 / metre |
| final_linear_speed_m_s | 最终质心线速度模长 | Final COM linear speed | m/s | 米每秒 / metre per second |
| final_angular_speed_rad_s | 最终角速度模长 | Final angular speed | rad/s | 弧度每秒 / radian per second |
| rigid_settled_time_s | 刚体静置时间 | Rigid-body settling time | s | 秒 / second |
| rest_observation_duration_s | 静置后观察时长 | Observation duration after settling | s | 秒 / second |
| settled_within_duration | 记录时长内刚体已静置 | Rigid body settled within recorded duration | 布尔 | 布尔值 / boolean |
| settling_angular_speed_threshold_rad_s | 静置角速度阈值 | Settling angular speed threshold | rad/s | 弧度每秒 / radian per second |
| mean_tail_normal_force_n | 末段平均法向接触力 | Mean normal contact force in final window | N | 牛顿 / newton |
| tail_support_weight_ratio | 末段平均支撑力与重力比 | Final-window mean support force to weight ratio | 1 | 无量纲 / dimensionless |
| max_horizontal_displacement_m | 最大水平偏移 | Maximum horizontal displacement | m | 米 / metre |
| total_contact_jz_ns | 全程Z接触冲量 | Total contact impulse Z | N·s | 牛顿秒 / newton second |
