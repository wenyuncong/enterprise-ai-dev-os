// 中文版离线站点 · 浏览器运行时校验（Playwright）
//
// 做两件事：
//   1) 交互检查：默认首页、侧栏自动加载、中文/English/并排对照三视图、Skill 页、tech 摘要页、同步总览、全文搜索、站内链接
//   2) 全量逐页扫描：111 篇逐一渲染，检查一级标题、渲染完整度（渲染文本/原文）、横向溢出、英文侧内容、控制台错误
//
// 用法：
//   node 90_校验/verify_site_runtime.mjs --site site/index.html [--shots 90_校验/screenshots] [--json 90_校验/site_runtime_verify.json]
//
// Playwright 解析顺序：环境变量 PLAYWRIGHT_ROOT 指向含 node_modules 的目录 → 当前工作目录 → 已安装的 playwright 包。
// 若本机 playwright 与浏览器版本不匹配，脚本会依次尝试：msedge 通道 → 缓存的 chromium → 默认 chromium。

import { createRequire } from 'module';
import { pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';

const argv = process.argv.slice(2);
function arg(name, def) {
  const i = argv.indexOf('--' + name);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : def;
}
const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const sitePath = path.resolve(arg('site', path.join(here, '..', 'site', 'index.html')));
const shotDir = path.resolve(arg('shots', path.join(here, 'screenshots')));
const jsonOut = path.resolve(arg('json', path.join(here, 'site_runtime_verify.json')));

function loadPlaywright() {
  const roots = [process.env.PLAYWRIGHT_ROOT, process.cwd(), here, path.join(here, '..')].filter(Boolean);
  for (const r of roots) {
    try { return createRequire(path.join(r, 'noop.js'))('playwright'); } catch (e) { /* next */ }
  }
  try { return createRequire(import.meta.url)('playwright'); } catch (e) { /* fall through */ }
  throw new Error('未找到 playwright；请设置 PLAYWRIGHT_ROOT 指向含 node_modules 的目录。');
}
const { chromium } = loadPlaywright();
fs.mkdirSync(shotDir, { recursive: true });

const result = { site: '', checks: [], consoleErrors: [], problems: [], stats: {}, screenshots: [] };
// 报告里只写相对路径，避免把本机绝对路径写进交付物
const rel = (p) => { try { return path.relative(here, p).replace(/\\/g, '/') || '.'; } catch (e) { return p; } };
const ok = (name, pass, detail) => result.checks.push({ name, ok: !!pass, detail: String(detail === undefined ? '' : detail) });

const browser = await (async () => {
  const tries = [
    ['chromium + msedge channel', () => chromium.launch({ channel: 'msedge' })],
    ['cached chromium', () => chromium.launch({ executablePath: path.join(process.env.LOCALAPPDATA || '', 'ms-playwright', 'chromium-1217', 'chrome-win', 'chrome.exe') })],
    ['chromium default', () => chromium.launch()],
  ];
  const errs = [];
  for (const [name, fn] of tries) {
    try { const b = await fn(); result.browser = name; return b; } catch (e) { errs.push(name + ': ' + String(e).split('\n')[0]); }
  }
  throw new Error('无法启动浏览器：\n' + errs.join('\n'));
})();

const page = await browser.newPage({ viewport: { width: 1440, height: 950 } });
page.on('console', m => { if (m.type() === 'error') result.consoleErrors.push(m.text()); });
page.on('pageerror', e => result.consoleErrors.push('PAGEERROR ' + String(e)));
await page.goto(pathToFileURL(sitePath).href, { waitUntil: 'load' });
await page.waitForTimeout(400);

const shot = async (n) => { const p = path.join(shotDir, n); await page.screenshot({ path: p }); result.screenshots.push(rel(p)); };

// ---------- 交互检查 ----------
const h1 = (await page.locator('#doc h1').first().innerText()).trim();
ok('默认首页是白皮书', h1.includes('白皮书'), h1);
const navCount = await page.locator('nav a.item').count();
ok('侧栏自动加载 >=100 条', navCount >= 100, navCount);
const navSkills = await page.locator('nav a.item[data-doc*="50_Skill正文中文版"]').count();
ok('侧栏含 Skill 正文 >=40 条', navSkills >= 40, navSkills);
const base = await page.evaluate(() => ({
  tables: document.querySelectorAll('#doc table').length,
  pres: document.querySelectorAll('#doc pre').length,
  h2: document.querySelectorAll('#doc h2').length,
}));
ok('白皮书渲染出表格/标题', base.tables > 0 && base.h2 > 2, JSON.stringify(base));
await shot('01_home_zh.png');

await page.click('#m-cmp'); await page.waitForTimeout(300);
const cmp = await page.evaluate(() => ({
  on: document.getElementById('cmp').className === 'on',
  zh: document.querySelectorAll('#zh h2').length,
  en: document.querySelectorAll('#en h2').length,
  enLen: document.querySelector('#en').innerText.length,
}));
ok('并排对照两侧都有内容', cmp.on && cmp.zh > 0 && cmp.en > 0 && cmp.enLen > 500, JSON.stringify(cmp));
await shot('02_compare.png');

await page.click('#m-en'); await page.waitForTimeout(250);
const enOnly = await page.evaluate(() => document.querySelector('#doc').innerText.slice(0, 160));
ok('English 单栏渲染英文原文', /Enterprise|Methodology|Skill|Scope/i.test(enOnly), enOnly.replace(/\n/g, ' '));
await page.click('#m-zh');

const skillLink = page.locator('nav a.item[data-doc*="ai-5s-delivery-governor.md"]').first();
await skillLink.click(); await page.waitForTimeout(300);
const sk = await page.evaluate(() => ({
  h1: document.querySelector('#doc h1').innerText,
  tables: document.querySelectorAll('#doc table').length,
  meta: document.querySelector('#meta').innerText.replace(/\n/g, ' '),
}));
ok('Skill 页可打开且含章节对齐信息', /5s|5S/.test(sk.h1) && /章节/.test(sk.meta), sk.h1 + ' | ' + sk.meta.slice(0, 140));
await shot('03_skill_5s.png');

const techLink = page.locator('nav a.item[data-doc="tech/vue.md"]').first();
if (await techLink.count()) {
  await techLink.click(); await page.waitForTimeout(250); await page.click('#m-cmp'); await page.waitForTimeout(250);
  const t = await page.evaluate(() => ({ zh: document.querySelector('#zh').innerText.length, en: document.querySelector('#en').innerText.length }));
  ok('tech Skill 页（中文摘要 + 英文原文）', t.zh > 200 && t.en > 1500, JSON.stringify(t));
  await shot('04_tech_skill.png');
  await page.click('#m-zh');
} else ok('tech Skill 页存在', false, '未找到 tech/vue.md');

await page.click('nav a.item[data-doc="__overview__"]'); await page.waitForTimeout(300);
const ov = await page.evaluate(() => ({
  h1: document.querySelector('#doc h1').innerText,
  rows: document.querySelectorAll('#doc table tbody tr').length,
}));
ok('中英同步总览页可用', ov.h1.includes('同步总览') && ov.rows > 50, JSON.stringify(ov));
await shot('05_overview.png');

await page.fill('#q', '原子服务'); await page.waitForTimeout(450);
const sr = await page.evaluate(() => ({
  on: document.getElementById('results').className === 'on',
  hits: document.querySelectorAll('#results .res').length,
  marks: document.querySelectorAll('#results mark').length,
}));
ok('全文搜索可用且有高亮', sr.on && sr.hits > 5 && sr.marks > 0, JSON.stringify(sr));
await shot('06_search.png');
await page.fill('#q', ''); await page.waitForTimeout(200);

await page.click('nav a.item[data-doc="README.md"]'); await page.waitForTimeout(300);
const linkTest = await page.evaluate(() => {
  const a = document.querySelector('#doc a[data-doc]');
  if (!a) return null;
  const before = document.querySelector('#doc h1').innerText;
  a.click();
  return { before, target: a.getAttribute('data-doc') };
});
await page.waitForTimeout(350);
const after = await page.evaluate(() => document.querySelector('#doc h1').innerText);
ok('站内链接可在 SPA 内跳转', !!linkTest && after && after !== linkTest.before, JSON.stringify({ linkTest, after }));

// ---------- 全量逐页扫描 ----------
const ids = await page.evaluate(() => {
  const p = JSON.parse(document.getElementById('payload').textContent);
  return p.docs.map(d => ({ id: d.id, raw: d.zh.length, enLen: d.en.length }));
});
let zhText = 0, zhRaw = 0, enText = 0, enRaw = 0, tables = 0, pres = 0, enTables = 0, enDocs = 0;
for (const d of ids) {
  await page.evaluate(id => { const a = document.querySelector('nav a.item[data-doc="' + id + '"]'); if (a) a.click(); }, d.id);
  await page.waitForTimeout(20);
  const m = await page.evaluate(() => {
    const doc = document.getElementById('doc'), main = document.querySelector('main');
    return { h1: (doc.querySelector('h1') || {}).innerText || '', text: doc.innerText.length,
             tables: doc.querySelectorAll('table').length, pres: doc.querySelectorAll('pre').length,
             overflow: main.scrollWidth - main.clientWidth };
  });
  tables += m.tables; pres += m.pres; zhText += m.text; zhRaw += d.raw;
  if (!m.h1) result.problems.push({ id: d.id, why: '未渲染出一级标题' });
  else if (d.raw && m.text / d.raw < 0.55) result.problems.push({ id: d.id, why: '渲染文本偏少 ratio=' + (m.text / d.raw).toFixed(2) });
  if (m.overflow > 12) result.problems.push({ id: d.id, why: '横向溢出 ' + m.overflow + 'px' });
  if (d.enLen > 0) {
    await page.click('#m-cmp'); await page.waitForTimeout(15);
    const e = await page.evaluate(() => ({ en: document.getElementById('en').innerText.length, tables: document.querySelectorAll('#en table').length }));
    enText += e.en; enRaw += d.enLen; enTables += e.tables; enDocs++;
    if (e.en / Math.max(1, d.enLen) < 0.55) result.problems.push({ id: d.id, why: '英文侧渲染偏少 ratio=' + (e.en / d.enLen).toFixed(2) });
    await page.click('#m-zh'); await page.waitForTimeout(10);
  }
}
ok('全量逐页扫描无问题', result.problems.length === 0, '问题 ' + result.problems.length + ' 项');

result.stats = {
  docs: ids.length,
  tablesRendered: tables,
  codeBlocksRendered: pres,
  zhRenderedRatio: +(zhText / Math.max(1, zhRaw)).toFixed(3),
  enDocsChecked: enDocs,
  enTablesRendered: enTables,
  enRenderedRatio: +(enText / Math.max(1, enRaw)).toFixed(3),
  consoleErrors: result.consoleErrors.length,
  problems: result.problems.length,
  passed: result.checks.filter(c => c.ok).length,
  total: result.checks.length,
};
await browser.close();
fs.writeFileSync(jsonOut, JSON.stringify(result, null, 2), 'utf-8');
console.log('运行时校验：' + result.stats.passed + '/' + result.stats.total + ' 通过；控制台错误 ' +
  result.stats.consoleErrors + '；逐页问题 ' + result.stats.problems +
  '；中文渲染完整度 ' + result.stats.zhRenderedRatio + '；英文 ' + result.stats.enRenderedRatio +
  '；结果已写入 ' + jsonOut);
process.exit(result.stats.problems === 0 && result.stats.consoleErrors === 0 ? 0 : 1);
