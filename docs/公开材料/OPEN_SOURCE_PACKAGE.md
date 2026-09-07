# 开源发布包边界

## 1. 完整开源方法论内核

本仓库不是只发布理念摘要或少量示例，而是公开完整、可迁移的方法论内核：

- `README.md`
- `.editorconfig`
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
- `docs/公开材料/INSTALL.md`
- `docs/公开材料/ROADMAP.md`
- `docs/公开材料/CUSTOMER_INVESTOR_VALUE.md`
- `docs/公开材料/VALUE_EVIDENCE.md`
- `docs/公开材料/RULE_RUNTIME_LITE.md`
- `docs/公开材料/OPEN_SOURCE_READINESS.md`
- `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- `docs/全项目总控/DISCLOSURE_BOUNDARY.md`
- `scripts/py/audit_methodology.py`
- `scripts/py/discover_tools.py`
- `scripts/py/env_check.py`
- `scripts/py/score_ai_development_readiness.py`
- `scripts/py/tool_registry.py`
- `scripts/ps1/install.ps1`
- `scripts/sh/install.sh`
- `scripts/js/cli.mjs`
- `tools/deploy.ps1`
- `tools/adapters.json`
- `package.json`
- `LICENSE`
- `NOTICE`
- `.github/`

上述内容可以作为一个可安装、可审计、可扩展的完整开源方法论包发布。方法论的完整性不意味着公开任何真实项目的生产资料。

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

## 3. 保持私有的真实交付资产

以下内容继续保持私有，即使它们能帮助解释方法论：

- 客户、租户、账号、联系方式和部署信息；
- ERP 或其他真实项目源代码、数据库、迁移历史和生产配置；
- 未脱敏业务流程、真实单据、报表、日志、截图和测试证据；
- 商业策略、报价、客户名单、销售过程和内部优先级；
- 未经泛化的项目专属实现细节；
- 本机工具状态、密钥、缓存和本地路径。

## 4. 公开前检查

发布前必须运行：

```powershell
py scripts/py/audit_methodology.py --project-root .
git status --short
git check-ignore -v docs/内部商业化 docs/商业化 reference 备用 verification-demo tools/tool-registry.json
```

如果 `git status --short` 出现内部目录、原始素材目录或本机配置文件，停止发布。

## 5. 推荐仓库策略

仓库可以作为公开的 Open-Core Methodology 项目运行。公开前仍需完成一次 GitHub UI 历史和当前分支复核；该复核针对敏感资料，不再要求把方法论内核压缩成简化版。

公开仓库名称建议：

- `enterprise-ai-dev-os`
- `dream-enterprise-ai-os`
- `ai-development-determinism-os`

公开定位建议：

> Enterprise AI Development OS: the complete portable methodology kernel for governed AI-native delivery, including rules, skills, templates, schemas, audits, adapters, and evolution loops.
