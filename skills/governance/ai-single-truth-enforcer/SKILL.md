---
name: ai-single-truth-enforcer
description: "Enforce backend-owned truth, single source of business logic, no duplicate computation, correct notification severity, and no silent failures. Use for frontend/backend splits, validation, calculations, permissions, status transitions, and shared business rules."
metadata:
  requires:
    scope: universal
    declared-by: enterprise-ai-dev-os
---

# ai-single-truth-enforcer — Single Source of Truth Governor

## Purpose | 用途

Enforce the fundamental rule: **frontend displays, backend decides**. Every piece of business logic, every validation, every computation, every data transformation must live in the backend. The frontend is a rendering layer — nothing more.

**Problem it solves**: AI frequently writes business logic in presentation-layer components, computes prices on the client, validates form data only on the client, and mixes data transformation with rendering. This creates fragile UIs that break when the same logic needs to run on mobile, mini-programs, or MCP.

---

## The Prime Directive | 最高指令

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   FRONTEND = DISPLAY ONLY                                  │
│   BACKEND  = SOLE SOURCE OF TRUTH                          │
│                                                            │
│   Never: compute, validate, transform, or decide in UI     │
│   Always: fetch, display, send back                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Rule 1: Zero Business Logic in Frontend | 前端零业务逻辑

### What Belongs EXCLUSIVELY in Backend

| Concern | Backend Responsibility | Frontend Must NOT |
|---|---|---|
| **Calculations** | Amount computation, rates, adjustments, totals | a reactive derived value that multiplies business values |
| **Validation** | Business rules (limits, availability checks, duplicate detection) | a client-side branch that applies a business threshold |
| **Data transformation** | Formatting, unit conversion, locale formatting | a display-formatting call carrying business logic |
| **Authorization** | Permission checks, role-based access | hiding UI from a local role string (use backend-returned permissions) |
| **State machines** | Document status, workflow transitions | a local branch that advances a business state |
| **Business decisions** | Which fields to show based on state | conditional rendering driven by locally computed flags instead of backend state flags |

### How Frontend Should Work

The code below is stack-neutral pseudocode; map it to the project's actual frontend framework.

```text
// ❌ WRONG: Business logic in a presentation component
total = derived from items:
  subtotal = sum(item.amount * item.qty)
  rate = subtotal * configured rate
  adjustment = subtotal * tier-based adjustment
  return subtotal + rate - adjustment

// ✅ CORRECT: Backend computes, frontend displays
total = display-only state (initially empty)
on load:
  resp = api.calculateTotal({ items })
  total = resp.total   // already computed by backend
```

### What Frontend MAY Do

- Conditional rendering based on data returned from backend (not computed locally)
- Iterating backend-returned arrays
- Basic UI formatting for display only (never for computation)
- Event binding that sends data to the backend API
- Client-side routing and navigation

---

## Rule 2: Single Source of Data Truth | 数据唯一真相

### Hierarchy

```
Level 1: DATABASE       ← Ultimate truth (canonical values)
Level 2: BACKEND API    ← Computed truth (prices, statuses, permissions)
Level 3: FRONTEND STATE ← Display copy only, never the authority
```

### Violations Detected by This Skill

| Violation | Detection Pattern |
|---|---|
| Frontend computes amounts | a reactive derived value that combines business values |
| Frontend validates business rules | a client-side branch comparing a business quantity against a threshold |
| Duplicate truth sources | Same field defined in 2+ components with different logic |
| Frontend modifies data before display | transforming items to add a locally computed business value |

---

## Rule 3: Notification Severity Policy | 通知分级策略

**This is the rule you asked about**: notifications must match their severity. No more "confirmation needed → flashed toast and gone."

### Severity → Notification Type

| Level | Name | Notification | Example | User Action |
|---|---|---|---|---|
| **P0** | Critical / Destructive | **Modal dialog** with title + body + confirm/cancel buttons | Delete all data, change plan, irreversible action | Explicit confirm or cancel |
| **P1** | Important / Actionable | **Persistent banner** or **modal** with action button | Payment failed, session expired, permission denied | User must acknowledge or act |
| **P2** | Informational / Success | **Toast** (auto-dismiss 4-6s) with optional undo | Save successful, file uploaded, settings updated | Optional: undo within timeout |
| **P3** | Debug / Transient | **Console log only** or silent | API call succeeded, cache updated | None required |

### Anti-Patterns (Seen in Your Project)

| ❌ Wrong | ✅ Correct |
|---|---|
| Delete confirmation as a toast that disappears | Delete confirmation as modal with explicit "Delete" button |
| Save error flashes briefly | Save error as persistent banner with "Retry" |
| Successful save blocks the screen with modal | Successful save as toast, auto-dismiss |
| "Are you sure?" for every form field change | Only confirm for destructive or high-cost actions |

### Implementation Check

```text
// ❌ WRONG: Critical action with a transient toast
on deleteAll:
  await api.deleteAll()
  showToast('Deleted!')   // gone in seconds; user never confirmed

// ✅ CORRECT: Critical action with a modal confirmation
on deleteAll:
  confirmed = await showModal(
    title: 'Delete All Records',
    body: 'This action is irreversible. All data will be permanently deleted.',
    confirmText: 'Delete All', danger style,
    cancelText: 'Cancel')
  if not confirmed: return
  await api.deleteAll()
  showToast('All records deleted')
```

---

## Audit Checklist | 审计清单

This skill audits frontend code for:

- [ ] Zero reactive derived values with business formulas (amounts, rates, adjustments, totals)
- [ ] Zero client-side branches with business rules (limits, availability checks, eligibility)
- [ ] All validation calls go to backend API, not local functions
- [ ] All data transformations happen in backend before sending to frontend
- [ ] Permission checks use server-returned permissions, not local role strings
- [ ] Delete/destructive actions use modal confirmation, never toast
- [ ] Save errors use persistent notification, never flash-toast
- [ ] Success events use toast (P2), not modal

---

## Integration | 集成

| Skill | How it uses ai-single-truth-enforcer |
|---|---|
| `ai-frontend-audit` | Adds business-logic-in-frontend detection to audit dimensions |
| `ai-atomic-architect` | Enforced: core business logic isolated from transport layer |
| `ai-runtime-verify` | Checks notification patterns during browser testing |
| `ai-component-standardizer` | Templates enforce display-only patterns |

---

## Guardrails | 防护规则

- **If it can be done in backend, it MUST be done in backend**
- **Frontend state is a cache, never the authority**
- **Notifications match severity: modal for critical, toast for info, console for debug**
- **No silent failures: every error must surface to the user at the right severity**
- **One truth per concept: never compute the same business value in two places**

## Maturity | 成熟度

**Stage**: New — Extracted from real-world AI development failures where frontend contained business logic causing multi-platform rewrite costs.

## Evolution History | 进化记录

- v1.0.0: Initial creation — 3 rules (zero logic, single truth, notification severity), audit checklist, integrations
