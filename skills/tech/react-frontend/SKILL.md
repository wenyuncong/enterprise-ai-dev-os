---
name: react-frontend
description: "React 18+ frontend engineering with TypeScript: function components and hooks, display-only views, state management, performance, error boundaries, and testing. Use when building or reviewing a React page or component, adding state, or fixing rendering/performance issues."
---

## Rule

- Frontend is display only: no business logic, pricing, validation decisions, or state transitions computed in the UI; request supported commands from the API and render the result.
- Function components + hooks; no class components for new code. TypeScript for all props and state.
- Single truth: never compute the same derived value in two places; derive in one selector/hook and reuse.
- Server state goes through a data layer (fetch wrapper / react-query), not scattered useEffect calls.
- No business logic in useMemo or useCallback; those are for identity/performance only.
- Every async fetch handles four states: loading, empty, error, edge; errors surface at the correct severity (never silent).
- Library first: prefer react-query, zod (shared with backend), and a mature component library over custom abstractions.

## Purpose

React is the primary frontend surface in modern enterprise stacks. This skill keeps React views deterministic and consistent with the methodology: UI renders, backend decides. It prevents the classic drift where AI adds business calculations, duplicate state, or silent error handling into components.

## Trigger | 触发条件

- Use when: creating, extending, or reviewing a React page, component, hook, or store.
- Use before: writing a component with props, adding state, or wiring an API call.
- Use for: rendering bugs, state duplication, performance audits, or adding component tests.

## Workflow

1. Confirm the truth lives in the backend/API; the component only maps API data to UI.
2. Define typed props and a typed API response; validate at the boundary if needed.
3. Choose the state home: server data in the data layer, UI state local, shared UI state in a store.
4. Render the four states (loading, empty, error, edge) explicitly; never leave a path silent.
5. Add a component test (Vitest + React Testing Library) for render and interaction; verify in the browser.

## Guardrails

- Never compute prices, totals, status transitions, or permission decisions in components, selectors, or useMemo.
- Never duplicate a field definition across components; centralize in the data layer or shared types.
- Do not hard-code colors or strings; use theme tokens and i18n keys.
- Avoid empty catch blocks around fetch calls; map errors to visible feedback.
