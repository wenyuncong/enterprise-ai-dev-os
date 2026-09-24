---
name: node-backend
description: "Node.js backend engineering for Express, NestJS, and Fastify services: layered structure, async discipline, validation, error handling, middleware, testing, and observability. Use when building or reviewing a Node.js API, adding a route or service, or debugging async/error behavior."
metadata:
  requires:
    bins: [node]
    scope: runtime
    declared-by: enterprise-ai-dev-os
---

## Rule

- Layered structure: route/controller -> service -> repository; no business logic inside route handlers or middleware.
- Single truth: validation schemas, domain rules, and calculations live in the service layer once; do not recompute in handlers.
- Every async operation is awaited or explicitly handled; no floating promises. Unhandled rejections fail the process.
- No silent failures: catch, log, and surface errors with the correct severity; never swallow exceptions in empty catch blocks.
- Validate every boundary input with a schema (zod or class-validator) before the service layer sees it.
- Library first: prefer mature packages (express, fastify, nest, zod, pino) over hand-rolled utilities.

## Purpose

Node.js powers most API backends in this ecosystem. This skill keeps Node backends deterministic: stable layering, strict input validation, explicit async handling, and testable units, so AI-generated endpoints follow the same shape as hand-written ones.

## Trigger | 触发条件

- Use when: creating, extending, or reviewing a Node.js/Express/NestJS/Fastify API.
- Use before: writing a route handler, a service method, or a repository query.
- Use for: async/await bug fixes, error-handling audits, validation and schema work, or adding tests.

## Workflow

1. Identify the layer that owns the truth (service) versus the transport (route/controller).
2. Define the input schema and the response shape before writing the handler.
3. Write the service method with explicit error types; handlers map errors to HTTP responses.
4. Add a focused test (supertest + jest/vitest) for the success path and the failure path.
5. Verify: run the tests, then call the endpoint and confirm status codes and payloads.

## Guardrails

- Never put business logic (pricing, state transitions, permission decisions) in route handlers or middleware.
- Never ignore rejected promises; never use empty catch blocks.
- Do not store secrets in code or config files; use environment variables and a secret manager.
- Avoid deep callback chains; prefer async/await with try/catch or error-boundary middleware.
