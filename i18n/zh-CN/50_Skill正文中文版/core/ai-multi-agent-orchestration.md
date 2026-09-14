# `ai-multi-agent-orchestration` — 多智能体编排

> **源文件**：skills/core/ai-multi-agent-orchestration/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-multi-agent-orchestration
description: "Orchestrate parallel AI agents across domain boundaries: partition a large project into domains, decide parallel vs serial execution by data-dependency, define contracts before integration, and set role/acceptance boundaries. Use when a task spans multiple modules or domains, or when fanning out work across several agents."
```

**中文描述**：跨领域边界编排并行 AI 智能体：把一个大项目切分为领域，按数据依赖决定并行还是串行执行，在集成之前先定义契约，并设定角色与验收边界。适用于任务横跨多个模块或领域，或需要把工作扇出到多个智能体时。

---

## Rule | 规则

- 按领域归属切分，而不是按文件类型切分：每个智能体拥有一个有界的领域，且该领域只有一个真相归属。
- 契约先行：任何跨领域集成点都必须在并行工作开始之前，先定义为读/写契约。
- 只有在没有共享表写入时才并行；只读依赖可以并行。
- 当一个领域写入的数据会被另一个领域在下游读取，或 API 契约尚未定义时，必须串行。
- 每个智能体都有明确的验收边界与非目标清单；禁止任何智能体跨领域静默扩大范围。

## Purpose | 目的

单智能体分解（`ai-task-decomposer`）把一个任务拆成有序批次。多智能体编排则把一个*项目*拆成可并发推进的领域，而不产生合并混乱。这正是方法论中「多 Agent 编排」所缺失的一层：它通过钉住领域边界、依赖方向与契约先行的集成方式，让并行 AI 工作变得确定。

## Trigger | 触发条件

- 何时使用：当一个任务横跨多个模块/领域，或你计划把工作扇出到多个智能体时。
- 何时之前使用：在启动并行智能体之前，或在判断两个任务能否并发执行之前。
- 用于：容易产生合并冲突的工作、跨领域集成，或跨智能体规划一个大批次。

## Workflow | 工作流

1. **切分领域**：按归属与真相归属切分；记录领域清单与每个领域的归属方。
2. **画依赖图**：哪个领域读取哪个其他领域的数据。
3. **对每一对领域定性**，使用并行/串行矩阵：

| 依赖 | 判定 | 原因 |
|---|---|---|
| 无数据依赖 | 并行 | 真相相互独立 |
| 只读依赖（经由 API） | 并行 | 无写入冲突 |
| 共享表写入 | 串行 | 数据竞争 / 锁冲突 |
| 下游读取上游写入 | 串行 | 上游必须先提交 |
| 契约未定义 | 串行 | 先定义契约 |

4. **先定义契约**：为每个跨领域边界定义请求/响应形状、字段真相、错误码、幂等键。
5. **派发智能体**：下发领域范围、读/写白名单、验收标准、非目标，以及契约文档。
6. **在契约边界上串行集成**：声明完成之前，运行回归与一次跨领域闭环审计。

## Guardrails | 防护规则

- 禁止让两个智能体并发写入同一张表或同一个真相源。
- 禁止在集成契约写定之前启动并行工作。
- 禁止在缺少该领域自身通过证据与跨领域契约检查的情况下合并该领域的产出。
- 禁止把「两个智能体都干完了」当作集成完成；必须端到端验证契约成立。

## 术语保留自检

本 Skill 源文件不含审计脚本针对 `ai-product-directed-delivery` 的那 18 条 FAIL 级英文断言短语，故不人为注入。本节只核对本译文按口径保留的英文标识符。

| 项 | 保留形态 | 出现在哪一小节 |
|---|---|---|
| Skill 名 | `ai-multi-agent-orchestration` | 头部 frontmatter、标题 |
| 关联 Skill 名 | `ai-task-decomposer` | `## Purpose 目的` |
| 源文件路径 | `skills/core/ai-multi-agent-orchestration/SKILL.md` | 头部「源文件」 |
| 契约与依赖术语 | 读/写契约、字段真相、幂等键、读/写白名单（对应 request/response shape、field truth、idempotency keys、read/write allowlist） | `## Workflow 工作流` 第 4、5 步 |
| 方法论原生中文词 | 「多 Agent 编排」 | `## Purpose 目的`（源文件即为中文，原样保留） |
