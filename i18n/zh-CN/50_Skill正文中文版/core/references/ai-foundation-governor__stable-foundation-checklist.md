# 基座稳定性检查清单 | Stable Foundation Checklist

> **源文件**：skills/core/ai-foundation-governor/references/stable-foundation-checklist.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-foundation-governor` 的配套参考文件中中文对照版，不是正式加载源。

---

当 GERP 任务触及版本、模块、功能、权限、路由、API、FieldPackage、参数、报表、schema 同步或发布收口时，使用本检查清单。

## 分类 | Classification

- [ ] 这次变更由哪一个唯一真相源拥有？
- [ ] 哪张表 / 哪个服务是权威的？
- [ ] 哪一项运行时输出应当消费它？
- [ ] 哪些前端 / 后端消费方必须同步更新？

## 现实核查 | Reality Check

- [ ] 已用 `DESCRIBE` 核查 DB 结构。
- [ ] 已核查计数或样例行。
- [ ] 已定位现有 service / controller / interceptor。
- [ ] 已阅读现有文档与发布任务。
- [ ] 没有仅凭命名得出的结论。

## 收口 | Closure

- [ ] 源对象存在。
- [ ] 归属清晰。
- [ ] 运行时编译器或 profile 输出存在。
- [ ] 消费方使用运行时输出。
- [ ] 后端防护规则存在。
- [ ] 缓存 / 版本失效策略已定义。
- [ ] 允许 / 拒绝测试或冒烟检查存在。
- [ ] 证据文件已写入。

## 证据 | Evidence

至少记录以下之一：

- SQL 结果；
- API 冒烟；
- 浏览器冒烟；
- 编译 / 测试输出；
- 日志证明；
- 当 UI 行为重要时的截图。
