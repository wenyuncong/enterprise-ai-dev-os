# AI 产品交付任务包 | AI Product Delivery Task Pack

> **源文件**：docs/_templates/全项目总控/AI_PRODUCT_DELIVERY_TASK_TEMPLATE.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

> 产品负责人（product owner）只填第 1–2 节。AI 智能体依据已验证的项目证据完成第 3–9 节。
> 不得要求 product owner 去定位代码、选择框架，或描述内部实现。
>
> 对于 L2/L3、并行或高风险工作，依据 `task_contract.json` 另建一份配套的机器可读契约，
> 并用 `scripts/py/validate_delivery_contract.py` 校验。

## 1. 产品负责人输入 | Product Owner Input

| 项目 | 输入 |
| --- | --- |
| 业务结果（Business outcome） | |
| 主要用户与场景 | |
| 期望的可见结果 | |
| 可用性期望 | |
| 优先级（Priority） | P0 / P1 / P2 |
| 非目标（non_goals） | |
| 参考资料、示例、截图 | |
| 业务流程验收（business-flow acceptance）步骤 | |

## 2. 产品决策日志 | Product Decision Log

| 决策 | 已考虑的选项 | 负责人决定 | 日期 |
| --- | --- | --- | --- |
| 业务规则歧义（business ambiguity） | | | |
| 范围权衡（scope trade-off） | | | |
| 破坏性（destructive）操作 / 发布授权 | | | |

## 3. AI 发现与路由 | AI Discovery and Routing

| 项目 | 证据 |
| --- | --- |
| 项目分类（project classification） | |
| 选定的主责 Skill | |
| 支撑 Skill | |
| 已有模式 / 可复用候选 | |
| 已发现的脚本与工具 | |
| 工作区（working-tree）边界 | |
| 共享语言（shared language）/ ADR 上下文 | 无需要 / [路径与术语] |
| 交付契约（DeliveryContract） | 不需要 / [任务本地契约路径] |
| 交付资格（delivery qualification） | Q0 / Q1 / Q2 / Q3；证据，以及缺失的更高层级证明 |
| 能力成熟度（capability maturity） | registered / configured / authorized / provider-covered / runtime-executable / business-closed |

## 4. 代码定位与真相地图 | Code Location and Truth Map

```text
用户流程 / 路由（User flow / route）：
渲染后的 Host 与共享模板（Rendered Host and shared template）：
前端服务或客户端适配器（Frontend service or client adapter）：
Controller / 传输适配器（transport adapter）：
聚合接口（aggregate interface）与命令网关（command gateway）：
编排（orchestration）与原子服务（atomic service）：
领域真相 / 元数据 / 权限（Domain truth / metadata / permissions）：
持久化 / 迁移 / 外部副作用（Persistence / migration / external side effect）：
聚焦测试与发布门禁（Focused tests and release gates）：
```

## 5. 范围、安全与架构 | Scope, Safety, and Architecture

| 项目 | 决策 |
| --- | --- |
| 范围内（In scope） | |
| 范围外（Out of scope） | |
| 真相责任人（truth_owner） | |
| 受影响的客户端 | |
| 候选文件与理由 | |
| 删除 / 重命名 / 迁移分类 | 无 / A / B / C / D |
| 回滚路径 | |
| L0-L3 门禁（gate） | |
| 数据库迁移一致性门禁 | 不适用 / [迁移门禁记录] |
| 租户生命周期回归（regression） | 不适用 / [回归记录] |
| 写入白名单（write_allowlist）/ 禁止路径（forbidden_paths） | |
| 破坏性（destructive）分类 / 负责人确认 | |

## 6. 可执行批次 | Executable Batches

| ID | 依赖 | 写入边界 | 公共可测试边界（public_test_seam）/ 有理由的替代方案 | 结果 | 验收 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| B-01 | 无 | | | | | |
| B-02 | B-01 | | | | | |

## 7. 验证记录 | Verification Record

| 层次 | 检查 | 结果 | 证据路径 / 命令 |
| --- | --- | --- | --- |
| 静态（Static） | | | |
| 单元 / 契约（Unit / contract） | | | |
| API / 数据库（API / database） | | | |
| 浏览器 / 运行时（Browser / runtime） | | | |
| 业务流程闭环（Business-flow closure） | | | |
| 新鲜最终证据（fresh evidence） | 主张（Claim）： | | 在最终相关改动之后运行的命令 / 检查 |
| 发布 / 部署（Release / deployment） | | | |

## 8. 双轴审查 | Two-Axis Review

两轴即 two independent axes：（a）标准 / 真相 / 架构 / 质量门禁；（b）原始业务结果 / 验收流程 / 显式非目标。

| 轴（Axis） | 问题 | 结果 | 证据 / 阻塞项 |
| --- | --- | --- | --- |
| 标准 / 真相（Standards / truth） | 仓库标准、真相归属、架构、质量门禁 | | |
| 产品 / 规格（Product / spec） | 结果、业务流程验收（business-flow acceptance）、显式非目标 | | |

## 9. 产品验收 | Product Acceptance

| 验收流程 | 期望 | 实际 | 负责人决定 |
| --- | --- | --- | --- |
| | | | 接受（Accept）/ 修订（Revise）/ 拒绝（Reject） |

## 10. 交付收口 | Delivery Closure

```text
改动类型（Change type）：
目标版本 / 线（Target version / line）：
受影响流程（Affected flow）：
真相责任人（Truth owner）：
选定门禁（Selected gate）：
证据（Evidence）：
交付状态（Delivery state）：complete / paused / blocked
已知限制或后续事项（Known limits or follow-up）：
```

---

## 译注 | Translation Notes

- 相关 Skill（见 00_导读/02_术语对照表.md 第 12.2 节）：本任务包的主责 Skill 通常取 `ai-product-directed-delivery`；需要机器可读契约时用 `ai-delivery-contract-governor`；版本化交付与放行门禁走 `ai-5s-delivery-governor`（Scope → Specify → Ship → Safeguard → Sell）。该路由依据 `AGENTS.md` 第 0.5–0.10 节，不是源模板原文。
- 第 4 节与第 10 节的 ```text 块是**字段标签脚手架**，不是代码：为便于直接套用，标签文字已译出，`Host`、`aggregate interface`、`command gateway`、`atomic service`、`orchestration`、`complete / paused / blocked` 等标识符与状态代号保持英文原样。
- 第 6 节的 `public_test_seam` 是任务包口径的键名；对应机器可读契约中的键是 `test_strategy.public_seam`。两处写法不一致，套用时以 `task_contract.json` 的键名为准（见《task_contract 字段说明》）。
- 第 3 节的成熟度链 `registered → configured → authorized → provider-covered → runtime-executable → business-closed` 保持英文代号，不译。
