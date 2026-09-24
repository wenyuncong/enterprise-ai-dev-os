---
name: java-performance-governance
description: "Java/Spring performance and memory governance: batch-operation efficiency, unbounded caches, thread/connection leaks, finally cleanup, SQL cost, and observability. Use when diagnosing slow batch operations, memory growth, timeouts, or when reviewing performance-sensitive Java code."
metadata:
  requires:
    bins: [java]
    scope: runtime
    declared-by: enterprise-ai-dev-os
---

## Rule

- No silent degradation: diagnose the root cause with evidence (profile, logs, metrics) before changing code; never paper over a leak with a restart or a bigger heap.
- Batch operations are set-based: never loop single-row deletes/updates when one bounded SQL can do the job.
- Every resource acquired across a request must be released in `finally` (thread-locals, schema/tenant context, streams, connections).
- Caches are bounded and evictable: unbounded `ConcurrentMapCacheManager` or grow-only maps leak memory.
- Queries are index-backed: run EXPLAIN / inspect the plan before accepting a slow query; no N+1 in loops.
- Observability first: structured logs, request IDs, and pool/cache metrics exist before optimization.

## Purpose

Java backends degrade in a small set of predictable ways: unbounded caches, missing finally cleanup, per-request logging/rewriting, oversized threads, and row-by-row batch operations. This skill turns those failure patterns into a reusable diagnostic-and-fix playbook, so AI fixes the root cause instead of hiding the symptom. It generalizes the batch-operation and memory-leak governance extracted from a large multi-tenant ERP.

## Trigger | 触发条件

- Use when: diagnosing slow batch deletes/updates/audits, memory growth or OOM, timeouts, or connection-pool exhaustion.
- Use before: reviewing performance-sensitive Spring/MyBatis code, or adding a cache/thread/async config.
- Use for: memory-leak investigation, batch SQL refactoring, index planning, and observability setup.

## Workflow

1. Capture the baseline: heap/cache/pool/thread metrics and the offending operation's latency.
2. Reproduce and profile: identify the specific root cause (unbounded cache, missing finally, N+1, missing index).
3. Fix the root cause: bound the cache, add finally cleanup, set-based SQL, index, or bounded pool.
4. Verify with fresh evidence: before/after latency, memory trend, query plan, and pool usage.
5. Record the pattern: if the same root cause recurs, feed it into a reusable checklist or skill.

## Common Root Causes | 常见根因

| Pattern | Symptom | Fix |
|---|---|---|
| Unbounded cache (ConcurrentMapCacheManager / grow-only map) | Heap grows steadily | Bound size + TTL/eviction |
| Missing `finally` cleanup (thread-local / tenant / schema context) | Cross-request leakage, wrong data | Always release in finally |
| Per-request DB logging / SQL regex rewrite | High CPU, slow requests | Gate to debug level, precompile |
| Oversized async pool / unbounded queue | Thread exhaustion | Bound pool + queue + reject policy |
| Row-by-row batch delete/update | Linear timeouts | Set-based SQL + index + paged batches |
| N+1 query / missing index | Slow lists | EXPLAIN, add index, batch-fetch |

## Guardrails

- Never fix a memory leak by enlarging the heap or restarting the service.
- Never delete/update in a per-row loop when a set-based statement applies.
- Do not add an index without an EXPLAIN baseline; do not add a cache without a bound and eviction policy.
- Keep optimizations evidence-driven; record before/after numbers, not vibes.
