---
name: ai-project-onboarding-and-skill-integration
description: "Safely onboard the methodology into a new or existing project by detecting its technology profile, preserving project-owned assets, staging external skills in quarantine, governing candidate compatibility, and generating an incremental knowledge index. Use before copying methodology assets, importing skills, or establishing a project knowledge base."
metadata:
  requires:
    bins: [python]
    scope: universal
    declared-by: enterprise-ai-dev-os
---

## Rule

External skills, scripts, and references are untrusted until their source, license, revision, compatibility, and structure are recorded and reviewed. Never overwrite an existing project asset by default, never activate a candidate directly from GitHub, and never treat a knowledge index as runtime business truth.

# ai-project-onboarding-and-skill-integration - Controlled Methodology Adoption

## Purpose

Provide the missing adoption chain for a project that receives this methodology:

```text
Detect -> Discover -> Evaluate -> Plan -> Stage -> Merge -> Govern -> Index -> Verify
```

This skill separates methodology assets from project-owned source, imported candidates from active skills, and discovery knowledge from the project's runtime/data truth.

## When to Use

- Before copying the methodology, rules, skills, scripts, or templates into an existing project.
- When selecting stack-specific skills for a detected language, framework, database, or deployment target.
- When considering a GitHub-hosted skill, script, or reference implementation.
- When the project needs a searchable technical knowledge index.
- After a methodology import, upgrade, or candidate-skill review.

## Ownership and Locations

| Location | Purpose | Callable |
| --- | --- | --- |
| `skills/core/`, `skills/governance/`, `skills/tech/` | Verified methodology skills registered in the manifest | Yes |
| `skills/project/` | Project-private patterns with an explicit project owner | Only when the project routes to them |
| `skills/candidates/` | Imported external material under evaluation | No |
| `skills/quarantine/` | Rejected, incomplete, incompatible, or unsafe material | No |
| `knowledge/` | Generated technical discovery indexes and governance reports | No |

Do not place an unreviewed GitHub clone under an active skill root. Do not merge a project-private rule into a portable core skill without repeated, cross-project evidence.

## Workflow

### 1. Detect and Discover

Run the existing project tool discovery first, then generate the technology profile and index:

```text
py scripts/py/discover_tools.py <project-root> --by-purpose
py scripts/py/project_onboarding.py inspect --project-root <project-root>
```

The profile records detected language, framework, package manager, database, tool inventory, and existing skill states. It selects only relevant `skills/tech/` candidates; it does not invent a stack from filenames alone.

### 2. Evaluate External Sources

Use official vendor documentation and official upstream repositories first. A GitHub candidate must have:

1. explicit `github.com/owner/repository` source;
2. pinned ref and resolved commit;
3. discoverable license file and compatible license decision;
4. maintenance/version compatibility assessment;
5. no secrets, binaries, install hooks, or executable code accepted without separate review;
6. an integration decision explaining reuse, extension, or rejection.

Study code and patterns; do not copy an incompatible implementation into the project.

### 3. Plan Before Copying

Generate a non-mutating installation plan:

```text
py scripts/py/project_onboarding.py preflight --source-root <methodology-root> --project-root <target-root> --mode lite
```

The plan labels each asset as `add`, `same`, or `conflict`. Default policy is add-only. Conflicts require an explicit merge/overwrite decision, a file-level rollback path, and preservation of the target's existing asset.

Copy selection is proportional:

| Target type | Copy |
| --- | --- |
| Lite adoption | Entry rules, templates, backlog scaffold |
| Full adoption | Core/governance skills, selected technology skills, audit scripts, adapters |
| Existing mature project | Only gaps approved by preflight; reuse existing scripts before adding replacements |

### 4. Stage, Do Not Activate

Stage a GitHub candidate only with an explicit revision:

```text
py scripts/py/project_onboarding.py stage-github --project-root <target-root> --name <candidate-name> --repository https://github.com/<owner>/<repository> --ref <tag-or-branch>
```

The command writes to `skills/candidates/<candidate-name>/` and records `skill-source-lock.json`. Staging is not activation.

### 5. Govern and Integrate

Run candidate governance and the existing methodology audits:

```text
py scripts/py/project_onboarding.py govern-candidates --project-root <target-root>
py scripts/py/audit_methodology.py --project-root <target-root>
py scripts/py/audit_skill_health.py --project-root <target-root>
```

Candidates with missing provenance, invalid frontmatter, missing skill entrypoint, incompatible licensing, or unreviewed executable content remain quarantined. Only after a project owner records the decision may a reviewed skill be moved into its intended root and registered in `skills/SKILL_MANIFEST.json`.

### 6. Maintain the Knowledge Index

Run an initial bounded scan during onboarding. Refresh incrementally after meaningful source, dependency, architecture, skill, or script changes. Do not force a full scan on every session.

The index supports discovery: it is not authorization, a database readback, a command provider, or runtime evidence.

## Verification

Before declaring adoption ready:

- [ ] Project technology profile and existing-tool catalog were generated.
- [ ] Copy plan contains no unreviewed overwrite.
- [ ] External candidates have source lock, commit, license decision, and review state.
- [ ] Candidate governance has no activation blocker.
- [ ] `audit_methodology.py` and `audit_skill_health.py` pass for activated assets.
- [ ] Knowledge index exists and identifies its bounded/incremental scan state.
- [ ] The product/project owner accepts the declared scope and non-goals.

## Guardrails

- Never use `-Force` or recursive deletion to resolve a preflight conflict.
- Never import all GitHub skills simply because a language was detected.
- Never make candidate content callable before provenance and governance pass.
- Never overwrite project-owned rules, scripts, or skills merely to make a methodology install look complete.
- Never delete obsolete candidates automatically; quarantine and record the decision.
- Never use the knowledge index as a replacement for actual runtime, authorization, API, database, or business-flow evidence.

## Integration

| Need | Primary skill |
| --- | --- |
| Project stack and origin | `ai-project-classifier` |
| Existing-project patterns and tools | `ai-brownfield-analyzer` |
| External reference research | `ai-reference-researcher` |
| Existing library selection | `ai-library-first` |
| Skill overlap and health | `ai-skill-governor` |
| Evidence-backed evolution | `ai-skill-evolver` |

## Evolution History

- v1.0.0: Added controlled methodology adoption, external candidate quarantine, safe copy preflight, post-copy governance, and bounded knowledge indexing.
