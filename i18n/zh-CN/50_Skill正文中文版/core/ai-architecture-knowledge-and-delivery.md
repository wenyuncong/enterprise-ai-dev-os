# `ai-architecture-knowledge-and-delivery` — 架构知识与交付

> **源文件**：skills/core/ai-architecture-knowledge-and-delivery/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-11-08
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-architecture-knowledge-and-delivery
description: "Use when scanning an existing project into a language-neutral Architecture IR, generating an applicable 13-step delivery plan and task DAG, or publishing bounded static knowledge-center evidence without treating the graph as runtime truth."
```

**中文描述**：在把存量项目扫描为语言中立的架构 IR（Architecture IR）、生成可适用的 13 步交付计划与任务 DAG，或发布有界的静态知识中心证据时使用；不把生成的图当作运行时真相。

---

## Rule | 规则

架构发现是只读证据。它必须保留来源归属、展示置信度与局限，绝不替代运行时、数据库、授权、业务流程或发布证据。

## When to Use | 何时使用

- 在存量项目接入之后、规划实现工作之前。
- 当项目使用不止一种语言、框架、客户端、服务或数据库，且依赖边界未被记录时。
- 当项目需要自动刷新的技术知识中心，或需要生成的交付任务包时。
- 禁止把生成的图当作修改代码、执行迁移或宣称业务流程完成的许可。

## Workflow | 工作流

```text
Project Scan -> Technology Profile -> Architecture IR
-> 13-Step Applicability Plan -> Task DAG -> Knowledge Center -> Incremental Refresh
项目扫描 -> 技术画像 -> 架构 IR
-> 13 步可适用性计划 -> 任务 DAG -> 知识中心 -> 增量刷新
```

当正在引入方法论资产、外部技能或项目知识基础设施时，在本技能之前先使用既有的接入工作流。

## Required outputs | 必交产出

`py scripts/py/architecture_delivery.py --project-root <project> --output knowledge/architecture`

- `architecture-ir.json`：语言中立的节点与边，含来源与置信度。
- `delivery-plan.json`：全部 13 步标注为 `applicable`、`not_applicable` 或 `needs_confirmation`。
- `task-dag.json`：按依赖排序的执行节点。
- `index.html`：只读静态知识中心。

## Supported evidence | 支持的证据

扫描器当前使用清单、源文件、导入、常见路由声明、SQL `CREATE TABLE` 语句、测试与部署标记。适配器可在不改变 IR 的前提下扩展对其他语言的检测。

## Guardrails | 防护规则

- 扫描期间禁止执行迁移或修改应用源码。
- 禁止从静态节点推断业务真相、权限、运行时健康或生产闭环。
- 禁止把破坏性、迁移、发布或业务验收工作标记为自动；它们保持 `needs_confirmation`。
- 在有实质的源码、依赖、脚本或技能变更后增量刷新，并保留扫描限制与时间戳。
