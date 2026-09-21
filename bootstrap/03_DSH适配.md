# DSH 适配设计 | DSH Adaptation Design

> **目标**：让 DSH（DeepSeek Harness）能**自动加载**项目规则、**自动执行**门禁、**自动创建**知识中心，并且**不把平台绑死在 DSH 上**。
> **实测依据**：DSH 安装目录（本机为 DeepSeek Harness 的 npm 安装包目录）是 npm 安装形态（`package.json` + `node_modules` + `start-dsh.cmd/ps1` + `upgrade-dsh.ps1`，依赖 `@deepseek-ai/dsh-*`），扩展缝为 `data/skills/`、`data/profiles/{web,headless}`、`data/settings.yaml`。
> **诚实标注**：本文标 ✅ 的是**实测确认**，标 ⚠️ 的是**待确认**（需要一次真机验证才能承诺）。

---

## 1. 接线图

```text
┌─────────────────────────── 项目（唯一真相） ───────────────────────────┐
│ AGENTS.md（短入口 ≤5KB）                                                │
│ project-profile.json   task-routing.json   gates.json                  │
│ rules/  skills/  docs/项目知识体系/  scripts/{py,ps1,ci}  .githooks/   │
└───────────────────────────────┬────────────────────────────────────────┘
                                │  ① 读取（内容层）
        ┌───────────────────────┴────────────────────────┐
        ▼                                                ▼
┌──────────────────────┐                     ┌──────────────────────────┐
│  DSH（执行引擎）      │                     │  CI / 服务端（强强制）    │
│  data/skills/ ✅      │                     │  .githooks + CI + 发布   │
│  data/profiles/ ✅    │                     │  ← 人绕不过去，模型也    │
│  settings.yaml ✅     │                     │    绕不过去              │
│  工具/钩子 ⚠️ 待确认   │                     └──────────────────────────┘
└──────────┬───────────┘
           │ ② 调用（执行层）
           ▼
┌─────────────────────────── 方法论工具层（5 个工具） ─────────────────────┐
│ route  precheck  gate  sync  knowledge                                │
│  ← 纯 stdlib / PowerShell 可执行；CLI 先行，MCP 为同一实现的第二个面   │
└───────────────────────────────────────────────────────────────────────┘
```

**关键顺序**：先把 5 个工具做成 **CLI**（不依赖任何 harness），再由 DSH 或任何其它引擎调用。这样"引擎可替换"不是口号，而是默认事实。

---

## 2. 四层适配

| 层 | 做什么 | 依据 | 备注 |
|---|---|---|---|
| **内容层** ✅ | 按 archetype/角色**裁剪**技能子集，落到 `data/skills/<skill>/`；项目画像与三件套放**项目内**，不复制进 DSH | `data/skills/` 是实测扩展缝（本会话加载的 40+ 技能即在此） | **禁止全量投放**：母版 47 技能 + 本仓库 49 技能全量注入会击穿上下文 |
| **组合层** ✅ | 一个 profile/bundle 按角色组合：`dsh.profile.bundles` | `data/profiles/headless/package.json` 的 bundle 组合机制 | 建议 profile：`methodology-backend` / `-frontend` / `-erp` / `-brownfield` |
| **执行层** ✅/⚠️ | 5 个工具（CLI 先行）+ 三挂点 | 工具原型已在本仓库跑通（见第 3 节） | 写入前自动拦截是否可行取决于 ⚠️ 钩子能力 |
| **模型层** ✅ | 国产模型适配是**配置**：`settings.yaml` 的 `llm-deepseek.models`、`agent-default-model{provider,model}`、`llm-pi-ai.providers` | `data/settings.yaml` 实测键名 | 适配结论用 M0–M3 验收，不用"感觉" |

### ⚠️ 必须确认的一点：DSH 是否开放"写前钩子"

> **2026-09-15 复核：已确认 ✅ —— DSH 开放写前钩子，但只到 shell 命令行粒度，且有一个会让门禁静默失效的坑。**
> 结论、证据与修法见 [§8 实测复核](#8-实测复核2026-09-15从--到-)；本节下面的 ⚠️ 判断已被实测取代，保留用于对照。

实测 `data/settings.yaml` 中**没有** `mcp` / `plugin` / `hook` 键。因此：

| 强制级别 | 落点 | 效果 |
|---|---|---|
| **弱强制**（DSH 内） | `precheck` 做成"必调工具" + 写入 `task-routing.json` 的 `pre_checks` + 完成判据要求提供证据路径 | 模型自律 + 结构约束；**能被绕开** |
| **强强制**（DSH 外） | `.githooks`（pre-commit / pre-push）+ CI + 服务端发布门禁 | **绕不过去**：不通过就无法提交/推送/发布 |

**结论**：在钩子能力确认之前，**强强制一律放 DSH 之外**——这也正是母版已经做对的事（`.githooks` 4 个 + 7 个 workflow + CI 门禁脚本）。

---

## 3. 五个工具签名

### 3.1 `route` —— 会话启动时算出"该加载什么"

```jsonc
// 输入
{ "task": "修复采购退货已记账单据的按钮不一致", "project_root": "<path>", "change_type": "B" }

// 输出
{
  "task_line": "bug",
  "lead_skill": "gerp-flow-closure-audit",
  "support_skills": ["ai-runtime-verify", "ai-single-truth-enforcer"],
  "risk_level": "L2",
  "first_documents": ["AGENTS.md", "docs/项目知识体系/02_业务手册/README.md"],
  "first_checks": ["搜索同类实现", "SHOW TABLES 核对现状"],
  "gates": ["G-DOC-STATUS-ACTION", "G-RUNTIME-REPLAY", "G-5S-CLOSE"],
  "boundary_warnings": ["不得端侧拼业务动作", "不得直改库"]
}
```
实现来源：`task-routing.json` + `project-profile.json`（本仓库已具备：`ai-rule-dispatcher` 的路由结果模板即其人工版）。

### 3.2 `precheck` —— 写文件前的静态拦截

```jsonc
// 输入
{ "paths": ["frontend/gerp-web/src/views/.../Detail.vue"], "change_type": "B", "project_root": "<path>" }

// 输出
{
  "allow": false,
  "violations": [
    { "rule": "frontend-no-business-action", "file": "...", "line": 334, "hint": "按钮集合必须来自后端动作画像" }
  ],
  "scope_escape": false,
  "evidence": "temp/precheck-20260914.json"
}
```
实现来源：`scripts/py/rule_lint.py`（本仓库）+ 母版的 `audit-document-*` 静态审计 + 交付契约的 `write_allowlist` 越界检查（本仓库 `validate_delivery_contract.py` 已有 `CONTRACT_SCOPE_ESCAPE`）。

### 3.3 `gate` —— 按门禁级别跑注册表

```jsonc
// 输入
{ "level": "L2", "changed_files": ["..."], "project_root": "<path>", "layers": ["static_audit","contract_test"] }

// 输出
{
  "pass": false,
  "results": [
    { "id": "G-CONTRACT-REGISTRY", "layer": "contract_test", "exit": 1, "evidence": "evidence/contract-20260914.json" }
  ],
  "fresh": true,
  "blocking_failures": ["G-CONTRACT-REGISTRY"]
}
```
实现来源：`gates.json` 驱动；对应本仓库的 `audit_methodology.py` / `check_constitution.py` / `rule_lint.py` 与母版的 `scripts/ci/*`、`scripts/ps1/enter|close-5s-*`。

### 3.4 `sync` —— 双语与方法论同步状态

```jsonc
// 输出
{ "synced": 114, "stale": ["20_方法论正文/07_方法论移植指南_中文版.md"], "missing": [], "site_built": true }
```
实现来源：本仓库 `i18n/zh-CN/90_校验/verify_cn_edition.py`（已实现哈希反查：改动过的英文源会精确列出需重同步的译文）。

### 3.5 `knowledge` —— 自动创建/校验知识中心

```jsonc
// 输入
{ "project_root": "<path>", "action": "build|check" }

// 输出
{ "pages": ["index.html", "business-flows.html", "architecture-map.html", "architecture-atlas.html"],
  "consistent": true, "changed": [] }
```
实现来源：母版 `scripts/py/generate_local_knowledge_center.py --check`、`generate_knowledge_subsites.py --check`、`scripts/ps1/open-local-knowledge-center.ps1`。

---

## 4. 三挂点：自动加载真正发生的地方

| 挂点 | 时机 | 调用 | 加载量 | 对应母版机制 |
|---|---|---|---|---|
| **挂点 1 会话启动** | 每条新会话/恢复会话 | `route` | **≤5 KB**：`project-profile.json` + 分支/远端状态 + 待办 + 路由索引 + 5S 接管指令 | 母版 `enter-5s-delivery-session.ps1 -Mode Inspect` + 短入口路由 |
| **挂点 2 写前** | 第一次触碰文件之前 | `precheck` | 命中规则切片 + 命中技能前 50 行 | 母版"低 token 启动规则"+"长规则读取边界" |
| **挂点 3 交付前** | 提交 / 推送 / 发布 | `gate` + `sync` + `knowledge` | 只跑注册表，不加载正文 | 母版 `close-5s-delivery-session.ps1` + `scripts/ci/*` |

**为什么这样切**：挂点 1 决定"读什么"，挂点 2 决定"能不能改"，挂点 3 决定"算不算完成"。三者都不需要把 700 KB 技能塞进上下文。

---

## 5. skills 裁剪与 profile 示例

**裁剪规则**（避免全量注入）：

| archetype | 投放技能 | 规模 |
|---|---|---|
| A 快速原型 | 路由 + 分解 + 技术栈（1–2 个） + 运行时验证 | ≤ 6 |
| B AI 原生 | core 16 + governance 13 中的常用 8 + 技术栈 3–5 | ≤ 20 |
| C 企业级 | 按角色分 profile（后端/前端/ERP/改造），每个 ≤ 12 | 按角色 |

**profile 示例**（`data/profiles/methodology-backend/package.json`）：

```json
{
  "name": "dsh-profile-methodology-backend",
  "private": true,
  "dependencies": {},
  "dsh": {
    "profile": {
      "bundles": ["@deepseek-ai/dsh-base", "@deepseek-ai/dsh-headless"],
      "skills": [
        "ai-rule-dispatcher", "ai-task-decomposer", "ai-delivery-contract-governor",
        "ai-single-truth-enforcer", "ai-runtime-verify", "ai-flow-closure-audit",
        "springboot-patterns", "mysql-best-practices", "java-springboot"
      ]
    }
  }
}
```
> `skills` 字段为**建议键名，需按 DSH 实际 profile 结构对齐**（⚠️ 待确认）。若 DSH 不支持在 profile 里声明技能，则在生成阶段把裁剪结果直接落到 `data/skills/`。

> **2026-09-15 复核：这个 profile 结构猜错了 ❌。** DSH 的 profile `package.json` 里**没有** `skills` 键；技能来自
> `@deepseek-ai/dsh-skill-filesystem` 的 `customSkillDirs`，且每个 root 必须是**一层**布局
> （`<root>/<name>/SKILL.md`）。本仓库是两层 `skills/<layer>/<name>/SKILL.md`，所以必须分别挂
> core / governance / tech 三个 root（见 `data/profiles/methodology/cordis.patch.yml`）。详见 §8.3。

---

## 6. 模型适配：M0–M3（对标 Q0–Q3）

| 级别 | 判据 | 测试方法 |
|---|---|---|
| **M0** | 能读规则并产出格式正确的文件 | 给 3 条规则，要求产出符合 schema 的文件 |
| **M1** | 能跑门禁并解释失败原因 | 故意注入一个已知违规，要求定位到具体门禁与修法 |
| **M2** | 对抗性测试下不漂移 | 给越界任务（例如"顺手把前端 fallback 加回来"），看是否拒绝并被门禁拦下 |
| **M3** | 无人干预完成 L2/L3 交付且留下**新鲜证据** | 端到端跑 `gate` + 证据路径检查 |

适配对象：DeepSeek / Qwen / GLM / Kimi / GPT / Claude，**同一套测试跑全部**，产出可发布的适配矩阵。母版当前的 `model_adaptation_level` 在 `project-profile.json` 里记为 `M1`（待实测复核）。

---

## 7. 落地检查清单（DSH 侧）

- [ ] ⚠️ 确认 DSH 是否支持第三方写前钩子；不支持则强强制全部落在 `.githooks` + CI
- [ ] ✅ 确认 `data/skills/` 的目录结构与加载规则（技能包需要哪些文件）
- [ ] ✅ 确认 `data/profiles/*/package.json` 是否支持声明技能清单
- [ ] 建立 `methodology-*` profile（后端/前端/ERP/改造）
- [ ] 5 个工具做成 CLI（`route/precheck/gate/sync/knowledge`），再暴露 MCP
- [ ] 用 M0–M3 测 3 家国产模型，产出适配矩阵
- [ ] 在母版上做一次**只读**回归：CLI 跑出的门禁结果与母版现有脚本一致

---

<a id="8-实测复核2026-09-15从--到-"></a>
## 8. 实测复核（2026-09-15）：从 ⚠️ 到 ✅

本节只写**跑出来过**的事实：每条结论后面都跟着复现命令或证据文件。凡是没能证实的，一律标「未验证」，不用推断补空。

### 8.1 结论速览

| 原设计判断 | 实测结论 | 证据 |
|---|---|---|
| ⚠️ DSH 是否开放写前钩子 | ✅ **开放**：`@deepseek-ai/dsh-hooks-codex` + `data/hooks.json`，5 个钩子点，`PreToolUse` 可阻断 | 模型执行 `Set-Content -Path temp\methodology-hook-probe.md` 被拦，文件未创建 |
| 「写前拦截」能覆盖到什么粒度 | ⚠️ **只到 shell 命令行**：载荷只有真实 `tool_name` 与 `tool_input.command`，非 shell 工具参数**不暴露**。按文件路径的写前拦截走 MCP 工具，或写原生插件（§8.5） | 见 §8.4 实测载荷 |
| ⚠️ 强强制必须放 DSH 之外 | ❌ **需要修正**：DSH 内已可做强强制（shell 粒度），但**必须**修掉退出码掩码这个坑（§8.2），否则是静默失效 | §8.2 |
| profile 里声明 `skills` 键 | ❌ **猜错了**：DSH 无此键，技能走 `skill-filesystem.customSkillDirs`，且 root 必须一层布局 | §8.3 |
| 5 个工具（route/precheck/gate/sync/knowledge） | ✅ 4 个已实现并真机调用（route/precheck/gate/sync）；⚠️ `knowledge` 未实现（它依赖母版的 knowledge-center 脚本，不在本仓库） | `scripts/py/methodology_mcp_server.py --selftest` |
| 工具先做 CLI、再暴露 MCP | ✅ 按此落地：`methodology_rules.py`（规则单点）→ `methodology_precheck_hook.py`（CLI/钩子）→ `methodology_mcp_server.py`（MCP 面） | 三个文件互不复制规则 |
| M0–M3 模型适配 | ⚠️ **未做矩阵**。只有一次非计划的对抗性观察：门禁拦下命令后，模型拒绝把「被拦截」谎报成「完成」，并请求授权路径 | §8.6 |

### 8.2 坑 1（最隐蔽）：PowerShell 把退出码 2 压成 1 → 门禁静默 fail-open

**现象**：钩子脚本明明判定为拦截（stderr 里已写出完整理由），命令却照常执行、文件照常创建；DSH 侧无任何报错。

**根因**：`dsh-hook-protocol` 只把**退出码 2** 当拦截，其它非零一律记为「钩子执行失败」并放行。而钩子经 `ctx.shell` 由 PowerShell 执行，`pwsh -Command "& python hook.py"` 会把原生命令的非零退出码**统一压成 1**：

```text
修前： GUARD-RUN name=pwsh exit=1  stderr="[methodology-precheck] 已拦截此 shell 调用…"   ← 理由有了，码丢了
修后： GUARD-RUN name=pwsh exit=2  stderr="[methodology-precheck] 已拦截此 shell 调用…"   ← 拦截生效
```

**修法**：命令末尾必须补 `; exit $LASTEXITCODE`：

```json
"command": "& \"<python>\" \"<project-root>/scripts/py/methodology_precheck_hook.py\"; exit $LASTEXITCODE"
```

**回归测试**：`scripts/py/test_methodology_guard.py::PowershellExitCodeContract` 同时锁住正反两面（有后缀=2；无后缀≠2）。**这个坑值得记住**：它不会报错，只会让所有门禁变成装饰。

### 8.3 坑 2：patch 只能改、不能加；要加必须用 `insert:`

`cordis.patch.yml` 的一个条目里：

| 写法 | 语义 |
|---|---|
| `- id: <base 里已有的 id>` + 字段 | **覆盖/修改**该条目 |
| `- id: <base 里没有的 id>` + 字段 | ⚠️ 只打一条 `warn: patch: entry "X" not found`，**然后静默忽略** |
| `- insert: [ {id, name, config}, … ]` | **真正新增**条目（无 id 时追加到顶层） |

早先按「直接写 id」的方式接 MCP 与钩子，两条都没进配置——`--dump-config` 是唯一能一眼看出的办法。

### 8.4 坑 3：Windows 下 Python 的 stdio 默认不是 UTF-8

`sys.stdout.encoding` / `sys.stdin.encoding` 在简体中文机上是 **gbk**。而 MCP stdio 传输与钩子载荷都是 UTF-8 字节。后果分两个方向：

- **出站**：服务端按 GBK 写、客户端按 UTF-8 读 → 模型看到乱码 `���ж����յȼ�`；
- **入站**：中文 task 被按 GBK 解坏 → `methodology_route` 对中文关键词**匹配失败**，返回 `matched_route_id: null`。

**最危险的不是乱码本身，而是模型的反应**：它照着乱码**编造**了一个不存在的路径 `bootstrap/02_方法论落地`（真实目录是 `02_机读三件套`），并且语气完全肯定。乱码会诱发幻觉。

**修法**：`methodology_rules.force_utf8()` 把三流钉死为 UTF-8（stdout/stderr 额外 `newline="\n"` 保证 JSON-RPC 恰好用 LF 分帧），MCP 服务与钩子都调用它。修后 `matched_route_id` 从 `null` 变成 `route-business-flow`，`_source` 是磁盘上真实存在的路径。

### 8.5 坑 4：cordis 的服务访问必须先 `inject`，否则整棵树加载失败

cordis 的 `inject` 不只是「等依赖就绪」，还是**访问白名单**：插件访问任何未在 `inject` 里声明的服务，`apply` 直接抛错，并且这个错是**致命的**——整棵插件树加载失败、DSH 起不来：

```text
Error: dsh: plugin tree failed to load: failed to apply loader entry probe-watch:
       cannot get property "shell" without inject
```

旁证：`dsh-hooks-codex` 的 `inject = ["shell", "sessionProjections"]`，`dsh-mcp-client` 是 `["tools"]`——两者都满足，所以都能激活。

**原生插件可行性（已实测）**：

- 本地插件包放在 `$DSH_HOME/profiles/<profile>/node_modules/<pkg>/`，用**裸包名**引用即可加载（`name: 'methodology-probe'`）✅；
- 用 `file:///…` 绝对 URL 作为 `name` 会让启动**直接崩** ❌；
- 原生拦截点是 `ctx.on("tools/pre-execute", async (exec, next) => …)`，拒绝时返回 `{ kind: "deny", reason }`；
- **关键差别**：原生插件拿得到 `exec.arguments` 的**完整参数**，实测 `write` 调用带 `{file_path, content}`、`read` 带 `{file_path, limit}`、`pwsh` 带 `{command, description, workdir}`。**所以「按写入路径拦截」只能靠原生插件，Codex 桥接做不到**——这是下一步该做的层。

### 8.6 落地物与复现命令

| 层 | 文件 | 自检/复现 |
|---|---|---|
| 规则单点 | `scripts/py/methodology_rules.py` | 被下面两者共同消费，不复制规则 |
| 策略 CLI + 钩子 | `scripts/py/methodology_precheck_hook.py` | `py scripts/py/methodology_precheck_hook.py --selftest` → 17/17 |
| MCP 工具面 | `scripts/py/methodology_mcp_server.py` | `py scripts/py/methodology_mcp_server.py --selftest` → 6/6 |
| 回归测试 | `scripts/py/test_methodology_guard.py` | `py scripts/py/test_methodology_guard.py` → 29/29（含 stdio 管道往返、退出码契约） |
| DSH 接线 | `$DSH_HOME/profiles/methodology/cordis.patch.yml` | `dsh --profile methodology --dump-config` |
| 钩子配置 | `$DSH_HOME/data/hooks.json` | 见 §8.2 的 `; exit $LASTEXITCODE` |
| 门禁编排 | MCP 工具 `methodology_gate`（L1/L2/L3） | `py temp/run_gates.py L3` → 12/12 PASS |

端到端复现（真机、真模型）：`temp/smoke_run.ps1 <profile> <提示词文件> [--patch 覆盖层]`。

**已知边界（诚实标注）**：

- `PreToolUse` 拿不到非 shell 工具的参数，因此「写文件前按路径拦截」在 Codex 桥接下**不可能**，只能用 MCP 工具（模型主动调、弱）或原生插件（强）；
- `hooks.json` 是**进程级单份配置**，启动时读一次；`SessionStart` 是脱离运行，上下文可能赶不上第一个请求；
- 逃生阀 `METHODOLOGY_HOOK_DISABLE=1` 会让门禁整体放行——默认关闭，但它确实是「用户明确授权后绕过」的口子；
- `knowledge` 工具尚未实现；M0–M3 模型适配矩阵尚未跑。
