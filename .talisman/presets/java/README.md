# Java preset

这个预设适用于 Java 服务端、工具项目、SDK 项目，以及基于 Maven 或 Gradle 的仓库。

## 推荐放置方式

把 `base/.talisman` 复制到 Java 项目根目录。

典型结构：

```text
/your-java-project
  /.talisman
  /src
  /build.gradle or pom.xml
```

## 推荐允许修改目录

1. `src/main/java/`
2. `src/test/java/`
3. `src/main/resources/` 中非敏感配置
4. `src/test/resources/`
5. 明确允许修改的 `build.gradle`、`settings.gradle`、`pom.xml`

## 默认禁改目录

1. `target/`
2. `build/`
3. `.gradle/`
4. 生成代码目录
5. 生产配置、密钥配置目录

## 推荐优先补充的规则

1. DTO、接口、数据库 schema 变更要同步接口文档
2. 构建脚本和依赖升级需要单独记录影响范围
3. 生产配置不得由 AI 直接修改
4. 公共 API 变更要经过兼容性 gate

## 首批任务建议

建议从下面几类入手：

1. API 层和 DTO 层结构整理
2. service 层逻辑补齐
3. 单元测试和集成测试补齐
4. 构建与启动文档整理

## 多模块项目建议

如果是多模块 Gradle 或 Maven 项目：

1. 先在 `spec/modules.yaml` 把模块边界拆清楚
2. 先定义模块依赖，再拆任务
3. 不要让任务跨模块任意扩散