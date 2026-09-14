# 业务流程文档模板 | Business Process Documentation Template

> **源文件**：docs/_templates/业务流程全案/BUSINESS_PROCESS_TEMPLATE.md
> **源版本**：未标注（模板内示例字段为 1.0.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

---

## [流程名] — 业务流程文档 | [Process Name] — Business Process Documentation

**版本（Version）**：1.0.0
**领域（Domain）**：[采购 / 销售 / 库存 / 财务 / ...]
**最后更新（Last Updated）**：YYYY-MM-DD

---

## 流程概述 | Process Overview

[用一段话概述该流程做什么、为什么存在。]

## 流程图 | Process Flow

`mermaid
graph TD
    A[Start: User Action] --> B[API Call]
    B --> C[Service Validation]
    C --> D{Check Pass?}
    D -->|Yes| E[DB Write]
    D -->|No| F[Return Error]
    E --> G[Writeback to Downstream]
    G --> H[Report Updated]
`

## 步骤详情 | Step Details

### 第 1 步：[步骤名] | Step 1: [Step Name]
- **入口（Entry）**：[什么会触发该步骤]
- **校验（Validation）**：[执行哪些校验]
- **成功（Success）**：[成功后发生什么]
- **失败（Failure）**：[失败后发生什么]

### 第 2 步：[步骤名] | Step 2: [Step Name]
[...]

## 相关实体 | Related Entities

| 实体 | 表 | Schema | 归属领域 |
|---|---|---|---|
| [实体 1] | [table_name] | [schema] | [领域] |

## 参数与配置 | Parameters & Configuration

| 参数 | 默认值 | 说明 | 影响范围 |
|---|---|---|---|
| [param_1] | [取值] | [说明] | [影响哪些步骤] |

## 审计与回写 | Audit & Writeback

| 下游系统 | 写入内容 | 触发时机 | 幂等键 |
|---|---|---|---|
| 库存（Inventory） | 库存流水（Stock movement） | 审计通过时 | source_type + source_id |
| 财务（Finance） | 凭证分录（Voucher entry） | 审计通过时 | source_type + source_id |

---

## 译注 | Translation Notes

- 源文件第 17 行与第 26 行的围栏是**单反引号**（`` `mermaid `` / `` ` ``），不是三反引号。本译文按「代码块原样保留」口径照抄该围栏；实际套用时请改为三反引号，Mermaid 图才会渲染。
- 表格中 `source_type + source_id` 为幂等键标识符，原样保留。
