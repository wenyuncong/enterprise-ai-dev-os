# 价值证据 | Value Evidence

> **源文件**：docs/公开材料/VALUE_EVIDENCE.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

---

本文件定义如何证明 Enterprise AI Development OS 是否创造了真实价值。公开表述不得使用未经验证的市场百分比或私有项目细节。

## 证据原则 | Evidence Principles

- 对比方法论安装前后的情况。
- 统计返工与缺陷修复成本，而不只是首次生成成本。
- 区分简单任务、复杂任务与整项目效果。
- 记录证据路径，但不发布私有日志。
- 优先给出小型可复现的例子，而不是宽泛的结论。

## 指标 | Metrics

| 指标 | 含义 | 记录方式 |
|---|---|---|
| 首次通过完成 | AI 的首次实现是否通过评审或测试 | 通过/失败，加简短原因 |
| 返工次数 | 需要多少轮纠正 | 整数 |
| 缺陷逃逸 | 缺陷是否进入运行时/人工验证 | 是/否 |
| 验证覆盖 | 跑了哪些门禁 | audit、单元、API、浏览器、适配器 dry-run |
| token 走向 | 任务总 token 是上升还是下降 | 上升/下降/未知，附上下文 |
| 规则召回 | 必需规则是否被加载并遵循 | 通过/失败 |
| 工具一致性 | 不同工具是否产生兼容行为 | 通过/失败/未知 |

## 单任务模板 | Task-Level Template

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

## 汇总表 | Summary Table

| 场景 | 基线结果 | 使用 Enterprise AI Dev OS | 证据 | 状态 |
|---|---|---|---|---|
| 单文件简单编辑 | TBD | TBD | TBD | 未测量 |
| 跨文件前端改动 | TBD | TBD | TBD | 未测量 |
| 后端 API + 前端集成 | TBD | TBD | TBD | 未测量 |
| 老项目（brownfield）接入 | TBD | TBD | TBD | 未测量 |
| 多工具适配器交接 | TBD | TBD | TBD | 未测量 |

## 脱敏案例证据 | Sanitized Case Evidence

> 来源：一个多租户企业级 ERP（采购/销售/库存/财务/生产/CRM/WMS/TMS），约 3 个月的 AI 辅助开发。公司名、仓库路径与内部日志均已脱敏。这些是该次合作中的示例性前后对比测量值，不是对其他项目的保证。

| 维度 | 之前 | 之后 | 测量方式 |
|---|---|---|---|
| 前端字段/接口对齐 | 每个新模块 3-5 个 API 404；约 40% 页面需要上线后返工；追踪一个缺失字段约 30 分钟/页 | 0 个 404；审计后 0% 返工；约 5 分钟/页 | 上线前逐页做字段对 API 审计 |
| 库存过账入口 | 6 个服务各自调用出入库，逻辑分散 | 1 个幂等过账服务 | 影响分析 2-3 小时 -> 约 15 分钟 |
| 权限可见性判定点 | 3 处（订阅、功能地图、页面代码） | 1 条裁定链 | 新模块接线 4 小时 -> 约 30 分钟；缺陷分诊 60 分钟 -> 约 10 分钟 |
| 入职 / 决策上下文 | 重建上下文要 5-7 天 | 通过 ADR 约 2 天 | 知识留存 |
| Skill 进化 | 0 个 Skill，每个会话都要手工提供上下文 | 42 个 Skill；重复错误模式触发进化 | 能力积累 |

**诚实的边界**：这些数字来自一个复杂的老项目（brownfield），只是方向性参考，并未跨项目做基准化。公开表述必须把它们当作单个脱敏案例引用，禁止当成通用百分比。

## 公开表述规则 | Public Claim Rules

允许：

- 「本项目提供规则、Skill、适配器与验证门禁。」（"The project provides rules, skills, adapters, and verification gates."）
- 「本项目的设计目标是减少返工与规则漂移。」（"The project is designed to reduce rework and rule drift."）
- 「证据收集方式已在 `VALUE_EVIDENCE.md` 中定义。」（"Evidence collection is defined in `VALUE_EVIDENCE.md`."）

在完成测量之前不允许：

- 「将缺陷减少 X%」（"reduces bugs by X%"）
- 「节省 X% token」（"saves X% tokens"）
- 「保证企业级交付」（"guarantees enterprise-grade delivery"）
- 「彻底解决 AI 幻觉」（"fully solves AI hallucination"）

## 下一步证据工作 | Next Evidence Work

1. 挑选 3 个可公开的小任务。
2. 每个任务分别在不使用方法论、以及使用 `lite`/`full` 模式下各跑一次。
3. 记录返工次数、验证结果与失败原因。
4. 只发布脱敏后的摘要。
