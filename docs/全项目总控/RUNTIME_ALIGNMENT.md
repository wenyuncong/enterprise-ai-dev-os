# RUNTIME_ALIGNMENT.md — Theory Skills → AI-OS Atoms

> 快照日期: 2026-07-05
> 来源: ai-os runtime 自动扫描
> 目的: 帮助理论母体侧了解哪些 Skill 已有 runtime 实现，哪些仍是纯理论

## Governance Skills (11)

| Theory Skill | AI-OS Atom | 文件 | 状态 |
|-------------|-----------|------|------|
| ai-single-truth-enforcer | single_truth_enforcer | atoms/governance/single_truth_enforcer.py | ✅ |
| ai-component-standardizer | component_standardizer | atoms/governance/component_standardizer.py | ✅ |
| ai-frontend-audit | frontend_audit | atoms/governance/frontend_audit.py | ✅ |
| ai-runtime-verify | runtime_verify | atoms/governance/runtime_verify.py | ✅ |
| ai-ui-ux-governor | ui_ux_governor | atoms/governance/ui_ux_governor.py | ✅ |
| ai-flow-closure-audit | task_closure_orchestrator | atoms/governance/task_closure_orchestrator.py | ✅ |
| ai-domain-boundary-mapper | domain_boundary_mapper | atoms/governance/domain_boundary_mapper.py | ✅ |
| ai-field-package-governor | field_package_governor | atoms/governance/field_package_governor.py | ✅ |
| ai-competitor-analyst | competitor_analyst | atoms/governance/competitor_analyst.py | ✅ |
| ai-brownfield-analyzer | brownfield_analyzer | atoms/governance/brownfield_analyzer.py | ✅ |
| ai-reference-researcher | reference_researcher | atoms/governance/reference_researcher.py | ✅ |

## Core Engine Skills (12)

| Theory Skill | AI-OS Atom | 文件 | 状态 |
|-------------|-----------|------|------|
| ai-architect-governor | architect_governor | atoms/governance/architect_governor.py | ✅ |
| ai-atomic-architect | atomic_architect | atoms/methodology/atomic_architect.py | ✅ |
| ai-chief-planner | chief_planner | atoms/methodology/chief_planner.py | ✅ |
| ai-command-executor | dev_pipeline | atoms/methodology/dev_pipeline.py | ⚠️ 间接映射 |
| ai-library-first | library_first | atoms/methodology/library_first.py | ✅ |
| ai-project-classifier | project_classifier | atoms/methodology/project_classifier.py | ✅ |
| ai-rule-dispatcher | task_router | atoms/methodology/task_router.py | ✅ |
| ai-skill-evolver | evolution_engine | atoms/governance/evolution_engine.py | ✅ |
| ai-skill-governor | skill_governor | atoms/governance/skill_governor.py | ✅ |
| ai-task-decomposer | — | — | ❌ 无直接实现 |
| ai-tool-bootstrapper | tool_bootstrapper | atoms/methodology/tool_bootstrapper.py | ✅ |
| ai-foundation-governor | foundation_governor | atoms/governance/foundation_governor.py | ✅ |

## 覆盖率

- **Governance**: 11/11 (100%)
- **Core Engine**: 10/12 (83%)
- **总计**: 21/23 (91%)

## 仅理论侧存在（未实现为 atom）

| Skill | 说明 |
|-------|------|
| ai-task-decomposer | 任务分解逻辑目前在 LangGraph orchestration 层，未封装为独立 atom |
| ai-command-executor | 功能由 dev_pipeline + tools/exec.py 分散实现，无独立 atom |

## 桥接验证

- 三仓链接: 3 workspaces, 3 rules, 1 adapter — all OK
- 证据回写: POST /runtime/gerp/field-package-truth-audit → 理论母体 daily writeback
- 同步检查: `python scripts/py/sync_check.py` — 4/4 OK

---

*此文件为只读快照，不建立理论母体对 ai-os 的硬依赖。*
*由 ai-os governance 系统自动生成，下次更新: 运行 `python scripts/py/gen_checkpoint.py`*
