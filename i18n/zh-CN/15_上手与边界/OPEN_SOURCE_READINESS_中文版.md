# 开源就绪度 | Open Source Readiness

> **源文件**：docs/公开材料/OPEN_SOURCE_READINESS.md
> **源版本**：未标注（源文件标注 Last reviewed: 2026-09-07）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

---

本文档记录 Open-Core Methodology 的边界：完整、可移植的方法论内核是公开的，而真实交付资产与敏感的运营证据保持私有。

## 当前决策 | Current Decision

在完成最后一轮 GitHub UI 复核与敏感历史复核之后，当前受 Git 跟踪的仓库适合作为公开 GitHub 仓库。

可公开范围的含义是：

- 不包含原始项目归档
- 不包含私有商业化笔记
- 不包含过程回写或测试证据归档
- 不包含本地工具注册表
- 不包含生成的适配器目录
- 受跟踪文件中不含硬编码的旧项目路径残留
- Apache-2.0 许可证文件与包元数据齐备
- 方法论审计与开源边界检查通过

## 当前可公开 | Public-Ready Now

| 领域 | 路径 | 决策 |
|---|---|---|
| 仓库入口 | `README.md`、`AGENTS.md`、`CLAUDE.md`、`package.json` | 可公开 |
| 许可证 | `LICENSE`、`NOTICE`、`package.json` license 字段 | 在 Apache-2.0 下可公开 |
| 规则 | `rules/AGENTS.md`、`lite/rules/AGENTS.md` | 可公开 |
| 正式 Skill | `skills/`、`skills/SKILL_MANIFEST.json` | 可公开 |
| 方法论正文 | `methodology/` | 可公开 |
| 文档模板 | `docs/_templates/`、`lite/docs/_templates/` | 可公开 |
| 公开文档 | `docs/公开材料/`、`docs/COMPATIBILITY.md`、`docs/TOOL_ADAPTERS.md` | 可公开 |
| 总控文档 | `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`、`AI_NATIVE_CANDIDATE_CAPABILITY_PROTOCOL.md`、`DISCLOSURE_BOUNDARY.md`、`MASTER_INDEX.md`、`TASK_BACKLOG.md`、`schemas/governance/` | 可公开 |
| lite 包 | `lite/` | 可公开 |
| 审计脚本 | `scripts/py/audit_methodology.py`、`audit_governance_contracts.py`、`audit_reference_links.py`、`check_open_source_boundary.py`、`discover_tools.py`、`env_check.py`、`score_ai_development_readiness.py`、`tool_registry.py` | 可公开 |
| CLI | `scripts/js/cli.mjs` | 可公开 |
| 工具适配器 | `tools/adapters.json`、`tools/deploy.ps1` | 作为适配器生成器可公开，生成产物不可公开 |
| 网站 | `site/`、`.github/workflows/pages.yml` | 可公开的 GitHub Pages 网站 |
| 社区 | `CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`SECURITY.md`、`SUPPORT.md`、`GOVERNANCE.md`、`.github/ISSUE_TEMPLATE/`、`.github/PULL_REQUEST_TEMPLATE.md`、`.github/workflows/ci.yml` | 可公开的社区工作流 |

## 必须保持私有 | Must Stay Private

| 领域 | 路径 | 原因 |
|---|---|---|
| 私有策略 | `docs/内部商业化/`、`docs/商业化/` | 私有定位、变现与决策笔记 |
| 过程日志 | `docs/每日调研回写/`、`docs/测试验收报告/` | 工作记录与本地证据 |
| 发布与内部分析 | `docs/LAUNCH_KIT.md`、`docs/ERP_TERM_AUDIT.md`、`docs/AB_EXPERIMENT.md` | 内部复核与发布计划材料 |
| 原始源码归档 | `备用/`、`reference/` | 未脱敏的源码材料与历史项目参考 |
| 演示项目 | `verification-demo/` | 本地验证项目，不是公开产品界面 |
| 工具生成产物 | `.agents/`、`.trae/`、`.qoder/`、`.claude/`、`.codebuddy/`、`.cursor/`、`.github/copilot-instructions.md`、`.github/instructions/enterprise-ai-dev-os.instructions.md` | 生成的适配器文件，不是正式源 |
| 本地状态 | `tools/tool-registry.json`、`temp/`、`tmp/`、`logs/`、各类缓存 | 本地路径、生成状态或缓存文件 |

## 暂时保留 | Temporarily Hold Back

| 事项 | 原因 |
|---|---|
| WorkBuddy 适配器声明 | 尚未验证出可靠的规则路径契约 |
| Trae Solo 适配器声明 | 需要单独的产品/版本验证 |
| 通义灵码适配器声明 | 需要实机验证规则加载与 Skill 加载 |
| 生成的适配器产物 | 应当由 `tools/deploy.ps1` 生成，不得作为源码提交 |
| 真实项目案例研究 | 需要单独脱敏并完成法务/商务复核 |
| Rule Runtime Lite 实现 | 公开文档只描述设计边界；禁止声称运行时引擎已实现 |
| 量化改进声明 | 在发布百分比之前，先使用 `docs/公开材料/VALUE_EVIDENCE.md` |
| 通用 AI 运行时、调度器或命令沙箱 | 本仓库不包含；目标项目可以自行实现各自的管控 |

## 公开发布前必须执行的检查 | Required Checks Before Public Release

在仓库根目录运行以下命令：

```powershell
py scripts/py/audit_methodology.py --project-root .
py scripts/py/audit_governance_contracts.py --project-root .
py scripts/py/audit_reference_links.py --project-root .
py scripts/py/check_open_source_boundary.py --project-root .
py scripts/py/score_ai_development_readiness.py --project-root .
powershell -NoProfile -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -DryRun
git status --short --ignored
```

预期结果：

- 方法论审计：`PASS`
- 开源边界检查：`PASS`
- 就绪度评分：`100/100`，这是结构性自检分，不是交付效果分
- 适配器部署 dry-run：无错误
- 被忽略的私有目录以 `!!` 出现，而不是作为受跟踪或已暂存文件出现

## GitHub UI 复核清单 | GitHub UI Review Checklist

在把 GitHub 仓库从私有改为公开之前，在 GitHub UI 中检索旧版带日期的总控文档名、历史源码仓库名、Windows 绝对盘符路径、私有策略目录名、发布套件文件名、本地验证项目名、原始归档名，以及未脱敏的案例研究路径。

除 `.gitignore` 或开源边界文档这类预期中的边界清单之外，所有检索都不应返回任何受跟踪的公开内容。

## 发布建议 | Release Recommendation

推荐的首次公开发布姿态：

- 作为完整、可移植的方法论与适配器框架发布
- 把仓库描述为 Open-Core Methodology：完整的方法论内核开源，而真实交付证据保持私有
- 私有策略与案例证据保持私有
- 在出现可测量的公开证据之前，价值类声明一律指向 `docs/公开材料/VALUE_EVIDENCE.md`
- 把 Rule Runtime Lite 描述为未来方向，而不是已经实现的引擎
- 暂不声称已验证支持 WorkBuddy、Trae Solo 或未经测试的地区变体
- 继续以 `tools/adapters.json` 作为公开兼容性声明的唯一来源
- 在把仓库切换为公开之后，启用 GitHub Pages 并以 GitHub Actions 作为来源，使 `site/` 由 `.github/workflows/pages.yml` 发布
- 启用 GitHub Discussions，用于问答、想法、工具兼容性与展示类讨论
