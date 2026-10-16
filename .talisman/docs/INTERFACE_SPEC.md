# INTERFACE_SPEC

`physics-bench run --engine {mujoco-cpu,mujoco-warp,genesis,physx}` 默认 CPU，兼容既有参数。
每个后端实现 `simulate(scene, cfg, dt, rows=None) -> Run`，异常不丢弃传入列表中已采集的样本。
`Run` 包含 rows、imported、xml；PhysX imported 中附带的 scene_usda 由 CLI 另存文件。

raw.csv 一行代表 `[t_start_s,t_end_s]`，保存两端状态、世界坐标接触合力与冲量、接触数、力矩。
自由体 qpos 为 `[x,y,z,qw,qx,qy,qz]`，qvel 为世界线速度与局部角速度；铰链为单个角度/角速度。
单位均为 SI。PhysX 额外保存 normal_j{axis}_ns 和 friction_j{axis}_ns。
动量残差独立使用状态差计算；不支持的独立约束合力校验指标为 null。

PhysX 工作进程协议：前缀 `PHYSICS_BENCH:` 后为单行 JSON；kind 为 ready、imported、sample、done、error。
请求包含 scene、config、dt。单进程复用 Isaac Sim，但每次请求重建 stage 和状态。
stdout 非协议文本写到诊断日志。容器退出或 180 秒没有协议消息视为失败。

run 退出码：全部通过 0；存在失败 1；参数错误 2；用户中断 130。
中断后保存 partial raw.csv、interruption.json 和部分报告。

`physics-bench compare INPUT... --output NEW_DIRECTORY` 接受至少两个不同引擎的结果目录。
config.json 必须一致；summary.csv 保留所有重复与失败，sources.json 保存来源与版本。
图与表使用第一次重复；缺少实验覆盖或存在失败时返回 1 并标注结果不完整。

验证包括 CPU 物理回归、原生摩擦冲量的动量检验、比较配置拒绝测试，以及真实引擎完整实验。
