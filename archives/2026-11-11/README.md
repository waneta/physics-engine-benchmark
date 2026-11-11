# 2026-11-11 轻量实验归档

这是关键实验摘要和历史脚本归档，不是完整实验数据备份。文件保留在原有
`results/...` 路径；精确文件列表、大小和 SHA-256 见 [manifest.json](manifest.json)。
归档不改变任何历史测量值、失败记录、验收状态或原有源码指纹。

## 保存范围

- `results/` 中的普通 JSON 文件：逐次结果、环境、配置、指标、来源、选择参数、
  运行/恢复状态、审计结果及清单。历史绝对路径按原始记录保留。
- 全部 Markdown 报告、指标说明、汇总与指标 CSV（不含 `raw.csv`）、日志和错误文本。
- 全部历史 Python 脚本，包括 task04 两批的 9 个运行/审计脚本，以及三批冻结源码；
  同时保存快照中的配置、许可证、依赖输入及锁文件，排除快照中的缓存和字节码。
- 对比目录中的 PNG，以及 `results/full-recovery-20261009/` 根目录的汇总曲线。
- `.cache/diagnose_warp_force.py` 原始诊断脚本，保留原路径和原始字节。

Git 仍默认忽略新生成的 `results/` 和 `.cache/` 文件；本次清单内的指定文件已显式
纳入版本控制。`.gitattributes` 禁止这些历史文件在 Windows 检出时自动转换换行符，
避免原始指纹变化。清单自身由 Git 提交保护，不将其自身列入校验清单。

## 查看与校验

在仓库根目录执行（仅需 Python 3.11+，不需要安装仿真引擎）：

```bash
python scripts/verify_lightweight_archive.py
```

Windows 如果只有 Python 启动器，可使用：

```powershell
py -3 scripts/verify_lightweight_archive.py
```

默认命令只读校验，检查每个归档文件的大小和 SHA-256。`--build` 仅用于在原始结果
仍完整存在时重新生成清单；在新克隆的轻量归档上不要使用，以免把缺失原始数据的
状态误记为原始归档范围。

主要报告入口：

- [完整补跑报告](../../results/full-recovery-20261009/report.md)
- [扩展实验对比](../../results/full-comparison/report.md)
- [task02 四引擎对比](../../results/task02-comparison/report.md)
- [滑块双语对比](../../results/task04-slide-20261010/bilingual/comparison/report.md)
- [滑块重新验证](../../results/task04-slide-rerun-20261010-1818/report.md)
- [下落实验](../../results/task04-drop-20261010/report.md)

## 未保存内容与 Windows 迁移限制

原始逐步采样 `raw.csv`、`trajectory.npz`、`reference.npz`、`verification.npz`，
其他未选择图片、场景文件、虚拟环境、缓存、外部 `references/` 资料和 Git 悬空对象
均未归档。保留 JSON 中记录的原始绝对路径和指纹不代表其指向的数据也已保存。
因此历史报告中的部分链接或图片可能不可用，历史运行/审计脚本也可能因原始数据
缺失而无法直接执行；不能仅凭本归档重新核验旧采样或完整恢复、复用旧批次。

本次不跟踪任何符号链接，尤其不将指向当前 Linux 机器的绝对路径链接提交。
`manifest.json` 记录被省略的普通文件及链接数量。它们仍保留在原本地仓库中。

当前运行器使用 `.venv/bin/python` 等 Linux 路径，可选依赖锁定 Linux x86_64 /
Python 3.11；PhysX 依赖 Isaac Sim 6.0.1 Linux Docker 镜像及 NVIDIA GPU 环境。
这次仅归档资料，没有完成原生 Windows 或 WSL2 适配与运行验证。新电脑需要重建
环境、检查 GPU/容器兼容性，并重新运行小规模测试后再开展新实验。原 Linux
虚拟环境不能直接复制为可用的 Windows 环境。

本归档不意味着旧目录可以安全删除；仍需原始实验数据时应另行完整备份。
