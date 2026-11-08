---
name: ai-library-first
description: "Enforce library-first development by checking mature packages, built-in framework features, and existing project utilities before custom implementation. Use before writing new logic, parsers, UI widgets, engines, integrations, or scripts from scratch."
metadata:
  requires:
    scope: universal
    declared-by: enterprise-ai-dev-os
---

## Rule

Before creating anything new: 1) Search existing libraries/components, 2) Check if existing can be extended, 3) Only create new if nothing matches, 4) Register new in shared catalog, 5) Document the reuse decision. Never duplicate without explicit justification.

# ai-library-first — Library-First Development Governor

## Purpose

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

### Frontend

The exact library follows the project's existing stack. For each need, use the component library's built-in component or a maintained, actively used library; never write it from scratch.

| Need | Use This | Never Write From Scratch |
|---|---|---|
| Date picker | component-library date picker or a maintained date library | custom date input |
| Table / data grid | component-library data grid or a maintained table library | custom table with sorting |
| Form validation | component-library form or a maintained validation library | custom validation functions |
| Charts | a maintained charting library | custom SVG/canvas drawings |
| Icons | the icon set shipped with the library or a maintained icon package | custom SVG icons |
| State management | a maintained state library | custom reactive store |
| Drag and drop | a maintained drag-and-drop library | custom drag handlers |
| Rich text editor | a maintained editor library | custom contenteditable |
| File upload | component-library upload or a maintained upload library | custom XHR upload |
| Toast / notification | component-library notification component | custom toast component |
| Modal / dialog | component-library dialog component | custom modal overlay |
| HTTP client | the stack's maintained HTTP client | custom fetch wrapper |
| Router | the stack's official router | custom routing logic |
| i18n | a maintained i18n library | custom translation system |
| Virtual scroll | a maintained virtualization library | custom scroll optimization |

### Backend

The exact library follows the project's language and framework. For each need, use the framework's module or a maintained library rather than building low-level infrastructure yourself.

| Need | Use This | Never Write From Scratch |
|---|---|---|
| Persistence / ORM | the stack's ORM or persistence library | custom low-level driver wrapper |
| Validation | the framework's validation module | custom annotation/hand-written validators |
| Cache | the framework's cache abstraction over a maintained cache store | custom in-memory map cache |
| Rate limiting | a maintained resilience/rate-limit library | custom counter logic |
| Logging | the framework's logging facade | custom logging framework |
| Serialization | the stack's maintained serialization library | custom parser |
| Spreadsheet export | a maintained spreadsheet library | custom file-format writer |
| API docs | the framework's documentation tool | hand-rolled spec config |
| Job scheduling | a maintained scheduler | custom cron executor |
| Security | the framework's security module | custom auth filter |
| Code generation | a maintained generator | custom template engine |
| Messaging (SMS/email) | a maintained messaging client | custom protocol client |
| Web framework | the stack's maintained framework | custom HTTP server |
| Queue / jobs | a maintained job queue | custom job queue |
| Real-time | a maintained real-time library | custom socket handler |
| Testing | the stack's maintained test runner | custom test runner |

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
- **Prefer the project's existing libraries** — if the project already has a component library, don't add a second one for a single component
- **Library version must be pinned** — no `^` or `~` in production, use exact versions
- **One library per concern** — don't use 3 different date libraries in one project
- **No wrapper libraries** — don't wrap axios in a "custom HTTP client" that adds nothing

## Maturity | 成熟度

**Stage**: New — Created from analysis of massive token waste patterns in AI-assisted development.

## Evolution History | 进化记录

- v1.0.0: Initial creation — stack-neutral library catalog and token cost analysis
