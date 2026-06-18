# Command Entry Points and Diagnosis Map

## 1. Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/.trae/rules/project_rules.md`
- current task pack or execution record under `{PROJECT_ROOT}/docs/全项目总控/` or `{PROJECT_ROOT}/docs/业务流程全案/`

## 2. Approved entrypoint priority

1. `{PROJECT_ROOT}/scripts/bat/gerp.bat`
2. direct batch scripts under `{PROJECT_ROOT}/scripts/bat`
3. helper scripts under `{PROJECT_ROOT}/scripts/ps1`
4. custom shell command only when the above do not cover the need

## 3. Scenario-to-entrypoint matrix

| Scenario | First entrypoint | First checks | Evidence |
| --- | --- | --- | --- |
| MySQL connectivity | `scripts/bat/gerp.bat mysql test` | DB host / account / process | command result |
| SQL read-only check | `scripts/bat/gerp.bat mysql exec gerp_enterprise "SHOW TABLES;"` | schema / table / field existence | SQL output |
| SQL write execution | exact SQL file under `database/` plus matching MySQL entrypoint | target schema, backup need, script path | SQL file + execution output |
| Backend compile | `scripts/bat/gerp.bat maven compile [module]` | module path, `pom.xml`, dependency state | compile output |
| Backend package | `scripts/bat/maven-package.bat` | module target, package path | package output |
| Backend start | `scripts/bat/start-service.bat [service]` | port / process / config / delayed-restart rule | runtime log |
| Frontend dev | `scripts/bat/frontend-dev.bat [app]` | app path, port, node state | dev output |
| Frontend build | `scripts/bat/frontend-build.bat [app]` | app path, dependency state | build output |
| Runtime diagnosis | existing script + matching log path | log file existence, first real error | log excerpt summary |

## 4. Common direct scripts

- `{PROJECT_ROOT}/scripts/bat/mysql-test.bat`
- `{PROJECT_ROOT}/scripts/bat/mysql-exec.bat`
- `{PROJECT_ROOT}/scripts/bat/maven-compile.bat`
- `{PROJECT_ROOT}/scripts/bat/maven-package.bat`
- `{PROJECT_ROOT}/scripts/bat/start-service.bat`
- `{PROJECT_ROOT}/scripts/bat/frontend-dev.bat`
- `{PROJECT_ROOT}/scripts/bat/frontend-build.bat`

## 5. Common helper scripts

- `{PROJECT_ROOT}/scripts/ps1/mysql-functions.ps1`
- `{PROJECT_ROOT}/scripts/ps1/maven-functions.ps1`
- `{PROJECT_ROOT}/scripts/ps1/frontend-functions.ps1`

## 6. Common log locations

- `{PROJECT_ROOT}/scripts/bat/logs`
- `{PROJECT_ROOT}/scripts/bat/logs/error`
- `{PROJECT_ROOT}/scripts/logs`
- module-local `target` or runtime log directories when explicitly configured

## 7. First-check matrix

| Check type | Typical actions |
| --- | --- |
| DB | `SHOW TABLES`, `DESCRIBE`, row count, schema confirmation |
| Code | `Test-Path`, `rg`, config read, module path confirmation |
| Runtime | port, process, PID, log file existence |
| Task boundary | current task pack, delayed restart rule, hot-file conflict |

## 8. Diagnosis categories

| Category | Typical symptom | Required next step |
| --- | --- | --- |
| Environment issue | command not found, port occupied, missing runtime | fix path / port / process |
| Script issue | approved script path wrong or parameter mismatch | correct script usage or script asset |
| Dependency issue | package missing, toolchain not ready | restore dependency or environment |
| Compile issue | compiler error, unresolved symbol | inspect first compile error and target files |
| Runtime issue | service starts then fails, HTTP 500 | inspect runtime log and failing stack |
| Data / config issue | wrong schema, missing config, bad sample | verify DB/config and patch source |

## 9. Git path reminder

If `git` is not recognized in PowerShell, check:

- `where.exe git`
- registered tool paths in `tools/tool-registry.json`
- package-manager install records

Do not conclude “Git not installed” before checking path resolution and the local tool registry.
