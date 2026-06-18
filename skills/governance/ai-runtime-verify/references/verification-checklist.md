# Runtime Verification Checklist | 运行时验证清单

> Companion reference for `ai-runtime-verify` skill.
> Use this checklist when manually reviewing verification results or extending the verification engine.

---

## P0: Must Pass (Blocking)

### 1. No Console Errors
- **Check**: `consoleErrors.length === 0`
- **Why**: Any uncaught JS error or console.error indicates broken code
- **Common causes**: Missing function definitions, undefined variables, API response parsing errors, React/Vue render errors
- **False positives**: Third-party analytics scripts, browser extension interference (filter if needed)

### 2. Loading Overlay Removed
- **Check**: No element matching `.loading-overlay.active`, `#loadingOverlay.active`, or similar
- **Why**: A stuck loading overlay means the page never finished initializing
- **Common causes**: Missing `renderCard`, missing `closeModal`, unhandled promise rejection in `render()`, API failure without error handling
- **Pattern to watch**: render() adds `.active` class but never removes it due to early return or exception

### 3. Core DOM Renders
- **Check**: Main content element visible with > 10 chars of text
- **Why**: An empty or hidden main area means the app shell rendered but content didn't
- **Common causes**: Empty API response with no empty state handling, routing failure, conditional rendering gone wrong

### 4. API Responses OK
- **Check**: No 4xx/5xx responses from API calls
- **Why**: Backend errors cascade to frontend failures
- **Common causes**: Missing API routes, database connection failure, schema mismatch, invalid query params

### 5. No White Screen
- **Check**: body textContent > 15 chars after whitespace normalization
- **Why**: A truly blank page means nothing rendered at all
- **Common causes**: Fatal JS error before DOM manipulation, CSS hiding everything, empty HTML template

### 6. No Infinite Refresh
- **Check**: Navigation count <= 5 during verification window
- **Why**: Refresh loops waste resources and make the page unusable
- **Common causes**: Router guard redirecting to itself, effect hook with missing dependency array, location.reload() in error handler

---

## P1: Should Pass (Warning)

### 7. Key Interactions Work
- **Check**: At least 1 clickable button found
- **Why**: A read-only page with no actions might be intentional, but usually indicates missing UI

### 8. Form Inputs Functional
- **Check**: At least 1 editable input accepts focus and fill
- **Why**: Forms that can't accept input are broken forms
- **Exception**: Read-only view pages may legitimately have no editable inputs

### 9. Tab Switching Works
- **Check**: If tabs exist, clicking non-active tab shows new content
- **Why**: Broken tab switching means half the UI is inaccessible
- **Exception**: Single-tab pages don't need tab switching

---

## P2: Nice to Have (Informational)

### 10. No Layout Overflow
- **Check**: No horizontal scrollbar at 1440px viewport width
- **Why**: Horizontal overflow suggests broken responsive design
- **Common causes**: Fixed-width elements > viewport, negative margins, absolute positioning without containment

### 11. No 404 Assets
- **Check**: All non-API resources load successfully
- **Why**: Missing CSS/JS/images degrade the experience
- **Common causes**: Wrong paths, deleted assets, build artifacts not deployed

---

## Interpreting Results

| Overall | P0 Status | Action |
|---|---|---|
| `passed: true` | All P0 passed | ✅ Page is runtime-verified. Proceed to "done" declaration. |
| `passed: false` | Any P0 failed | ❌ Page is broken. Fix P0 failures before claiming complete. |
| `passed: true` with P1 warnings | All P0 passed | ⚠️ Page works but has UX issues. Fix P1 warnings if time permits. |

---

## Extending the Verification Engine

To add a new check:
1. Add the check logic in `scripts/verify.js` inside the `try` block
2. Add the check to the appropriate array (`p0Checks`, `p1Checks`, or `p2Checks`)
3. Update this checklist with the new check description
4. Bump the skill version in `SKILL.md` Evolution History
