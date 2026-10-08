# Unity preset

这个预设适用于 Unity 应用、Unity 插件项目、Unity + 原生引擎桥接项目。

## 推荐放置方式

把 `base/.talisman` 复制到 Unity 项目根目录。

典型结构：

```text
/YourUnityProject
  /.talisman
  /Assets
  /Packages
  /ProjectSettings
```

## 推荐允许修改目录

优先白名单这些目录：

1. `Assets/Scripts/`
2. `Assets/Tests/`
3. `Assets/Editor/`
4. `Packages/` 中你自己维护的包目录
5. 明确授权的 `ProjectSettings/` 文件

## 默认禁改目录

1. `Library/`
2. `Temp/`
3. `Logs/`
4. `Obj/`
5. 构建产物目录
6. 大型场景、资源、材质、Prefab，除非明确进白名单

## 推荐优先补充的规则

把下面几条写进 `docs/RULES.md`：

1. 场景、Prefab、材质修改必须显式授权
2. 允许先改脚本和测试，不默认改资源
3. 原生插件桥接变更必须同步 `INTERFACE_SPEC.md`
4. 涉及 `ProjectSettings/` 的修改要写明原因和回滚方法

## 首批任务建议

建议先做这 4 类：

1. 脚本层接口接入
2. 原生 SDK bridge 接线
3. 编辑器工具或构建脚本整理
4. PlayMode / EditMode 测试补齐

## 与库项目混合时的提醒

如果 Unity 项目依赖外部 SDK 或原生引擎：

1. 把接口契约先写进 `docs/INTERFACE_SPEC.md`
2. 把桥接任务写进 `spec/tasks.yaml`
3. 不要直接让 AI 越过接口文档改双端实现