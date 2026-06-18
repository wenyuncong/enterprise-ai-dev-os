# Rule Runtime Lite | 轻量规则运行时

Rule Runtime Lite is a future design direction for making project rules executable. It is not required for the current open-source methodology to be useful, and it is not yet a full implementation.

Rule Runtime Lite 是让项目规则可执行的未来设计方向。当前开源方法论不依赖它才能使用，它也不是已经完成的完整实现。

## Goal | 目标

Turn selected rules from documentation into small, testable checks that can run before, during, or after AI-assisted code changes.

把部分文档规则转成可测试的小型检查，可在 AI 改代码前、过程中或完成后执行。

## Non-Goals | 非目标

- no large AI platform rewrite
- no model lifecycle management
- no Kubernetes scheduler
- no blockchain audit storage
- no physical access-control integration
- no claim that all business rules can be automatically verified

## Runtime Stages | 运行阶段

| Stage | Purpose | Example |
|---|---|---|
| Pre-generation | Load constraints before the AI writes files | required skills, file placement, forbidden paths |
| During generation | Give the AI structured checks it can call or reason over | path policy, schema checklist, adapter target validation |
| Post-generation | Verify outputs before "done" | audit scripts, boundary check, runtime verification |
| Evolution | Convert repeated failures into stronger rules | add rule, template, skill, or test |

## Minimum Viable Rule Types | 最小可行规则类型

Start with rules that are cheap, deterministic, and useful:

| Type | Example | Implementation path |
|---|---|---|
| Path rules | no files in private folders, no generated adapter outputs committed | Python audit |
| Structure rules | required docs/templates/skills exist | Python audit |
| Manifest rules | every `SKILL.md` is listed in `SKILL_MANIFEST.json` | Python audit |
| Text residue rules | no hard-coded local paths or legacy repo names | Python audit |
| Adapter rules | verified adapters can dry-run without errors | PowerShell dry-run |

AST or Tree-sitter rules are useful later, but they should be added only after simple deterministic checks have measurable value.

AST 或 Tree-sitter 规则有价值，但应在简单确定性检查证明价值后再加入。

## Rule File Sketch | 规则文件草案

```yaml
rules:
  - id: no_private_paths
    severity: error
    scope:
      include:
        - README.md
        - docs/**
        - skills/**
      exclude:
        - docs/公开材料/**
    check:
      type: text_pattern
      deny:
        - "[A-Z]:\\\\"
        - "legacy-private-repo-name"
    fix_hint: "Move private paths to non-public notes or replace with portable placeholders."
```

This is a design sketch, not a committed engine contract.

这是设计草案，不是已经承诺的引擎接口。

## Public / Advanced Boundary | 公开版与高级版边界

Open-source-friendly:

- rule schema drafts
- simple deterministic audits
- examples using sanitized fixtures
- adapter verification reports

Potential advanced/commercial layer:

- team policy packs
- rule hit analytics
- multi-repository governance dashboard
- MCP/tool-call audit gateway
- enterprise approval workflows

## First Implementation Candidate | 首个实现候选

The safest first implementation is not AST. It is a small rule runner around the checks already used by this repository:

```text
rule config -> deterministic checks -> JSON report -> README/site badge or release evidence
```

This keeps the project grounded and avoids building an oversized platform before evidence exists.
