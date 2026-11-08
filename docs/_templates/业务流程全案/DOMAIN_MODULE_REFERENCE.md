# Domain Module Decomposition Reference | 领域模块分解参考

> **Generalized from**: real enterprise delivery evidence — generic responsibility categories, project and business names removed
> **Use when**: Designing atomic service boundaries for a new enterprise project

---

## Decomposition Principles | 分解原则

1. **One module = one business capability** — not one table, not one screen
2. **Max 3 dependencies** — any module depending on > 3 others should be split
3. **Data ownership is exclusive** — each data collection belongs to exactly one module
4. **API is the only contract** — modules communicate only through defined APIs

---

## Reference Category Map | 参考类别地图

Map the system's own modules onto these generic responsibility categories rather than assuming a fixed module list:

```
┌─────────────────────────────────────────────────────────────┐
│  FOUNDATION — shared base, master/reference data, identity  │
├─────────────────────────────────────────────────────────────┤
│  CORE TRANSACTION — primary flows, asset state, execution   │
├─────────────────────────────────────────────────────────────┤
│  FINANCE — accounting, settlement, funds                    │
├─────────────────────────────────────────────────────────────┤
│  EXTENDED BUSINESS — channels, supply coordination, trade   │
├─────────────────────────────────────────────────────────────┤
│  OPERATIONS — reporting, output, collaboration, quality     │
├─────────────────────────────────────────────────────────────┤
│  PLATFORM — provisioning, agent capabilities, automation    │
└─────────────────────────────────────────────────────────────┘
```

---

## Module Dependency Rules | 模块依赖规则

| Rule | Rationale |
|---|---|
| Foundation modules depend on nothing | They are the root of the dependency tree |
| Core transaction depends on Foundation | transaction flows need reference and identity data |
| Finance depends on Core transaction | accounting needs the transactional evidence |
| Extended business depends on Core | channels need the transaction history |
| Operations depends on the layers above | reporting reads across modules |
| Platform depends on the layers above | provisioning governs all tenants |

**Anti-pattern**: a circular dependency between two modules. Fix: both depend on a shared event bus.

---

*Last updated: 2026-11-08 | Status: universal — project and business names removed*
