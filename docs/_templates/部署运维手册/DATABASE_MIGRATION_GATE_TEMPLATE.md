# Database Migration Consistency Gate

Use this record for schema, seed, parameter-baseline, or tenant-data
migrations. A deployment job or successful API response does not replace this
gate.

## Migration Identity

| Item | Value |
| --- | --- |
| Migration ID | |
| Target version | |
| Source path | |
| Dependency / execution order | |
| Checksum | |
| Replacement or supersession relation | None / [record] |

## Environment Registration

| Environment | Registered | Registry / manifest path | Commit or version |
| --- | --- | --- | --- |
| Test / staging | Yes / No | | |
| Production | Yes / No | | |

## Safety and Recovery

| Check | Result | Evidence |
| --- | --- | --- |
| Idempotent or guarded precondition | Pass / Fail / N/A | |
| Duplicate or superseded migration prevented | Pass / Fail / N/A | |
| Recovery path | Pass / Fail | |
| Backup / compensating migration / revert point | | |

## Execution History

| Environment | Status | Finished at | Operator / job | Commit / version | Evidence |
| --- | --- | --- | --- | --- | --- |
| Test / staging | | | | | |
| Production | | | | | |

## Post-Migration Checks

| Scope | Check | Result | Evidence |
| --- | --- | --- | --- |
| Schema | Tables, columns, indexes, constraints | Pass / Fail | |
| Seed / parameters | Required rows and values | Pass / Fail | |
| Runtime profile | Compiled profile reflects the migration | Pass / Fail | |
| Tenant scope | Intended tenants changed; unrelated tenants unchanged | Pass / Fail | |
| Business flow | Affected flow still closes | Pass / Fail | |

## Decision

```text
Migration gate: pass / blocked
Missing evidence or blockers:
Recovery decision:
Release decision:
```
