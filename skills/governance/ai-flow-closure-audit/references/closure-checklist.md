# Flow Closure Checklist

## Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- `{PROJECT_ROOT}/docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- relevant process document under `{PROJECT_ROOT}/docs/业务流程全案/`
- latest verification report under `{PROJECT_ROOT}/docs/测试验收报告/`

## Typical chain categories

- O2C: order to cash
- S2P: source to pay
- R2R: record to report
- L2C: lead to cash
- production fulfillment
- WMS / TMS execution
- SaaS subscription lifecycle

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
