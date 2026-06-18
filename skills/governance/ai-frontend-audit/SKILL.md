---
name: ai-frontend-audit
description: "Audit frontend availability, state handling, API integration, component reuse, accessibility, loading/empty/error states, performance, and user-facing readiness. Use before PRs, screenshots, releases, or when a page exists but may not be usable."
---

# ai-frontend-audit — Frontend Quality & Availability Auditor

## Purpose | 用途

Systematically audit frontend module quality across all critical dimensions:

- **Availability**: Does every menu item and route render without error?
- **Completeness**: Are all declared fields present and functional?
- **Consistency**: Do pages follow the design system uniformly?
- **Performance**: Load time, rendering issues, blocking operations
- **Error States**: Loading, empty, error, and edge cases handled
- **Accessibility**: Keyboard navigation, screen reader, contrast

This skill is for **frontend quality audit**, not feature implementation or code review alone.

---

## Audit Dimensions | 审计维度

### 1. Availability (P0)
Every route and menu item must render without console errors.
- [ ] All menu items navigate to correct routes
- [ ] No blank pages or unhandled routing errors
- [ ] No console errors on initial render
- [ ] Auth/permission gating works correctly

### 2. Completeness (P0)
All declared fields, actions, and features must be functional.
- [ ] All form fields render and accept input
- [ ] All buttons trigger correct actions
- [ ] All table columns display data correctly
- [ ] All dropdowns/selectors populate with options
- [ ] Search/filter functionality works

### 3. Consistency (P1)
Pages should follow the same patterns across the application.
- [ ] Consistent toolbar/filter/table/form layout
- [ ] Consistent button placement (primary/secondary)
- [ ] Consistent form validation behavior
- [ ] Consistent loading indicators
- [ ] Consistent empty state displays

### 4. Performance (P1)
Pages should load and respond within acceptable thresholds.
- [ ] Initial page load < [threshold]ms
- [ ] No blocking synchronous operations
- [ ] Large lists use virtualization
- [ ] Images and assets are optimized

### 5. Error States (P1)
All states should be handled gracefully.
- [ ] Loading state shown during data fetch
- [ ] Empty state shown when no data exists
- [ ] Error state shown with retry option when fetch fails
- [ ] Form validation errors displayed inline
- [ ] Network error recovery handled

### 6. Accessibility (P2)
Basic accessibility should be maintained.
- [ ] Keyboard navigation works for primary actions
- [ ] Form inputs have associated labels
- [ ] Color contrast meets WCAG AA minimum
- [ ] Focus indicators visible

---

## Audit Output Format | 审计输出格式

```markdown
## Frontend Audit Report: [Module Name]

### Summary
| Total Pages | Pass | Warn | Fail | P0 Issues | P1 Issues | P2 Issues |
|---|---|---|---|---|---|---|
| [N] | [N] | [N] | [N] | [N] | [N] | [N] |

### Page-Level Results
| Page | Route | Availability | Completeness | Consistency | Performance | Error States | Accessibility |
|---|---|---|---|---|---|---|---|
| [Name] | [Route] | ✅ | ✅ | ⚠️ | ✅ | ❌ | ⚠️ |

### Issue Details
| # | Page | Severity | Dimension | Description | Fix Recommendation |
|---|---|---|---|---|---|
| 1 | [Page] | P0 | Completeness | Missing validation | Add required validator |
| 2 | [Page] | P1 | Performance | Slow load (3.2s) | Add pagination, lazy load |
```

---

## Standard Workflow | 标准工作流

1. **Inventory**: List all pages/routes in scope
2. **Crawl**: Open each page in browser, verify render
3. **Inspect**: Check console for errors, network for performance
4. **Compare**: Check consistency against design system reference pages
5. **Score**: Assign severity (P0/P1/P2) to each finding
6. **Report**: Produce structured audit report with fix recommendations

---

## Guardrails | 防护规则

- Do not audit from code alone — open actual pages in browser
- Do not mark a page as "available" if it throws console errors
- Do not skip empty/error state verification
- Do not treat "looks okay" as a pass — verify with real data
- Do not audit without a reference (design system standard page)

## Maturity | 成熟度

**Stage**: Effective — Validated on enterprise ERP frontend audits across 50+ page types with 6 audit dimensions.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-frontend-availability-audit
- v1.1.0: Generalized with universal frontend quality dimensions
