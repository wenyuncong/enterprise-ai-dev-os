---
name: ai-command-executor
description: "Standardize command execution, environment checks, tool discovery, approved script usage, runtime diagnosis, logs, service start/stop, build verification, and evidence capture. Use before shell/CLI work, runtime debugging, or tool installation decisions."
---

# ai-command-executor — Standardized Command Execution Engine

## Purpose | 用途

Turn execution requests into standardized, auditable command runs:

- Approved entrypoint selection (prefer existing scripts)
- Check-before-execute verification
- Script/command execution records
- Root-cause diagnosis from logs and output
- Safest next-step recommendations

This skill is for **execution and diagnosis**, not task routing or project scheduling.

## Core Rule | 核心规则

**Do not invent a new command flow when the project already provides an approved entrypoint.**

Execution priority:
1. Project-standard scripts (e.g., `scripts/bat/`, `scripts/ps1/`, `scripts/py/`)
2. Reusable helper scripts within the project
3. Documented one-liners with clear justification
4. Custom shell commands only with explicit reason and record

---

## Check-Before-Execute Protocol | 执行前检查

Before running any command, verify:

1. **Goal**: Which exact outcome does the user want?
2. **Approved script**: Which existing script already covers this?
3. **Environment facts**: What must be true before execution?

| Check | Example | Command |
|---|---|---|
| Git availability | Is git on PATH? | `where git` or check known paths |
| Node.js version | Correct Node for tool? | `node --version` |
| Java version | Correct JDK? | `java --version` |
| Port availability | Is port already bound? | `netstat -an` or equivalent |
| Process status | Is service already running? | `ps aux` or equivalent |
| Disk space | Enough space for build? | `df -h` or equivalent |

---

## Standard Workflow | 标准工作流

### Phase 1: Environment Verification
- Verify tool dependencies are available
- **If any tool is missing → invoke i-tool-bootstrapper to auto-install**
- Check port availability before starting services
- Confirm working directory and permissions

### Phase 2: Script Selection
- Check `scripts/` directory for existing solutions
- Prefer project-standard scripts over ad-hoc commands
- If no script exists, save the command as a new reusable script

### Phase 3: Execution
- Run the command with appropriate flags
- Capture stdout and stderr separately
- Record execution time and exit code

### Phase 4: Diagnosis
- Parse output for known error patterns
- Check logs for additional context
- Classify: environment issue, code issue, or configuration issue

### Phase 5: Recommendation
- If successful: report result, suggest verification step
- If failed: classify root cause, suggest fix, provide exact commands

---

## Working Tree Gate | 工作树闸门

Before starting a new task and before committing a completed task, verify the working tree state:

```
1. Check for unexpected dirty files
2. Stage only current task's files
3. Verify staged changes with diff
4. Classify untracked files as evidence, temp, or misplaced
```

**Rules**:
- Do not use whole-repository cleanup for unrelated dirty files
- Stage only current task files, verify before commit
- Treat untracked files under documented directories as potentially valid evidence
- If unrelated dirty files block execution, stash them explicitly with descriptive message

---

## Command Category Reference | 命令分类参考

| Category | Typical Script Prefix | Example |
|---|---|---|
| Build/Compile | `build-*`, `compile-*` | `build-backend.ps1`, `npm run build` |
| Service Start/Stop | `start-*`, `stop-*` | `start-server.ps1`, `docker-compose up` |
| Database | `db-*`, `migrate-*` | `db-migrate.sh`, `mysql -e "..."` |
| Test | `test-*`, `run-tests-*` | `run-tests.sh`, `npm test` |
| Deploy | `deploy-*`, `release-*` | `deploy-staging.sh` |
| Health Check | `health-*`, `check-*` | `health-check.sh`, `curl /health` |

---

## Guardrails | 防护规则

- Do not run parallel builds in the same workspace (shared output directories)
- Do not assume a service is not running without checking ports first
- Do not trust a health endpoint alone if an old process may still be bound
- Do not skip environment verification when a previous step failed
- Do not use destructive commands (`reset --hard`, `clean -fdx`) without explicit user confirmation

## Maturity | 成熟度

**Stage**: Effective — Extracted from 28KB of enterprise command execution workflows with environment-specific diagnostics.


## Integration with ai-tool-bootstrapper | 工具自动引导集成

When environment verification detects a missing tool, do not fail. Instead:

1. Report: "Tool X not found"
2. Invoke i-tool-bootstrapper to auto-install X
3. Re-verify after installation
4. Continue execution

This creates a self-healing environment where missing tools are acquired automatically rather than blocking development.

---

## Evolution History | 进化记录

- v1.0.0: Extracted from gerp-command-executor (28KB original)
- v1.1.0: Generalized to universal command execution patterns
- Source: Daily enterprise development environments with multi-service orchestration

