# `ai-single-truth-enforcer` — 唯一真相源治理

> **源文件**：skills/governance/ai-single-truth-enforcer/SKILL.md
> **源版本**：未标注（源文件 `## Evolution History` 最新记录为 v1.0.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-single-truth-enforcer
description: "Enforce backend-owned truth, single source of business logic, no duplicate computation, correct notification severity, and no silent failures. Use for frontend/backend splits, validation, calculations, permissions, status transitions, and shared business rules."
```

**中文描述**：强制「真相归后端所有、业务逻辑只有一个来源、禁止重复计算、通知分级正确、无静默失败」。用于前后端职责切分、校验、计算、权限、状态流转与共享业务规则的场景。

---

## Purpose | 用途

强制一条根本规则：**前端展示，后端决策（frontend displays, backend decides）**。每一条业务逻辑、每一次校验、每一次计算、每一次数据变换都必须落在后端。前端是渲染层——仅此而已。

**它解决的问题**：智能体频繁把业务逻辑写进 Vue 组件、在 JavaScript 里算价格、只在客户端校验表单数据，并把数据变换和渲染混在一起。这会造出脆弱的前端：同一套逻辑要跑到移动端、微信或 MCP 上时就崩。

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

**中文对照**：`frontend = display only`（前端纯展示），后端是唯一真相源。**禁止**在 UI 里做计算、校验、变换或决策；**必须**只做取值、展示、回传。

---

## Rule 1: Zero Business Logic in Frontend | 前端零业务逻辑

### What Belongs EXCLUSIVELY in Backend | 只属于后端的事项

| 关注点 | 后端职责 | 前端禁止（Must NOT） |
|---|---|---|
| **计算（Calculations）** | 价格计算、税、折扣、合计 | `computed(() => price * quantity)` |
| **校验（Validation）** | 业务规则（信用额度、库存检查、重复检测） | `if (amount > 10000) show error` |
| **数据变换（Data transformation）** | 格式化、单位换算、区域化格式 | 带业务逻辑的 `date.toLocaleDateString()` |
| **授权（Authorization）** | 权限检查、基于角色的访问 | `v-if="user.role === 'admin'"`（应使用后端返回的权限） |
| **状态机（State machines）** | 订单状态、工作流流转 | `if (status === 'pending' && user pressed...)` |
| **业务决策（Business decisions）** | 依据状态决定显示哪些字段 | 前端依据后端状态标记做条件渲染 |

### How Frontend Should Work | 前端应当怎么写

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

### What Frontend MAY Do | 前端可以做什么

- 依据后端返回的数据做 `v-if`（不是本地计算出来的条件）
- 用 `v-for` 遍历后端返回的数组
- 基础 UI 格式化：`toLocaleDateString()` 仅用于展示（**禁止**用于计算）
- 事件绑定：`@click="save()"` → 把数据发给后端 API
- 客户端路由与导航

---

## Rule 2: Single Source of Data Truth | 数据唯一真相

### Hierarchy | 层级

```
Level 1: DATABASE       ← Ultimate truth (canonical values)
Level 2: BACKEND API    ← Computed truth (prices, statuses, permissions)
Level 3: FRONTEND STATE ← Display copy only, never the authority
```

**中文对照**：`Level 1: DATABASE` 是终极真相（权威取值）；`Level 2: BACKEND API` 是计算真相（价格、状态、权限）；`Level 3: FRONTEND STATE` 只是展示副本，永远不是权威。这就是 `single source of truth`（唯一真相源）在前端语境下的落地方式。

### Violations Detected by This Skill | 本 Skill 检出的违规

| 违规 | 检出模式 |
|---|---|
| 前端计算价格 | `computed(() => ... * ...)` 中出现业务取值 |
| 前端校验业务规则 | `.vue` 文件里出现 `if (quantity > stockLevel)` |
| 重复真相源 | 同一字段在 2 个以上组件中定义且逻辑不同 |
| 前端在展示前改写数据 | `.map(item => ({ ...item, displayPrice: item.price * rate }))` |

---

## Rule 3: Notification Severity Policy | 通知分级策略

**这就是你要问的那条规则**：通知必须匹配其严重度。不能再出现「需要确认 → 闪一个轻提示就没了」。

**分级速记**：`P0=Modal`、`P1=Banner`、`P2=Toast`、`P3=Console`。

### Severity → Notification Type | 严重度 → 通知类型

| 级别 | 名称 | 通知形式 | 示例 | 用户动作 |
|---|---|---|---|---|
| **P0** | Critical / Destructive（关键／破坏性） | 带标题 + 正文 + 确认/取消按钮的 **Modal dialog** | 删除全部数据、变更套餐、不可逆操作 | 显式确认或取消 |
| **P1** | Important / Actionable（重要／需处理） | 带操作按钮的 **Persistent banner** 或 **Modal** | 支付失败、会话过期、权限被拒 | 用户必须确认或处理 |
| **P2** | Informational / Success（信息／成功） | 带可选撤销的 **Toast**（4-6 秒自动消失） | 保存成功、文件已上传、设置已更新 | 可选：超时前撤销 |
| **P3** | Debug / Transient（调试／瞬时） | **Console log only** 或静默 | API 调用成功、缓存已更新 | 无需动作 |

### Anti-Patterns (Seen in Your Project) | 反模式（在你的项目中出现过）

| ❌ 错误 | ✅ 正确 |
|---|---|
| 删除确认做成一闪就没的轻提示 | 删除确认做成带显式「Delete」按钮的模态框 |
| 保存错误只闪一下 | 保存错误做成带「Retry」的常驻横幅 |
| 保存成功用模态框挡住整屏 | 保存成功用轻提示并自动消失 |
| 表单每个字段一变就弹「确定吗？」 | 只对破坏性或高代价操作做确认 |

### Implementation Check | 实现检查

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

本 Skill 审计前端代码的以下各项：

- [ ] 零个带业务公式的 `computed()`（价格、税、折扣、合计）
- [ ] 零个带业务规则的 `if/else`（信用额度、库存检查、资格判定）
- [ ] 所有校验调用都走后端 API，而不是本地函数
- [ ] 所有数据变换都在后端完成后再发给前端
- [ ] 权限检查使用服务端返回的权限，而不是本地角色字符串
- [ ] 删除/破坏性操作使用模态框确认，绝不使用轻提示
- [ ] 保存错误使用常驻通知，绝不使用一闪而过的提示
- [ ] 成功事件使用轻提示（P2），不使用模态框

---

## Integration | 集成

| Skill | 它如何使用 ai-single-truth-enforcer |
|---|---|
| `ai-frontend-audit` | 把「前端含业务逻辑」检测加入审计维度 |
| `ai-atomic-architect` | 强制：核心业务逻辑与传输层隔离 |
| `ai-runtime-verify` | 在浏览器测试中检查通知分级模式 |
| `ai-component-standardizer` | 模板强制纯展示（display-only）模式 |

---

## Guardrails | 防护规则

- **能在后端做的，必须（MUST）在后端做**
- **前端状态是缓存，永远不是权威**
- **通知匹配严重度：关键用模态框、信息用轻提示、调试用控制台**
- **`no silent failures`（无静默失败）：每个错误都必须以正确的严重度暴露给用户**
- **一个概念一个真相：禁止在两地重复计算同一个业务取值**

## Maturity | 成熟度

**Stage**: New — 提炼自真实 AI 开发事故：前端承载业务逻辑，导致多平台重写成本。

## Evolution History | 进化记录

- v1.0.0: 初始创建 —— 3 条规则（零逻辑、单一真相、通知分级）、审计清单、集成关系

---

## 译注

1. **源版本未标注**：源文件头部只有 `name` 与 `description` 两个 frontmatter 字段，无版本号或日期，故「源版本」记为「未标注」，并以 `## Evolution History` 最新记录作为参考。
2. **通知分级速记**：源文件的四行表格本身未写成 `P0=Modal` 形式，为对齐 `AGENTS.md` 第 6 节第 6 条的固定写法，译文在 `## Rule 3` 开头补一行速记 `P0=Modal`、`P1=Banner`、`P2=Toast`、`P3=Console`；表格内容逐行照译，未改变语义。
3. **未做颜色字面量改写**：源文件不含颜色字面量，无示例需要改写。
4. 代码块（含 `The Prime Directive` 的 ASCII 框与两段 `javascript` 示例）按原文原样复制，仅在其后补中文对照说明。
