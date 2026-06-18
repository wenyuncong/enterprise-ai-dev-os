# Architecture Governance Map

## Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- domain map or system-boundary document under `{PROJECT_ROOT}/docs/架构决策记录/`
- business process documents under `{PROJECT_ROOT}/docs/业务流程全案/`
- deployment / runtime ownership documents under `{PROJECT_ROOT}/docs/部署运维手册/`

## Typical architecture questions

1. Which domain is the business source of truth?
2. Which domain is only an entry layer?
3. Which domain is only an enablement / enhancement layer?
4. Who owns identity, tenant, org, and permission subjects?
5. Which objects may cross domains, and in what direction?
6. Which domain closes finance / settlement / reporting truth?
7. Which settings are global, tenant-level, or channel-level?
8. Which object belongs to which schema / main table / main service?

## Cross-domain governance checklist

### A. Boundary

- involved domains
- primary owner
- forbidden duplicate ownership
- entry vs truth vs enhancement distinction

### B. Identity and tenant

- login subject
- tenant scope
- role / permission injection
- external user / internal user / partner subject split when the domain has multiple identity types

### C. Data ownership

- master data source
- document source
- object owner
- status writeback owner
- report / finance close owner

### D. Object landing

- main table
- main service
- schema placement
- allowed writers
- forbidden writers

### E. Chain design

- entry
- transfer object
- downstream truth table
- writeback path
- failure / fallback handling

## Expected artifacts

- domain boundary matrix
- architecture decision notes
- object-level ownership map
- schema placement matrix
- main-chain ownership map
- follow-up task list
