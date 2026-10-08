# Library preset

这个预设适用于 SDK、共享库、工具库、基础组件库。重点不是页面或服务，而是公共接口、版本兼容和测试可信度。

## 推荐放置方式

把 `base/.talisman` 复制到库项目根目录。

典型结构：

```text
/your-library
  /.talisman
  /src
  /tests
  /examples or samples
```

## 推荐允许修改目录

1. `src/`
2. `tests/`
3. `examples/` 或 `samples/`
4. `docs/`
5. 明确授权的打包配置文件

## 默认禁改目录

1. `dist/`
2. `build/`
3. `target/`
4. 发布产物目录
5. 自动生成文档目录
6. 发布脚本和版本文件，除非明确授权

## 推荐优先补充的规则

1. 公共 API 变更必须写入 `INTERFACE_SPEC.md`
2. 破坏兼容性的变更必须人工 gate
3. 示例和测试必须覆盖公共 API 的主要路径
4. 发布流程不能自动触发

## 首批任务建议

建议优先做：

1. 公共 API 梳理
2. 兼容性测试补齐
3. 使用示例整理
4. 文档和版本约束整理

## 为什么库项目更适合先接入 talisman

因为库项目边界更清楚：

1. 公共接口天然适合写 `INTERFACE_SPEC.md`
2. 版本兼容天然适合做 gate
3. 任务边界通常更适合结构化