---
name: ai-reference-researcher
description: "Research primary references, official docs, open-source implementations, and comparable systems before designing unfamiliar features. Use when the domain is new, standards may have changed, or implementation should follow proven external practice."
---

# ai-reference-researcher — Reference-Driven Development Research Engine

## Purpose | 用途

Before developing complex features in unfamiliar domains, search for, download, analyze, and extract patterns from the best open-source reference implementations. This transforms "AI guesses from training data" into "AI learns from real production code."

**Problem it solves**: AI's training data is broad but shallow. For specialized domains (ERP workflows, financial calculations, supply chain, permission systems, multi-tenant SaaS), AI often invents suboptimal patterns because it has never seen how mature systems actually implement them. Reference research fixes this by giving AI concrete, high-quality examples to learn from before writing code.

---

## When to Trigger | 触发条件

### MUST trigger when:
- Building a domain the team has never built before (e.g., first payroll module, first WMS)
- Architecting a complex subsystem (auth, multi-tenancy, workflow engine, report engine)
- The AI makes 2+ incorrect architecture assumptions
- User says "I'm not sure how this should work" or "find me a reference"

### SHOULD trigger when:
- Choosing between 3+ competing libraries/frameworks
- Designing database schema for a new business domain
- New project initialization (before scaffolding)
- `ai-library-first` finds multiple candidate libraries — reference research helps pick the best one

### SKIP when:
- Simple CRUD features
- Domain the team has extensive experience with
- Urgent bug fixes (time-sensitive)
- Rapid prototype (Archetype A)

---

## Research Workflow | 研究流程

```
┌──────────────────────────────────────────────────────────────┐
│  PHASE 1: SEARCH                                            │
│  Search GitHub/GitLab/npm/PyPI for top projects in domain   │
├──────────────────────────────────────────────────────────────┤
│  PHASE 2: EVALUATE                                          │
│  Score candidates by stars, maintenance, architecture       │
├──────────────────────────────────────────────────────────────┤
│  PHASE 3: DOWNLOAD                                          │
│  Clone the best 1-2 projects locally for analysis           │
├──────────────────────────────────────────────────────────────┤
│  PHASE 4: EXTRACT                                           │
│  Analyze: architecture, patterns, naming, libraries, schema │
├──────────────────────────────────────────────────────────────┤
│  PHASE 5: APPLY                                             │
│  Integrate findings into architecture design + skill updates │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Search | 搜索

### Search Sources

| Source | Search Method | Best For |
|---|---|---|
| **GitHub** | `site:github.com {domain} {language} stars:>100` | Full-stack apps, frameworks, libraries |
| **npm** | `npm search {keyword}` or `npmjs.com` | Frontend libraries, Node.js tools |
| **Maven Central** | `mvnrepository.com` | Java libraries, Spring Boot starters |
| **PyPI** | `pypi.org` | Python tools, ML libraries |
| **Awesome Lists** | `site:github.com awesome {domain}` | Curated lists of best projects |

### Search Strategy
```
# Example: Researching "multi-tenant SaaS ERP"
1. Search: site:github.com "multi-tenant" erp spring-boot stars:>50
2. Search: site:github.com "saas" "multi-tenant" java architecture
3. Search: site:github.com awesome erp
4. For specific features: site:github.com "purchase order" workflow engine
```

---

## Phase 2: Evaluate | 评估

### Scoring Criteria (weighted)

| Criteria | Weight | What to Check |
|---|---|---|
| **Stars** | 25% | >100 = good, >1000 = excellent |
| **Active maintenance** | 30% | Last commit < 6 months, issues being closed |
| **Architecture quality** | 20% | Clean module separation, clear README, documented patterns |
| **Code quality** | 15% | Tests exist, linting passes, reasonable complexity |
| **Domain relevance** | 10% | How closely does it match our specific need? |

### Evaluation Output
```markdown
| Project | Stars | Last Commit | Arch Quality | Overall | Verdict |
|---|---|---|---|---|---|
| repo-owner/project-a | 1.2K | 3 days ago | ⭐⭐⭐⭐⭐ | 92% | **SELECT** |
| repo-owner/project-b | 450 | 2 months ago | ⭐⭐⭐⭐ | 78% | Reference only |
| repo-owner/project-c | 89 | 1 year ago | ⭐⭐ | 45% | Skip |
```

---

## Phase 3: Download | 下载

### Clone Strategy

```bash
# Clone selected projects to a reference directory
mkdir -p reference/ && cd reference/
git clone --depth 1 https://github.com/repo-owner/project-a.git
```

**Rules**:
- Use `--depth 1` for shallow clone (save time and disk)
- Store in `reference/` directory (git-ignored, not committed)
- Never commit reference code to the project repository
- Delete after analysis is complete (or keep for ongoing reference)

---

## Phase 4: Extract | 提取

### What to Analyze

| Dimension | What to Look For | Output |
|---|---|---|
| **Directory Structure** | How are modules organized? Monorepo vs multi-repo? | Recommended folder structure |
| **Architecture Patterns** | How are services split? Event-driven? CQRS? | Architecture decision inputs |
| **Database Schema** | Table naming, relationships, indexing strategy | Schema design patterns |
| **API Design** | REST vs GraphQL, endpoint naming, versioning | API conventions |
| **Library Choices** | What libraries are used? Why those? | Library selection for ai-library-first |
| **Naming Conventions** | Consistent patterns in class/table/endpoint names | Naming standards |
| **Error Handling** | How are errors structured and propagated? | Error handling patterns |
| **Testing Patterns** | What test frameworks? How are tests organized? | Test strategy |
| **Configuration** | How are env vars, feature flags managed? | Config patterns |

### Extraction Output Format
```markdown
## Reference Analysis: [Project Name]

### Key Patterns Extracted
1. **Module organization**: [Description + example path]
2. **Service boundary**: [How they split services]
3. **Database design**: [Table patterns observed]
4. **Library stack**: [Key libraries with versions]

### Patterns to Adopt
- [Pattern 1]: [Why it's good for us]
- [Pattern 2]: [Why it's good for us]

### Patterns to Avoid
- [Anti-pattern 1]: [Why it caused problems]

### Recommended Architecture Decisions
- ADR candidate: [Decision based on reference findings]
```

---

## Phase 5: Apply | 应用

### Integration Points

| Skill/Artifact | How Reference Research Feeds In |
|---|---|
| `ai-atomic-architect` | Architecture patterns from reference → atomic service design |
| `ai-library-first` | Library choices from reference → library catalog update |
| `ai-component-standardizer` | Folder structure from reference → scaffold templates |
| `ai-project-classifier` | Domain complexity assessment → quality target selection |
| `ai-architect-governor` | ADR based on reference findings |
| `ai-skill-evolver` | New patterns → skill updates |
| `docs/架构决策记录/` | ADR citing reference projects |

---

## Domain-Specific Reference Targets | 领域参考目标

### ERP / Enterprise Systems
| Domain | Search Keywords | Expected Findings |
|---|---|---|
| Multi-tenant SaaS | `multi-tenant spring boot saas` | Tenant isolation patterns, schema-per-tenant vs shared |
| Inventory/WMS | `warehouse management system open source` | Stock movement patterns, barcode, location hierarchy |
| Accounting/Finance | `open source accounting double-entry` | Ledger patterns, reconciliation, period close |
| CRM | `open source crm node.js` | Pipeline, lead management, contact hierarchy |
| Workflow Engine | `workflow engine open source bpmn` | State machines, approval chains, process definition |

### General Architecture
| Domain | Search Keywords | Expected Findings |
|---|---|---|
| Microservices | `microservices reference architecture java` | Service boundaries, event bus, API gateway |
| Permission/RBAC | `rbac permission system open source` | Role hierarchy, resource-based auth, tenant isolation |
| Report Engine | `report engine open source` | Template rendering, data source abstraction, export |
| Real-time | `websocket real-time dashboard open source` | Event streaming, push patterns |

---

## License Awareness | 许可证意识

**Study, don't copy.** Reference code is for learning patterns, not copying code.

| License | Can Study? | Can Copy? |
|---|---|---|
| MIT / Apache 2.0 / BSD | ✅ Yes | ✅ With attribution |
| GPL / AGPL | ✅ Yes | ⚠️ Only if project is also GPL |
| Proprietary / No License | ❌ Skip | ❌ Never |

**Default rule**: Only study projects with MIT, Apache 2.0, or BSD licenses.

---

## Integration with Methodology | 方法论集成

```
Step 0: Project Classification
    │
    ├── Complex domain? YES → Step 0a: Reference Research
    │     ├── Search GitHub for top 3 projects
    │     ├── Evaluate → Download best 1-2
    │     ├── Extract patterns → Feed to architects
    │     └── Apply findings
    │
    └── Simple domain? SKIP

Step 1: Database Init (informed by reference schema patterns)
Step 2-12: Standard development flow
Step 13: Runtime Verify
```

---

## Guardrails | 防护规则

- **Study patterns, never copy code** — this is learning, not plagiarizing
- **License check first** — skip projects with incompatible or missing licenses
- **Quality over quantity** — 1-2 well-studied projects > 10 shallow scans
- **Shallow clone** — `--depth 1` always, don't waste disk space
- **Git-ignore reference/** — never commit reference code to project repo
- **Document what you learned** — every research session produces a doc in `docs/每日调研回写/`
- **Timebox research** — max 30 minutes per domain; if no good reference found, proceed without

## Maturity | 成熟度

**Stage**: New — Created to fill the gap between competitor analysis (product-level) and actual implementation (code-level).

## Evolution History | 进化记录

- v1.0.0: Initial creation — 5-phase research workflow, domain reference targets, license awareness
