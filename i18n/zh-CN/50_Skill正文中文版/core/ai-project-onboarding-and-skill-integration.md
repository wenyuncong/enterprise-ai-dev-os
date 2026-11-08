# `ai-project-onboarding-and-skill-integration` — 受控方法论接入

> **源文件**：skills/core/ai-project-onboarding-and-skill-integration/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-11-08
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-project-onboarding-and-skill-integration
description: "Safely onboard the methodology into a new or existing project by detecting its technology profile, preserving project-owned assets, staging external skills in quarantine, governing candidate compatibility, and generating an incremental knowledge index. Use before copying methodology assets, importing skills, or establishing a project knowledge base."
```

**中文描述**：通过探测技术画像、保留项目自有资产、在隔离区暂存外部技能、治理候选兼容性并生成增量知识索引，把方法论安全接入新项目或存量项目。在拷贝方法论资产、导入技能或建立项目知识库之前使用。

---

## Rule | 规则

外部技能、脚本与参考材料在其来源、许可证、版本、兼容性与结构被记录并评审之前，一律视为不可信。默认禁止覆盖任何既有项目资产，禁止直接激活来自代码托管平台的候选，禁止把知识索引当作运行时业务真相。

## Purpose | 目的

为接收本方法论的项目补齐缺失的接入链路：

```text
Detect -> Discover -> Evaluate -> Plan -> Stage -> Merge -> Govern -> Index -> Verify
探测 -> 发现 -> 评估 -> 计划 -> 暂存 -> 合并 -> 治理 -> 索引 -> 验证
```

本技能把方法论资产与项目自有源码分离，把导入候选与在用技能分离，把发现性知识与项目的运行时/数据真相分离。

## When to Use | 何时使用

- 在把方法论、规则、技能、脚本或模板拷贝进存量项目之前。
- 在为已探测到的语言、框架、数据库或部署目标选择技术栈技能时。
- 在考虑托管于代码平台的技能、脚本或参考实现时。
- 当项目需要可检索的技术知识索引时。
- 在方法论导入、升级或候选技能评审之后。

## Ownership and Locations | 归属与位置

| 位置 | 用途 | 可调用 |
| --- | --- | --- |
| `skills/core/`、`skills/governance/`、`skills/tech/` | 已在清单登记、经过验证的方法论技能 | 是 |
| `skills/project/` | 有明确项目所有者的项目私有模式 | 仅当项目路由到它们时 |
| `skills/candidates/` | 评估中的外部导入材料 | 否 |
| `skills/quarantine/` | 被拒绝、不完整、不兼容或不安全的材料 | 否 |
| `knowledge/` | 生成的技术发现索引与治理报告 | 否 |

禁止把未经评审的代码平台克隆放到活跃技能根下。禁止在缺乏跨项目反复证据的情况下，把项目私有规则并入可移植的核心技能。

## Workflow | 工作流

### 1. 探测与发现

先运行既有的项目工具发现，再生成技术画像与索引：

```text
py scripts/py/discover_tools.py <project-root> --by-purpose
py scripts/py/project_onboarding.py inspect --project-root <project-root>
```

画像记录探测到的语言、框架、包管理器、数据库、工具清单与既有技能状态。它只选择相关的 `skills/tech/` 候选；不仅凭文件名臆造技术栈。

### 2. 评估外部来源

优先使用官方厂商文档与官方上游仓库。一个代码平台候选必须具备：

1. 显式的 `github.com/owner/repository` 来源；
2. 锁定的 ref 与已解析的提交；
3. 可找到的许可证文件与兼容的许可证决策；
4. 维护/版本兼容性评估；
5. 无密钥、二进制、安装钩子或可执行代码在未经单独评审的情况下被接受；
6. 一份说明复用、扩展或拒绝的集成决策。

学习代码与模式；不要把不兼容的实现抄进项目。

### 3. 拷贝前先计划

生成一份非变更性的安装计划：

```text
py scripts/py/project_onboarding.py preflight --source-root <methodology-root> --project-root <target-root> --mode lite
```

计划把每项资产标注为 `add`、`same` 或 `conflict`。默认策略是只增不改。冲突项需要显式的合并/覆盖决策、文件级回滚路径，并保留目标既有资产。

拷贝选择按比例进行：

| 目标类型 | 拷贝内容 |
| --- | --- |
| 轻量接入 | 入口规则、模板、待办骨架 |
| 完整接入 | 核心/治理技能、选定的技术技能、审计脚本、适配器 |
| 成熟存量项目 | 仅 preflight 批准的缺口；先复用既有脚本再考虑新增 |

### 4. 暂存，而非激活

仅在带显式版本的情况下暂存代码平台候选：

```text
py scripts/py/project_onboarding.py stage-github --project-root <target-root> --name <candidate-name> --repository https://github.com/<owner>/<repository> --ref <tag-or-branch>
```

该命令写入 `skills/candidates/<candidate-name>/` 并记录 `skill-source-lock.json`。暂存不等于激活。

### 5. 治理与集成

运行候选治理与既有方法论审计：

```text
py scripts/py/project_onboarding.py govern-candidates --project-root <target-root>
py scripts/py/audit_methodology.py --project-root <target-root>
py scripts/py/audit_skill_health.py --project-root <target-root>
```

来源缺失、frontmatter 无效、技能入口缺失、许可证不兼容或可执行内容未经评审的候选，继续留在隔离区。只有在项目所有者记录决策之后，经过评审的技能才可移入目标根并在 `skills/SKILL_MANIFEST.json` 登记。

### 6. 维护知识索引

在接入期间运行一次有界扫描。在有实质的源码、依赖、架构、技能或脚本变更后增量刷新。不要在每次会话都强制全量扫描。

索引只支持发现：它不是授权、数据库回读、命令提供者或运行时证据。

## Verification | 验证

在宣称接入就绪之前：

- [ ] 已生成项目技术画像与既有工具目录。
- [ ] 拷贝计划中无未经评审的覆盖。
- [ ] 外部候选具备来源锁、提交、许可证决策与评审状态。
- [ ] 候选治理无激活阻断项。
- [ ] 对已激活资产，`audit_methodology.py` 与 `audit_skill_health.py` 通过。
- [ ] 知识索引存在，并标明其有界/增量扫描状态。
- [ ] 产品/项目所有者接受所声明的范围与非目标。

## Guardrails | 防护规则

- 禁止用 `-Force` 或递归删除解决 preflight 冲突。
- 禁止仅因探测到某种语言就导入该平台的全部技能。
- 禁止在来源与治理通过前让候选内容可被调用。
- 禁止仅为让方法论安装看起来完整，就覆盖项目自有的规则、脚本或技能。
- 禁止自动删除过时候选；应隔离并记录决策。
- 禁止把知识索引当作真实运行时、授权、API、数据库或业务流程证据的替代。

## Integration | 集成

| 需求 | 主要技能 |
| --- | --- |
| 项目技术栈与来源 | `ai-project-classifier` |
| 存量项目模式与工具 | `ai-brownfield-analyzer` |
| 外部参考研究 | `ai-reference-researcher` |
| 既有库选择 | `ai-library-first` |
| 技能重叠与健康 | `ai-skill-governor` |
| 有证据支撑的进化 | `ai-skill-evolver` |

## Evolution History | 进化记录

- v1.0.0：新增受控方法论接入、外部候选隔离、安全拷贝 preflight、拷贝后治理与有界知识索引。
