# Business Process Documentation Template

## [Process Name] — Business Process Documentation

**Version**: 1.0.0
**Domain**: [Purchase / Sales / Inventory / Finance / ...]
**Last Updated**: YYYY-MM-DD

---

## Process Overview | 流程概述

[One-paragraph summary of what this process does and why it exists.]

## Process Flow | 流程图

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

## Step Details | 步骤详情

### Step 1: [Step Name]
- **Entry**: [What triggers this step]
- **Validation**: [What checks are performed]
- **Success**: [What happens on success]
- **Failure**: [What happens on failure]

### Step 2: [Step Name]
[...]

## Related Entities | 相关实体

| Entity | Table | Schema | Owner Domain |
|---|---|---|---|
| [Entity 1] | [table_name] | [schema] | [domain] |

## Parameters & Configuration | 参数与配置

| Parameter | Default | Description | Affects |
|---|---|---|---|
| [param_1] | [value] | [desc] | [which steps] |

## Audit & Writeback | 审计与回写

| Downstream System | What is Written | When | Idempotency Key |
|---|---|---|---|
| Inventory | Stock movement | On audit | source_type + source_id |
| Finance | Voucher entry | On audit | source_type + source_id |
