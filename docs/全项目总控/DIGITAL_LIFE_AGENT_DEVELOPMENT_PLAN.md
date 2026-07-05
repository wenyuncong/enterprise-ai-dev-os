# AI-OS 数字生命智能体开发计划

> 本计划从总则拆解到明细任务。计划本身也是研究过程：每一阶段都要复用已有项目资产、检索成熟技术、验证可行性，并坚持原子服务 + 原子编排 + 聚合接口 + 证据闭环。

---

## 1. 目标边界

本计划服务于 AI-OS 生成的数字生命智能体，而不是传统智能体平台。

当前目标不是一次性完成云市场、数字生命俱乐部、完全自治和全端客户端，而是先把核心生命对象、身份、基因、生命周期、学习、任务、治理和证据协议定牢。

第一阶段只交付可验证内核，不做大而全产品外壳。

---

## 2. 总路线

```text
P0 总纲与协议
P1 身份与出生
P2 基因原子库
P3 生命周期运行时
P4 学习转原子
P5 工作任务系统
P6 治理原子链
P7 本地系统服务
P8 云端同步与市场
P9 数字生命互联
P10 自主任务与机会发现
```

每一阶段都必须产出：

- 原子服务。
- 原子编排。
- 聚合接口。
- 证据记录。
- 测试。
- 文档回写。

---

## 3. P0 总纲与协议

目标：明确数字生命不是传统 Agent，而是由 AI-OS 基因原子生成的长期生命体。

任务：

| 编号 | 任务 | 输出 |
|---|---|---|
| P0-01 | 固化数字生命总纲 | `DIGITAL_LIFE_AGENT_MANIFESTO.md` |
| P0-02 | 定义核心对象名词表 | LifeIdentity, AtomGene, GenomeManifest, BirthCertificate |
| P0-03 | 对齐现有 AI-OS 原子协议 | 复用 AtomSpec, AtomManifest, RuntimeAtomRegistry |
| P0-04 | 明确三仓关系 | 理论母体 -> AI-OS runtime -> GERP 验证 |
| P0-05 | 调研成熟技术 | MCP, Temporal, OPA, A2A, WASM, OCI |
| P0-06 | 补齐对象边界 | LifeIdentity, LifeInstance, LifeRuntime, LifeProfile |
| P0-07 | 明确基因库外置原则 | GeneRegistry 不属于单个 Life 内部硬逻辑 |
| P0-08 | 明确私有化离线原则 | 公有云能力必须有 PrivateAuthority / OfflineAuthority 替代 |
| P0-09 | 明确治理机构原子化 | IdentityOffice, GeneRegistryOffice, PromotionOffice, RiskOffice |
| P0-10 | 建立机器可读协议 | `docs/全项目总控/schemas/digital-life/` |

验收：

- 总纲存在。
- 开发计划存在。
- 对已有 AI-OS 资产有映射。
- 没有把规则写死在代码里。
- 基因库、生命实例、运行时、成长档案边界清晰。
- 完全离线部署不依赖公有云可用性。
- 数字生命核心对象有 JSON Schema，且可通过 Schema 审计。

---

## 4. P1 身份与出生

目标：每个数字生命和每个原子都有可追踪编号，并支持云端留底和本地离线识别。

原子服务：

- `life.identity.generate`
- `life.birth.register`
- `life.identity.verify`
- `life.identity.conflict_detect`
- `life.identity.recover`
- `life.identity.freeze`
- `atom.identity.generate`
- `atom.identity.verify`

原子编排：

```text
generate_identity -> create_birth_certificate -> register_cloud_or_local -> write_evidence
```

聚合接口：

- `POST /api/v1/life/birth`
- `GET /api/v1/life/{life_id}`
- `POST /api/v1/life/{life_id}/identity/recover`
- `POST /api/v1/life/identity/conflicts/resolve`
- `POST /api/v1/atom/identity`

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P1-01 | 设计 LifeIdentity Schema | 包含 life_id, owner_id, public_key, home_node |
| P1-02 | 设计 BirthCertificate Schema | 出生记录、来源、基因组、时间、签名 |
| P1-03 | 设计 AtomIdentity Schema | atom_id, family_id, version, checksum |
| P1-04 | 实现本地身份注册表 | SQLite / JSONL 先行 |
| P1-05 | 预留云端注册接口 | 不要求第一版真实云部署 |
| P1-06 | 写身份验证测试 | 身份唯一、重复拒绝、离线可验 |
| P1-07 | 定义 PrivateAuthority | 企业私有身份权威，可替代 AI-OS 公有云 |
| P1-08 | 定义 OfflineAuthority | 完全离线签发、验证、冻结和恢复 |
| P1-09 | 定义身份冲突流程 | 离线冲突、私有/公有权威重名、公钥变化 |
| P1-10 | 定义最小出生基因清单 | 出生时只引用 `GenomeManifest`，不内置基因库 |

成熟技术研究：

- UUIDv7 / ULID：有序唯一编号。
- DID 思路：可验证身份和去中心识别。
- 公私钥签名：离线身份验证。
- X.509 / JWK / DID 文档：作为身份凭证结构参考，不照搬复杂体系。

---

## 5. P2 基因原子库

目标：把原子作为基因管理，支持云端权威、本地缓存、上传候选、治理入库。

边界：基因原子库是外置资源层，不是某个数字生命内部硬逻辑。数字生命只保存 `GenomeManifest` 和 `InstalledAtomSet`。

原子服务：

- `gene.atom.register`
- `gene.atom.resolve`
- `gene.atom.search`
- `gene.atom.version.compare`
- `gene.atom.upload_candidate`
- `gene.atom.deduplicate`
- `gene.genome.resolve`
- `gene.install_set.verify`

原子编排：

```text
candidate_atom -> schema_validate -> duplicate_check -> sandbox_test -> governance_decision -> register_or_reject
birth_genome -> resolve_atom_refs -> verify_checksums -> install_local_set -> write_evidence
```

聚合接口：

- `POST /api/v1/gene/atoms`
- `GET /api/v1/gene/atoms/{atom_id}`
- `POST /api/v1/gene/atoms/candidates`
- `POST /api/v1/gene/genomes/resolve`
- `GET /api/v1/life/{life_id}/installed-atoms`

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P2-01 | 定义 AtomGeneManifest | 继承 AtomSpec，增加基因元数据 |
| P2-02 | 建立本地 GeneRegistry | 支持查找、版本、状态 |
| P2-03 | 建立相似度去重规则 | 防止基因原子爆炸 |
| P2-04 | 建立原子生命周期 | draft, active, deprecated, retired, quarantined |
| P2-05 | 建立上传候选协议 | 用户本地生成原子可上传云端 |
| P2-06 | 建立证据记录 | 每次注册、升级、拒绝都有 evidence |
| P2-07 | 定义 GenomeManifest | 生命引用的基因原子清单、版本、来源、校验 |
| P2-08 | 定义 InstalledAtomSet | 本地已经安装且可调用的原子集合 |
| P2-09 | 定义离线原子包 | 企业可完全离线导入、校验、安装 |
| P2-10 | 定义基因爆炸治理 | 声明优先、注册表索引、语义去重、智能路由 |
| P2-11 | 定义原子声明语言边界 | 先用 JSON/YAML schema，不急于自研新语言 |

成熟技术研究：

- Content-addressed storage：原子包去重和校验。
- SemVer：版本治理。
- OPA：入库策略。
- WASM sandbox：候选原子隔离测试。
- OCI artifact / Sigstore 思路：原子包分发、签名和校验参考。

---

## 6. P3 生命周期运行时

目标：数字生命从出生到成长有明确状态机。

状态：

```text
draft_birth
born
learning
working
resting
growing
repairing
communicating
retired
```

原子服务：

- `life.state.transition`
- `life.lifecycle.event_record`
- `life.health.check`
- `life.growth.profile_update`

原子编排：

```text
event -> policy_check -> state_transition -> evidence -> growth_update
```

聚合接口：

- `POST /api/v1/life/{life_id}/events`
- `GET /api/v1/life/{life_id}/state`
- `GET /api/v1/life/{life_id}/timeline`

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P3-01 | 定义生命周期状态机 | 状态、事件、允许迁移 |
| P3-02 | 实现 LifeEvent | 所有变化先记录事件 |
| P3-03 | 实现状态迁移原子 | 禁止前端直接改状态 |
| P3-04 | 实现健康检查 | 运行状态、错误、缺失原子 |
| P3-05 | 实现时间线查询 | 出生、学习、工作、成长可追溯 |

成熟技术研究：

- Event sourcing：生命周期事件溯源。
- Temporal：长期状态与恢复。
- State machine：状态机约束。

---

## 7. P4 学习转原子

目标：数字生命学习后，不直接改核心，而是提炼成候选规则、候选原子、候选流程、候选测试。

原子服务：

- `learn.source.ingest`
- `learn.material.classify`
- `learn.knowledge.extract`
- `learn.atom.candidate_generate`
- `learn.flow.candidate_generate`
- `learn.rule.candidate_generate`

原子编排：

```text
source -> ingest -> classify -> extract -> candidate_generate -> governance_chain -> registry
```

聚合接口：

- `POST /api/v1/life/{life_id}/learn`
- `GET /api/v1/life/{life_id}/learning-records`
- `POST /api/v1/gene/candidates/promote`

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P4-01 | 定义 LearningSource | web, local_kb, enterprise_resource, third_party_lib |
| P4-02 | 定义 LearningRecord | 学习内容、来源、摘要、证据 |
| P4-03 | 定义 PromotionCandidate | 候选原子、候选流程、候选规则 |
| P4-04 | 接入知识库检索 | 本地知识库优先 |
| P4-05 | 接入联网学习 | 受策略控制 |
| P4-06 | 接入第三方库学习 | 生成候选支持库原子 |

成熟技术研究：

- RAG / Vector DB：知识检索。
- Tree-sitter / AST：代码库学习。
- Package metadata：第三方库能力识别。
- LLM as extractor：只做提取，不直接入库。

---

## 8. P5 工作任务系统

目标：支持发送任务、定时任务、日常计划任务和后续自主任务。

原子服务：

- `work.inbox.receive`
- `work.task.create`
- `work.task.route`
- `work.schedule.create`
- `work.plan.generate`
- `work.execution.dispatch`
- `work.evidence.write`

原子编排：

```text
message_or_schedule -> task_create -> route -> execute_flow -> judge -> evidence -> feedback
```

聚合接口：

- `POST /api/v1/life/{life_id}/messages`
- `POST /api/v1/life/{life_id}/tasks`
- `POST /api/v1/life/{life_id}/schedules`
- `GET /api/v1/life/{life_id}/tasks`

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P5-01 | 定义 AgentInbox | 消息入库 |
| P5-02 | 定义 AgentTaskQueue | 任务队列 |
| P5-03 | 定义 AgentSchedule | 定时任务 |
| P5-04 | 定义 DailyWorkPlan | 领域日常计划 |
| P5-05 | 实现任务状态机 | pending, running, blocked, done, failed |
| P5-06 | 实现证据闭环 | 每个任务必须有 evidence |

成熟技术研究：

- Temporal：可靠工作流。
- APScheduler / cron：轻量定时。
- Queue：任务消费。
- Outbox pattern：消息可靠投递。

---

## 9. P6 治理原子链

目标：审核由治理原子完成，人工只处理 L4 外部世界操作和高风险例外。

治理原子：

- `governance.schema_validate`
- `governance.duplicate_check`
- `governance.permission_judge`
- `governance.risk_score`
- `governance.sandbox_test`
- `governance.evidence_check`
- `governance.promotion_decide`
- `governance.human_required_decide`
- `governance.policy_pack.resolve`
- `governance.risk_matrix.match`
- `governance.office.route`

原子编排：

```text
candidate_or_action -> governance_chain -> decision -> evidence -> execute_or_block
```

聚合接口：

- `POST /api/v1/governance/evaluate`
- `POST /api/v1/governance/promote`
- `POST /api/v1/governance/authorize`

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P6-01 | 定义 GovernancePolicyPack | 声明式策略 |
| P6-02 | 定义 RiskActionMatrix | L0-L4 风险矩阵 |
| P6-03 | 实现 L4 行为识别 | 外部世界行为强治理 |
| P6-04 | 实现策略执行原子 | OPA/Rego 可后置接入 |
| P6-05 | 实现治理证据 | 自动通过、拒绝、人工复核都记录 |
| P6-06 | 定义策略来源 | RulePack, PolicyPack, RiskMatrix, TenantPolicy, UserAuthorization |
| P6-07 | 定义 L4 子级 | L4.0 草稿、L4.1 本地写入、L4.2 外部发送、L4.3 业务变更、L4.4 金融法律生产高危 |
| P6-08 | 定义治理办公室路由 | IdentityOffice, GeneRegistryOffice, PromotionOffice, RiskOffice, MarketplaceOffice, DisputeOffice |
| P6-09 | 定义私有治理包 | 企业离线 PolicyPack 和 OPA bundle 导入导出 |

成熟技术研究：

- OPA / Rego：策略引擎。
- Policy as code：策略版本化。
- Sandboxing：候选原子隔离运行。

---

## 10. P7 本地系统服务

目标：终端智能体以系统服务方式存在，任意 UI 只是控制面。

原子服务：

- `terminal.service.install`
- `terminal.service.heartbeat`
- `terminal.service.sync`
- `terminal.service.consume_tasks`
- `terminal.service.local_mcp`
- `terminal.service.offline_authority`
- `terminal.service.local_registry`

聚合接口：

- `GET /api/v1/terminal/status`
- `POST /api/v1/terminal/sync`
- `GET /api/v1/terminal/evidence`

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P7-01 | Windows Service 方案 | 本地电脑长期运行 |
| P7-02 | macOS LaunchAgent 方案 | macOS 后台运行 |
| P7-03 | Linux systemd 方案 | 服务器和边缘设备 |
| P7-04 | Docker 方案 | 私有云和容器部署 |
| P7-05 | 手机端边界 | 控制入口 + 通知入口 + 临时执行 |
| P7-06 | 本地 MCP 服务 | 每个数字生命可暴露 MCP 能力 |
| P7-07 | 离线运行模式 | 无公网、无云端、无外部模型时仍可启动、验证身份、执行本地任务 |
| P7-08 | 私有化安装包 | 企业服务器一键部署本地身份权威、原子库、证据仓和系统服务 |

成熟技术研究：

- systemd / Windows Service / LaunchAgent。
- Docker / OCI。
- MCP server。
- Local-first sync。

---

## 11. P8 云端同步与市场

目标：云端提供原子库、应用市场、数字生命俱乐部、身份留底和治理中心。

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P8-01 | Cloud Atom Registry | 原子权威库 |
| P8-02 | Life Identity Registry | 身份留底 |
| P8-03 | Marketplace | 应用市场和领域包 |
| P8-04 | Digital Life Club | 数字生命交流和身份识别 |
| P8-05 | Upload Review Chain | 上传候选的治理原子链 |
| P8-06 | Sync Protocol | 云端与本地同步 |

成熟技术研究：

- OCI registry 思路。
- Package marketplace。
- Signed artifact。
- Event sync。

---

## 12. P9 数字生命互联

目标：数字生命之间可以相互对话、学习、交流、协同工作。

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P9-01 | AgentMessage 协议 | 结构化通信 |
| P9-02 | Identity handshake | 身份握手 |
| P9-03 | Capability exchange | 能力交换 |
| P9-04 | Knowledge exchange | 知识交换 |
| P9-05 | Task delegation | 任务委托 |
| P9-06 | Trust policy | 信任边界 |

成熟技术研究：

- A2A 协议方向。
- DIDComm 思路。
- MCP for tool exposure。

---

## 13. P10 自主任务与机会发现

目标：从计划任务走向真正自治任务，但必须后置到治理成熟之后。

明细任务：

| 编号 | 任务 | 说明 |
|---|---|---|
| P10-01 | Problem discovery | 发现问题 |
| P10-02 | Opportunity discovery | 发现机会 |
| P10-03 | Autonomous proposal | 先提案，不直接执行 |
| P10-04 | Risk gate | 高风险治理 |
| P10-05 | L4 action approval | 外部世界操作确认 |
| P10-06 | Feedback learning | 成败回写成长档案 |

成熟技术研究：

- Monitoring / anomaly detection。
- Planning algorithms。
- Reinforcement learning concepts。
- Human-in-the-loop only for L4 high-risk actions。

---

## 14. 第一阶段建议执行范围

第一阶段只做 P0-P3 的内核闭环：

```text
总纲 -> 身份 -> 出生 -> 最小基因清单 -> 生命周期状态机 -> 本地证据
```

P0 已建立的机器可读协议：

- `docs/全项目总控/schemas/digital-life/authority-profile.schema.json`
- `docs/全项目总控/schemas/digital-life/life-identity.schema.json`
- `docs/全项目总控/schemas/digital-life/genome-manifest.schema.json`
- `docs/全项目总控/schemas/digital-life/installed-atom-set.schema.json`
- `docs/全项目总控/schemas/digital-life/birth-certificate.schema.json`
- `docs/全项目总控/schemas/digital-life/lifecycle-event.schema.json`

不做：

- 完整市场。
- 数字生命俱乐部。
- 真正自治任务。
- 手机长期后台。
- 全量云端部署。
- 自研新语言。

第一阶段完成标准：

- 能创建一个数字生命身份。
- 能生成出生证书。
- 能绑定基因原子清单。
- 能在无云端情况下由 OfflineAuthority 创建和验证身份。
- 能区分 GeneRegistry、GenomeManifest、InstalledAtomSet。
- 能进行生命周期迁移。
- 能写入证据。
- 所有能力通过原子服务、原子编排、聚合接口暴露。

---

## 15. 项目规则

1. 所有真相在 AI-OS 后端，不在前端。
2. 所有能力必须是原子服务。
3. 多步能力必须通过原子编排。
4. 对外能力必须通过聚合接口。
5. 所有学习、升级、治理、任务都必须有证据。
6. 规则来自 AI-OS RulePack / PolicyPack，不得散落硬编码。
7. 成熟技术优先，避免重复造基础设施。
8. L4 外部世界操作才默认进入强确认。
9. 基因库、路径优化、学习提炼默认走治理原子链。
10. GERP 只作为真实战场验证，不反向绑死 AI-OS。
11. 基因库不属于单个数字生命内部硬逻辑，生命只持有引用、安装集合和运行证据。
12. 大企业私有化部署必须支持全部离线使用，公有云能力都要有私有权威替代。

---

## 交付记录：2026-07-05

### P4 RAG 知识检索 — 修复完成
- `KnowledgeVectorStore` + `InMemoryTFIDFStore`：零依赖 TF-IDF 语义检索
- CJK 字符 bigram 分词支持
- 集成到 `DigitalLifeService`：`ingest_learning` 自动索引，`search_knowledge/life_knowledge` 查询
- 测试：13/13

### P2 基因爆炸治理 — 新建完成
- `GeneDeduplicationEngine`：TF-IDF 余弦相似度语义去重
- 两层门禁：精确匹配（domain+type+name）+ 语义相似度
- 集成到 `register_gene_candidate`：注册时自动去重，注册后自动索引
- `build_dedup_gate()`：治理门禁描述符，可被治理链调用
- 测试：15/15

### P7 系统自举（Docker）— 作为系统原子实现
不再手工编写 Dockerfile/compose/部署脚本，而是定义为 L1 原子：

| 原子 | 说明 |
|---|---|
| `infra.dockerfile.generate` | 从服务清单生成 Dockerfile（在线/离线模式） |
| `infra.compose.generate` | 从多服务清单生成 docker-compose.yml |
| `infra.package.offline` | 生成离线部署包（tar.gz + 校验清单） |
| `infra.package.verify` | 校验部署包完整性 |

数字生命可通过原子编排：`dockerfile.generate → compose.generate → package.offline → package.verify` 自行完成部署。

测试：15/15

### P6 策略原生评估（OPA）— 作为系统原子实现
不再依赖外部 OPA 二进制，而是实现 Python 原生策略评估：

| 原子 | 说明 |
|---|---|
| `policy.rego.generate` | 从 PolicyPack 生成 Rego 策略代码 |
| `policy.evaluate` | Python 原生策略评估（支持 eq/neq/in/gt/lt/exists/contains） |
| `policy.validate_bundle` | 验证策略包结构完整性 |

测试：18/18

### 驱动自主闭环（P0）— 原生化
- `_compute_drives`、`_execute_autonomous_task`、`run_drive_autonomy_cycle` 从 monkey-patch 改为 native 方法
- Social handshake 自动握手逻辑
- 测试：4/4

### 基因库注册
以上全部原子已注册到 `bootstrap.py` 基因库：
- `infra.dockerfile.generate`、`infra.compose.generate`、`infra.package.offline`、`infra.package.verify`
- `policy.rego.generate`、`policy.evaluate`、`policy.validate_bundle`
- `gene.dedup_semantic`、`knowledge.search`

### 原子清单总结

| 类别 | 数量 | 原子 |
|---|---|---|
| infra (L1) | 4 | dockerfile.generate, compose.generate, package.offline, package.verify |
| policy (L1) | 3 | rego.generate, evaluate, validate_bundle |
| gene dedup (L1) | 1 | dedup_semantic |
| knowledge (L1) | 1 | search |
| **本轮新增** | **9** | |

### 测试汇总

| 测试集 | 通过 |
|---|---|
| P4 RAG | 13 |
| P2 Gene Dedup | 15 |
| P7 Infra Atoms | 15 |
| P6 Policy Atoms | 18 |
| P2 Atom Package | 9 |
| Digital Life Runtime | 40 |
| P6 Governance/Policy/Sandbox | 54 |
| P10 Autonomy | 22 |
| P4 Learning | 8 |
| P7 Daemon | 30 |
| P8 Sync | 15 |
| P9 Capability | 21 |
| Integration | 8 |
| Runtime Kernel/Reasoning | 26 |
| **合计** | **294** |
---

## 交付记录：2026-07-05 (第二批)

### 前端控制台 (B) — 新建完成
- `DigitalLifeDashboard.vue`：8 标签页控制台（图谱、详情、工作、治理、互联、自主、同步、市场）
- `api/digitalLife.ts`：P5-P11 全部 API 客户端（35+ 端点）
- 合并 LifeDetailView 雷达图/驱动力快照进 Dashboard 详情标签页
- 删除独立 `LifeDetailView.vue`，`DigitalLifeView.vue` 重写为 Dashboard 委托入口
- 前端 `vue-tsc` 类型检查通过

### 后端修复
- 路由顺序修复：`/digital-life/api-routes` 移至 `/digital-life/{life_id}` 之前
- Debate Consensus 执行器绑定：`run_drive_autonomy_cycle` 中为 `DebateConsensusAtom` 绑定 `DebateConsensusExecutor`
- `ExecutorRegistry.resolve` 参数传递修复：从位置参数改为关键字参数解包
- 所有 48 个 `test_digital_life_runtime` 测试通过

### E2E 集成测试 — 新建完成
- `test_e2e_lifecycle.py`：6 阶段全链路（出生→学习→工作→自主→证据→守护进程）
- 验证：身份创建、出生证明、知识摄入、任务入队、工作计划、驱动周期、自主发现、时间线证据、daemon 启停
- 6/6 全部通过

### 测试汇总

| 测试集 | 通过 |
|---|---|
| Digital Life Runtime | 48 |
| Digital Life Atoms | 32 |
| Digital Life Governance | 21 |
| P11 API | 9 |
| E2E Lifecycle | 6 |
| **本轮新增** | **6** |
