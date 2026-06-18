# Domain Boundary Map Template

## Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- architecture decision records under `{PROJECT_ROOT}/docs/架构决策记录/`
- business process documents under `{PROJECT_ROOT}/docs/业务流程全案/`
- deployment and runtime ownership docs under `{PROJECT_ROOT}/docs/部署运维手册/`

## 1. Scope Freeze

| Item | Content |
| --- | --- |
| Related domains | |
| Target objects | |
| Existing docs checked | |
| Existing code / tables / APIs checked | |
| Main conflict type | ownership / placement / write / writeback / extension |

## 2. Current Object Map

| Object | Object type | Current owner guess | Current table / schema | Current write path |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 3. Target Ownership Matrix

| Object | Source domain | Extension domain | Source-of-truth object | Write owner | Read domains |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## 4. Storage Placement Matrix

| Object | Platform DB / service | `tenant_default` | `tenant_*` | Writeback direction |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 5. Conflict and Risk List

| Conflict | Risk | Required decision |
| --- | --- | --- |
|  |  |  |

## 6. Dispatch-Ready Tasks

| Task type | Priority | Task | Evidence / acceptance |
| --- | --- | --- | --- |
| Doc / governance | P0/P1/P2 |  |  |
| Schema / DB | P0/P1/P2 |  |  |
| API / backend | P0/P1/P2 |  |  |
| Frontend / menu | P0/P1/P2 |  |  |
| QA / acceptance | P0/P1/P2 |  |  |
