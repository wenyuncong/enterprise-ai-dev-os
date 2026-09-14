# 架构决策记录模板 | Architecture Decision Record Template

> **源文件**：docs/_templates/架构决策记录/ADR_TEMPLATE.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

---

## ADR-{NNN}：[标题] | ADR-{NNN}: [Title]

**状态（Status）**：[提案（Proposed）/ 已接受（Accepted）/ 已废弃（Deprecated）/ 已被取代（Superseded）]
**日期（Date）**：YYYY-MM-DD
**决策人（Deciders）**：[姓名]
**取代（Supersedes）**：[ADR-NNN]（如有）

---

## 背景 | Context

[描述问题、约束与相关作用力。是什么问题促使做出该决策？]

## 决策 | Decision

[描述已做出的决策。必须清晰、无歧义。]

## 备选方案 | Alternatives Considered

| 备选方案 | 优点 | 缺点 | 未采纳原因 |
|---|---|---|---|
| [方案 1] | [...] | [...] | [...] |
| [方案 2] | [...] | [...] | [...] |

## 后果 | Consequences

### 正面 | Positive
- [...]

### 负面 | Negative
- [...]

### 缓解 | Mitigation
- [...]

## 实施任务 | Implementation Tasks

- [ ] [任务 1]
- [ ] [任务 2]

## 证据 | Evidence

- [相关代码 / 文档 / 测试的链接]

---

## 译注 | Translation Notes

- 文件名中的 `ADR-{NNN}` 为编号占位符，按代码型占位符口径原样保留；`ADR` 不译。
- 状态取值枚举保留英文括注，便于与既有 ADR 文件保持一致。
