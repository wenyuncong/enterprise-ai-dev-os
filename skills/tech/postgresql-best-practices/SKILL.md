---
name: postgresql-best-practices
description: "PostgreSQL schema design and query optimization: data types, constraints, indexing, EXPLAIN, transactions, migrations, connection pooling, and backups. Use when designing a table or schema, writing or tuning a query, adding an index, or reviewing migration safety."
metadata:
  requires:
    bins: [psql]
    scope: runtime
    declared-by: enterprise-ai-dev-os
---

## Rule

- Design for correctness first: explicit types, NOT NULL, check constraints, and foreign keys before indexes.
- Index for the queries that exist, not the columns that might be used; verify with EXPLAIN ANALYZE.
- One migration per change (Alembic/Flyway); migrations are append-only and reversible.
- Transactions own multi-statement consistency; never rely on implicit autocommit for compound writes.
- Connection pooling (PgBouncer or app-level pool) is mandatory for production; never open a connection per request.
- No silent degradation: slow queries get EXPLAIN ANALYZE and a targeted fix, never a workaround or N+1 acceptance.
- Backups and restore drills are part of the schema lifecycle, not an afterthought.

## Purpose

PostgreSQL is the default relational truth store in this methodology (DB -> backend -> API). This skill keeps the data layer deterministic: correct constraints, proven indexes, safe migrations, and observable query performance, so the single-source-of-truth rule holds at the storage layer.

## Trigger | 触发条件

- Use when: designing a table or schema, writing a complex query, adding an index, or running a migration.
- Use before: creating a new table, altering a column, or writing a report query.
- Use for: slow query tuning, N+1 fixes, migration safety reviews, or backup/restore planning.

## Workflow

1. Write the schema with types, constraints, and FKs; state the business rule the table serves.
2. Write the query; run EXPLAIN ANALYZE before and after indexing to prove the improvement.
3. Add the migration in a single reversible step; test upgrade and rollback.
4. Verify data integrity with a targeted readback; confirm the index is used in the plan.
5. Record the evidence: plan output, row counts, and latency before/after.

## Guardrails

- Never add an index without an EXPLAIN ANALYZE baseline; never index speculative columns.
- Never delete or rewrite data without a backup and a rollback path.
- Do not put business logic in stored procedures or triggers when the service layer owns the truth.
- Avoid SELECT * and untyped columns; keep the schema explicit and auditable.
