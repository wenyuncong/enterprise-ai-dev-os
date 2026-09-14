# 任务 DAG 字段说明 | task_dag.json Field Reference

> **源文件**：docs/_templates/全项目总控/task_dag.json
> **源版本**：未标注（文件内 `schemaVersion` 为 1.0.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

> 本文件是**字段说明文档**，不是 DAG 本身。原样 JSON 模板见第 6 节，直接复制即可套用。
> 校验与排期命令：`py scripts/py/orchestrate_dag.py --dag <DAG 路径> [--json]`

---

## 1. 用途 | Purpose

`task_dag.json` 是多智能体编排（orchestration）用的任务 DAG（有向无环图）契约：`nodes` 描述工作项及其数据依赖，`contracts` 固定跨节点集成点。

`scripts/py/orchestrate_dag.py` 负责校验图、检测环，并输出并行层次执行计划。

> 它是**契约 + 规划器**，不是派发器（dispatcher）：真正的扇出（fan-out）由宿主机运行时（子智能体 / 后台任务）执行。

---

## 2. 顶层字段 | Top-Level Fields

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `schemaVersion` | 应当填写 | 字符串，模板为 `"1.0.0"` | 结构版本号；键名按原样保留 |
| `description` | 可选 | 字符串 | 说明该图是什么、谁来校验它。脚本不读取该字段，仅供人读 |
| `nodes` | 必须 | 对象数组，见第 3 节 | 工作项及其依赖；`orchestrate_dag.py` 缺失时按空数组处理（会输出 0 层计划） |
| `contracts` | 可选 | 对象数组，见第 4 节 | 跨节点集成点契约；缺失时按空数组处理 |

---

## 3. `nodes[]` | 节点

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `id` | 必须 | 字符串，全局唯一 | 节点标识；重复即判为非法 DAG |
| `name` | 可选 | 字符串 | 展示名；缺失时脚本回退用 `id` 代替 |
| `depends` | 可选 | 字符串数组 | 前置节点 `id` 列表；指向不存在的 `id` 即判为非法 DAG |

**规则**

- 节点可以有零个依赖（`depends: []`），这类节点进入第 1 并行层。
- 依赖只能指向同一图内已声明的 `id`。
- 依赖关系必须无环；出现环时校验失败并返回退出码 1。

---

## 4. `contracts[]` | 集成契约

| 字段 | 是否必填 | 取值 / 格式 | 用途 |
|---|---|---|---|
| `from` | 应当填写 | 字符串（上游节点 `id`） | 契约上游 |
| `to` | 应当填写 | 字符串（下游节点 `id`） | 契约下游 |
| `contract` | 应当填写 | 字符串 | 集成点约定：口径、幂等键、交付物等 |

> 脚本只做原样回显（`contracts` 计数与内容透传），不校验 `from` / `to` 是否存在于 `nodes`。**这是使用方需要自己守住的边界**。

---

## 5. 校验与输出 | Validation and Output

| 行为 | 结果 |
|---|---|
| `id` 重复 | 报错 `duplicate node id`，退出码 1 |
| 依赖不存在的节点 | 报错 `node '<id>' depends on unknown node '<dep>'`，退出码 1 |
| 存在环 | 报错 `cycle detected in task DAG`，退出码 1 |
| 合法 | 按 Kahn 拓扑排序分层输出：节点数、顺序层数、每层可并行节点（`--json` 时输出结构化结果） |

每层内的节点可并发执行；上一层全部完成后才能进入下一层。

---

## 6. 完整 JSON 模板 | Full JSON Template（原样保留，键名不译）

```json
{
  "schemaVersion": "1.0.0",
  "description": "Task DAG template for multi-agent orchestration. nodes describe work items and their data dependencies; contracts pin cross-node integration points. scripts/py/orchestrate_dag.py validates the graph, detects cycles, and emits a parallel-layer execution plan. Replace the example nodes with a real plan; this is a contract + planner, not a dispatcher.",
  "nodes": [
    { "id": "platform-foundation", "name": "平台基础（租户/权限/菜单）", "depends": [] },
    { "id": "inventory", "name": "库存域", "depends": ["platform-foundation"] },
    { "id": "finance", "name": "财务域", "depends": ["platform-foundation"] },
    { "id": "reports", "name": "报表域", "depends": ["inventory", "finance"] }
  ],
  "contracts": [
    { "from": "inventory", "to": "finance", "contract": "出入库金额口径：库存过账后以事件通知应付/成本，幂等键 = 单据号+行号" }
  ]
}
```

---

## 7. 套用步骤 | How to Reuse

1. 复制第 6 节 JSON 到任务目录。
2. 用真实工作项替换示例 `nodes`：`id` 一律用英文短横线命名（沿用原模板风格，如 `platform-foundation`）。
3. 用真实集成点替换示例 `contracts`：写清口径与幂等键。
4. 运行校验与排期：`py scripts/py/orchestrate_dag.py --dag <DAG 路径> --json`；退出码非 0 表示图非法。
5. 按输出的层序并行派发子智能体。

---

## 译注与待确认 | Notes and Open Points

- **无独立 Schema**：`docs/全项目总控/schemas/` 下没有 `task_dag` 的 JSON Schema；第 2–4 节的「是否必填」是按 `scripts/py/orchestrate_dag.py` 的实际读取逻辑推断的，而非模式声明。
- **`description` 中的路径**：源模板 `description` 内引用了 `scripts/py/orchestrate_dag.py`（仓库相对路径），已原样保留。
- **示例节点名本就是中文**：源模板的 `name` 值（「平台基础（租户/权限/菜单）」「库存域」「财务域」「报表域」）已是中文，按「JSON 模板原样保留」口径未作改动。
