# AI-OS 数字生命核心协议 Schema

本目录存放数字生命智能体 P0/P1 阶段的机器可读协议。它们不是运行时代码，也不是页面说明，而是 AI-OS runtime 后续实现原子服务、原子编排和聚合接口时必须遵守的契约。

## 边界

- 理论母体：本目录定义协议和约束。
- AI-OS runtime：读取或生成等价 Schema，落地后端原子服务、编排和接口。
- GERP：作为真实业务场景验证这些协议是否可用。

## Schema 清单

| 文件 | 对象 | 用途 |
|---|---|---|
| `authority-profile.schema.json` | `AuthorityProfile` | 公有云、私有云、完全离线身份权威 |
| `life-identity.schema.json` | `LifeIdentity` | 数字生命全局身份、公钥、证书、登记状态 |
| `life-profile.schema.json` | `LifeProfile` | 数字生命静态画像、治理配置和运行时关联 |
| `life-instance.schema.json` | `LifeInstance` | 数字生命在节点上的运行实例与宿主绑定 |
| `life-runtime.schema.json` | `LifeRuntime` | 当前任务、状态机、队列深度和证据引用 |
| `genome-manifest.schema.json` | `GenomeManifest` | 数字生命引用的基因原子清单 |
| `installed-atom-set.schema.json` | `InstalledAtomSet` | 某个运行节点已安装且可调用的原子集合 |
| `birth-certificate.schema.json` | `BirthCertificate` | 出生证书，绑定身份、权威、初始基因清单 |
| `lifecycle-event.schema.json` | `LifecycleEvent` | 生命周期事件、状态迁移、证据引用 |
| `candidate-capability-evaluation.schema.json` | `CandidateCapabilityEvaluation` | 外部或内部候选能力的项目适配评估、验证计划和晋升决策 |
| `delegation-grant.schema.json` | `DelegationGrant` | 人或 runtime 向 Agent/执行器授予的范围化、限时授权 |
| `execution-attestation.schema.json` | `ExecutionAttestation` | 评估、沙箱或命令执行的可复现证据记录 |
| `delivery-contract.schema.json` | `DeliveryContract` | 任务写入范围、阶段准入、测试缝隙、新鲜证据与独立双轴复核契约 |

## 强制原则

1. 基因库不属于单个数字生命内部硬逻辑。
2. 数字生命只保存基因引用、安装集合、运行状态和成长档案。
3. 公有云权威必须可被企业私有权威或完全离线权威替代。
4. 每个状态变化、身份变化、基因安装和外部动作都必须能写入证据。
5. 后续实现必须保持原子服务 + 原子编排 + 聚合接口。
6. 候选能力不按来源标签直接采用；必须先完成项目适配评估和受控验证。
7. Agent 执行必须具有可追溯授权委托；关键执行必须记录可复现证据。
8. L2/L3、并行或高风险任务必须在写入前形成 `DeliveryContract`；越界写入、陈旧最终证据或未独立复核不得进入完成状态。
