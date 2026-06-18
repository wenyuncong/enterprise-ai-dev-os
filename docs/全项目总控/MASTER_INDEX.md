# 全项目总控 — 企业级全 AI 开发方法论知识库索引

> Purpose: single source of truth for navigating the portable methodology package.
> Update rule: update this index after changing official skill counts, rule entrypoints, or delivery-loop assets.

---

## 1. 正式源目录

| 类型 | 路径 | 说明 |
|---|---|---|
| 规则入口 | `AGENTS.md`, `rules/AGENTS.md` | 会话启动、执行顺序、目录边界、验证门禁 |
| Skill 源目录 | `skills/` | 唯一正式可迁移 Skill 根目录 |
| Skill Manifest | `skills/SKILL_MANIFEST.json` | 正式 Skill 数量、层级、来源、成熟度 |
| 工具适配 | `.agents/`, `.trae/`, `.qoder/`, `.claude/`, `.codebuddy/` | 由部署脚本同步或适配，不作为源目录 |

---

## 2. 方法论文档

| # | 文档 | 路径 | 状态 |
|---|---|---|---|
| 00 | 核心方法论白皮书 | `methodology/00_核心方法论白皮书.md` | 已完成 |
| 01 | Skill 体系分层架构 | `methodology/01_Skill体系分层架构.md` | 已完成 |
| 02 | 自动寻路与任务调度 | `methodology/02_自动寻路与任务调度.md` | 已完成 |
| 03 | 12 步开发执行引擎 | `methodology/03_12步开发执行引擎.md` | 已完成 |
| 04 | MD 文档总控体系 | `methodology/04_MD文档总控体系.md` | 已完成 |
| 05 | Skill 自动进化机制 | `methodology/05_Skill自动进化机制.md` | 已完成 |
| 06 | 企业级部署与验收标准 | `methodology/06_企业级部署与验收标准.md` | 已完成 |
| 07 | 方法论移植指南 | `methodology/07_方法论移植指南.md` | 已完成 |
| 08 | 项目文件夹结构标准 | `methodology/08_项目文件夹结构标准.md` | 已完成 |
| 09 | 老项目改造方法论 | `methodology/09_老项目改造方法论.md` | 已完成 |
| 10 | 发布治理与锁版体系 | `methodology/10_发布治理与锁版体系.md` | 已完成 |
| LOOP | 企业级全 AI 开发落地闭环 | `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md` | 已完成 |

---

## 3. 正式 Skill 总览

正式 Skill 数量以 `skills/SKILL_MANIFEST.json` 为准。

| 层级 | 数量 | 路径 |
|---|---:|---|
| Core Engine | 12 | `skills/core/` |
| Governance | 11 | `skills/governance/` |
| Tech Stack | 15 | `skills/tech/` |
| Platform | 0 | `skills/platform/` 当前为空 |
| **合计** | **38** | `skills/` |

### Core Engine

| Skill | 路径 |
|---|---|
| ai-architect-governor | `skills/core/ai-architect-governor/` |
| ai-atomic-architect | `skills/core/ai-atomic-architect/` |
| ai-chief-planner | `skills/core/ai-chief-planner/` |
| ai-command-executor | `skills/core/ai-command-executor/` |
| ai-foundation-governor | `skills/core/ai-foundation-governor/` |
| ai-library-first | `skills/core/ai-library-first/` |
| ai-project-classifier | `skills/core/ai-project-classifier/` |
| ai-rule-dispatcher | `skills/core/ai-rule-dispatcher/` |
| ai-skill-evolver | `skills/core/ai-skill-evolver/` |
| ai-skill-governor | `skills/core/ai-skill-governor/` |
| ai-task-decomposer | `skills/core/ai-task-decomposer/` |
| ai-tool-bootstrapper | `skills/core/ai-tool-bootstrapper/` |

### Governance

| Skill | 路径 |
|---|---|
| ai-brownfield-analyzer | `skills/governance/ai-brownfield-analyzer/` |
| ai-competitor-analyst | `skills/governance/ai-competitor-analyst/` |
| ai-component-standardizer | `skills/governance/ai-component-standardizer/` |
| ai-domain-boundary-mapper | `skills/governance/ai-domain-boundary-mapper/` |
| ai-field-package-governor | `skills/governance/ai-field-package-governor/` |
| ai-flow-closure-audit | `skills/governance/ai-flow-closure-audit/` |
| ai-frontend-audit | `skills/governance/ai-frontend-audit/` |
| ai-reference-researcher | `skills/governance/ai-reference-researcher/` |
| ai-runtime-verify | `skills/governance/ai-runtime-verify/` |
| ai-single-truth-enforcer | `skills/governance/ai-single-truth-enforcer/` |
| ai-ui-ux-governor | `skills/governance/ai-ui-ux-governor/` |

### Tech Stack

| Skill | 路径 |
|---|---|
| docker-expert | `skills/tech/docker-expert/` |
| flutter-animations | `skills/tech/flutter-animations/` |
| flutter-expert | `skills/tech/flutter-expert/` |
| java-springboot | `skills/tech/java-springboot/` |
| javascript-typescript-jest | `skills/tech/javascript-typescript-jest/` |
| multi-stage-dockerfile | `skills/tech/multi-stage-dockerfile/` |
| mysql-best-practices | `skills/tech/mysql-best-practices/` |
| springboot-patterns | `skills/tech/springboot-patterns/` |
| springboot-security | `skills/tech/springboot-security/` |
| tailwind-css-patterns | `skills/tech/tailwind-css-patterns/` |
| tailwind-design-system | `skills/tech/tailwind-design-system/` |
| typescript-advanced-types | `skills/tech/typescript-advanced-types/` |
| vue | `skills/tech/vue/` |
| vue-best-practices | `skills/tech/vue-best-practices/` |
| vue-pinia-best-practices | `skills/tech/vue-pinia-best-practices/` |

---

## 4. 文档模板

| 类别 | 路径 |
|---|---|
| 架构决策记录 | `docs/_templates/架构决策记录/` |
| 每日调研回写 | `docs/_templates/每日调研回写/` |
| 业务流程全案 | `docs/_templates/业务流程全案/` |
| 测试验收报告 | `docs/_templates/测试验收报告/` |
| 部署运维手册 | `docs/_templates/部署运维手册/` |

---

## 5. 披露边界

| 文档 | 路径 |
|---|---|
| 披露边界 | `docs/全项目总控/DISCLOSURE_BOUNDARY.md` |

公开仓库只保留披露边界，不收录私有策略材料、过程记录或未脱敏案例。

---

## 6. 验证与门禁

| 工具 | 路径 | 用途 |
|---|---|---|
| 环境检查 | `scripts/py/env_check.py` | 检查 Node、Python、Git、Java、MySQL、Playwright 等工具 |
| 工具发现 | `scripts/py/discover_tools.py` | 按用途盘点项目现有脚本 |
| 方法论审计 | `scripts/py/audit_methodology.py` | 检查 manifest、路径残留、AGENTS 引用、Skill 结构 |
| AI 开发确定性评分 | `scripts/py/score_ai_development_readiness.py` | 输出结构就绪分和缺口建议 |
| 多工具部署 | `tools/deploy.ps1` | 将 `skills/` 和 `rules/AGENTS.md` 同步到 AI 工具适配目录 |

推荐收尾命令：

```powershell
py scripts/py/audit_methodology.py --project-root .
py scripts/py/score_ai_development_readiness.py --project-root .
```

---

## 7. 私有素材说明

私有素材、过程记录和未脱敏案例不属于公开仓库内容。公开发布只以 `skills/`、`rules/`、`methodology/`、`docs/公开材料/` 和验证脚本为准。

---

**上次更新**: 2026-06-18
