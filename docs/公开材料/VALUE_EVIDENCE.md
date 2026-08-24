# Value Evidence | 价值证据

This file defines how to prove whether Enterprise AI Development OS creates real value. Do not use unverified market percentages or private project details in public claims.

本文件用于定义如何证明 Enterprise AI Development OS 的真实价值。公开表述不得使用未经验证的市场百分比或私有项目细节。

## Evidence Principles | 证据原则

- Compare before and after the methodology is installed.
- Count rework and bug-fix cost, not only first-pass generation cost.
- Separate simple tasks, complex tasks, and whole-project effects.
- Record evidence paths without publishing private logs.
- Prefer small reproducible examples over broad claims.

## Metrics | 指标

| Metric | Meaning | How to record |
|---|---|---|
| First-pass completion | Whether the first AI implementation passed review or tests | pass/fail plus short reason |
| Rework count | How many correction rounds were needed | integer |
| Defect escape | Whether a defect reached runtime/manual verification | yes/no |
| Verification coverage | Which gates were run | audit, unit, API, browser, adapter dry-run |
| Token direction | Whether total task tokens increased or decreased | up/down/unknown with context |
| Rule recall | Whether required rules were loaded and followed | pass/fail |
| Tool consistency | Whether different tools produced compatible behavior | pass/fail/unknown |

## Task-Level Template | 单任务模板

```text
Task:
Project type:
Tool used:
Mode: no methodology / lite / full / full + adapters

Before:
- completion result:
- rework count:
- major defects:
- verification result:
- estimated token direction:

After:
- completion result:
- rework count:
- major defects:
- verification result:
- estimated token direction:

Conclusion:
- improved:
- unchanged:
- worse:
- evidence path:
```

## Summary Table | 汇总表

| Scenario | Baseline result | With Enterprise AI Dev OS | Evidence | Status |
|---|---|---|---|---|
| Simple single-file edit | TBD | TBD | TBD | not measured |
| Cross-file frontend change | TBD | TBD | TBD | not measured |
| Backend API + frontend integration | TBD | TBD | TBD | not measured |
| Brownfield project onboarding | TBD | TBD | TBD | not measured |
| Multi-tool adapter handoff | TBD | TBD | TBD | not measured |

## Sanitized Case Evidence | 脱敏案例证据

> Source: a multi-tenant enterprise ERP (purchase/sales/inventory/finance/production/CRM/WMS/TMS), ~3 months of AI-assisted development. Company, repository paths, and internal logs are redacted. These are illustrative before/after measurements from that engagement, not a guarantee for other projects.

| Dimension | Before | After | Measurement |
|---|---|---|---|
| Frontend field/interface alignment | 3-5 API 404s per new module; ~40% pages needed post-launch rework; ~30 min/page to trace a missing field | 0 404s; 0% rework after audit; ~5 min/page | per-page field-vs-API audit before launch |
| Inventory posting entry points | 6 services each calling stock in/out, logic scattered | 1 idempotent posting service | impact analysis 2-3h -> ~15 min |
| Permission visibility decision points | 3 places (subscription, feature map, page code) | 1 adjudication chain | new-module wiring 4h -> ~30 min; bug triage 60 min -> ~10 min |
| Onboarding / decision context | 5-7 days to rebuild context | ~2 days via ADRs | knowledge retention |
| Skill evolution | 0 skills, manual context each session | 42 skills; evolution triggered on repeated error patterns | capability accumulation |

**Honest limits**: these numbers come from one complex brownfield project and are directional, not benchmarked across projects. Public claims must cite them as a sanitized single case, not as a universal percentage.

## Public Claim Rules | 公开表述规则

Allowed:

- "The project provides rules, skills, adapters, and verification gates."
- "The project is designed to reduce rework and rule drift."
- "Evidence collection is defined in `VALUE_EVIDENCE.md`."

Not allowed until measured:

- "reduces bugs by X%"
- "saves X% tokens"
- "guarantees enterprise-grade delivery"
- "fully solves AI hallucination"

## Next Evidence Work | 下一步证据工作

1. Pick 3 small public-safe tasks.
2. Run each task without the methodology and with lite/full mode.
3. Record rework count, verification result, and failure causes.
4. Publish only sanitized summaries.

