# `ai-frontend-audit` — 前端质量与可用性审计

> **源文件**：skills/governance/ai-frontend-audit/SKILL.md
> **源版本**：未标注（源文件 `## Evolution History` 最新记录为 v1.1.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-frontend-audit
description: "Audit frontend availability, state handling, API integration, component reuse, accessibility, loading/empty/error states, performance, and user-facing readiness. Use before PRs, screenshots, releases, or when a page exists but may not be usable."
```

**中文描述**：审计前端的可用性、状态处理、API 集成、组件复用、无障碍、加载/空/错误态、性能与面向用户的可交付程度。用于提 PR、截图、发布之前，或页面已存在但可能不可用的场景。

---

## Rule | 规则

前端审计**必须**：1）检查页面加载指标；2）运行无障碍审计；3）测试响应式断点；4）扫描控制台错误；5）与视觉基线比对。前端审计未通过，**禁止**部署。

# ai-frontend-audit — Frontend Quality & Availability Auditor | 前端质量与可用性审计器

## Purpose | 用途

跨全部关键维度系统性审计前端模块质量：

- **可用性（Availability）**：每个菜单项与路由是否都能无错渲染？
- **完备性（Completeness）**：所有声明字段是否都存在且可用？
- **一致性（Consistency）**：页面是否统一遵循设计系统？
- **性能（Performance）**：加载时间、渲染问题、阻塞操作
- **错误态（Error States）**：加载、空、错误与边界是否都已处理
- **无障碍（Accessibility）**：键盘导航、屏幕阅读器、对比度

本 Skill 面向**前端质量审计**，不是功能实现，也不等同于代码评审。

---

## Audit Dimensions | 审计维度

### 1. Availability (P0) | 可用性（P0）

每个路由与菜单项**必须**无控制台错误地渲染。

- [ ] 所有菜单项都导航到正确的路由
- [ ] 无空白页，无未处理的路由错误
- [ ] 首次渲染无控制台错误
- [ ] 认证/权限门禁工作正常

### 2. Completeness (P0) | 完备性（P0）

所有声明的字段、操作与功能**必须**可用。

- [ ] 所有表单字段都能渲染并接受输入
- [ ] 所有按钮都触发正确的动作
- [ ] 所有表格列都正确显示数据
- [ ] 所有下拉框/选择器都填充了选项
- [ ] 搜索/筛选功能可用

### 3. Consistency (P1) | 一致性（P1）

页面**应当**在应用范围内遵循同一套模式。

- [ ] 工具条/筛选/表格/表单布局一致
- [ ] 按钮位置一致（主/次）
- [ ] 表单校验行为一致
- [ ] 加载指示一致
- [ ] 空状态展示一致

### 4. Performance (P1) | 性能（P1）

页面**应当**在可接受的阈值内加载与响应。

- [ ] 首屏加载 < [threshold]ms
- [ ] 无阻塞式同步操作
- [ ] 大列表使用虚拟化
- [ ] 图片与资源已优化

### 5. Error States (P1) | 错误态（P1）

所有状态**应当**被优雅处理。

- [ ] 数据拉取期间显示加载态
- [ ] 无数据时显示空状态
- [ ] 拉取失败时显示错误态并提供重试
- [ ] 表单校验错误内联显示
- [ ] 网络错误可恢复

### 6. Accessibility (P2) | 无障碍（P2）

**应当**维持基础无障碍能力。

- [ ] 主要操作可用键盘导航
- [ ] 表单输入有关联的 label
- [ ] 颜色对比度达到 WCAG AA 下限
- [ ] 焦点指示可见

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

**中文对照**：审计报告固定为三张表——第一张 `### Summary`（总页数 / 通过 / 警告 / 失败 / P0 问题数 / P1 问题数 / P2 问题数）；第二张 `### Page-Level Results`（逐页 × 六个维度逐格打 ✅/⚠️/❌）；第三张 `### Issue Details`（序号 / 页面 / 严重度 / 维度 / 描述 / 修复建议），每条问题**必须**带 `P0`、`P1` 或 `P2` 严重度。

---

## Standard Workflow | 标准工作流

1. **盘点（Inventory）**：列出范围内的所有页面/路由
2. **爬取（Crawl）**：在浏览器中打开每个页面，确认渲染
3. **检查（Inspect）**：查控制台报错、查网络性能
4. **比对（Compare）**：对照设计系统参考页面检查一致性
5. **定级（Score）**：给每条发现分配严重度（`P0`/`P1`/`P2`）
6. **报告（Report）**：产出结构化审计报告与修复建议

---

## Guardrails | 防护规则

- **禁止**只看代码就下审计结论——**必须**在浏览器中打开真实页面
- 页面抛出控制台错误时，**禁止**标记为「可用」
- **禁止**跳过空状态/错误态验证
- **禁止**把「看起来还行」当作通过——**必须**用真实数据验证
- **禁止**在没有参考物（设计系统标准页）的情况下做审计

## Maturity | 成熟度

**Stage**: Effective — 在企业级 ERP 前端审计中经过 50+ 页面类型、6 个审计维度的验证。

## Evolution History | 进化记录

- v1.0.0: 提炼自 gerp-frontend-availability-audit
- v1.1.0: 泛化为通用前端质量维度

---

## 译注

1. **源版本未标注**：源文件头部只有 `name` 与 `description` 两个 frontmatter 字段，无版本号或日期，故「源版本」记为「未标注」，并以 `## Evolution History` 最新记录 v1.1.0 作为参考。
2. **H1 位置**：源文件中 `## Rule` 小节出现在 `# ai-frontend-audit — Frontend Quality & Availability Auditor` 标题之前。译文按本中文版固定结构把文档标题置于最前，并把源 H1 的中英对照保留在 `## Rule` 之后的同位置，正文各节顺序与源文件一致。
3. **六个审计维度的分级标注**：`### 1. Availability (P0)`、`### 2. Completeness (P0)`、`### 3. Consistency (P1)`、`### 4. Performance (P1)`、`### 5. Error States (P1)`、`### 6. Accessibility (P2)` 的 `P0`/`P1`/`P2` 标注原样保留，未做任何翻译或改写。
4. **颜色字面量**：`## Audit Output Format` 中的 ✅/⚠️/❌ 为 emoji 符号而非十六进制颜色字面量，按原文保留；译文未新增任何颜色字面量。
5. `## Audit Output Format` 的 `markdown` 报告模板与 `[threshold]ms`、`WCAG AA` 等标识符按原文原样复制，仅在其后补中文对照段。
