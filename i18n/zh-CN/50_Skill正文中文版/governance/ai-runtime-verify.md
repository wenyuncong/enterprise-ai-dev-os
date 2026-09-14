# `ai-runtime-verify` — 浏览器运行时验证

> **源文件**：skills/governance/ai-runtime-verify/SKILL.md
> **源版本**：未标注（源文件无版本字段；`## Evolution History` 最新记录为 v1.1.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-runtime-verify
description: "Verify runtime behavior with browser/API checks, console inspection, loading-state removal, DOM rendering, screenshots, logs, and structured evidence. Use before claiming code or page work is complete, especially for frontend and integration changes."
```

**中文描述**：用浏览器/API 检查、控制台检查、加载状态移除、DOM 渲染、截图、日志与结构化证据来验证运行时行为。在声称代码或页面工作完成之前使用，前端与集成类改动尤其如此。

---

## Rule | 规则

运行时验证必须：1) 执行真实代码路径；2) 捕获输出/错误/日志；3) 对照预期行为校验；4) 检查副作用（DB、文件、API）；5) 记录证据。**禁止**在没有运行时证明的情况下声称可用。

## Purpose | 目的

在声称开发完成之前，于真实浏览器中自动验证前端页面渲染正确。本 Skill 是**可由 AI 执行（AI-executable）**的——它运行无头浏览器（headless browser）检查，无需人工介入。

**它要解决的问题**：智能体经常仅凭静态代码分析就宣称「完成」，而页面可能存在运行时错误（`ReferenceError`、加载 spinner 卡死、白屏、无限刷新）。本 Skill 补上这个缺口。

## Trigger | 触发条件

- 每次前端代码改动之后（`src/**/*.html`、`src/**/*.vue`、`src/**/*.jsx`、`src/**/*.tsx`）
- 任何「done / complete / finished」声明之前
- `ai-frontend-audit` 完成其静态分析之后
- 服务重启或部署之后

## Verification Dimensions | 验证维度

### P0 —— 必须通过（失败即页面已损坏）| P0 — Must pass (page is broken if fails)

| 判据 | 验证内容 |
|---|---|
| **No console errors（0 控制台错误）** | `console.error` 或未捕获异常**必须**为零 |
| **Loading overlay disappears（加载遮罩已移除）** | 任何 `.loading-overlay.active` 或类似遮罩**必须**在超时内被移除 |
| **Core DOM renders（DOM 已渲染）** | 关键元素（`#app`、`#board`、主内容区）**必须**存在且可见 |
| **API responses OK** | 页面加载期间的 API 调用**禁止**出现 4xx/5xx 响应 |
| **No white screen** | body **必须**有可见文本内容，而不是一列空 div |
| **No infinite refresh** | 页面**禁止**循环刷新（检测连续导航） |

即：**浏览器必须 0 控制台错误、加载遮罩必须已移除、DOM 必须已渲染**——上述三条均为 `P0`，任一条失败即为页面损坏，**必须**修复后才能继续。

### P1 —— 应当通过（失败则体验降级）| P1 — Should pass (degraded experience if fails)

| 判据 | 验证内容 |
|---|---|
| **Key interactions work** | 主要 CTA 按钮可点击（未被禁用、未被遮挡） |
| **Form inputs functional** | 首个表单输入可获焦点并接受输入 |
| **Tab switching works** | 若存在标签页，切换标签页会更新内容 |
| **Network calls complete** | 所有 fetch/XHR 均完成且未挂起 |

### P2 —— 锦上添花 | P2 — Nice to have

| 判据 | 验证内容 |
|---|---|
| **No layout overflow** | 视口 <= 1920px 时无横向滚动条 |
| **Fonts loaded** | 系统字体或自定义字体正常渲染（无不可见文字） |
| **No 404 assets** | 所有 CSS/JS/图片均加载成功 |

---

## Usage | 使用方式

### AI Agent 调用本 Skill 的方式 | AI Agent invokes this skill by running:

```bash
node skills/governance/ai-runtime-verify/scripts/verify.js --url http://localhost:3000 --project-root . [--selector "#app"] [--timeout 15000]
```

### Output format | 输出格式

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

本 Skill 位于开发执行引擎（`methodology/03_12步开发执行引擎.md`）的 **Step 13**：

```
Step 11: Code Implementation   → AI writes code
Step 12: Static Audit          → ai-frontend-audit checks code quality
Step 13: Runtime Verify        → ai-runtime-verify checks browser behavior  ← THIS
Step 14: Mark Complete         → Only if Step 13 passes
```

**规则**：除非 `ai-runtime-verify` 在**最终相关前端或运行时改动之后**执行并返回 `passed: true`，AI 智能体**禁止（MUST NOT）**声称「开发完成」。此前的报告、健康检查端点或智能体报告都不证明当前行为。

---

## Guardrails | 防护规则

- 使用 `--project-root` 把证据 JSON 自动归档到 `docs/测试验收报告/` —— 这是任务完成证明

- 对真实运行中的服务执行，**禁止**对 mock 执行
- 明确要证明的具体断言，并在最终相关改动之后运行能证明它的检查
- `P0` 检查失败意味着页面已损坏——**必须**先修复再继续
- **禁止**忽略「轻微」控制台错误；每个错误都是真实缺陷
- 失败时截图以便调试
- 超时即失败——永不稳定的页面就是坏的

## Dependencies | 依赖

- Node.js >= 18
- `playwright` npm 包（并已安装 chromium 浏览器）
- 目标服务已运行且可访问

## Maturity | 成熟度

**Stage**：New —— 为填补静态审计与人工评审之间的缺口而创建。首次部署。

## Evolution History | 进化记录

- v1.1.0：新增 `--project-root` 自动归档到 `docs/测试验收报告/`，作为强制性的任务完成证据

- v1.0.0：初次创建 —— `P0`/`P1`/`P2` 验证维度、基于 Playwright 的无头验证
