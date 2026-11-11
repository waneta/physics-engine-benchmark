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
| stop_time_s | 停止时间 | Stopping time | s | 秒 / second |
| stop_distance_m | 停止距离 | Stopping distance | m | 米 / metre |
| final_displacement_m | 最终X位移 | Final X displacement | m | 米 / metre |
| max_com_lift_m | 最大质心抬升 | Maximum COM lift | m | 米 / metre |
| ideal_coulomb_distance_m | 理想库仑停止距离 | Ideal Coulomb stopping distance | m | 米 / metre |
| configured_friction_coefficient | 设定摩擦系数 | Configured friction coefficient | 1 | 无量纲 / dimensionless |
| friction_measurement_samples | 滑动段测量步数 | Sliding measurement steps | 步 | 步 / step |
| friction_contact_samples | 滑动窗口内有接触步数 | Contact steps in sliding window | 步 | 步 / step |
| mean_friction_force_n | 滑动段平均摩擦力 | Mean sliding friction force | N | 牛顿 / newton |
| mean_normal_force_n | 滑动段平均法向力 | Mean sliding normal force | N | 牛顿 / newton |
| effective_friction_coefficient | 实测等效摩擦系数 | Measured effective friction coefficient | 1 | 无量纲 / dimensionless |
| mean_deceleration_m_s2 | 滑动段平均X减速度 | Mean sliding X deceleration | m/s² | 米每二次方秒 / metre per second squared |
| friction_opposes_motion | 滑动段摩擦力反向 | Sliding friction opposes motion | 布尔 | 布尔值 / boolean |
| total_contact_jx_ns | 全程X接触冲量 | Total contact impulse X | N·s | 牛顿秒 / newton second |
| max_displacement_error_m | 相对理想轨迹最大X位移误差 | Maximum X displacement error vs ideal trajectory | m | 米 / metre |
| rms_displacement_error_m | 相对理想轨迹X位移均方根误差 | RMS X displacement error vs ideal trajectory | m | 米 / metre |
| max_slide_velocity_error_m_s | 相对理想轨迹最大X速度误差 | Maximum X velocity error vs ideal trajectory | m/s | 米每秒 / metre per second |
| max_lateral_displacement_m | 最大侧向偏移 | Maximum lateral displacement | m | 米 / metre |
| ideal_coulomb_stop_time_s | 理想库仑停止时间 | Ideal Coulomb stopping time | s | 秒 / second |
| stop_distance_error_percent | 停止距离相对理想值偏差 | Stopping distance deviation from ideal | % | 百分比 / percent |
