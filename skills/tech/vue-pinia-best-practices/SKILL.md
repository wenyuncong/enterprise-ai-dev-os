---
name: vue-pinia-best-practices
description: "Pinia stores, state management patterns, store setup, and reactivity with stores. Use when creating, reviewing, debugging, or refactoring Pinia stores, setup stores, store consumption, URL-backed state, SSR state, or reactivity problems in Vue apps."
version: 1.0.0
license: MIT
author: github.com/vuejs-ai
---

Pinia best practices, common gotchas, and state management patterns.

## Purpose

Use this skill to keep Pinia state predictable, reactive, testable, and appropriately scoped.

## Workflow

1. Decide whether state belongs in Pinia, URL/query params, component-local state, or backend data.
2. Use setup stores carefully and return all state needed by DevTools, SSR, plugins, or persistence.
3. Preserve reactivity when consuming store state in components.
4. Keep actions as the place for state transitions and side effects.
5. Verify state behavior by refreshing, navigating, and checking affected components.

### Store Setup
- Getting "getActivePinia was called" error at startup → See [pinia-no-active-pinia-error](reference/pinia-no-active-pinia-error.md)
- Setup stores missing state in DevTools or SSR → See [pinia-setup-store-return-all-state](reference/pinia-setup-store-return-all-state.md)

### Reactivity
- Store destructuring stops updating UI reactively → See [pinia-store-destructuring-breaks-reactivity](reference/pinia-store-destructuring-breaks-reactivity.md)
- Store methods lose context in template calls → See [store-method-binding-parentheses](reference/store-method-binding-parentheses.md)

### State Patterns
- Filters reset on refresh or can't be shared → See [state-url-for-ephemeral-filters](reference/state-url-for-ephemeral-filters.md)
- Building production app without DevTools or conventions → See [state-use-pinia-for-large-apps](reference/state-use-pinia-for-large-apps.md)

## Guardrails

- Do not destructure store state directly when it must stay reactive; use `storeToRefs`.
- Do not put durable business truth only in frontend state.
- Do not make Pinia a cache for data that must be revalidated by backend APIs.
