# talisman_template

本仓库用于提供 talisman 类型项目的标准骨架与协作约定。

目标：为每一个真实项目派生一份“项目专用 talisman 仓库”，并以 `.talisman` 目录名接入到业务项目根目录。

## 使用流程

1. 新建一个真实项目仓库，并克隆到本地。
2. 基于 talisman_template 派生一个“该项目专用”的 talisman 仓库，并克隆到真实项目根目录下，目录名必须是 `.talisman`。

示例命令：

```bash
git clone git@gitlab.datamesh.com:AiCode/talisman_project_LaoTzu.git .talisman
```

注意：不要使用原仓库名作为本地目录名，统一使用 `.talisman`，这样可以明确标识 talisman 类型项目，便于长期维护。

3. 与 AI 对话的任务文档，统一新建并保存到 `.talisman/dev_docs/`。

示例：

- 新建文档：`.talisman/dev_docs/2026-07/task03_20260713.md`
- 在 VS Code 的 GitHub Copilot Chat 中打开并引用该文档
- 输入：`看文档完成任务`

## 目录说明

当前仓库为 talisman 标准目录结构，常用目录如下：

- `docs/`：项目规则、架构、任务等核心文档
- `spec/`：结构化规格定义
- `runtime/`：运行态状态与任务队列
- `dev_docs/`：与 AI 协作的过程文档
- `skills/`：技能与提示词资产
- `memory/`：记忆文件

## LaoTzu 的产出物

LaoTzu 的核心产出物不是单一代码文件，而是一整套可持续协作的工程资产。

1. 控制面目录：`.talisman` 或 `.talisman_array`。
2. 规则文档：如 `AGENTS.md`、`docs/` 下的规则、架构、任务说明。
3. 结构化规格：如 `spec/` 下的项目清单、依赖关系、任务定义与调度规则。
4. 运行态记录：如 `runtime/` 下的状态、队列、执行痕迹。
5. 过程文档：如 `dev_docs/` 下的人机协作文档、任务记录、阶段计划。
6. 架构图与说明：帮助 AI 与人快速理解项目结构、层级与边界。
7. 可复用模板仓库：用于派生新的 talisman 或 talisman_array 项目。

如果从结果视角理解，LaoTzu 的目标产出物包括：

1. 可被 AI 稳定理解的项目说明。
2. 可被持续执行的任务拆解。
3. 可追踪、可回放、可复盘的执行记录。
4. 可复制到下一个项目的模板与方法。

## 新手如何使用这个项目

如果你是第一次接触 LaoTzu，可以按下面步骤使用：

1. 先准备一个真实项目仓库。
2. 再基于 talisman_template 派生项目专用 talisman 仓库，并克隆为 `.talisman`。
3. 阅读 `.talisman/架构总览.md`、`AGENTS.md`、`docs/`。
4. 在 `.talisman/dev_docs/` 下新建任务文档。
5. 在 VS Code 中打开该任务文档，并在 GitHub Copilot Chat 中引用它。
6. 输入：`看文档完成任务`。
7. 执行后检查 `runtime/` 是否已回写状态，并继续下一轮任务。

一个最小上手顺序可以这样理解：

1. 先克隆真实项目。
2. 再克隆 `.talisman`。
3. 再写任务文档。
4. 再让 AI 读文档开始执行。
5. 最后检查状态与产出物是否完整。

## 维护约定

- 每个真实项目使用独立的 talisman 派生仓库。
- 业务代码仓库中统一使用 `.talisman` 目录名。
- 优先通过 `dev_docs` 下的任务文档驱动 AI 执行，避免口头需求丢失上下文。