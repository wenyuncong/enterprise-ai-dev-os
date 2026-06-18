---
name: ai-field-package-governor
description: "Govern field metadata, database-authoritative fields, UI field packages, personalization config, report fields, and duplicate field definitions. Use when adding columns, changing form/table fields, centralizing metadata, or auditing hard-coded page fields."
---

# ai-field-package-governor — Field Metadata & Component Configuration Governor

## Purpose | 用途

Govern the field metadata layer in enterprise systems — the infrastructure that connects database schemas to UI components:

- Field truth source hierarchy (DB → metadata → component configuration)
- Component reuse and composition enforcement
- Field configuration governance (visibility, validation, ordering)
- Report generation from metadata
- Page personalization as a configuration layer, not primary definition

This skill applies to any enterprise system (ERP, CRM, SaaS admin, operations tools) where pages display structured data from a database and field definitions must be centralized rather than duplicated per page.

## Core Rule | 核心规则

**The page does not own the field truth.**

Field truth flows from:
1. **Database schema** — actual table structure, column types, constraints
2. **Field metadata registry** — business labels, validation rules, UI metadata, multilingual labels
3. **Component configuration** — field visibility, ordering, required state, editability
4. **Page personalization** — user-level display preferences (NOT primary field definitions)

The frontend should receive a `businessCode` or `entityKey` and consume fields from the metadata layer — never hard-code field names, labels, or column definitions in individual pages.

---

## Field Truth Source Hierarchy | 字段真相源层次

| Layer | Responsibility | Example |
|---|---|---|
| **Database** | Structural truth | Column types, constraints, nullability |
| **Field Metadata** | Business truth | Labels, validation rules, multilingual names |
| **Component Config** | Display truth | Visibility, ordering, width, required state |
| **Page Personalization** | User preference | Saved filters, column order, hidden fields |

**Violation detection**: If the same field label appears in 3+ page files, it belongs in the metadata layer, not in individual pages.

---

## Configuration Sources | 配置来源

### 1. Database-First
Before any field configuration, verify the actual database schema:
```
Check: column exists, type matches, constraints are correct
Source: DESCRIBE table / SHOW COLUMNS
```

### 2. Metadata Registry
Central field definitions contain:
- Field key (matches DB column)
- Display label (multilingual)
- Data type and format
- Validation rules
- Default values
- Relation mappings (foreign key → selector)

### 3. Component Binding
Pages bind to metadata via identifiers:
- `businessCode` — for standard CRUD pages
- `entityKey` — for domain-specific components
- `reportCode` — for report and analytics pages

### 4. User Personalization
Users can customize without breaking truth:
- Show/hide optional fields
- Reorder columns
- Save filter presets
- Adjust column widths

---

## Component Reuse Pattern | 组件复用模式

| If you need to... | Use... | NOT... |
|---|---|---|
| Display a data list | Shared list component + businessCode | Hard-coded table with page-local columns |
| Show a form | Shared form component + entityKey | Manually written form fields per page |
| Generate a report | Shared report engine + reportCode | Page-local SQL + custom chart rendering |
| Filter data | Metadata-driven filter bar | Per-page filter component duplication |

**Acceptance check**: Adding a new database column should update the metadata registry, and ALL pages consuming that entity should reflect the change — without modifying a single page file.

---

## Report Generation Pattern | 报表生成模式

For standard list/chart reports that can be described by metadata:

1. **Register dataset** — define source tables, field whitelist, dimensions, metrics
2. **Register metadata** — auto-import relation fields (customer→customerId, product→productId)
3. **Generate frontend** — shared report component receives `reportCode`, renders dynamically
4. **Enforce permissions** — backend report engine controls access, not frontend component

**Only create a custom report page when**: the report requires interactive workflows, multi-step commands, or a specialized UX that metadata cannot express.

---

## Document Identity Pattern | 文档身份模式

When one physical entity (table) represents multiple business identities:

1. Register each identity as a formal entity type with its own metadata alias
2. Route decisions through the identity, not the table name
3. Each identity has its own numbering, permissions, and field visibility rules
4. Reuse the shared component, lock/hide identity-irrelevant fields

---

## Standard Workflow | 标准工作流

### Adding a New Field
1. **DB**: Add column to table (migration script)
2. **Metadata**: Register in field metadata registry
3. **Configuration**: Set default visibility, ordering, validation
4. **Verification**: All consuming pages display the field correctly — verify 3+ pages

### Modifying a Field
1. **Check consumers**: Find all pages/components referencing this field
2. **Verify DB**: Confirm column type and constraints match metadata
3. **Update metadata**: Change label, validation, or display rules centrally
4. **Verify**: All consumers reflect the change, no page-local overrides break

---

## Guardrails | 防护规则

- Do not hard-code field labels in individual pages
- Do not treat page personalization config as the primary field definition
- Do not add a database column without registering it in the metadata layer
- Do not create a second source of truth for the same field
- Do not bypass metadata for "quick fixes" — they become permanent debt
- Do not duplicate filter/column/form logic across pages of the same entity

## Maturity | 成熟度

**Stage**: Effective — Extracted from 111KB enterprise field governance system with metadata-driven component architecture.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-atomic-component-fieldpackage (111KB original)
- Source: Enterprise ERP metadata governance across purchase/sales/inventory/finance/capital modules
