---
name: ai-competitor-analyst
description: "Research competitors, market references, product positioning, benchmark gaps, and decision implications while separating facts, inference, and project choices. Use for market analysis, product strategy, pricing, feature comparison, or investor-facing positioning."
---

# ai-competitor-analyst — Competitive Benchmarking & Market Research Engine

## Purpose | 用途

Research and compare products, features, and market positioning:

- Competitor feature benchmarking
- Market-facing feature mapping
- Product packaging and version strategy analysis
- Technology stack comparison
- Industry trend analysis

This skill is for **competitive research and benchmark**, not product strategy decisions.

---

## Core Rule | 核心规则

**Benchmark against actual product behavior, not marketing materials.**

Verify competitor claims by:
- Using the product directly (trial/demo)
- Reading technical documentation
- Checking community forums for real user feedback
- Comparing public API/architecture when available

---

## Benchmark Framework | 对标框架

### 1. Feature Matrix
```markdown
| Feature | Our Product | Competitor A | Competitor B | Competitor C |
|---|---|---|---|---|
| [Category]: [Feature] | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ |
```

Rating:
- ✅ Full support, production-grade
- ⚠️ Partial support or in development
- ❌ Not available

### 2. Pricing & Packaging
```markdown
| Dimension | Our Product | Competitor A | Competitor B |
|---|---|---|---|
| Free Tier | [Details] | [Details] | [Details] |
| Entry Price | [Price] | [Price] | [Price] |
| Enterprise | [Price] | [Price] | [Price] |
| Pricing Model | [Model] | [Model] | [Model] |
```

### 3. Technology & Architecture
```markdown
| Dimension | Our Product | Competitor A | Competitor B |
|---|---|---|---|
| Tech Stack | [Stack] | [Stack] | [Stack] |
| Deployment | [Options] | [Options] | [Options] |
| API/SDK | [Available] | [Available] | [Available] |
| Multi-tenancy | [Model] | [Model] | [Model] |
```

### 4. Market Positioning
```markdown
| Dimension | Our Product | Competitor A | Competitor B |
|---|---|---|---|
| Target Segment | [Segment] | [Segment] | [Segment] |
| Key Differentiator | [Diff] | [Diff] | [Diff] |
| Geographic Focus | [Region] | [Region] | [Region] |
| GTM Strategy | [Strategy] | [Strategy] | [Strategy] |
```

---

## Research Methodology | 研究方法

### Primary Research (Recommended)
1. **Product Trial**: Sign up for competitor trial/demo
2. **Documentation Review**: Read official docs, API references
3. **Community Analysis**: Review forums, GitHub issues, Stack Overflow
4. **Customer Interviews**: Talk to users of competitor products

### Secondary Research
1. **Review Sites**: G2, Capterra, TrustRadius
2. **Industry Reports**: Gartner, Forrester, IDC
3. **Technical Blogs**: Engineering blogs, case studies
4. **Conference Talks**: Recent presentations, roadmap reveals

---

## Benchmark Decision Template | 对标决策模板

```markdown
## Benchmark: [Feature/Product Area]

### Research Date
[YYYY-MM-DD]

### Research Method
- [ ] Product trial
- [ ] Documentation review
- [ ] Community analysis
- [ ] Secondary sources

### Key Findings
1. [Finding 1] — Impact: [High/Medium/Low]
2. [Finding 2] — Impact: [High/Medium/Low]

### Gap Analysis
| Gap | Severity | Competitors With This | Recommended Action |
|---|---|---|---|

### Decision
[Build / Buy / Partner / Defer]

### Timeline
[Immediate / Q1 / Q2 / Future]
```

---

## Standard Workflow | 标准工作流

1. **Define Scope**: Which product area or feature to benchmark?
2. **Identify Competitors**: Which 3-5 competitors to compare?
3. **Research**: Collect data using primary and secondary methods
4. **Score**: Fill in the benchmark framework tables
5. **Analyze Gaps**: Identify strengths, weaknesses, opportunities
6. **Recommend**: Produce concrete action recommendations

---

## Guardrails | 防护规则

- Do not benchmark against marketing claims — verify with actual product usage
- Do not compare against outdated competitor versions
- Do not ignore competitor community/ecosystem strength
- Do not skip pricing model analysis — it's often the key differentiator
- Do not produce recommendations without evidence in the benchmark tables

## Maturity | 成熟度

**Stage**: Effective — Extracted from enterprise ERP competitive analysis workflows.

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-competitor-analyst
- v1.1.0: Generalized with universal benchmark framework
