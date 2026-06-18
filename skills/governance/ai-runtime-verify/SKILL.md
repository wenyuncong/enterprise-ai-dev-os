---
name: ai-runtime-verify
description: "Verify runtime behavior with browser/API checks, console inspection, loading-state removal, DOM rendering, screenshots, logs, and structured evidence. Use before claiming code or page work is complete, especially for frontend and integration changes."
---

# ai-runtime-verify — Browser Runtime Verification

## Purpose | 用途

Automatically verify frontend pages render correctly in a real browser before claiming development complete. This skill is **AI-executable** — it runs headless browser checks without human intervention.

**Problem it solves**: AI frequently claims "done" based on static code analysis alone, but the page may have runtime errors (ReferenceError, loading spinner stuck, blank screen, infinite refresh). This skill closes that gap.

## Trigger | 触发条件

- After every frontend code change (`src/**/*.html`, `src/**/*.vue`, `src/**/*.jsx`, `src/**/*.tsx`)
- Before any "done / complete / finished" claim
- After `ai-frontend-audit` completes its static analysis
- After server restart or deployment

## Verification Dimensions | 验证维度

### P0 — Must pass (page is broken if fails)

| Check | What it verifies |
|---|---|
| **No console errors** | Zero `console.error` or uncaught exceptions |
| **Loading overlay disappears** | Any `.loading-overlay.active` or similar is removed within timeout |
| **Core DOM renders** | Key elements (`#app`, `#board`, main content area) exist and are visible |
| **API responses OK** | No 4xx/5xx responses from API calls during page load |
| **No white screen** | Body has visible text content, not just empty divs |
| **No infinite refresh** | Page does not reload in a loop (detect consecutive navigations) |

### P1 — Should pass (degraded experience if fails)

| Check | What it verifies |
|---|---|
| **Key interactions work** | Primary CTA buttons are clickable (not disabled/covered) |
| **Form inputs functional** | First form input can receive focus and accept input |
| **Tab switching works** | If tabs exist, switching between them updates content |
| **Network calls complete** | All fetch/XHR complete without hanging |

### P2 — Nice to have

| Check | What it verifies |
|---|---|
| **No layout overflow** | No horizontal scrollbar on viewport <= 1920px |
| **Fonts loaded** | System fonts or custom fonts render (no invisible text) |
| **No 404 assets** | All CSS/JS/images load successfully |

---

## Usage | 使用方式

### AI Agent invokes this skill by running:

```bash
node skills/governance/ai-runtime-verify/scripts/verify.js --url http://localhost:3000 --project-root . [--selector "#app"] [--timeout 15000]
```

### Output format:

```json
{
  "url": "http://localhost:3000",
  "passed": true,
  "checks": {
    "no_console_errors": { "passed": true, "details": "0 errors" },
    "loading_overlay_removed": { "passed": true, "details": "Removed after 320ms" },
    "core_dom_renders": { "passed": true, "details": "#board visible with 3 columns" },
    "api_responses_ok": { "passed": true, "details": "4/4 API calls returned 2xx" },
    "no_white_screen": { "passed": true, "details": "Page has visible content" },
    "no_infinite_refresh": { "passed": true, "details": "Page stable" }
  },
  "console_errors": [],
  "failed_api_calls": [],
  "screenshot": "/path/to/screenshot.png",
  "duration_ms": 2340
}
```

---

## Integration with Methodology | 方法论集成

This skill sits at **Step 13** in the development execution engine (`methodology/03_12步开发执行引擎.md`):

```
Step 11: Code Implementation   → AI writes code
Step 12: Static Audit          → ai-frontend-audit checks code quality
Step 13: Runtime Verify        → ai-runtime-verify checks browser behavior  ← THIS
Step 14: Mark Complete         → Only if Step 13 passes
```

**Rule**: An AI agent MUST NOT claim "development complete" unless `ai-runtime-verify` returns `passed: true`.

---

## Guardrails | 防护规则

- Use --project-root to auto-archive evidence JSON to docs/测试验收报告/ — this is the task completion proof


- Run against the actual running server, not a mock
- A failed P0 check means the page is broken — fix before proceeding
- Do not ignore "minor" console errors; every error is a real bug
- Screenshot on failure for debugging
- Timeout means failure — a page that never settles is broken

## Dependencies | 依赖

- Node.js >= 18
- `playwright` npm package (with chromium browser installed)
- Target server running and accessible

## Maturity | 成熟度

**Stage**: New — Created to fill the gap between static audit and human review. First deployment.

## Evolution History | 进化记录

- v1.1.0: Added --project-root auto-archive to docs/测试验收报告/ for mandatory task completion evidence

- v1.0.0: Initial creation — P0/P1/P2 verification dimensions, Playwright-based headless verification
