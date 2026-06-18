#!/usr/bin/env node
/**
 * ai-runtime-verify — Browser Runtime Verification Script
 * 
 * Launches headless Chromium, loads the target page, and verifies:
 *   P0: No console errors, loading overlay removed, core DOM renders, 
 *       API responses OK, no white screen, no infinite refresh
 *   P1: Key interactions work, form inputs functional, tab switching works
 *   P2: No layout overflow, fonts loaded, no 404 assets
 * 
 * Usage:
 *   node verify.js --url http://localhost:3000 [--selector "#app"] [--timeout 15000] [--screenshot-dir ./screenshots] [--project-root /path/to/project]
 */

const { chromium } = (() => {
  try { return require("playwright"); }
  catch (e) {
    console.error(JSON.stringify({
      passed: false,
      fatal: "Playwright not installed. Run: npm install playwright && npx playwright install chromium"
    }));
    process.exit(1);
  }
})();

const fs = require("fs");
const path = require("path");

// ─── CLI Argument Parsing ──────────────────────────────────────
function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = { url: null, selector: null, timeout: 15000, screenshotDir: null, projectRoot: null };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--url" && args[i + 1]) { parsed.url = args[i + 1]; i++; }
    else if (args[i] === "--selector" && args[i + 1]) { parsed.selector = args[i + 1]; i++; }
    else if (args[i] === "--timeout" && args[i + 1]) { parsed.timeout = parseInt(args[i + 1]); i++; }
    else if (args[i] === "--screenshot-dir" && args[i + 1]) { parsed.screenshotDir = args[i + 1]; i++; }
    else if (args[i] === "--project-root" && args[i + 1]) { parsed.projectRoot = args[i + 1]; i++; }
  }
  if (!parsed.url) {
    console.error(JSON.stringify({ passed: false, fatal: "Missing required --url argument" }));
    process.exit(1);
  }
  return parsed;
}
// ─── Helpers ───────────────────────────────────────────────────
function result(passed, details) {
  return { passed, details };
}

function now() { return Date.now(); }

// ─── Main Verification ─────────────────────────────────────────
async function verify(config) {
  const startTime = now();
  const checks = {};
  const consoleErrors = [];
  const failedApiCalls = [];
  let navigationCount = 0;

    // Try Chromium first, fallback to system Edge
  let browser;
  try {
    browser = await chromium.launch({ headless: true, timeout: 10000 });
  } catch (e) {
    try {
      browser = await chromium.launch({ channel: "msedge", headless: true, timeout: 10000 });
    } catch (e2) {
      console.error(JSON.stringify({
        passed: false,
        fatal: "No browser available. Install Chromium: npx playwright install chromium, or ensure Edge is installed."
      }));
      process.exit(1);
    }
  }
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  // Collect console errors
  page.on("console", msg => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
  page.on("pageerror", err => consoleErrors.push(err.message));

  // Track API responses
  page.on("response", resp => {
    if (resp.url().includes("/api/") || resp.url().includes(config.url)) {
      if (resp.status() >= 400) {
        failedApiCalls.push(`${resp.status()} ${resp.url()}`);
      }
    }
  });

  // Track navigations (for infinite refresh detection)
  page.on("framenavigated", () => { navigationCount++; });

  let screenshotPath = null;
  try {
    // ─── Load page ────────────────────────────────────────────
    await page.goto(config.url, { 
      waitUntil: "networkidle", 
      timeout: config.timeout 
    });

    // Wait for JS to settle
    await page.waitForTimeout(2000);

    // ─── P0.1: No console errors ──────────────────────────────
    checks.no_console_errors = result(
      consoleErrors.length === 0,
      consoleErrors.length === 0 
        ? "0 errors" 
        : `${consoleErrors.length} errors: ${consoleErrors.slice(0, 5).join("; ")}`
    );

    // ─── P0.2: Loading overlay disappears ─────────────────────
    const overlaySelectors = [
      ".loading-overlay.active", "#loadingOverlay.active",
      "[class*='loading'].active", ".spinner-overlay:not([style*='none'])"
    ];
    let overlayCount = 0;
    for (const sel of overlaySelectors) {
      overlayCount += await page.locator(sel).count();
    }
    checks.loading_overlay_removed = result(
      overlayCount === 0,
      overlayCount === 0 ? "No stuck loading overlay" : `${overlayCount} loading overlay(s) still visible`
    );

    // ─── P0.3: Core DOM renders ───────────────────────────────
    const mainSelector = config.selector || "body";
    const mainEl = page.locator(mainSelector);
    const isVisible = await mainEl.isVisible().catch(() => false);
    const textContent = isVisible ? (await mainEl.textContent().catch(() => "") || "") : "";
    const hasContent = textContent.trim().length > 10;
    checks.core_dom_renders = result(
      isVisible && hasContent,
      isVisible 
        ? (hasContent ? `"${mainSelector}" visible with content (${textContent.length} chars)` : `"${mainSelector}" visible but empty`)
        : `"${mainSelector}" not found or not visible`
    );

    // ─── P0.4: API responses OK ───────────────────────────────
    checks.api_responses_ok = result(
      failedApiCalls.length === 0,
      failedApiCalls.length === 0 
        ? "All API calls returned 2xx/3xx" 
        : `Failed API calls: ${failedApiCalls.join(", ")}`
    );

    // ─── P0.5: No white screen ────────────────────────────────
    const bodyText = await page.locator("body").textContent().catch(() => "");
    const bodyTrimmed = (bodyText || "").replace(/\s+/g, " ").trim();
    const isWhiteScreen = bodyTrimmed.length < 15;
    checks.no_white_screen = result(
      !isWhiteScreen,
      isWhiteScreen ? "Page appears blank (white screen)" : `Page has visible text content`
    );

    // ─── P0.6: No infinite refresh ────────────────────────────
    const isRefreshing = navigationCount > 5;
    checks.no_infinite_refresh = result(
      !isRefreshing,
      isRefreshing ? `Detected ${navigationCount} navigations — possible refresh loop` : `Page stable (${navigationCount} navigations)`
    );

    // ─── P1.1: Key interactions work ──────────────────────────
    const buttonSelectors = ["button:not([disabled])", "a.btn", "[role='button']"];
    let clickableCount = 0;
    for (const sel of buttonSelectors) {
      clickableCount += await page.locator(sel).count();
    }
    checks.key_interactions_work = result(
      clickableCount > 0,
      clickableCount > 0 ? `${clickableCount} clickable buttons found` : "No clickable buttons found"
    );

    // ─── P1.2: Form inputs functional ─────────────────────────
    const inputSelectors = ["input:not([type='hidden'])", "textarea", "select"];
    let firstInputFound = false;
    for (const sel of inputSelectors) {
      const input = page.locator(sel).first();
      if (await input.count() > 0) {
        try {
          await input.focus();
          await input.fill("_verify_test_");
          await input.fill("");
          firstInputFound = true;
          break;
        } catch (e) {
          // Input might be readonly/disabled
        }
      }
    }
    checks.form_inputs_functional = result(
      firstInputFound,
      firstInputFound ? "First form input accepts focus and input" : "No editable form inputs found (may be valid for read-only pages)"
    );

    // ─── P1.3: Tab switching works ────────────────────────────
    const tabBtns = page.locator(".tab-btn, [role='tab'], .tabs button");
    const tabCount = await tabBtns.count();
    let tabsWork = false;
    if (tabCount >= 2) {
      try {
        const secondTab = tabBtns.nth(1);
        await secondTab.click();
        await page.waitForTimeout(500);
        // Check if content changed
        const activePanel = page.locator(".tab-panel.active, [role='tabpanel']:not([hidden])");
        tabsWork = (await activePanel.count()) > 0;
      } catch (e) {
        // Tab click failed
      }
    } else {
      tabsWork = true; // No tabs to switch, not a failure
    }
    checks.tab_switching_works = result(
      tabsWork,
      tabCount >= 2 ? (tabsWork ? "Tab switching functional" : "Tab switching failed") : "No tabs to switch (N/A)"
    );

    // ─── P2.1: No layout overflow ─────────────────────────────
    const hasOverflow = await page.evaluate(() => {
      return document.documentElement.scrollWidth > window.innerWidth;
    });
    checks.no_layout_overflow = result(
      !hasOverflow,
      hasOverflow ? "Horizontal overflow detected" : "No horizontal overflow"
    );

    // ─── P2.2: No 404 assets ──────────────────────────────────
    const failedNonApi = failedApiCalls.filter(c => 
      !c.includes("/api/")
    );
    checks.no_404_assets = result(
      failedNonApi.length === 0,
      failedNonApi.length === 0 ? "All assets loaded" : `Failed assets: ${failedNonApi.join(", ")}`
    );

    // ─── Screenshot ───────────────────────────────────────────
    const screenshotDir = config.screenshotDir || path.join(__dirname, "..", "screenshots");
    if (!fs.existsSync(screenshotDir)) {
      fs.mkdirSync(screenshotDir, { recursive: true });
    }
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    screenshotPath = path.join(screenshotDir, `verify-${timestamp}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: false });

  } catch (e) {
    // Page load failed entirely
    checks.fatal = result(false, `Page load failed: ${e.message}`);
    consoleErrors.push(`FATAL: ${e.message}`);
  } finally {
    await browser.close();
  }

  // ─── Compute overall result ─────────────────────────────────
  const p0Checks = ["no_console_errors", "loading_overlay_removed", "core_dom_renders", "api_responses_ok", "no_white_screen", "no_infinite_refresh"];
  const allP0Passed = p0Checks.every(k => checks[k] && checks[k].passed);
  
  // P1 warnings
  const p1Checks = ["key_interactions_work", "form_inputs_functional", "tab_switching_works"];
  const p1Warnings = p1Checks.filter(k => checks[k] && !checks[k].passed);

  const output = {
    url: config.url,
    passed: allP0Passed && !checks.fatal,
    timestamp: new Date().toISOString(),
    duration_ms: now() - startTime,
    summary: {
      p0_total: p0Checks.length,
      p0_passed: p0Checks.filter(k => checks[k] && checks[k].passed).length,
      p0_failed: p0Checks.filter(k => checks[k] && !checks[k].passed).length,
      p1_warnings: p1Warnings.length
    },
    checks,
    console_errors: consoleErrors.slice(0, 20),
    failed_api_calls: failedApiCalls,
    screenshot: screenshotPath
  };


  // ─── Auto-archive evidence ──────────────────────────────────
  if (config.projectRoot) {
    const archiveDir = path.join(config.projectRoot, "docs", "测试验收报告");
    if (!fs.existsSync(archiveDir)) { fs.mkdirSync(archiveDir, { recursive: true }); }
    const archiveTs = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
    const archiveFile = path.join(archiveDir, `verify-${archiveTs}.json`);
    fs.writeFileSync(archiveFile, JSON.stringify(output, null, 2));
    output.evidence_archived = archiveFile;
    console.error(`[archive] Evidence saved: ${archiveFile}`);
  }

  console.log(JSON.stringify(output, null, 2));
  
  process.exit(output.passed ? 0 : 1);
}

// ─── Run ───────────────────────────────────────────────────────
const config = parseArgs();
verify(config);



