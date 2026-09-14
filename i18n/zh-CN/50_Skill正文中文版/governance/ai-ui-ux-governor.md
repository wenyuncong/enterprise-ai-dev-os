# `ai-ui-ux-governor` — 企业级 UI/UX 设计系统治理

> **源文件**：skills/governance/ai-ui-ux-governor/SKILL.md
> **源版本**：未标注（源文件 `## Evolution History` 最新记录为 v1.0.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-ui-ux-governor
description: "Govern enterprise UI/UX density, zero-fluff wording, action semantics, states, hierarchy, usability, visual consistency, and design-system fit. Use when designing or reviewing ERP/SaaS/admin pages, forms, dashboards, reports, and operational workflows."
```

**中文描述**：治理企业级 UI/UX 的密度、零废话文案、操作语义、状态、层级、可用性、视觉一致性与设计系统契合度。用于设计与评审 ERP/SaaS/admin 页面、表单、看板、报表与操作工作流的场景。

---

## Purpose | 用途

治理企业应用跨页面的 UI/UX 一致性：

- 布局分类强制（list、form、report、workbench、settings）
- 密度与间距一致
- 状态处理（加载、空、错误、边界）
- 面向操作工具的行动优先表达
- 主题与令牌治理
- 性能 UX 标准

本 Skill 面向**设计系统治理**，不是像素级设计。它适用于 ERP、SaaS admin、运营看板以及任何数据密集型企业工具。

## Rule | 规则

**企业操作页是行动优先界面，不是营销页。**

**必须**把工具条、操作、状态指示与数据排在说明性文字之前。**必须**通过控件与结构表达业务含义——按钮、状态标签、流程链接——而不是散文段落。

---

## Layout Taxonomy | 页面布局分类

每个企业页面都落入以下类型之一。每种类型有规定的布局倾向：

| 页面类型 | 要求的布局 | 关键元素 |
|---|---|---|
| **List / History**（列表／历史） | filter bar + toolbar + table + batch actions + drilldown | 搜索、状态筛选、CRUD 操作、分页 |
| **Document / Form**（单据／表单） | header fields + line items + summary + pinned footer actions | 字段分组、校验、保存/提交操作 |
| **Report / Analytics**（报表／分析） | dimension tabs + default table + chart toggle + summary row | 筛选、下钻、导出 |
| **Workbench / Dashboard**（工作台／看板） | summary cards + todo list + quick actions | 聚合指标、快捷入口 |
| **Settings / Parameters**（设置／参数） | grouped fields + toggles + defaults + compact help | 配置、系统参数 |

**违规判定**：如果列表页出现 hero banner，或设置页出现多段解释文字，就是用了错误的布局模式。

---

## Zero-Fluff Rule | 零废话规则

对 ERP、SaaS admin 与运营工具，**必须**移除一切不直接帮助完成任务的文案：

| 删除 | 保留 |
|---|---|
| 欢迎语 | 字段标签 |
| 营销文案 | 校验规则 |
| 占位帮助文字 | 内联 tooltip |
| 「如何使用本页」区块 | 约束提示（如编码规则） |
| 功能描述 | 操作按钮 |
| 页面级教程 | 状态指示 |

**例外**：登录页与对外门户可以带简短的品牌/信任文案。该例外**不**扩展到内部操作页。

---

## State Handling | 状态处理

每个数据驱动视图**必须**显式处理四态：

| 状态 | 视觉 | 出现时机 |
|---|---|---|
| **Loading**（加载） | 稳定容器内的骨架屏或 spinner | 数据拉取进行中 |
| **Empty**（空） | 情境化空状态插画 + 可选 CTA | 不存在数据 |
| **Error**（错误） | 错误信息 + 重试动作 | 拉取或动作失败 |
| **Edge Cases**（边界） | 优雅处理 | 超长文本、空值、特殊字符 |

**规则**：ERP 表格**禁止**使用逐行加载骨架或错峰动画。整张表**必须**使用一个稳定的加载态。

---

## Density Standards | 密度标准

企业操作页**应当**默认使用紧凑密度：

| 元素 | 指导值 |
|---|---|
| 页面内边距 | ~4px |
| 区块间距 | ~3px |
| 工具条按钮高度 | ~26px |
| 表格操作按钮 | ~22px |
| 筛选/搜索按钮 | ~24px |
| 分页间距 | ~4-6px |

**页面外壳**（list、document、report 模板）**必须**通过共享令牌强制这些值，而不是页面级 CSS。

---

## Table Viewport Rule | 表格视区规则

每个数据表**必须**吃满可用的页面高度：

- 表体拥有纵向滚动
- 主要操作与分页钉在底部
- 底部顺序：横向滚动条 → 汇总行 → 分页
- 表格合计放在底部区域，并与列对齐
- **禁止**用悬空的右下角统计块替代与列对齐的合计

**验收**：验证四态——少行、多行、多列且带横向滚动、分页与汇总同时存在。

---

## Theme Governance | 主题治理

| 规则 | 细节 |
|---|---|
| **令牌驱动（Token-driven）** | 所有视觉取值来自 CSS 变量，**禁止**硬编码 |
| **禁止页面级覆盖** | **禁止**为品牌或主题令牌写页面级 CSS |
| **多主题测试** | 合并视觉变更前，**必须**验证所有受支持主题 |
| **滚动条一致性** | 滚动条样式**必须**使用主题令牌，**禁止**硬编码颜色 |

---

## Performance UX | 性能UX

可用性包含运行时流畅度：

| 规则 | 细节 |
|---|---|
| **分页优先** | 先做服务端分页，再加更多列 |
| **批量优于逐条** | 用批量 API 调用替代逐行请求 |
| **虚拟化** | 大列表（>100 行）使用虚拟滚动 |
| **禁止重复请求** | 加载/重试/轮询**禁止**产生并发请求 |
| **组件拆分** | 长表单拆分为编排、行表格、汇总 |

---

## Notification Severity Policy | 通知分级策略

每个面向用户的通知**必须**匹配其严重度级别。分级错误会摧毁信任并造成数据丢失。

**分级速记**：`P0=Modal`、`P1=Banner`、`P2=Toast`、`P3=Console`。

| 级别 | 名称 | UX 模式 | 自动消失 | 示例 |
|---|---|---|---|---|
| **P0** | Critical / Destructive（关键／破坏性） | 带确认/取消按钮的 **Modal** | 永不 | 删除全部记录、不可逆操作、套餐变更 |
| **P1** | Important / Action Required（重要／需处理） | **Persistent banner**，或带操作按钮的模态框 | 永不 | 支付失败、会话过期、同步错误 |
| **P2** | Informational / Success（信息／成功） | 带可选撤销的 **Toast** | 4-6 秒 | 保存成功、文件已上传、设置已保存 |
| **P3** | Debug / Transient（调试／瞬时） | Console 日志或静默 | 不适用 | 缓存已更新、埋点事件 |

### Anti-Patterns (Common AI Mistakes) | 反模式（智能体常见错误）

| ❌ 错误 | 分级错配 | ✅ 正确 |
|---|---|---|
| 删除全部之后 `showToast('Deleted')` | P0 动作 → P2 通知 | 模态框：「Delete 500 records? This cannot be undone.」 |
| `ElMessage.error('Save failed')` 一闪而过 | P1 动作 → P2 通知 | 常驻横幅：「Save failed. [Retry] [Details]」 |
| 每个输入都 `ElMessageBox.confirm('Field changed')` | P2 动作 → P0 通知 | 静默保存，或不做确认 |
| 表单校验错误用闪提示 | P1 → P2 | 字段下方内联错误，保持显示直到修复 |

### Implementation Contract | 实现契约

```typescript
// Every notification system must expose these:
interface NotificationAPI {
  modal(config: ModalConfig): Promise<boolean>;     // P0: returns user choice
  banner(config: BannerConfig): { dismiss(): void }; // P1: persistent, dismissable
  toast(config: ToastConfig): void;                  // P2: auto-dismiss
  debug(message: string): void;                       // P3: console only
}
```

**中文对照**：每个通知系统**必须**暴露这四个方法——`modal(config): Promise<boolean>`（P0，返回用户选择）、`banner(config): { dismiss(): void }`（P1，常驻可关闭）、`toast(config): void`（P2，自动消失）、`debug(message: string): void`（P3，仅写控制台）。

---

## Standard Workflow | 标准工作流

1. **给页面分类** —— 属于哪一类布局？
2. **找出违规** —— 零废话、密度、状态处理、表格视区
3. **核对密度** —— 测量值对照紧凑标准
4. **验证状态** —— loading、empty、error、边界情形
5. **提出改动建议** —— 增量的、基于共享组件的，**禁止**页面级重写

---

## Guardrails | 防护规则

- **禁止**用同一套布局模板套所有页面类型
- **禁止**用页面级 CSS 解决布局问题——**必须**修共享外壳
- **禁止**给 ERP 页面加装饰性文案（零废话规则）
- **禁止**在数据密集页面上为表格加载使用动画
- **禁止**在页面 CSS 中硬编码滚动条、hover 或主题颜色
- **禁止**为页面级品牌需求覆盖主题令牌

## Maturity | 成熟度

**Stage**: Effective — 提炼自 19KB 的企业级 ERP UI/UX 治理，含布局分类与密度标准。

## Evolution History | 进化记录

- v1.0.0: 提炼自 gerp-ui-ux（原始 19KB + 2 个参考）
- Source: 覆盖 50+ 页面类型的企业级 ERP UI/UX 治理

---

## 译注

1. **源版本未标注**：源文件头部只有 `name` 与 `description` 两个 frontmatter 字段，无版本号或日期，故「源版本」记为「未标注」，并以 `## Evolution History` 最新记录 v1.0.0 作为参考。
2. **代码围栏修复（1 处）**：`### Implementation Contract` 的代码块在源文件中围栏损坏——起始是单反引号加制表符再加 `ypescript`（本应写作 `typescript` 语言标注），结束为一枚孤立反引号。译文改为标准 ```typescript 围栏。这是排版修复，接口名、方法签名与注释一字未改。
3. **通知分级速记**：为对齐 `AGENTS.md` 第 6 节第 6 条的固定写法，译文在 `## Notification Severity Policy` 开头补一行速记 `P0=Modal`、`P1=Banner`、`P2=Toast`、`P3=Console`；表格逐行照译，未改变语义。
4. **未做颜色字面量改写**：源文件不含颜色字面量，`## Theme Governance` 中的滚动条与主题颜色要求以「主题令牌」表述译出，无示例需要改写。
5. 反模式表中的代码片段（`showToast(...)`、`ElMessage.error(...)`、`ElMessageBox.confirm(...)`、模态框与横幅文案）保持英文标识符与英文提示语原样。
