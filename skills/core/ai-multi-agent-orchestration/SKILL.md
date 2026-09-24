---
name: ai-multi-agent-orchestration
description: "Orchestrate parallel AI agents across domain boundaries: partition a large project into domains, decide parallel vs serial execution by data-dependency, define contracts before integration, and set role/acceptance boundaries. Use when a task spans multiple modules or domains, or when fanning out work across several agents."
metadata:
  requires:
    scope: universal
    declared-by: enterprise-ai-dev-os
---

## Rule

- Partition by domain ownership, not by file type: each agent owns a bounded domain with a single truth owner.
- Contracts first: any cross-domain integration point is defined as a read/write contract before parallel work starts.
- Parallel only when there is no shared-table write; read-only dependencies may run in parallel.
- Serial when one domain writes data another domain reads downstream, or when an API contract is not yet defined.
- Every agent gets an explicit acceptance boundary and a non-goals list; no agent may silently expand scope across domains.

## Purpose

Single-agent decomposition (ai-task-decomposer) breaks one task into ordered batches. Multi-agent orchestration breaks a *project* into concurrently worked domains without merge chaos. This is the missing layer for "多 Agent 编排" in the methodology: it makes parallel AI work deterministic by pinning domain boundaries, dependency direction, and contract-first integration.

## Trigger | 触发条件

- Use when: a task spans multiple modules/domains, or you plan to fan out work across several agents.
- Use before: starting parallel agents, or deciding whether two tasks can run concurrently.
- Use for: merge-conflict-prone work, cross-domain integrations, or planning a large batch across agents.

## Workflow

1. **Partition domains** by ownership and truth owner; document the domain list and each owner.
2. **Draw the dependency graph**: which domain reads which other domain's data.
3. **Classify each pair** with the parallel/serial matrix:

| Dependency | Verdict | Reason |
|---|---|---|
| No data dependency | Parallel | Independent truth |
| Read-only dependency (via API) | Parallel | No write conflict |
| Shared-table write | Serial | Data race / lock conflict |
| Downstream reads upstream writes | Serial | Upstream must commit first |
| Contract not defined | Serial | Define contract first |

4. **Define contracts first**: request/response shape, field truth, error codes, idempotency keys for every cross-domain boundary.
5. **Assign agents** with: domain scope, read/write allowlist, acceptance criteria, non-goals, and the contract document.
6. **Integrate serially** on contract boundaries; run regression and a cross-domain closure audit before declaring done.

## Guardrails

- Never let two agents write the same table or the same truth source concurrently.
- Never start parallel work before the integration contracts are written.
- Never merge a domain's output without its own passing evidence and the cross-domain contract check.
- Do not treat "both agents finished" as integration complete; verify the contract holds end-to-end.
