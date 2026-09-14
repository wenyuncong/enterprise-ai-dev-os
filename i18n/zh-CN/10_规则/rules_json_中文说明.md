# rules.json 可执行规则注册表字段说明 | rules.json Field Reference

> **源文件**：rules/rules.json
> **源版本**：1.0.0（源文件 `schemaVersion` 字段标注）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。**JSON 键名与取值原样保留，不翻译。**

---

## 1. 文件用途 | Purpose

`rules/rules.json` 是方法论的**可执行规则注册表**（executable rule registry），登记的是方法论禁止的写法（forbidden patterns）。每条规则都带 trigger / severity / write-block 元数据，因此同一份规则可以同时驱动三处：

1. **静态 lint** —— 扫描文件内容与路径，例如硬编码盘符路径、控制字符。
2. **写入前守卫**（pre-write guard）—— 在落盘前拦截，例如 `writeBlock: true` 的规则命中即阻断写入。
3. **CI 门禁**（CI gate）—— 在流水线中把 `FAIL` 级命中当作构建失败。

消费方是 `scripts/py/rule_lint.py`。当本文件缺失时，`rule_lint.py` 内建的那份规则仍然作为**回退**（fallback）生效——也就是说本文件是「可配置的显式清单」，而不是唯一实现。

---

## 2. 顶层结构 | Top-level Structure

| 键名（原样保留） | 类型 | 本文件取值 | 说明 |
|---|---|---|---|
| `schemaVersion` | string | `"1.0.0"` | 注册表模式的版本号。消费脚本据此判断字段结构，模式升级时递增。 |
| `description` | string | 见第 7 节完整内容 | 注册表自述：说明这是「方法论禁止写法的可执行规则注册表」，说明每条规则携带 trigger/severity/write-block 元数据，并说明三处消费方与回退关系。 |
| `rules` | array | 6 个规则对象 | 规则清单本体。数组顺序即扫描顺序，也是报告中规则的呈现顺序。 |

---

## 3. `rules[]` 单条规则的字段 | Rule Object Fields

| 键名（原样保留） | 类型 | 示例取值 | 语义 |
|---|---|---|---|
| `key` | string | `"root_clutter"` | 规则唯一标识。脚本用它做命中上报、豁免登记与规则-文档互链，**不得改写**。 |
| `name` | string | `"根目录散落文件"` | 规则的人类可读短名（本文件用中文），只用于报告展示，不参与匹配。 |
| `severity` | string | `"FAIL"` / `"WARN"` | 命中后的严重级。`FAIL` 阻断（CI 失败、写入被拒），`WARN` 只告警不阻断。语义强度不得下调。 |
| `glob` | array of string | `["*.md", "*.json"]` | 规则作用的文件范围。只有匹配这些 glob 的文件才参与本条规则的扫描。 |
| `trigger` | string | `"file creation at project root"` | 触发条件的英文断言（保留英文原样）。它说明「什么动作会命中」，并绑定审计断言。 |
| `writeBlock` | boolean | `true` / `false` | `true` = 命中即阻断写入（写入前守卫生效）；`false` = 只报告，不阻断。 |
| `description` | string | 见第 7 节完整内容 | 规则的判定说明与正确做法，供人和 AI 阅读。 |

---

## 4. 内置规则清单（6 条） | Built-in Rules

| `key` | `name` | `severity` | `glob` | `trigger` | `writeBlock` |
|---|---|---|---|---|---|
| `root_clutter` | 根目录散落文件 | WARN | `*` | file creation at project root | true |
| `control_chars` | 控制字符 | FAIL | `*.md`、`*.json`、`*.py`、`*.ps1`、`*.mjs`、`*.js`、`*.yml`、`*.yaml` | forbidden control character in a text file | false |
| `drive_paths` | 硬编码盘符路径 | FAIL | `*.md`、`*.json`、`*.py`、`*.ps1` | local drive path in portable assets | true |
| `stale_repo_paths` | 私有仓库路径残留 | FAIL | `*.md`、`*.json`、`*.py` | reference to a private workspace in portable assets | true |
| `hardcoded_colors` | 硬编码颜色 | WARN | `*.css`、`*.scss`、`*.vue`、`*.html` | hard-coded color where a theme token should be used | false |
| `empty_catches` | 静默失败 | WARN | `*.js`、`*.mjs`、`*.ts` | empty catch/except block hides a failure | false |

逐条说明（`description` 字段的中文解释，原文见第 7 节）：

1. **`root_clutter`（根目录散落文件，WARN，写入阻断）** —— 项目根目录只允许放 `AGENTS.md`、`.editorconfig`、构建文件，以及自动生成的适配器文件。在项目根新建其他文件即命中。对应规则：文件存放规范（临时文件进 `temp/` 或 `tmp/`，脚本进 `scripts/`，SQL 进 `database/`，文档进 `docs/`）。
2. **`control_chars`（控制字符，FAIL，不阻断写入）** —— 文本文件禁止包含被禁控制字符。命中即 `FAIL`，说明文件已损坏或由错误工具链生成。
3. **`drive_paths`（硬编码盘符路径，FAIL，写入阻断）** —— 可移植资产（portable assets）禁止硬编码本机盘符路径。示例一律使用仓库相对路径；本中文版全部译文同样遵守该约束。
4. **`stale_repo_paths`（私有仓库路径残留，FAIL，写入阻断）** —— 可移植资产禁止引用私有源仓库的路径。发布包里不得残留私有工作区引用。
5. **`hardcoded_colors`（硬编码颜色，WARN，不阻断写入）** —— 已有主题时必须用主题变量，禁止硬编码颜色。对应非协商规则第 5 条「只用主题变量」。
6. **`empty_catches`（静默失败，WARN，不阻断写入）** —— 空的 catch/except 块会吞掉失败；必须按正确严重级把失败暴露出来。对应非协商规则第 9 条「无静默失败」。

---

## 5. 取值语义约定 | Value Semantics

| 取值 | 含义 | 不得改变的理由 |
|---|---|---|
| `"FAIL"` | 阻断级：CI 判失败，或写入被拒（配合 `writeBlock`）。 | 降级为 `WARN` 等于把硬门禁改成建议，违反「语义强度不得改变」。 |
| `"WARN"` | 告警级：报告但不阻断。 | 升级为 `FAIL` 会误伤既有可移植资产。 |
| `writeBlock: true` | 命中即阻断写入。 | 这是「失败即阻断（fail-closed）」在工具层的体现。 |
| `writeBlock: false` | 只报告，不阻断。 | 用于需要人工判断、或修复成本高的项。 |

`name` 字段是本文件中唯一使用中文的取值（例如 `"根目录散落文件"`），它在译文中同样**原样保留**，不做任何改写。

---

## 6. 消费者与回退关系 | Consumers and Fallback

- **消费者**：`scripts/py/rule_lint.py` 读取本注册表，把每条规则编译成扫描项。
- **回退**：本文件缺失时，`rule_lint.py` 内建规则继续生效，保证 lint 不会因为注册表丢失而静默失效。
- **与文档的对应**：本注册表是 `rules/AGENTS.md` 第 6 节「非协商规则」与第 10 节「文件存放规范」的可执行化表达；文档说明「为什么」，注册表说明「怎么判、判多严、是否阻断」。

---

## 7. 完整文件内容 | Full File Content

以下为 `rules/rules.json` 的完整内容，**逐字节对应源文件，键名与取值未做任何翻译或改写**：

```json
{
  "schemaVersion": "1.0.0",
  "description": "Executable rule registry for the methodology's forbidden patterns. Each rule carries trigger/severity/write-block metadata so the same rules can drive static lint, pre-write guards, and CI gates. scripts/py/rule_lint.py consumes this registry; the built-in rules in rule_lint.py remain the fallback when this file is absent.",
  "rules": [
    {
      "key": "root_clutter",
      "name": "根目录散落文件",
      "severity": "WARN",
      "glob": ["*"],
      "trigger": "file creation at project root",
      "writeBlock": true,
      "description": "Project root only holds AGENTS.md, .editorconfig, build files, and generated adapters."
    },
    {
      "key": "control_chars",
      "name": "控制字符",
      "severity": "FAIL",
      "glob": ["*.md", "*.json", "*.py", "*.ps1", "*.mjs", "*.js", "*.yml", "*.yaml"],
      "trigger": "forbidden control character in a text file",
      "writeBlock": false,
      "description": "Text files must not contain forbidden control characters."
    },
    {
      "key": "drive_paths",
      "name": "硬编码盘符路径",
      "severity": "FAIL",
      "glob": ["*.md", "*.json", "*.py", "*.ps1"],
      "trigger": "local drive path in portable assets",
      "writeBlock": true,
      "description": "Portable assets must not hard-code local drive paths (C:, G:, H:, ...)."
    },
    {
      "key": "stale_repo_paths",
      "name": "私有仓库路径残留",
      "severity": "FAIL",
      "glob": ["*.md", "*.json", "*.py"],
      "trigger": "reference to a private workspace in portable assets",
      "writeBlock": true,
      "description": "Portable assets must not reference the private source repository."
    },
    {
      "key": "hardcoded_colors",
      "name": "硬编码颜色",
      "severity": "WARN",
      "glob": ["*.css", "*.scss", "*.vue", "*.html"],
      "trigger": "hard-coded color where a theme token should be used",
      "writeBlock": false,
      "description": "Theme variables only; no hard-coded colors when a theme exists."
    },
    {
      "key": "empty_catches",
      "name": "静默失败",
      "severity": "WARN",
      "glob": ["*.js", "*.mjs", "*.ts"],
      "trigger": "empty catch/except block hides a failure",
      "writeBlock": false,
      "description": "Empty catch/except blocks hide failures; surface them at the correct severity."
    }
  ]
}
```

---

## 译注 | Translator's Notes

1. 源文件是 JSON 数据文件，不是叙述性文档；本文按「逐字段解释 + 完整内容代码块」的方式对应，键名与取值一律原样保留。第 7 节代码块与 `rules/rules.json` 内容逐行一致（缩进为 2 空格，数组内联写法照抄源文件）。
2. `name` 字段的中文取值（`"根目录散落文件"` 等）属源文件既有取值，译文不改写、不重译。
3. 源文件 `drive_paths.description` 中的 `(C:, G:, H:, ...)` 是对「盘符路径」这一写法的文字说明，不是本机路径，按原样保留在代码块内，未出现在任何示例路径中。
4. 英文断言锚点（审计用，原样英文）：`5S Delivery Governance`、`scope -> specify -> ship -> safeguard -> sell`、`product-directed AI delivery`、`command gateway`、`safe AI change and code location`、`read, prove, then change`、`exact file or hunk staging`、`business ambiguity`、`fresh evidence before claims`、`review two independent axes`、`qualification`、`saleability`、`product owner`、`business-flow acceptance`、`fresh evidence`、`two independent axes`、`shared language`、`host page`、`ui atom`、`atomic service`、`atomic orchestration`、`aggregate interface`、`safe change`、`code location`、`working-tree`、`destructive`、`impact`、`exact task-owned`、`L0`–`L3`、`Q0`–`Q3`、`P0`–`P3`、`MUST-1`–`MUST-8`、`Scope`、`Specify`、`Ship`、`Safeguard`、`Sell`、`Host`、`FieldPackage`、`BusinessProfile`、`DeliveryContract`。完整断言清单的正文归属见 `rules_AGENTS_中文版.md`。
