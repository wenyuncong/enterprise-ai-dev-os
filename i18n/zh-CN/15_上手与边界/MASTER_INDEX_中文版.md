# 全项目总控 — 企业级全 AI 开发方法论知识库索引 | Master Index — Enterprise-Grade Full-AI Development Methodology Knowledge Base

> **源文件**：docs/全项目总控/MASTER_INDEX.md
> **源版本**：未标注（源文件末尾仅标注「上次更新: 2026-08-21」）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。已是中文的段落原样保留，不重译。

---

> 目的：作为可移植方法论包导航的唯一真相源（single source of truth）。
> 更新规则：正式 Skill 数量、规则入口或交付闭环资产发生变更后，必须更新本索引。

---

## 1. 正式源目录

| 类型 | 路径 | 说明 |
|---|---|---|
| 规则入口 | `AGENTS.md`, `rules/AGENTS.md` | 会话启动、执行顺序、目录边界、验证门禁 |
| Skill 源目录 | `skills/` | 唯一正式可迁移 Skill 根目录 |
| Skill 清单（Skill Manifest） | `skills/SKILL_MANIFEST.json` | 正式 Skill 数量、层级、来源、成熟度 |
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
| CANDIDATE | 全 AI 原生候选能力评估与验证协议 | `docs/全项目总控/AI_NATIVE_CANDIDATE_CAPABILITY_PROTOCOL.md` | 已完成 |
| CONTRACT | 可执行交付契约 | `docs/全项目总控/schemas/governance/delivery-contract.schema.json` | 已完成 |
| AUTOPILOT | 全自动交付协议 | `docs/全项目总控/AUTOPILOT_DELIVERY_PROTOCOL.md` | 已完成 |

---

## 3. 正式 Skill 总览

正式 Skill 数量以 `skills/SKILL_MANIFEST.json` 为准。

| 层级 | 数量 | 路径 |
|---|---:|---|
| 核心引擎（Core Engine） | 16 | `skills/core/` |
| 治理（Governance） | 13 | `skills/governance/` |
| 技术栈（Tech Stack） | 20 | `skills/tech/` |
| 平台（Platform） | 0 | `skills/platform/` 当前为空 |
| **合计** | **49** | `skills/` |

### 核心引擎 | Core Engine

| Skill | 路径 |
|---|---|
| ai-architect-governor | `skills/core/ai-architect-governor/` |
| ai-atomic-architect | `skills/core/ai-atomic-architect/` |
| ai-chief-planner | `skills/core/ai-chief-planner/` |
| ai-command-executor | `skills/core/ai-command-executor/` |
| ai-5s-delivery-governor | `skills/core/ai-5s-delivery-governor/` |
| ai-delivery-contract-governor | `skills/core/ai-delivery-contract-governor/` |
| ai-foundation-governor | `skills/core/ai-foundation-governor/` |
| ai-library-first | `skills/core/ai-library-first/` |
| ai-multi-agent-orchestration | `skills/core/ai-multi-agent-orchestration/` |
| ai-project-classifier | `skills/core/ai-project-classifier/` |
| ai-product-directed-delivery | `skills/core/ai-product-directed-delivery/` |
| ai-rule-dispatcher | `skills/core/ai-rule-dispatcher/` |
| ai-skill-evolver | `skills/core/ai-skill-evolver/` |
| ai-skill-governor | `skills/core/ai-skill-governor/` |
| ai-task-decomposer | `skills/core/ai-task-decomposer/` |
| ai-tool-bootstrapper | `skills/core/ai-tool-bootstrapper/` |

### 治理 | Governance

| Skill | 路径 |
|---|---|
| ai-brownfield-analyzer | `skills/governance/ai-brownfield-analyzer/` |
| ai-competitor-analyst | `skills/governance/ai-competitor-analyst/` |
| ai-component-standardizer | `skills/governance/ai-component-standardizer/` |
| ai-cross-project-audit | `skills/governance/ai-cross-project-audit/` |
| ai-domain-boundary-mapper | `skills/governance/ai-domain-boundary-mapper/` |
| ai-field-package-governor | `skills/governance/ai-field-package-governor/` |
| ai-flow-closure-audit | `skills/governance/ai-flow-closure-audit/` |
| ai-frontend-audit | `skills/governance/ai-frontend-audit/` |
| ai-reference-researcher | `skills/governance/ai-reference-researcher/` |
| ai-runtime-verify | `skills/governance/ai-runtime-verify/` |
| ai-single-truth-enforcer | `skills/governance/ai-single-truth-enforcer/` |
| ai-ui-ux-governor | `skills/governance/ai-ui-ux-governor/` |

### 技术栈 | Tech Stack

| Skill | 路径 |
|---|---|
| docker-expert | `skills/tech/docker-expert/` |
| flutter-animations | `skills/tech/flutter-animations/` |
| flutter-expert | `skills/tech/flutter-expert/` |
| java-springboot | `skills/tech/java-springboot/` |
| java-performance-governance | `skills/tech/java-performance-governance/` |
| javascript-typescript-jest | `skills/tech/javascript-typescript-jest/` |
| multi-stage-dockerfile | `skills/tech/multi-stage-dockerfile/` |
| mysql-best-practices | `skills/tech/mysql-best-practices/` |
| node-backend | `skills/tech/node-backend/` |
| postgresql-best-practices | `skills/tech/postgresql-best-practices/` |
| python-fastapi | `skills/tech/python-fastapi/` |
| react-frontend | `skills/tech/react-frontend/` |
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
| 开源发布包 | `docs/公开材料/OPEN_SOURCE_PACKAGE.md` |
| 开源就绪清单 | `docs/公开材料/OPEN_SOURCE_READINESS.md` |
| 安装说明 | `docs/公开材料/INSTALL.md` |
| 路线图 | `docs/公开材料/ROADMAP.md` |
| 价值证据 | `docs/公开材料/VALUE_EVIDENCE.md` |
| 轻量规则运行时 | `docs/公开材料/RULE_RUNTIME_LITE.md` |

公开仓库只保留披露边界，不收录私有策略材料、过程记录或未脱敏案例。

---

## 6. 验证与门禁

| 工具 | 路径 | 用途 |
|---|---|---|
| 环境检查 | `scripts/py/env_check.py` | 检查 Node、Python、Git、Java、MySQL、Playwright 等工具 |
| 工具发现 | `scripts/py/discover_tools.py` | 按用途盘点项目现有脚本 |
| 方法论审计 | `scripts/py/audit_methodology.py` | 检查 manifest、路径残留、AGENTS 引用、Skill 结构 |
| AI 开发确定性评分 | `scripts/py/score_ai_development_readiness.py` | 输出结构就绪分和缺口建议 |
| 治理契约 Schema 审计 | `scripts/py/audit_governance_contracts.py` | 检查公开治理契约 JSON Schema 可解析、ID 唯一、索引完整 |
| 全 AI 治理契约审计 | `scripts/py/audit_ai_native_governance.py` | 检查候选能力评估、授权委托和执行证据契约是否齐全 |
| 交付契约校验 | `scripts/py/validate_delivery_contract.py` | 拒绝越界写入、陈旧证据和缺失独立复核 |
| 多工具部署 | `tools/deploy.ps1` | 将 `skills/` 和 `rules/AGENTS.md` 同步到 AI 工具适配目录 |

推荐收尾命令：

```powershell
py scripts/py/audit_methodology.py --project-root .
py scripts/py/audit_governance_contracts.py --project-root .
py scripts/py/audit_ai_native_governance.py --project-root .
py scripts/py/validate_delivery_contract.py --contract <task-contract.json> --check-freshness
py scripts/py/score_ai_development_readiness.py --project-root .
```

---

## 7. 私有素材说明

私有素材、过程记录和未脱敏案例不属于公开仓库内容。公开发布只以 `skills/`、`rules/`、`methodology/`、`docs/公开材料/` 和验证脚本为准。

---

**上次更新**: 2026-08-21

---

## 译注 | Translation Notes

### 1. 本次翻译的范围

- **原为英文、本次翻译（共 9 处）**：源文件开头 `Purpose` / `Update rule` 引用块 1 处（2 句）；第 1 节表项 `Skill Manifest` 1 处；第 3 节计数表中的层级名 `Core Engine`、`Governance`、`Tech Stack`、`Platform` 共 4 处；第 3 节层级小标题 `### Core Engine`、`### Governance`、`### Tech Stack` 共 3 处。
- **原本已是中文、原样保留**：其余全部正文块——章节标题、第 1 节表格（除 `Skill Manifest` 表项）、第 2 节方法论文档表、第 3 节三张 Skill 表与合计表（除层级名）、第 4 节模板表、第 5 节披露边界表、第 6 节验证与门禁表与收尾命令代码块、第 7 节私有素材说明、末尾更新日期。
- **标题处理**：源文件主标题已是中文，按本篇格式补英文对照题名。已为中文的小节标题（如「## 1. 正式源目录」）一律原样保留，不新造英文题名、不改写中文。

### 2. 索引路径核对结果（逐条比对仓库实际文件系统）

- 源文件 `MASTER_INDEX.md` 中全部索引路径均存在，**未发现指向不存在路径的索引项**。已核对范围包括：`methodology/00...10` 共 11 个方法论文档；`docs/全项目总控/` 下的 `AI_NATIVE_DELIVERY_LOOP.md`、`AI_NATIVE_CANDIDATE_CAPABILITY_PROTOCOL.md`、`AUTOPILOT_DELIVERY_PROTOCOL.md`、`schemas/governance/delivery-contract.schema.json`；`docs/_templates/` 下 5 个模板目录；`docs/公开材料/` 下 7 个披露边界文档；`scripts/py/` 下 7 个验证脚本与 `tools/deploy.ps1`；以及第 3 节列出的全部 Skill 目录（源文件 48 个，补齐缺行后 49 个）。`skills/platform/` 目录存在，但**并非空目录**（见第 3 节过时信息第 3 项），源文件「当前为空」的表述与磁盘现状不符。
- **源文件遗漏的表行（保留原样，未补）**：源文件第 3 节合计表将 Governance 记为 13，但紧随其后的 Governance 表只列出 12 个 Skill，缺少 `ai-atomic-governance`。该 Skill 实际存在于 `skills/governance/ai-atomic-governance/`，且属于术语表第 12.2 节所列 49 个正式 Skill 之一。**为保持「中英逐行可对表、译文不增删语义」的口径，译文未补入该行**，仅在此处登记，供源仓库修正。

### 3. 源文件中发现的过时信息

| # | 位置 | 源文件表述 | 与现状的差异 |
|---|---|---|---|
| 1 | 第 3 节 Governance 表 | 只列 12 个 Skill（合计表记为 13） | 缺 `ai-atomic-governance`；该目录已存在于 `skills/governance/`，且计入 49 个正式 Skill |
| 2 | 文末 | `**上次更新**: 2026-08-21` | 索引日期早于规则文件的 `Last updated: 2026-08-24`；此后新增的总控资产未反映到本索引 |
| 3 | 第 3 节合计表 | Platform 行写「`skills/platform/` 当前为空」 | 该目录下实际存在 `cnb-api`、`cnb-code-commit`、`cnb-code-review`、`cnb-pipeline` 4 个平台集成 Skill 目录；`skills/SKILL_MANIFEST.json` 的 `counts.byLayer.platform` 记为 0，并将它们列入 `rawOnlySkills`（未计为正式 Skill）。准确表述应为「Platform 层当前无正式 Skill」，而非「目录为空」 |
| 4 | 第 5 节披露边界表 | 只登记 7 个 `docs/公开材料/` 文档 | 未登记已存在且已被 `docs/公开材料/OPEN_SOURCE_PACKAGE.md` 列为公开内容的 `docs/公开材料/CUSTOMER_INVESTOR_VALUE.md` |
| 5 | 第 2 节方法论文档表 | 只登记 `methodology/00...10` 与 4 项 `docs/全项目总控/` 交付资产 | 未登记仓库中已存在的总控资产：`docs/全项目总控/CONSTITUTION.md`、`docs/全项目总控/TASK_BACKLOG.md`、`docs/全项目总控/AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX.md`、`docs/全项目总控/pattern_ledger.json`；`docs/公开材料/` 下的 `FULL_AI_NATIVE_DEVELOPMENT_STANDARD_CN.md`、`FULL_AI_NATIVE_DEVELOPMENT_STANDARD_EN.md`、`FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_CN.md`、`FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_EN.md` 亦未登记 |
| 6 | 第 6 节验证与门禁表 | 未登记 `scripts/py/audit_reference_links.py`、`scripts/py/tool_registry.py` | 两个脚本均存在于 `scripts/py/`（其中 `audit_reference_links.py` 已被 `docs/公开材料/OPEN_SOURCE_PACKAGE.md` 列为公开内容） |

> 说明：第 1–3 项属内容与标注陈旧，第 4–6 项属索引覆盖缺口（路径本身有效）。本译文只如实翻译并在此登记，未改动源文件 `docs/全项目总控/MASTER_INDEX.md`。

### 4. 保留英文的项

- Skill 名、Skill 目录路径、`methodology/`、`docs/`、`scripts/`、`tools/` 等路径全部原样保留。
- 第 2 节表内的 `LOOP`、`CANDIDATE`、`CONTRACT`、`AUTOPILOT` 为索引代号，原样保留。
- 收尾命令代码块（`powershell`）原样复制，未译、未改。
