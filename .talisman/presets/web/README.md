# Web preset

这个预设适用于前端项目、全栈 Web 项目、管理台项目，也适用于 React、Vue、Next、Vite 等常见结构。

## 推荐放置方式

把 `base/.talisman` 复制到 Web 项目根目录。

典型结构：

```text
/your-web-project
  /.talisman
  /src
  /public
  /package.json
```

## 推荐允许修改目录

1. `src/`
2. `app/` 或 `pages/`
3. `components/`
4. `tests/` 或 `e2e/`
5. `public/` 中明确授权的静态资源

## 默认禁改目录

1. `dist/`
2. `.next/`
3. `coverage/`
4. `node_modules/`
5. `.env*`
6. 部署、密钥、平台配置目录

## 推荐优先补充的规则

1. UI 改动要说明影响页面和交互
2. 接口字段变更要同步接口契约
3. 构建链路和部署配置必须单独 gate
4. 生成产物不得直接提交到源码目录

## 首批任务建议

建议先从下面几类做起：

1. 页面或组件开发
2. 接口接线和状态管理整理
3. 测试补齐
4. 文案和交互流程优化

## 单仓多端建议

如果同仓同时有前端、BFF、管理台：

1. 优先按端拆 `modules.yaml`
2. 一个模块一组任务，不要把所有任务揉成一坨
3. 真正到项目集编排阶段，再考虑 talisman_array