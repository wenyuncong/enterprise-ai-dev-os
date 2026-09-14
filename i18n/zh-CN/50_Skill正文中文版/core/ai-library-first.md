# `ai-library-first` — 库优先开发治理

> **源文件**：skills/core/ai-library-first/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-library-first
description: "Enforce library-first development by checking mature packages, built-in framework features, and existing project utilities before custom implementation. Use before writing new logic, parsers, UI widgets, engines, integrations, or scripts from scratch."
```

**中文描述**：在自研实现之前，核查成熟包、框架内建能力与项目既有工具，强制「库优先（library first）」开发。在从零手写新逻辑、解析器、UI 组件、引擎、集成或脚本之前使用。

---

## Rule | 规则

在创建任何新东西之前：1）检索既有库/组件；2）检查既有对象能否被扩展；3）只有在没有任何匹配项时才新建；4）把新建项登记进共享目录；5）记录复用决策。禁止在没有明确理由的情况下重复实现（duplicate）。

# ai-library-first — Library-First Development Governor | 库优先开发治理

## Purpose | 用途

强制这条规则：**在写下第一行自研代码之前，先核查成熟开源库是否已经实现了它。** 本 Skill 阻断 AI 辅助开发中 Token 浪费与代码不稳定的第一大成因——重新发明 npm/pip/maven 中早已存在的组件。

**它解决的问题**：AI 习惯性地从零手写日期选择器、表格组件、表单校验器、图表渲染器，甚至状态管理。这会浪费数千个 Token，产出有缺陷的代码，并留下可维护性极差的自研实现——而成熟可靠的库多年前就已解决同类问题。

---

## The Prime Directive | 最高指令

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   NEVER WRITE FROM SCRATCH WHAT A LIBRARY ALREADY DOES   │
│                                                          │
│   Check → Choose → Install → Configure → Use             │
│   (10 tokens)  vs  Rewrite from scratch (5000+ tokens)   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Decision Flow | 决策流程

```
Task: "I need a [component / utility / feature]"

    ┌─────────────────┐
    │ Does a standard  │
    │ library exist?   │
    └────────┬─────────┘
             │
      ┌──────┼──────┐
      │ YES          │ NO
      ▼              ▼
┌──────────┐   ┌──────────────┐
│ Is library│   │ Is this truly │
│ mature?   │   │ novel/unique? │
└────┬─────┘   └──────┬───────┘
     │                │
 ┌───┼───┐       ┌────┼────┐
 │YES    │NO     │YES       │NO
 ▼       ▼       ▼          ▼
USE   FIND     WRITE     SEARCH
IT    BETTER   CUSTOM    HARDER
      ONE                (you probably
                          missed one)
```

---

## Standard Library Catalog | 标准库目录

### Frontend (Vue/React) | 前端（Vue/React）

| 需求 | 应当使用 | 禁止自研 |
|---|---|---|
| 日期选择器 | `element-plus` DatePicker / `vuetify` / `react-datepicker` | 自研日期输入 |
| 表格/数据网格 | `element-plus` Table / `ag-grid` / `tanstack-table` | 自研带排序的 `<table>` |
| 表单校验 | `element-plus` Form / `vee-validate` / `react-hook-form` | 自研校验函数 |
| 图表 | `echarts` / `chart.js` / `recharts` | 自研 SVG/canvas 绘制 |
| 图标 | `lucide-vue-next` / `@element-plus/icons-vue` | 自研 SVG 图标 |
| 状态管理 | `pinia` / `zustand` / `jotai` | 自研响应式 store |
| 拖拽 | `vuedraggable` / `@dnd-kit/core` | 自研拖拽处理器 |
| 富文本编辑器 | `tiptap` / `quill` | 自研 contenteditable |
| 文件上传 | `element-plus` Upload / `uppy` | 自研 XHR 上传 |
| 轻提示（Toast）/通知 | `element-plus` ElMessage / `sonner` | 自研 toast 组件 |
| 模态框（Modal）/对话框 | `element-plus` ElMessageBox / Dialog | 自研模态遮罩层 |
| HTTP 客户端 | `axios` / `ofetch` | 自研 `fetch` 封装 |
| 路由 | `vue-router` / `react-router` | 自研路由逻辑 |
| 国际化（i18n） | `vue-i18n` / `i18next` | 自研翻译系统 |
| 虚拟滚动 | `vue-virtual-scroller` / `@tanstack/virtual` | 自研滚动优化 |

### Backend (Java/Spring Boot) | 后端（Java/Spring Boot）

| 需求 | 应当使用 | 禁止自研 |
|---|---|---|
| ORM | `MyBatis-Plus` / `JPA/Hibernate` | 自研 JDBC 封装 |
| 校验 | `jakarta.validation` / `hibernate-validator` | 自研注解校验器 |
| 缓存 | `Spring Cache` + `Redis/Caffeine` | 自研 HashMap 缓存 |
| 限流 | `bucket4j` / `resilience4j` | 自研计数器逻辑 |
| 日志 | `SLF4J` + `Logback` | 自研日志框架 |
| JSON | `Jackson` / `Gson` / `fastjson2` | 自研 JSON 解析器 |
| Excel | `EasyExcel` / `Apache POI` | 自研 XLSX 写入器 |
| API 文档 | `SpringDoc OpenAPI` / `Knife4j` | 自研 Swagger 配置 |
| 任务调度 | `XXL-Job` / `Quartz` | 自研 cron 执行器 |
| 安全 | `Spring Security` + `Sa-Token` | 自研认证过滤器 |
| 代码生成 | `MyBatis-Plus Generator` | 自研模板引擎 |
| 短信/邮件 | `aliyun-sms` / `javax.mail` | 自研 SMTP 客户端 |

### Backend (Node.js/Express) | 后端（Node.js/Express）

| 需求 | 应当使用 | 禁止自研 |
|---|---|---|
| Web 框架 | `express` / `fastify` / `hono` | 自研 HTTP 服务器 |
| ORM | `prisma` / `drizzle-orm` / `typeorm` | 自研 SQL 构造器 |
| 校验 | `zod` / `joi` / `yup` | 自研校验器 |
| 认证 | `lucia-auth` / `next-auth` / `passport` | 自研会话处理 |
| 文件上传 | `multer` / `busboy` | 自研 multipart 解析器 |
| 队列/任务 | `bullmq` / `bee-queue` | 自研任务队列 |
| 实时通信 | `socket.io` / `ws` | 自研 WebSocket 处理器 |
| 日志 | `pino` / `winston` | 自研 logger |
| 测试 | `vitest` / `jest` + `supertest` | 自研测试运行器 |
| 限流 | `express-rate-limit` | 自研速率计数器 |

---

## Token Cost Analysis | Token 成本分析

自研 vs 使用库：

| 组件 | 自研实现 | 使用库 | Token 节省 |
|---|---|---|---|
| 带排序/筛选/分页的数据表格 | ~8000 tokens | ~200 tokens（import + 配置） | **97.5%** |
| 日期选择器 | ~5000 tokens | ~150 tokens | **97%** |
| 表单校验 | ~3000 tokens | ~100 tokens | **96.7%** |
| 图表（柱/线/饼） | ~7000 tokens | ~250 tokens | **96.4%** |
| 拖拽 | ~4000 tokens | ~150 tokens | **96.3%** |
| 富文本编辑器 | ~15000 tokens | ~300 tokens | **98%** |
| 认证系统 | ~10000 tokens | ~500 tokens | **95%** |

**平均节省**：Token 减少约 96%，且库版本更稳定、还有文档。

---

## When Custom IS Acceptable | 允许自研的场景

只有以下三种情况才构成自研的正当理由：

1. **确实全新**：该具体需求没有任何库存在（罕见——必须彻底核查）
2. **许可证**：库许可与项目不兼容（例如专有软件中引入 GPL）
3. **性能**：在该具体用例下，库比自研实现慢 10 倍以上（必须实测基准）

**如果你主张第 1 种情况，必须列出你核查过的 3 个库，并说明每个被否决的原因。**

---

## Integration | 集成

| Skill | 它如何使用 ai-library-first |
|---|---|
| `ai-chief-planner` Phase 1 | 任务分解前先核查库目录 |
| `ai-task-decomposer` | 每个任务批次列出所需库 |
| `ai-tool-bootstrapper` | 自动安装已声明的库依赖 |
| `ai-skill-evolver` | 把新发现的库补充进目录 |

---

## Audit: Has AI Reinvented a Wheel? | 审计：AI 是否重复造轮子？

对任何 PR 或已完成任务执行此项检查：

```
1. List all custom utility functions/modules created
2. For each: does a standard library exist that already does this?
3. If YES → REJECT: replace with library
4. If NO → document why custom was necessary
```

**中文对照**：

1. 列出本次创建的所有自研工具函数/模块。
2. 逐个核查：是否已存在能实现同一功能的成熟库？
3. 若存在 → **拒绝**：改为使用库。
4. 若不存在 → 记录为何必须自研。

## Guardrails | 防护规则

- **在写任何代码之前核查库目录** —— 而不是写完之后
- **优先使用项目既有库** —— 若项目使用 Element Plus，禁止为单个组件引入 Ant Design
- **库版本必须锁定** —— 生产环境禁止使用 `^` 或 `~`，必须使用精确版本
- **一个关注点只用一个库** —— 禁止在同一项目里使用 3 个不同的日期库
- **禁止包装型库** —— 禁止把 `axios` 包一层毫无增益的「自研 HTTP 客户端」

## Maturity | 成熟度

**Stage**：New（新建）—— 来源于对 AI 辅助开发中大规模 Token 浪费模式的分析。

## Evolution History | 进化记录

- v1.0.0：初始创建 —— 覆盖 Vue、React、Java Spring Boot、Node.js 的库目录，以及 Token 成本分析

---

## 译注

- 源文件 frontmatter 未标注版本号；`skills/SKILL_MANIFEST.json` 中该 Skill 的 `maturity` 为 `verified`，且 `source` 记为 `methodology extraction`。正文 `## Maturity` 自述 Stage 为 `New`，两者口径不同，本译文如实保留原文。
- 源文件第 175 行原文为 `project''s`（双单引号），译文按 `project's` 处理。
- `## Audit: Has AI Reinvented a Wheel?` 与 `## Guardrails`、`## Maturity`、`## Evolution History` 在源文件中没有 `| 中文` 后缀，本译文为可读性补了中文标题，未改动章节内容。
