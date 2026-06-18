---
name: ai-library-first
description: "Enforce library-first development by checking mature packages, built-in framework features, and existing project utilities before custom implementation. Use before writing new logic, parsers, UI widgets, engines, integrations, or scripts from scratch."
---

# ai-library-first — Library-First Development Governor

## Purpose | 用途

Enforce the rule: **before writing a single line of custom code, check if a mature open-source library already does it.** This skill prevents the #1 cause of token waste and unstable code in AI-assisted development — reinventing components that already exist in npm/pip/maven.

**Problem it solves**: AI routinely writes custom date pickers, table components, form validators, chart renderers, and even state management from scratch. This wastes thousands of tokens, produces buggy code, and creates unmaintainable custom implementations that a proven library solved years ago.

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

### Frontend (Vue/React)

| Need | Use This | Never Write From Scratch |
|---|---|---|
| Date picker | `element-plus` DatePicker / `vuetify` / `react-datepicker` | Custom date input |
| Table/DataGrid | `element-plus` Table / `ag-grid` / `tanstack-table` | Custom `<table>` with sorting |
| Form validation | `element-plus` Form / `vee-validate` / `react-hook-form` | Custom validation functions |
| Charts | `echarts` / `chart.js` / `recharts` | Custom SVG/canvas drawings |
| Icons | `lucide-vue-next` / `@element-plus/icons-vue` | Custom SVG icons |
| State management | `pinia` / `zustand` / `jotai` | Custom reactive store |
| Drag & drop | `vuedraggable` / `@dnd-kit/core` | Custom drag handlers |
| Rich text editor | `tiptap` / `quill` | Custom contenteditable |
| File upload | `element-plus` Upload / `uppy` | Custom XHR upload |
| Toast/notification | `element-plus` ElMessage / `sonner` | Custom toast component |
| Modal/Dialog | `element-plus` ElMessageBox / Dialog | Custom modal overlay |
| HTTP client | `axios` / `ofetch` | Custom `fetch` wrapper |
| Router | `vue-router` / `react-router` | Custom routing logic |
| i18n | `vue-i18n` / `i18next` | Custom translation system |
| Virtual scroll | `vue-virtual-scroller` / `@tanstack/virtual` | Custom scroll optimization |

### Backend (Java/Spring Boot)

| Need | Use This | Never Write From Scratch |
|---|---|---|
| ORM | `MyBatis-Plus` / `JPA/Hibernate` | Custom JDBC wrapper |
| Validation | `jakarta.validation` / `hibernate-validator` | Custom annotation validators |
| Cache | `Spring Cache` + `Redis/Caffeine` | Custom HashMap cache |
| Rate limiting | `bucket4j` / `resilience4j` | Custom counter logic |
| Logging | `SLF4J` + `Logback` | Custom logging framework |
| JSON | `Jackson` / `Gson` / `fastjson2` | Custom JSON parser |
| Excel | `EasyExcel` / `Apache POI` | Custom XLSX writer |
| API docs | `SpringDoc OpenAPI` / `Knife4j` | Custom Swagger config |
| Job scheduling | `XXL-Job` / `Quartz` | Custom cron executor |
| Security | `Spring Security` + `Sa-Token` | Custom auth filter |
| Code generation | `MyBatis-Plus Generator` | Custom template engine |
| SMS/Email | `aliyun-sms` / `javax.mail` | Custom SMTP client |

### Backend (Node.js/Express)

| Need | Use This | Never Write From Scratch |
|---|---|---|
| Web framework | `express` / `fastify` / `hono` | Custom HTTP server |
| ORM | `prisma` / `drizzle-orm` / `typeorm` | Custom SQL builder |
| Validation | `zod` / `joi` / `yup` | Custom validator |
| Auth | `lucia-auth` / `next-auth` / `passport` | Custom session handler |
| File upload | `multer` / `busboy` | Custom multipart parser |
| Queue/Jobs | `bullmq` / `bee-queue` | Custom job queue |
| Real-time | `socket.io` / `ws` | Custom WebSocket handler |
| Logging | `pino` / `winston` | Custom logger |
| Testing | `vitest` / `jest` + `supertest` | Custom test runner |
| Rate limit | `express-rate-limit` | Custom rate counter |

---

## Token Cost Analysis | Token成本分析

Writing from scratch vs using a library:

| Component | Custom Implementation | Using Library | Token Savings |
|---|---|---|---|
| Data table with sort/filter/page | ~8000 tokens | ~200 tokens (import + config) | **97.5%** |
| Date picker | ~5000 tokens | ~150 tokens | **97%** |
| Form validation | ~3000 tokens | ~100 tokens | **96.7%** |
| Chart (bar/line/pie) | ~7000 tokens | ~250 tokens | **96.4%** |
| Drag and drop | ~4000 tokens | ~150 tokens | **96.3%** |
| Rich text editor | ~15000 tokens | ~300 tokens | **98%** |
| Auth system | ~10000 tokens | ~500 tokens | **95%** |

**Average savings**: ~96% fewer tokens, and the library version is more stable and has documentation.

---

## When Custom IS Acceptable | 允许自定义的情况

Only these three scenarios justify custom implementation:

1. **Truly novel**: No library exists for this specific need (rare — verify thoroughly)
2. **Licensing**: Library license incompatible with project (GPL in proprietary software)
3. **Performance**: Library is 10x+ slower than custom implementation for this specific use case (must benchmark)

**If you claim scenario 1, you must list the 3 libraries you checked and why each was rejected.**

---

## Integration | 集成

| Skill | How it uses ai-library-first |
|---|---|
| `ai-chief-planner` Phase 1 | Check library catalog before task decomposition |
| `ai-task-decomposer` | Each task batch lists required libraries |
| `ai-tool-bootstrapper` | Auto-installs declared library dependencies |
| `ai-skill-evolver` | Adds newly discovered libraries to catalog |

---

## Audit: Has AI Reinvented a Wheel? | 审计

Run this check on any PR or completed task:

```
1. List all custom utility functions/modules created
2. For each: does a standard library exist that already does this?
3. If YES → REJECT: replace with library
4. If NO → document why custom was necessary
```

## Guardrails | 防护规则

- **Check library catalog BEFORE writing any code** — not after
- **Prefer the project''s existing libraries** — if the project uses Element Plus, don't install Ant Design for one component
- **Library version must be pinned** — no `^` or `~` in production, use exact versions
- **One library per concern** — don't use 3 different date libraries in one project
- **No wrapper libraries** — don't wrap axios in a "custom HTTP client" that adds nothing

## Maturity | 成熟度

**Stage**: New — Created from analysis of massive token waste patterns in AI-assisted development.

## Evolution History | 进化记录

- v1.0.0: Initial creation — library catalog for Vue, React, Java Spring Boot, Node.js, token cost analysis
