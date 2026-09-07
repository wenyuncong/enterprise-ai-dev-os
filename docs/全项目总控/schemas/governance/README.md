# Governance Contract Schemas | 治理契约 Schema

本目录存放可迁移方法论的机器可读治理契约。它们不是运行时代码，也不代表本仓库已经提供通用 AI Runtime、调度器或命令执行沙箱。

项目可以在自己的 Runtime、CI 或交付系统中读取这些契约，并据此实现权限、范围、新鲜证据、授权和复核门禁。

## Schema 清单

| 文件 | 对象 | 用途 |
|---|---|---|
| `candidate-capability-evaluation.schema.json` | `CandidateCapabilityEvaluation` | 外部或内部候选能力的项目适配评估、验证计划和晋升决策 |
| `delegation-grant.schema.json` | `DelegationGrant` | 人或 runtime 向 Agent/执行器授予的范围化、限时授权 |
| `execution-attestation.schema.json` | `ExecutionAttestation` | 评估、沙箱或命令执行的可复现证据记录 |
| `delivery-contract.schema.json` | `DeliveryContract` | 任务写入范围、阶段准入、测试缝隙、新鲜证据与独立双轴复核契约 |

## 强制原则

1. 候选能力不按来源标签直接采用；必须先完成项目适配评估和受控验证。
2. Agent 执行必须具有可追溯授权委托；关键执行必须记录可复现证据。
3. L2/L3、并行或高风险任务必须在写入前形成 `DeliveryContract`；越界写入、陈旧最终证据或未独立复核不得进入完成状态。
4. 这些 Schema 是治理边界，不是业务系统或 Runtime 的实现证明。
