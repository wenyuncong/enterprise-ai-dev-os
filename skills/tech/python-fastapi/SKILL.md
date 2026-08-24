---
name: python-fastapi
description: "Python FastAPI backend engineering: layered services, Pydantic validation, async endpoints, dependency injection, SQLAlchemy persistence, and pytest coverage. Use when building or reviewing a FastAPI service, adding an endpoint or model, or fixing validation/async issues."
---

## Rule

- Layered structure: router -> service -> repository; routers only map HTTP to service calls, never carry business logic.
- Define Pydantic schemas for every input and output; the boundary validates before the service layer runs.
- Async endpoints must await all I/O; do not block the event loop with sync DB/HTTP calls inside async def.
- No silent failures: raise domain exceptions, let FastAPI exception handlers map them to responses; never bare except + pass.
- Single truth: domain rules and calculations live in the service layer once; models are data, not logic.
- Library first: prefer FastAPI + SQLAlchemy + Pydantic + pytest instead of hand-rolled validation or ORM wrappers.

## Purpose

FastAPI is the fastest-growing Python API stack in enterprise adoption. This skill keeps FastAPI services deterministic: explicit schemas, clean layering, async discipline, and testable services, matching the methodology's backend truth chain (truth -> service -> orchestration -> API).

## Trigger | 触发条件

- Use when: creating, extending, or reviewing a FastAPI/Python API.
- Use before: writing a router, a Pydantic schema, a SQLAlchemy model, or a service method.
- Use for: validation bugs, async deadlocks, dependency-injection refactors, or adding pytest coverage.

## Workflow

1. Declare the Pydantic schemas (request, response, internal) before endpoints.
2. Write the service layer with explicit domain exceptions; routers stay thin.
3. Configure dependency injection (Depends/Annotated) for auth, DB sessions, and settings.
4. Add pytest tests: httpx TestClient for the happy path and each failure path.
5. Verify: run pytest, then exercise the endpoint and confirm status codes and payloads.

## Guardrails

- Never put business logic in routers, Pydantic validators, or SQLAlchemy events.
- Never mix sync and async ORM calls in the same async endpoint.
- Do not log secrets or full request bodies; use structured logging (structlog/std logging) with request IDs.
- Keep migrations explicit (Alembic); never mutate the schema implicitly from models.
