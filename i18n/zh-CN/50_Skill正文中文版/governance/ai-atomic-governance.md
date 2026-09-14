# `ai-atomic-governance` — 原子系统架构治理器

> **源文件**：skills/governance/ai-atomic-governance/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-atomic-governance
description: "Govern atomic system architecture: declaration+executor separation, layering (L0-L5), governance integration, and anti-pattern detection. Use when auditing or building atomic systems, adding new atoms, or integrating governance into existing atom executors."
```

**中文描述**：治理原子系统架构：声明与执行器分离、分层（L0–L5）、治理集成与反模式检测。适用于审计或构建原子系统、新增原子，或把治理集成进既有原子执行器的场景。

---

## Purpose | 目标

强制执行原子系统纪律：每个原子都是一份纯声明，每个执行器都可独立测试，每个执行器都集成治理。本 Skill 用于防止原子系统最常见的失效模式 —— **分层衰减（layered decay）**，即低层（L0）遵循模式，而高层（L2/L3）却退化回"逻辑写在声明上"的反模式。

**它解决的问题**：AI 经常把业务逻辑直接写在 DeclarationAtom 类上、产出单体式执行器文件、跳过治理集成，并把 L0 与 L3 的模式混用得不一致。

---

## The Prime Directive | 最高准则

```
DECLARATION = CONTRACT ONLY（仅契约：schema、meta、relations）
EXECUTOR    = ALL BUSINESS LOGIC（全部业务逻辑：可测试、可替换）
GOVERNANCE  = MANDATORY PARAMETER ON EVERY EXECUTOR（每个执行器的必备参数）

Never（禁止）:  在 DeclarationAtom 上写 run()
Always（必须）: 每个原子一个独立的执行器文件
```

---

## Rule 1: Declaration + Executor Separation (P0) | 规则 1：声明与执行器分离（P0）

### What a DeclarationAtom MUST contain | DeclarationAtom 必须包含什么

| 字段 | 是否必须 | 说明 |
|-------|----------|-------------|
| _atom_name | 是 | 唯一的原子标识符 |
| _atom_provider | 是 | 包名 |
| _atom_category | 是 | 功能分类 |
| meta | 是 | AtomMeta，含 name、level、description、tags、version、lifecycle |
| input_schema | 是 | field_name: type_string 的字典 |
| output_schema | 是 | field_name: type_string 的字典 |
| provider | 是 | 简短的 provider 字符串 |
| category | 是 | 简短的 category 字符串 |

### What a DeclarationAtom MUST NOT contain | DeclarationAtom 禁止包含什么

- 带业务逻辑的 run() 方法
- 对 services、stores 或外部 API 的直接 import
- 会构造业务对象的 __post_init__
- @dataclass 装饰器（应当使用标准类继承）

### Standard Declaration Pattern | 标准声明模式

```python
from atoms.declarative_base import DeclarationAtom
from atoms import AtomMeta

class MyAtom(DeclarationAtom):
    _atom_name = "my_atom"
    _atom_provider = "domain"
    _atom_category = "audit"
    meta = AtomMeta(name="my_atom", level=3,
        description="[L3] Description here",
        tags=["l3","domain"], version="1.0.0", lifecycle="active")
    input_schema = {"field": "str"}
    output_schema = {"result": "dict", "evidence_id": "str"}
    provider = "domain"; category = "audit"
```

### Standard Executor Pattern | 标准执行器模式

```python
from uuid import uuid4

class MyExecutor:
    def execute(self, field, governance=None, **inputs):
        if governance:
            result = governance.classify(action="my_action")
            if result.get("decision") in ("auto_reject",):
                return {"evidence_id": f"ev_{uuid4().hex[:12]}",
                        "error": "Governance denied"}
        # 业务逻辑写在这里
        return {"result": {}, "evidence_id": f"ev_{uuid4().hex[:12]}"}
```

---

## Rule 2: Governance Integration (P0) | 规则 2：治理集成（P0）

每个执行器**必须**：

1. 接受 governance=None 参数
2. 在入口处调用 governance.classify(action="...")
3. 在每一条 return 路径上都返回 evidence_id
4. 处理 auto_reject 决策分支

### Governance Guard Template | 治理护栏模板

```python
def execute(self, ..., governance=None):
    if governance:
        result = governance.classify(action="atomic_execute")
        if result.get("decision") in ("auto_reject",):
            return {"evidence_id": f"ev_{uuid4().hex[:12]}",
                    "error": "Governance denied"}
    # ... 正常执行
```

---

## Rule 3: Atomic Layering (P1) | 规则 3：原子分层（P1）

| 层级 | 名称 | 模式 | 示例 |
|-------|------|---------|---------|
| L0 | Base Atom（基础原子） | 纯函数，零外部依赖 | comparator, drive_homeostasis |
| L1 | Operator（算子） | 调用外部 API / 库 | llm_chat, metacognitive_gate |
| L2 | Composite（组合） | 编排 L0/L1 原子 | orch_sequential, duty_delegation |
| L3 | Domain App（领域应用） | 完整业务场景 | domain_code_audit, debate_consensus |
| L4 | Terminal（终端） | 对外部世界产生副作用 | file_write, draft_email |
| L5 | Application（应用） | 把 L3+L4 组合成工作流 | governance_orchestrator, release_pipeline |

**关键规则**：高层通过执行器委派来组合低层，**禁止**靠复制逻辑来组合。

---

## Anti-Patterns | 反模式

### AP1: Layered Decay | AP1：分层衰减

**症状**：L0 原子完美遵循模式，但 L2/L3 原子却在声明上挂着 run() 方法、跳过治理、使用不一致的模式。

**成因**：初期开发只盯着底层；高层是后来加的，没经过治理评审。

**检测**：运行 app_governance_orchestrator，参数 `audit_types=["code"]` —— 它会检出带 run() 方法、以及缺失治理的原子。

**修复**：把 run() 抽到独立执行器，补上 governance=None 参数，并在返回值中补 evidence_id。

### AP2: Monolithic Executor File | AP2：单体式执行器文件

**症状**：单个 500+ 行文件里塞了 18 个以上执行器类。

**修复**：每个原子一个执行器文件。对既有单体文件，先用基于 AST 的批量治理注入，再做拆分。

### AP3: Governance Gap | AP3：治理缺口

**症状**：执行器本身工作正常，但因为缺少 governance= 参数，无法被接入 L5 治理编排。

**修复**：基于 AST 的治理注入。

---

## Patterns | 模式

### Bulk Governance Injection (AST Transform) | 批量治理注入（AST 变换）

当单体式执行器文件里有大量类缺少治理时，使用 Python AST 变换：

```python
import ast

class GovernanceInjector(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        if node.name != "execute":
            return node
        node.args.args.append(ast.arg(arg="governance"))
        node.args.defaults.append(ast.Constant(value=None))
        guard = ast.parse('''
if governance is not None:
    result = governance.classify(action="atomic_execute")
    if result.get("decision") in ("auto_reject",):
        return {"evidence_id": f"ev_{uuid4().hex[:12]}", "error": "Governance denied"}
''').body[0]
        node.body.insert(0, guard)
        return node

new_tree = GovernanceInjector().visit(ast.parse(source))
new_source = ast.unparse(new_tree)
```

---

## Verification Checklist | 验证清单

在宣布某个原子系统"已受治理"之前：

- [ ] 所有 DeclarationAtom 类都是纯的（无 run()、无业务 import）
- [ ] 每个执行器都有 governance=None 参数
- [ ] 每个执行器都返回 evidence_id
- [ ] 所有原子与其声明的层级一致（L0–L5）
- [ ] DeclarationAtom 子类上没有 @dataclass
- [ ] 原子目录中没有死文件
- [ ] 测试覆盖完整，包含治理集成测试
- [ ] L5 app_governance_orchestrator 能消费所有原子

---

## Case Studies | 案例

### Digital Life Governance Remediation (2026-07-05) | Digital Life 治理整改（2026-07-05）

**整改前**：drive/attention/selfmodel/metacognitive + debate/multi-agent 共 21 个原子。L0 干净，L2/L3 在声明上挂着 run()，治理集成为零。

**整改后**：从声明中抽出 3 个执行器，用 AST 给 18 个执行器注入治理，新增 15 个治理测试。共 151 个测试，0 失败。

**关键指标**：一个会话内，具备治理集成的原子从 0 个变为 21 个。

### GERP Cross-Project Audit (2026-07-05) | GERP 跨项目审计（2026-07-05）

**整改前**：GERP 中 623 条代码审计发现 + 100 条字段审计发现，没有治理流水线。

**整改后**：L5 governance_orchestrator 消费 L3 domain_code_audit + domain_erp_field_check，产出证据 + 索引 + 报告。只读模式，未修改 GERP。

---

## 译注

- 「源版本」源文件未标注版本号；案例日期为 2026-07-05。
- `(P0)`、`(P1)` 分级标注、`DeclarationAtom`、`ExecutorAtom` 概念、`L0`–`L5` 层级代号一律保留英文。
- Python 代码块整体原样复制，仅将英文行内注释译为中文；`Governance denied` 等返回值字符串未改动。
- 源文件的部分围栏使用单反引号（渲染为行内代码），本对照版统一改为三反引号代码块以正确渲染，块内内容逐字未改。
