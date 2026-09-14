# `ai-foundation-governor` — 稳定基座与唯一真相源治理（Stable Foundation & Single Source of Truth Governor）

> **源文件**：skills/core/ai-foundation-governor/SKILL.md
> **源版本**：未标注（源文件 frontmatter 无版本字段；进化记录最新条目为 v1.2.0）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-foundation-governor
description: "Govern stable project foundations including version control, permissions, routes, feature switches, menus, API contracts, configuration ownership, release gates, and single-source platform rules. Use when foundational behavior or shared project infrastructure changes."
```

**中文描述**：治理项目稳定的基座层，包括版本控制、权限、路由、功能开关、菜单、API 契约、配置归属、发布门禁与单一源平台规则。当基座行为或共享项目基础设施发生变更时使用。

---

## Purpose | 目的

治理项目稳定的基座层（foundation layer）—— 每个功能都依赖、但没有任何单一功能拥有的基础设施：

- 版本控制、模块/插件管理
- 权限系统、基于角色的访问控制
- 菜单/路由、统一导航
- API 标准化、统一登录/SSO
- 字段/元数据框架
- 系统/业务参数与配置
- 数据库模式（schema）治理（版本、迁移、种子）
- 运行时快照与编译后的 profile
- 发布门禁与证据收集

对触及**任何**基座层组件的任务，本 Skill 都是强制性的。基座一破，会级联到每个功能。

## Rule | 规则

**每项能力只有一个唯一真相源。缺失的闭环必须在给页面打补丁之前补齐。**

当根因在基座（权限、schema、参数、配置）时，**禁止**在表层（UI、API 端点）给功能打补丁。先分类，再修复。

---

## 1. Classify the Source of Truth | 真相来源分类

在修改任何基座组件之前，先对它的权威来源分类：

| 类别 | 典型真相源 | 核实方法 |
|---|---|---|
| 版本/模块/插件 | 包注册表、依赖清单 | 检查包管理器、授权项（entitlements） |
| 功能开关/切换项 | 功能开关服务、配置数据库 | 检查开关状态、灰度发布规则 |
| 权限/RBAC | 权限表、角色分配 | 核实角色-权限映射 |
| 认证/SSO | 身份提供方（identity provider）、令牌服务 | 检查认证中间件、令牌校验 |
| 字段定义 | 字段元数据注册表 | 核实字段 schema、约束 |
| 系统参数 | 参数/配置服务 | 读运行时配置与编译结果 |
| 业务参数 | 领域专用参数表 | 检查参数模板与校验 |
| 报表 | 报表服务、事实表（fact tables） | 核实报表查询与数据新鲜度 |
| 数据库模式（schema） | 迁移文件、schema 基线 | 检查正式脚本、租户 schema |
| 运行时 profile | 编译后的 AccessProfile、运行时策略 | 核实 profile 快照 |
| 审计/证据 | 审计日志、发布证据文档 | 检查审计轨迹完整性 |

**若一个任务无法分类，禁止写代码。先查文档、数据库与现有代码。**

---

## 2. Check Reality | 现实检查

在做出任何基座变更之前，执行「先检查后执行」协议：

| 检查项 | 方法 | 最低核实要求 |
|---|---|---|
| **数据库** | `SHOW TABLES`、`DESCRIBE`、`SELECT COUNT(*)` | 表存在，列与预期一致 |
| **数据库治理** | 核实变更属于 `schema/`、`seed/`、`patch/` 还是 `templates/` | 正式源目录正确 |
| **代码** | 定位 service/controller/interceptor 的消费方 | 改之前先弄清所有消费方 |
| **文档** | 读总控文档、发布文档 | 现有文档与本次改动不矛盾 |
| **运行时** | API 探测、浏览器检查、日志检查 | 运行中的系统与代码状态一致 |

**禁止**仅凭命名约定推断。必须对照真实的数据库表、真实的代码路径与真实的运行时行为来核实。

---

## 3. Backend Truth Rule | 后端真相规则

**业务真相必须存在于后端服务，而不是前端入口层。**

| 层 | 角色 | 允许的动作 |
|---|---|---|
| **后端应用服务（Backend application services）** | 真相源 | 校验、计算、持久化、回写 |
| **后端领域服务（Backend domain services）** | 领域逻辑 | 业务规则、不变式、状态流转 |
| **后端 atomic service（Backend atomic services）** | 单一职责操作 | 原子写入、事实记录 |
| **前端（Web/Mobile）** | 入口层 | 展示、采集输入、轻量预览 |
| **API 适配器 / AI 工具** | 入口层 | 格式转换、任务派发 |
| **外部集成** | 入口层 | 数据摄入、webhook 处理 |

**验收检查**：来自任何入口层的同一业务动作，必须产生完全一致的校验、持久化结果、回写行为与审计事实。

---

## 4. Release Gates | 发布门禁

每次发布必须通过两道最低门禁：

### DB Gate | DB 门禁

- 正式 schema 脚本位于正确的目录
- 基线 schema 与预期状态一致
- 必需的表、列、索引存在
- 关键种子行存在
- 系统/业务参数取值正确

### Core Flow Gate | 核心流程门禁

- 目标租户能完成认证并加载运行时 profile
- 核心页面无错误渲染
- 关键 API 端点响应正确
- 关键业务流程（新增、读取、更新、报表）可用
- 回写与审计轨迹完整

**DB 门禁通过而核心流程门禁失败，仍然构成发布阻断。**

---

### Database Migration Consistency Gate | 数据库迁移一致性门禁

对任何 schema、种子、参数基线或租户数据迁移，都要把迁移清单（migration manifest）与每个环境的执行注册表当作同一份发布契约：

| 检查项 | 必需的证明 |
|---|---|
| 清单身份（Manifest identity） | 迁移 id、版本、源路径、依赖/顺序与校验和（checksum） |
| 环境注册 | 测试/预发与生产的执行清单注册的是同一份预期迁移 |
| 安全性 | 幂等性、显式的替换/取代关系，或有文档记录的一次性前置条件 |
| 执行历史 | 目标环境记录状态、时间戳、操作者/作业与提交/版本 |
| 迁移后状态 | schema、种子、参数、运行时 profile 与租户范围检查通过 |
| 恢复 | 可回滚补丁、补偿迁移、备份，或显式的恢复决策 |

当某个迁移只存在于源代码里、只在一个环境注册而另一个环境没有、没有校验和/历史，或没有迁移后验证时，迁移门禁**失败即阻断（fail-closed）**。一次成功的部署作业**不能**替代这些检查。

## 5. Foundation Change Impact Checklist | 基础变更影响清单

在合并任何基础变更之前，逐项核实：

- [ ] 权限（Permissions）：RBAC 表、角色分配一致
- [ ] 菜单/路由（Menus/Routes）：导航结构完整
- [ ] API（APIs）：端点已注册，认证中间件生效
- [ ] 字段（Fields）：元数据注册表一致
- [ ] 参数（Parameters）：运行时编译成功
- [ ] Schema：迁移位于正确目录，基线已更新
- [ ] 迁移（Migrations）：清单、环境注册、校验和、执行历史与迁移后检查相互一致
- [ ] 报表（Reports）：查询引用正确的来源
- [ ] 租户（Tenants）：所有在用租户通过 schema 同步与租户范围隔离检查
- [ ] 发布文档（Release docs）：证据已收集

---

## Guardrails | 防护规则

- **禁止**未检查全部消费方就修改基座组件
- **禁止**为任何能力创建第二个真相源
- **禁止**因为改动「很小」就跳过 DB 门禁
- **禁止**把「在我机器上是好的」当作核心流程门禁通过
- **禁止**删除审计证据 —— 应当对它分类并提交

## Maturity | 成熟度

**Stage**：Effective —— 提炼自企业级 ERP 治理，含 65KB 已验证模式与发布门禁流程。

## Evolution History | 进化记录

- v1.0.0：提炼自 gerp-stable-foundation-governor（原始 65KB）
- v1.1.0：通用化为普适的企业级基座模式
- v1.2.0：加入失败即阻断（fail-closed）的跨环境迁移一致性门禁，覆盖清单、校验和、执行历史、迁移后检查与恢复证据
- 来源：12 个月以上的企业级 ERP 基座治理实践

---

## 译注

1. **源版本**：源文件 frontmatter 只有 `name`/`description` 两个键，未标注版本；本译文按「进化记录」最新条目注记 v1.2.0。
2. **引用路径存在性核对**（源文件引用的路径/脚本）：
   - `schema/`、`seed/`、`patch/`、`templates/`：源文件把它们作为「正式源目录」的类别名引用，不是本仓库路径。其中 `schema/`、`seed/` 在 `methodology/08_项目文件夹结构标准.md` 中被定义为项目 `database/` 下的子目录（`database/schema`、`database/seed`）；**`patch/`、`templates/` 在本仓库内未找到定义**（全仓库检索 `patch/` 仅命中本源文件自身），属源文件沿用历史项目的目录约定，采用时需按目标项目实际结构确认。
   - `SHOW TABLES`、`DESCRIBE`、`SELECT COUNT(*)`：SQL 命令，按口径原样保留。
   - `gerp-stable-foundation-governor`：源文件引用的历史 Skill 名（原始 65KB），当前 `skills/` 下已不存在该目录，属历史来源注记。
   - 全文未引用任何脚本或命令，故无脚本存在性风险。
3. **术语统一**：源文件小节标题自带中文「发布闸门」，按术语表（gate = 门禁，不译作「闸门」）统一为「发布门禁」，语义未变；`fail-closed` 按术语表统一为「失败即阻断（fail-closed）」并保留英文。
4. **强制语气**：`## 3. Backend Truth Rule` 的强制表述未弱化 —— 「业务真相**必须**存在于后端服务」「**验收检查**：……**必须**产生完全一致的校验、持久化结果、回写行为与审计事实」「**禁止**把入口层当作真相源」均按原强度译出；迁移门禁的「**失败即阻断（fail-closed）**」「成功的部署作业**不能**替代这些检查」同样保持原强度。
5. **术语保留自检**：本译文保留了 `atomic service`、`RBAC`、`SSO`、`AccessProfile`、`fail-closed`、`schema`、`seed`、`patch`、`templates`、`DB Gate`、`Core Flow Gate` 等英文标识符；源文件未出现 `atomic orchestration`、`aggregate interface`、`command gateway`、`Host`、`DeclarationAtom`、`ExecutorAtom`、`FieldPackage`、`BusinessProfile`、`L0`–`L5`、`Q0`–`Q3`、`P0`–`P3`，本译文不引入源文件没有的概念，这些标识符在术语表中仍保持英文写法。
