# 开源发布包边界

## 1. 可进入公开仓库

建议首版公开仓库只包含：

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`（如确认内容与 AGENTS 同步且无内部材料）
- `rules/AGENTS.md`
- `skills/`
- `methodology/`
- `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- `docs/全项目总控/DISCLOSURE_BOUNDARY.md`
- `docs/全项目总控/MASTER_INDEX.md`
- `docs/公开材料/`
- `docs/_templates/`
- `docs/COMPATIBILITY.md`
- `docs/TOOL_ADAPTERS.md`
- `docs/公开材料/OPEN_SOURCE_READINESS.md`
- `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- `docs/全项目总控/DISCLOSURE_BOUNDARY.md`
- `scripts/py/audit_methodology.py`
- `scripts/py/discover_tools.py`
- `scripts/py/env_check.py`
- `scripts/py/score_ai_development_readiness.py`
- `scripts/py/tool_registry.py`
- `scripts/js/cli.mjs`
- `tools/deploy.ps1`
- `tools/adapters.json`
- `package.json`

## 2. 不进入公开仓库

以下目录和文件默认不公开：

- `docs/内部商业化/`
- `docs/商业化/`
- `docs/每日调研回写/`
- `docs/测试验收报告/`
- `docs/LAUNCH_KIT.md`
- `docs/ERP_TERM_AUDIT.md`
- `docs/AB_EXPERIMENT.md`
- `reference/`
- `备用/`
- `verification-demo/`
- `.agents/`
- `.claude/`
- `.codebuddy/`
- `.qoder/`
- `.trae/`
- `tools/tool-registry.json`
- `temp/`, `tmp/`, `logs/`
- 任何私有策略、真实案例、真实部署、联系方式、未脱敏证据或过程记录

## 3. 公开前检查

发布前必须运行：

```powershell
py scripts/py/audit_methodology.py --project-root .
git status --short
git check-ignore -v docs/内部商业化 docs/商业化 reference 备用 verification-demo tools/tool-registry.json
```

如果 `git status --short` 出现内部目录、原始素材目录或本机配置文件，停止发布。

## 4. 推荐仓库策略

首仓建议创建为 private，确认文件边界无误后再改 public。

公开仓库名称建议：

- `enterprise-ai-dev-os`
- `dream-enterprise-ai-os`
- `ai-development-determinism-os`

首版开源定位建议：

> Enterprise AI Development OS: rules, skills, documentation memory, audit gates, and evolution loop for deterministic AI-assisted engineering.
