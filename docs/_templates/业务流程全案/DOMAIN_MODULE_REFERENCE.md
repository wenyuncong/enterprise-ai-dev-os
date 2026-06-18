# Domain Module Decomposition Reference | 领域模块分解参考

> **Extracted from**: GERP Enterprise ERP — 24 domain modules across 6 categories
> **Use when**: Designing atomic service boundaries for a new enterprise project

---

## Decomposition Principles | 分解原则

1. **One module = one business capability** — not one table, not one screen
2. **Max 3 dependencies** — any module depending on > 3 others should be split
3. **Data ownership is exclusive** — each table belongs to exactly one module
4. **API is the only contract** — modules communicate only through defined APIs

---

## Reference Module Map | 参考模块地图

```
┌─────────────────────────────────────────────────────────────┐
│                     FOUNDATION LAYER                         │
│  ┌──────────┐  ┌──────────────┐  ┌──────────┐              │
│  │   base   │  │  masterdata  │  │   auth   │              │
│  │ (system  │  │  (product,   │  │  (user,  │              │
│  │  config) │  │  customer,   │  │  role,   │              │
│  │          │  │  supplier)   │  │  tenant) │              │
│  └──────────┘  └──────────────┘  └──────────┘              │
├─────────────────────────────────────────────────────────────┤
│                     CORE BUSINESS LAYER                      │
│  ┌──────┐  ┌──────────┐  ┌─────┐  ┌────────────┐  ┌─────┐ │
│  │ sale │  │ purchase │  │ inv │  │ production │  │ wms │ │
│  └──────┘  └──────────┘  └─────┘  └────────────┘  └─────┘ │
├─────────────────────────────────────────────────────────────┤
│                     FINANCE LAYER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ finance  │  │ payment  │  │ capital  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
├─────────────────────────────────────────────────────────────┤
│                     EXTENDED BUSINESS LAYER                  │
│  ┌─────┐  ┌──────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌───────┐ │
│  │ crm │  │ mall │  │ b2b │  │ scm │  │ tms │  │ trade │ │
│  └─────┘  └──────┘  └─────┘  └─────┘  └─────┘  └───────┘ │
├─────────────────────────────────────────────────────────────┤
│                     OPERATIONS LAYER                         │
│  ┌────────┐  ┌───────┐  ┌────┐  ┌─────┐  ┌─────┐          │
│  │ report │  │ print │  │ oa │  │ mes │  │ qms │          │
│  └────────┘  └───────┘  └────┘  └─────┘  └─────┘          │
├─────────────────────────────────────────────────────────────┤
│                     PLATFORM LAYER                           │
│  ┌──────┐  ┌───────┐  ┌────┐                                │
│  │ saas │  │ agent │  │ ai │                                │
│  └──────┘  └───────┘  └────┘                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Module Dependency Rules | 模块依赖规则

| Rule | Rationale |
|---|---|
| Foundation modules depend on NOTHING | They are the root of the dependency tree |
| Core Business depends on Foundation | sale → masterdata (needs product/customer data) |
| Finance depends on Core Business | finance → sale (needs invoice data) |
| Extended Business depends on Core | crm → sale (needs customer order history) |
| Operations depends on ALL above | report reads from all modules |
| Platform depends on ALL above | saas manages all tenant subscriptions |

**Anti-pattern**: `sale → payment` (circular dependency). Fix: both depend on a shared event bus.

---

*Last updated: 2026-06-17 | Source: GERP Enterprise ERP*
