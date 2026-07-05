---
name: ai-atomic-governance
description: "Govern atomic system architecture: declaration+executor separation, layering (L0-L5), governance integration, and anti-pattern detection. Use when auditing or building atomic systems, adding new atoms, or integrating governance into existing atom executors."
---

# ai-atomic-governance — Atomic System Architecture Governor

## Purpose

Enforce atomic system discipline: every atom is a pure declaration, every executor is independently testable, every executor integrates governance. This skill prevents the most common atomic system failure mode — **layered decay**, where lower layers (L0) follow the pattern but upper layers (L2/L3) regress into logic-on-declaration anti-patterns.

**Problem it solves**: AI frequently writes business logic directly on DeclarationAtom classes, creates monolithic executor files, skips governance integration, and mixes L0 and L3 patterns inconsistently.

---

## The Prime Directive

`
DECLARATION = CONTRACT ONLY (schema, meta, relations)
EXECUTOR    = ALL BUSINESS LOGIC (testable, replaceable)
GOVERNANCE  = MANDATORY PARAMETER ON EVERY EXECUTOR

Never: write run() on a DeclarationAtom
Always: separate executor file per atom
`

---

## Rule 1: Declaration + Executor Separation (P0)

### What a DeclarationAtom MUST contain

| Field | Required | Description |
|-------|----------|-------------|
| _atom_name | Yes | Unique atom identifier |
| _atom_provider | Yes | Package name |
| _atom_category | Yes | Functional category |
| meta | Yes | AtomMeta with name, level, description, tags, version, lifecycle |
| input_schema | Yes | Dict of field_name: type_string |
| output_schema | Yes | Dict of field_name: type_string |
| provider | Yes | Short provider string |
| category | Yes | Short category string |

### What a DeclarationAtom MUST NOT contain

- run() method with business logic
- Direct imports of services, stores, or external APIs
- __post_init__ that constructs business objects
- @dataclass decorator (use standard class inheritance)

### Standard Declaration Pattern

`python
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
`

### Standard Executor Pattern

`python
from uuid import uuid4

class MyExecutor:
    def execute(self, field, governance=None, **inputs):
        if governance:
            result = governance.classify(action="my_action")
            if result.get("decision") in ("auto_reject",):
                return {"evidence_id": f"ev_{uuid4().hex[:12]}",
                        "error": "Governance denied"}
        # business logic here
        return {"result": {}, "evidence_id": f"ev_{uuid4().hex[:12]}"}
`

---

## Rule 2: Governance Integration (P0)

Every executor MUST:
1. Accept governance=None parameter
2. Call governance.classify(action="...") at entry
3. Return evidence_id in every return path
4. Handle the auto_reject decision path

### Governance Guard Template

`python
def execute(self, ..., governance=None):
    if governance:
        result = governance.classify(action="atomic_execute")
        if result.get("decision") in ("auto_reject",):
            return {"evidence_id": f"ev_{uuid4().hex[:12]}",
                    "error": "Governance denied"}
    # ... normal execution
`

---

## Rule 3: Atomic Layering (P1)

| Level | Name | Pattern | Example |
|-------|------|---------|---------|
| L0 | Base Atom | Pure function, zero external deps | comparator, drive_homeostasis |
| L1 | Operator | External API/lib call | llm_chat, metacognitive_gate |
| L2 | Composite | Orchestrates L0/L1 atoms | orch_sequential, duty_delegation |
| L3 | Domain App | Full business scenario | domain_code_audit, debate_consensus |
| L4 | Terminal | External-world side effects | file_write, draft_email |
| L5 | Application | Composes L3+L4 into workflows | governance_orchestrator, release_pipeline |

**Key rule**: Higher layers compose lower layers through executor delegation, never by copying logic.

---

## Anti-Patterns

### AP1: Layered Decay

**Symptom**: L0 atoms follow the pattern perfectly, but L2/L3 atoms have run() methods on declarations, skip governance, and use inconsistent patterns.

**Cause**: Initial development focused on bottom layers; upper layers added later without governance review.

**Detection**: Run app_governance_orchestrator with audit_types=["code"] — it will detect atoms with run() methods and missing governance.

**Fix**: Extract run() into separate executor, add governance=None parameter, add evidence_id to returns.

### AP2: Monolithic Executor File

**Symptom**: 18+ executor classes in a single 500+ line file.

**Fix**: One executor per atom file. Use AST-based bulk governance injection for existing monoliths before splitting.

### AP3: Governance Gap

**Symptom**: Executors work correctly but cannot be integrated into L5 governance orchestration because they lack governance= parameter.

**Fix**: AST-based governance injection.

---

## Patterns

### Bulk Governance Injection (AST Transform)

When a monolithic executor file has many classes without governance, use Python AST transformation:

`python
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
`

---

## Verification Checklist

Before declaring an atomic system "governed":

- [ ] All DeclarationAtom classes are pure (no run(), no business imports)
- [ ] Every executor has governance=None parameter
- [ ] Every executor returns evidence_id
- [ ] All atoms match their declared level (L0-L5)
- [ ] No @dataclass on DeclarationAtom subclasses
- [ ] No dead files in atom directories
- [ ] Full test coverage including governance integration tests
- [ ] L5 app_governance_orchestrator can consume all atoms

---

## Case Studies

### Digital Life Governance Remediation (2026-07-05)

**Before**: 21 atoms across drive/attention/selfmodel/metacognitive + debate/multi-agent. L0 clean, L2/L3 had run() on declarations, zero governance integration.

**After**: Extracted 3 executors from declarations, AST-injected governance into 18 executors, 15 new governance tests. 151 total tests, 0 failures.

**Key metric**: 0 → 21 atoms with governance integration in one session.

### GERP Cross-Project Audit (2026-07-05)

**Before**: 623 code audit findings + 100 field audit findings in GERP, no governance pipeline.

**After**: L5 governance_orchestrator consumed L3 domain_code_audit + domain_erp_field_check, produced evidence + index + report. Read-only mode, no GERP modification.