---
name: ai-project-classifier
description: "Classify projects by origin, quality target, deployment targets, and scale to choose the correct methodology path and skill set. Use at project start, during onboarding, or before applying the methodology to a new or existing codebase."
---

# ai-project-classifier — Project Classification Decision Framework

## Purpose | 用途

Classify every project at inception across four critical dimensions. This determines which skills to load, which architecture to use, which steps to follow, and what "done" means.

**Problem it solves**: Without explicit classification, the methodology applies the same rules to a 1-day prototype and a 6-month enterprise system. This causes over-engineering for small projects and under-engineering for large ones.

## Trigger | 触发条件

- **ALWAYS** run before any other skill when starting work on a project
- When the user says "new project", "start building", "create app"
- When encountering an existing project for the first time
- When the project scope changes significantly

---

## Classification Flow | 分类流程

```
                 ┌──────────────────┐
                 │  Project Start   │
                 └────────┬─────────┘
                          │
              ┌───────────▼───────────┐
              │ DIMENSION 1:          │
              │ Brownfield or         │
              │ Greenfield?           │
              └───────────┬───────────┘
                          │
            ┌─────────────┼─────────────┐
            │             │             │
     ┌──────▼──────┐ ┌───▼────┐        │
     │ Brownfield  │ │Greenfield       │
     │ (Existing)  │ │(New)            │
     └──────┬──────┘ └───┬────┘        │
            │             │             │
            │    ┌────────▼────────┐    │
            │    │ DIMENSION 2:    │    │
            │    │ Quality Target? │    │
            │    └────────┬────────┘    │
            │             │             │
            │   ┌─────────┼─────────┐   │
            │   │         │         │   │
            │ ┌─▼───┐ ┌──▼──┐ ┌───▼──┐ │
            │ │Rapid│ │AI-  │ │Enter-│ │
            │ │Proto│ │Native│ │prise │ │
            │ └──┬──┘ └──┬──┘ └──┬───┘ │
            │    │       │       │     │
            │    │  ┌────▼───────▼──┐  │
            │    │  │ DIMENSION 3: │  │
            │    │  │ Deployment   │  │
            │    │  │ Targets?     │  │
            │    │  └────┬─────────┘  │
            │    │       │            │
            │    │  ┌────▼────┐       │
            │    │  │DIM 4:   │       │
            │    │  │Scale?   │       │
            │    └──┤         │       │
            │       └─────────┘       │
            └─────────────────────────┘
```

---

## Dimension 1: Project Origin | 项目来源

### Brownfield (Existing Project)
**Indicators**: Has `package.json`, `.git`, database, existing code structure
**Approach**:
1. READ before WRITE — audit existing architecture first
2. EXTRACT patterns — document current conventions, don't impose new ones
3. UPGRADE incrementally — add methodology layers one at a time
4. NEVER break existing functionality

**Key Questions**:
- What framework/stack is already in use?
- Are there existing coding conventions?
- Is there a database schema to respect?
- Are there existing users/data to protect?

### Greenfield (New Project)
**Indicators**: Empty directory, no code, "start from scratch"
**Approach**:
1. Classify by dimensions 2-4 FIRST
2. Scaffold based on classification
3. Apply full methodology from Step 1
4. Architecture decisions are fresh — choose wisely

---

## Dimension 2: Quality Target | 质量目标

### Rapid Prototype
**When**: MVP, demo, proof-of-concept, < 1 week timeline, 1-2 developers
**Characteristics**:
- Single codebase (monorepo acceptable)
- One database, simple schema
- Minimal testing (smoke tests only)
- UI-first development (get something visible fast)
- Documentation: minimal (README + API list)

**Skills to load**: core skills only (planner, decomposer, command-executor)
**Steps to follow**: Streamlined 13-step (skip deep architecture, skip ADR)
**Architecture**: Archetype A (Single-Service)

### AI-Native (Production Quality)
**When**: Real product, users will depend on it, > 1 month timeline, 2-5 developers
**Characteristics**:
- Atomic service boundaries from day one
- Full test coverage (unit + integration + runtime verify)
- Interface-first design (OpenAPI/GraphQL before implementation)
- Documentation: full methodology docs
- Multi-platform ready (web + at least one other target planned)

**Skills to load**: All core + governance skills
**Steps to follow**: Full 13-step with all gates
**Architecture**: Archetype B (Atomic Services)

### Enterprise
**When**: Multi-tenant, compliance requirements, SLA guarantees, team of 5+
**Characteristics**:
- Full atomic service architecture with event-driven orchestration
- Multi-region deployment consideration
- Security audit, penetration testing
- HA/DR strategy
- Full CI/CD pipeline with deployment gates

**Skills to load**: All skills (core + governance + platform + tech)
**Steps to follow**: Full 13-step + deployment gates + security scan
**Architecture**: Archetype C (Multi-Platform)

---

## Dimension 3: Deployment Targets | 部署目标

| Target | Implication |
|---|---|
| **Web only** | Standard SPA/SSR, REST API |
| **Web + Mobile** | API-first design, mobile SDK consideration |
| **Web + WeChat** | WeChat auth adapter, wx.request compatibility |
| **Web + MCP Server** | MCP Tools protocol alongside REST |
| **All platforms** | Unified interface layer, transport adapters for each |

**Rule**: Always design for web + 1 extra target. It costs 10% more upfront but saves 90% of rewrite cost later.

---

## Dimension 4: Scale | 规模

### Monolith/Modular Monolith
**When**: < 10K users, < 50 API endpoints, single team
**Pattern**: One deployable with clear module boundaries
**Evolution**: Split modules into services when any exceeds 500 LOC in core logic

### Microservices
**When**: > 10K users, > 50 API endpoints, multiple teams
**Pattern**: Atomic services, event-driven, independent deploy
**Requirement**: Must invest in monitoring, service mesh, distributed tracing

### Decision Rule
```
If (team_size == 1 && endpoints < 20) → Monolith
If (team_size >= 3 || endpoints >= 50) → Atomic Services
If (team_size >= 5 && compliance_required) → Enterprise Microservices
```

---

## Classification Output | 分类输出

Every project start must produce this summary:

```markdown
## Project Classification

| Dimension | Value | Rationale |
|---|---|---|
| Origin | Greenfield | New project, no existing code |
| Quality | AI-Native | Production SaaS, real users |
| Deploy Targets | Web + Mobile | Web SPA now, mobile within 3 months |
| Scale | Atomic Services | Team of 3, expecting 30+ endpoints |

### Implications
- Architecture: Archetype B (Atomic Services)
- Skills: All core + governance
- Steps: Full 13-step with all gates
- DB: Schema-per-service
- API: REST + GraphQL (OpenAPI-first)
- Mobile: React Native with same API
```

---

## Integration | 集成

| Entry Point | Action |
|---|---|
| `ai-chief-planner` Phase 1 | Run classifier before any planning |
| `ai-rule-dispatcher` | Use classification to select skill set |
| `ai-architect-governor` | Use classification to select archetype |
| `ai-atomic-architect` | Apply based on Quality Target and Scale |

---

## Guardrails | 防护规则

- **Classify before you code** — never start implementation without classification
- **Brownfield ≠ free-for-all** — existing code has conventions; respect them
- **Rapid prototype ≠ garbage** — rapid means simpler, not worse
- **Default to AI-Native** — if unclear, choose AI-Native (easier to downgrade than upgrade)
- **Re-classify when scope changes** — a prototype that becomes a product needs re-classification

## Maturity | 成熟度

**Stage**: New — Created to fill the project inception decision gap.

## Evolution History | 进化记录

- v1.0.0: Initial creation — 4 dimensions, 3 quality targets, classification output template
