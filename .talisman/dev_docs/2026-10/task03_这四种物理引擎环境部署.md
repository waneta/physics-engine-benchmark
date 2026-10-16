# task03_这四种物理引擎环境部署
##  任务
这四种物理引擎环境部署出四份文档保存到‘docs’目录下。

## 2026-10-09 交付记录

已保存 `docs/deploy-mujoco.md`、`docs/deploy-mujoco-warp.md`、`docs/deploy-genesis.md`、`docs/deploy-physx.md`，README 已链接四份文档。内容包括安装前提、固定依赖、运行与检查命令，以及本机已验证范围和限制。

Genesis 另外记录隔离的 1.4.1 / Quadrants 1.3.0 补跑环境，`requirements/genesis-recovery.lock` 经完整依赖闭包检查生成；不替换旧 1.4.3 环境或数据。PhysX 使用既有 Isaac Sim 6.0.1 镜像。

复核基于已有本机环境及实验记录，未重新安装四套全新环境。完整扩展实验仍在补跑，部署文档完成不代表全部实验通过。
