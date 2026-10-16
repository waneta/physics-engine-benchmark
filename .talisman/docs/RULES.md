# RULES

## 当前任务允许修改

- `src/physics_benchmark/`、`tests/`、`configs/`、`docs/`、`requirements/`、`scripts/`、`native/`
- 根目录 `README.md`、`pyproject.toml`、`uv.lock`、`.gitignore`
- `.talisman/docs/`、`.talisman/spec/`、`.talisman/runtime/`、`.talisman/memory/`
- `.talisman/dev_docs/2026-10/task01_我做这个实验对比.md` 追加验收记录

task02 还允许在对应任务文档追加验收记录，在 references/ 下载官方引擎源码并在本地构建。
允许创建隔离虚拟环境和新的实验结果目录。保持转载原文、现有历史结果、密钥和本地配置不变。
不覆盖或删除旧实验目录，不修改系统驱动/代理，不发布、不推送。

## 验证与回写

涉及物理测量、时间采样或指标的修改必须运行相关物理校验测试。
当前验收执行 `pytest -q`、`ruff check src tests` 和默认 18 组实验。
失败保留数据与异常；`NaN`、MuJoCo 警告和动量残差超容差不得算作成功。

任务执行前后更新 runtime，完成后在任务原文追加实际环境、结果与未覆盖范围。
依赖通过 uv.lock 锁定；记录实际运行版本，不宣称和作者相同。

用户已授权完成全部剩余实验；允许新增 configs/assets、扩展实验代码、依赖及运行记录。
原文类别均需实现和实测，不以仅基础刚体通过替代完整任务验收。
