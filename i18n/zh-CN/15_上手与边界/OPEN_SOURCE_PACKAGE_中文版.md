# 开源发布包边界 | Open Source Package Boundary

> **源文件**：docs/公开材料/OPEN_SOURCE_PACKAGE.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。已是中文的段落原样保留，不重译。

---

## 1. 完整开源方法论内核

本仓库不是只发布理念摘要或少量示例，而是公开完整、可迁移的方法论内核：

- `README.md`
- `.editorconfig`
- `AGENTS.md`
- `CLAUDE.md`（如确认内容与 AGENTS 同步且无内部材料）
- `rules/AGENTS.md`
- `skills/`
- `methodology/`
- `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- `docs/全项目总控/AI_NATIVE_CANDIDATE_CAPABILITY_PROTOCOL.md`
- `docs/全项目总控/DISCLOSURE_BOUNDARY.md`
- `docs/全项目总控/MASTER_INDEX.md`
- `docs/全项目总控/schemas/governance/`
- `docs/公开材料/`
- `docs/_templates/`
- `docs/COMPATIBILITY.md`
- `docs/TOOL_ADAPTERS.md`
- `docs/公开材料/INSTALL.md`
- `docs/公开材料/ROADMAP.md`
- `docs/公开材料/CUSTOMER_INVESTOR_VALUE.md`
- `docs/公开材料/VALUE_EVIDENCE.md`
- `docs/公开材料/RULE_RUNTIME_LITE.md`
- `docs/公开材料/OPEN_SOURCE_READINESS.md`
- `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- `docs/全项目总控/DISCLOSURE_BOUNDARY.md`
- `scripts/py/audit_methodology.py`
- `scripts/py/audit_governance_contracts.py`
- `scripts/py/audit_reference_links.py`
- `scripts/py/discover_tools.py`
- `scripts/py/env_check.py`
- `scripts/py/score_ai_development_readiness.py`
- `scripts/py/tool_registry.py`
- `scripts/ps1/install.ps1`
- `scripts/sh/install.sh`
- `scripts/js/cli.mjs`
- `tools/deploy.ps1`
- `tools/adapters.json`
- `package.json`
- `LICENSE`
- `NOTICE`
- `.github/`

上述内容可以作为一个可安装、可审计、可扩展的完整开源方法论包发布。方法论的完整性不意味着公开任何真实项目的生产资料。

## 2. 不进入公开仓库

以下目录和文件默认不公开：

- `docs/内部商业化/`
- `docs/商业化/`
- `docs/每日调研回写/`
- `docs/测试验收报告/`
- `docs/LAUNCH_KIT.md`
- `docs/ERP_TERM_AUDIT.md`
- `docs/AB_EXPERIMENT.md`
- `reference/`
- `备用/`
- `verification-demo/`
- `docs/全项目总控/DIGITAL_LIFE_AGENT_MANIFESTO.md`
- `docs/全项目总控/DIGITAL_LIFE_AGENT_DEVELOPMENT_PLAN.md`
- `docs/全项目总控/RUNTIME_ALIGNMENT.md`
- `docs/全项目总控/SELF_BOOTSTRAP.md`
- `docs/全项目总控/schemas/digital-life/`
- `scripts/py/generate_promo_articles.py`
- `.agents/`
- `.claude/`
- `.codebuddy/`
- `.qoder/`
- `.trae/`
- `tools/tool-registry.json`
- `temp/`, `tmp/`, `logs/`
- 任何私有策略、真实案例、真实部署、联系方式、未脱敏证据或过程记录

## 3. 保持私有的真实交付资产

以下内容继续保持私有，即使它们能帮助解释方法论：

- 客户、租户、账号、联系方式和部署信息；
- ERP 或其他真实项目源代码、数据库、迁移历史和生产配置；
- 未脱敏业务流程、真实单据、报表、日志、截图和测试证据；
- 商业策略、报价、客户名单、销售过程和内部优先级；
- 未经泛化的项目专属实现细节；
- 本机工具状态、密钥、缓存和本地路径。

## 4. 公开前检查

发布前必须运行：

```powershell
py scripts/py/audit_methodology.py --project-root .
git status --short
git check-ignore -v docs/内部商业化 docs/商业化 reference 备用 verification-demo tools/tool-registry.json
```

如果 `git status --short` 出现内部目录、原始素材目录或本机配置文件，停止发布。

## 5. 推荐仓库策略

仓库可以作为公开的 Open-Core Methodology 项目运行。公开前仍需完成一次 GitHub UI 历史和当前分支复核；该复核针对敏感资料，不再要求把方法论内核压缩成简化版。

公开仓库名称建议：

- `enterprise-ai-dev-os`
- `dream-enterprise-ai-os`
- `ai-development-determinism-os`

公开定位建议：

> 企业级 AI 开发操作系统（Enterprise AI Development OS）：一套面向 AI 辅助交付的可移植方法论与治理工具包，包含规则、Skill、模板、治理 Schema、审计、适配器与进化闭环。它不包含通用 AI 运行时或调度器。

---

## 译注 | Translation Notes

### 1. 本次翻译的范围

- **原为英文、本次翻译（共 1 处）**：第 5 节「公开定位建议」引用块，原文为 2 句英文（`Enterprise AI Development OS: ...` 与 `It does not include a universal AI runtime or scheduler.`），已全句译出，否定句「它不包含通用 AI 运行时或调度器」保持否定，未弱化。
- **原本已是中文、原样保留**：其余全部内容——5 个章节标题、第 1 节「完整开源方法论内核」的说明句与 41 条路径清单、第 2 节「不进入公开仓库」的说明句与清单、第 3 节「保持私有的真实交付资产」的说明句与清单、第 4 节「公开前检查」的说明句与 `powershell` 代码块、第 5 节正文与公开仓库名称建议清单。上述中文段落一字未改，未重译。
- **保留英文的术语**：`Open-Core Methodology` 属公开定位专名，按术语表禁译口径与同批译文（`ROADMAP_中文版.md`、`OPEN_SOURCE_READINESS_中文版.md`）的既有处理保留英文原样；该句其余中文部分未改写。

### 2. 公开 / 不公开边界表述核对（逐条，不得弱化）

| # | 源文件表述 | 译文表述 | 是否弱化 |
|---|---|---|---|
| 1 | 以下目录和文件默认不公开 | 以下目录和文件默认不公开 | 否，照译 |
| 2 | 以下内容继续保持私有 | 以下内容继续保持私有 | 否，照译 |
| 3 | 任何私有策略、真实案例、真实部署、联系方式、未脱敏证据或过程记录 | 同左，逐字照译 | 否，照译 |
| 4 | 方法论的完整性不意味着公开任何真实项目的生产资料 | 同左，逐字照译 | 否，照译 |
| 5 | 如果 `git status --short` 出现内部目录、原始素材目录或本机配置文件，停止发布 | 同左，逐字照译 | 否，照译 |
| 6 | 该复核针对敏感资料，不再要求把方法论内核压缩成简化版 | 同左，逐字照译 | 否，照译 |

> 说明：全文未出现「暂不公开」「暂不发布」「后续考虑开放」等弱化表述；不公开项一律译为确定性的「不公开 / 不进入公开仓库 / 继续保持私有」。

### 3. 路径核对与源文件问题（本译文不改动源文件）

- **公开清单路径核对**：第 1 节 41 条路径（含目录）已在仓库中逐条验证，全部存在；第 2 节私有清单路径亦均为仓库中的真实对象，唯一例外是 `logs/`（当前仓库中不存在该目录，该行是排除模式而非索引项，不影响边界表述）。
- **源文件重复条目（译文按源逐条保留，未去重、未删行）**：
  - `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md` 在第 1 节出现 2 次（源文件第 14 行与第 29 行）。
  - `docs/全项目总控/DISCLOSURE_BOUNDARY.md` 在第 1 节出现 2 次（源文件第 16 行与第 30 行）。
- **源文件待补登记项（覆盖缺口）**：
  1. 第 1 节未登记本文件自身 `docs/公开材料/OPEN_SOURCE_PACKAGE.md`。
  2. 第 1 节公开清单未登记 `scripts/py/validate_delivery_contract.py` 与 `scripts/py/audit_ai_native_governance.py`，但 `docs/全项目总控/MASTER_INDEX.md` 第 6 节将二者列为验证与门禁工具，且同属公开范围的 `docs/全项目总控/schemas/governance/` 内已含 `delivery-contract.schema.json`、`candidate-capability-evaluation.schema.json`、`delegation-grant.schema.json`、`execution-attestation.schema.json`：公开的治理契约 Schema 缺少对应公开校验脚本的登记。
  3. `docs/公开材料/` 下的 `FULL_AI_NATIVE_DEVELOPMENT_STANDARD_CN.md`、`FULL_AI_NATIVE_DEVELOPMENT_STANDARD_EN.md`、`FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_CN.md`、`FULL_AI_NATIVE_DEVELOPMENT_WHITEPAPER_EN.md` 既未列入第 1 节公开清单，也未列入第 2 节私有清单，边界归属未表态。
- **源文件过时信息**：第 4 节的三条公开前检查命令仍然有效（脚本与检查对象均存在）；源文件通篇未标注版本或日期（故头部「源版本」记为「未标注」），无法据此判断第 5 节「GitHub UI 历史复核」是否已完成。

### 4. 保留英文的项

- 第 1 节与第 2 节、第 3 节清单中的全部路径、目录名与文件名原样保留。
- 第 4 节 `powershell` 代码块原样复制，命令、参数、中文目录名均未译、未改。
- 第 5 节 3 个建议仓库名（`enterprise-ai-dev-os`、`dream-enterprise-ai-os`、`ai-development-determinism-os`）与 `GitHub UI`、`ERP` 等标识符原样保留。
