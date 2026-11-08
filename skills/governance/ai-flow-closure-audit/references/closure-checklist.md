# Flow Closure Checklist

## Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- `{PROJECT_ROOT}/docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- relevant process document under `{PROJECT_ROOT}/docs/业务流程全案/`
- latest verification report under `{PROJECT_ROOT}/docs/测试验收报告/`

## Typical chain shapes (generic; map the project's own flows onto these)

- primary transaction chain: request -> execution -> document -> settlement
- procurement-style chain: request -> order -> receipt -> settlement
- record/report chain: transaction -> ledger -> analytical report
- opportunity chain: lead -> opportunity -> quote -> commitment
- fulfillment chain: commitment -> preparation -> shipment
- operations execution
- subscription lifecycle

## Audit checklist

### A. Basic facts

- page exists
- route / menu exists
- API exists
- table exists
- parameters exist

### B. Main behavior

- create / save
- submit / audit
- downstream push
- state transition
- writeback / reconciliation

### C. Extended closure

- report / history / ledger support
- export or query support
- permission / parameter gating
- cross-module consistency

### D. Evidence

- SQL
- API logs
- UI screenshots
- compile or runtime verification when needed
- execution backfill reference

## Expected artifacts

- closure evidence table
- gap list
- acceptance checklist
- regression task list
- task-log and backfill references
