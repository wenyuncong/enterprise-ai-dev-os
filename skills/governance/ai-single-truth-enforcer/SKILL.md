---
name: ai-single-truth-enforcer
description: "Enforce backend-owned truth, single source of business logic, no duplicate computation, correct notification severity, and no silent failures. Use for frontend/backend splits, validation, calculations, permissions, status transitions, and shared business rules."
---

# ai-single-truth-enforcer — Single Source of Truth Governor

## Purpose | 用途

Enforce the fundamental rule: **frontend displays, backend decides**. Every piece of business logic, every validation, every computation, every data transformation must live in the backend. The frontend is a rendering layer — nothing more.

**Problem it solves**: AI frequently writes business logic in Vue components, computes prices in JavaScript, validates form data only on the client, and mixes data transformation with rendering. This creates fragile UIs that break when the same logic needs to run on mobile, WeChat, or MCP.

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
| **Calculations** | Price computation, tax, discounts, totals | `computed(() => price * quantity)` |
| **Validation** | Business rules (credit limit, stock check, duplicate detection) | `if (amount > 10000) show error` |
| **Data transformation** | Formatting, unit conversion, locale formatting | `date.toLocaleDateString()` with business logic |
| **Authorization** | Permission checks, role-based access | `v-if="user.role === 'admin'"` (use backend-returned permissions) |
| **State machines** | Order status, workflow transitions | `if (status === 'pending' && user pressed...)` |
| **Business decisions** | Which fields to show based on state | Frontend conditional rendering from backend state flags |

### How Frontend Should Work

```javascript
// ❌ WRONG: Business logic in Vue component
const totalPrice = computed(() => {
  const subtotal = items.reduce((sum, i) => sum + i.price * i.qty, 0);
  const tax = subtotal * 0.13;
  const discount = user.vipLevel === 'gold' ? 0.1 : 0;
  return subtotal + tax - (subtotal * discount);
});

// ✅ CORRECT: Backend computes, frontend displays
const totalPrice = ref(0);
async function loadTotal() {
  const resp = await api.calculateTotal({ items: items.value });
  totalPrice.value = resp.total;  // Already computed by backend
}
```

### What Frontend MAY Do

- `v-if` based on data returned from backend (not computed locally)
- `v-for` to iterate backend-returned arrays
- Basic UI formatting: `toLocaleDateString()` for display only (never for computation)
- Event binding: `@click="save()"` → sends data to backend API
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
| Frontend computes prices | `computed(() => ... * ...)` with business values |
| Frontend validates business rules | `if (quantity > stockLevel)` in .vue |
| Duplicate truth sources | Same field defined in 2+ components with different logic |
| Frontend modifies data before display | `.map(item => ({ ...item, displayPrice: item.price * rate }))` |

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

```javascript
// ❌ WRONG: Critical action with transient toast
async function deleteAll() {
  await api.deleteAll();
  showToast('Deleted!');  // Gone in 3 seconds, user didn't confirm
}

// ✅ CORRECT: Critical action with modal confirmation
async function deleteAll() {
  const confirmed = await showModal({
    title: 'Delete All Records',
    body: 'This action is irreversible. All data will be permanently deleted.',
    confirmText: 'Delete All',
    confirmStyle: 'danger',
    cancelText: 'Cancel'
  });
  if (!confirmed) return;
  await api.deleteAll();
  showToast('All records deleted');
}
```

---

## Audit Checklist | 审计清单

This skill audits frontend code for:

- [ ] Zero `computed()` with business formulas (prices, taxes, discounts, totals)
- [ ] Zero `if/else` with business rules (credit limits, stock checks, eligibility)
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
