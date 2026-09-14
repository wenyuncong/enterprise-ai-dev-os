# AI 原生任务拆解模板 | AI-Native Task Decomposition Template

> **源文件**：skills/core/ai-task-decomposer/references/decomposition-template.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-task-decomposer` 的配套参考文件中中文对照版，不是正式加载源。

---

## 1. 优先阅读的主要文档 | Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/docs/全项目总控/TASK_BACKLOG.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- 当前父任务包、执行记录、认领池行（claim-pool row）与主任务表行

## 2. 范围冻结 | Scope Freeze

| 条目 | 内容 |
| --- | --- |
| 父任务 / 任务包 | |
| 相关任务线 | 当前主线 / 治理支撑线 / 特殊线 / 本地线 |
| 范围内 | |
| 范围外 | |
| 受影响模块 / 路径 | |
| 已核查的现有任务包 | |
| 热点文件或协作边界 | |

## 3. 已核实的现状事实 | Verified Current-State Facts

| 类型 | 来源 | 已核实事实 | 阻断性影响 |
| --- | --- | --- | --- |
| 文档事实 | | | |
| 代码事实 | | | |
| DB 事实 | | | |
| 运行时事实 | | | |

## 4. `Current / Target / Implementation` 三段拆分 | `Current / Target / Implementation` Split

| 层 | 必须回答 |
| --- | --- |
| Current | 今天存在什么、什么是坏的、什么证据能证明 |
| Target | 冻结后的结果应当是什么 |
| Implementation | 哪些具体工作项能填补差距 |

## 5. 批次表 | Batch Table

| 批次 ID | 优先级 | 领域 / 模块 | 层 | 范围 | 依赖 / 阻断项 | 文件 / 路径 | 验收 | 证据 | 建议归属人 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | P0/P1/P2 | | current / target / implementation / QA | | | | | | |

## 6. 内部包 vs 外部派单 | Internal Pack vs External Dispatch

| 输出类型 | 使用时机 | 必须包含 |
| --- | --- | --- |
| 内部拆解包 | 仍需 chief-planner 控盘或需要更细的依赖拆解 | 阻断项、拆分逻辑、风险说明、回流规则 |
| 外部派单包 | 可被另一对话或执行者直接认领 | 可执行批次、写入范围、验收、证据、无隐藏假设 |

## 7. 交接块模板 | Handoff Block Template

```text
Task ID:
Parent task:
Task line:
Priority:
Scope:
Current facts:
Target state:
Implementation items:
Dependency / blocker:
Files / paths:
Acceptance:
Evidence required:
Do-not-touch boundaries:
```

## 8. 典型批次顺序 | Typical batch order

1. 现状核实
2. 设计或规则冻结
3. 后端 / DB 基础工作
4. 前端或页面工作
5. 集成 / 运行时验证
6. 文档收口与回填
