# Changelog

本项目的显著变更记录。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，日期为 Asia/Shanghai。

## 2026-11-08 — 方法论本体治理回流 + 换电脑位置关联 + 断链清零（v2.7.0）

### Added

- **方法论本体治理回流（`27a089c`，128 文件 +3395/-2059）**：新增 `methodology/11_通用架构与治理模式库.md`（16 个中立模式，覆盖数据库/架构/前端等治理层——治理层本身即方法论的一部分）；新增可执行回流驱动 `scripts/py/reconcile_writeback.py`（check / mark-resolved）与每周一 10:23 本地定时对账任务；中立适配初始化器 `scripts/py/project_onboarding.py` 扩展架构/AI 工具/Git 平台检测与 `bind-remote` 推送绑定，两阶段扫描避免大项目目录饿死。
- **断链审计器五分类**：`audit_reference_links.py` 由三分类扩为五分类，新增 `excluded_asset`（gitignore 排除的内部材料）、`reference_context`（参考项目/目标项目语境路径），并以逻辑路径归一化正确处理带/不带斜杠的同一目录。
- **论文公式代码化（技能库即代码）**：新增纯标准库测量模块 `scripts/py/evidence_metrics.py`，把论文与三模型报告中的公式实现为可调用函数——Wilson 区间、Jeffreys Beta 后验（含正则化不完全 Beta `betainc` 与分位数 `beta_ppf`）、样本量功效 n=z²p(1−p)/d²、证据分级 E0–E3、数据时钟裁决、缓存/成本构念；新增治理技能 `skills/governance/ai-evidence-metrics/`（SKILL.md 含公式→函数映射与 CLI/import 用法），注册进 `SKILL_MANIFEST.json`（official 51→52、governance 13→14）。
- **方法论新增 6A/6B/6C**：`rules/AGENTS.md` 增加治理机制准入判据（B/V/E/O）、证据门测量与统计纪律、独立审计拓扑，并写入代码模块/技能指针。

### Changed / Fixed

- **换电脑位置关联（#9）**：`scan_skill_health.py` 与 `skill_requires_governor.py` 中按盘符硬编码的方法论技能归属判断，改为基于 `__file__` 动态推导（`METHODOLOGY_SKILLS_ROOT` + normcase/abspath 比较，兼容盘符/斜杠/大小写），换盘符不再失效。
- **writeback bridge 空待办治理（#10）**：删除生成快照中三条无人执行的空 checkbox，改为说明本地证据快照性质与 reconcile 回流机制；移除硬编码旧盘符、零引用的死脚本 `writeback_evidence.py`。
- **断链清零（#11）**：当前生效文档的 prose 斜杠词组改为 `and` 表述；按需目录（`skills/candidates|quarantine|project`、`docs/发布闭环`）、目标项目旁路脚本与模板示例路径纳入白名单；历史归档（`docs/技能治理/`、90_校验历史清单）不参与链接审计。`missing_asset` 由 100 降至 0，`--strict-missing` 门控通过。
- **版本对齐**：`package.json` 与规则源版本标注统一为 2.7.0。

### Verification

- 断链审计 `missing_asset=0`、`--strict-missing` 退出码 0；方法论审计、规则 lint、i18n 校验全绿（英文源改动后重签 baseline）。
- `test_evidence_metrics.py` 20 个用例全部通过；`--demo` 复现论文真实数字（37/655=5.65%、127/148=85.8%、69/71=97.2%），Wilson 与 Jeffreys 区间互证。

## 2026-09-24 — 技能治理：全量语义审查 + 前置条件声明化

### Added

- **全量 264 技能逐篇语义审查**：对系统库 114 + 用户库 99 + 方法论库 51 的全部 `SKILL.md` 原文逐篇精读，按四个维度判定（逻辑自洽 / 无明显歧义 / 运行时可执行 / 能力匹配），结论 **PASS 197 / WARN 67 / FAIL 0**（语义层零 FAIL）。产物位于 `docs/技能治理/`（MD + CSV + JSONL）。(`2f3b83a`)
- **技能前置条件声明化（skill-requirements/v1）**：
  - 新增治理脚本 `scripts/py/skill_requires_governor.py`（`scan` 校验 / `--fix` 文本级安全注入，保留原 frontmatter、BOM、CRLF；幂等可重复运行）。
  - 新增依赖映射表 `scripts/py/skill_requirements_map.json`（114 条 + schema 说明）。
  - 为技能 frontmatter 注入 `metadata.requires`（`bins` / `libs` / `env` / `path-vars` / `scope` / `declared-by`），让技能可用性在**加载前即可判定**。
  - **豆包 app 电脑客户端**：对其实际加载的 `.skills` / `.user_skills` 运行时库中 63 篇 WARN（系统 32 + 用户 31）完成前置条件补齐。
  - **豆包模型匹配**：补齐后 frontmatter 为合法 YAML，`name` / `description` / `metadata.requires` 结构完整；豆包模型按 `description` 做技能语义匹配后，可据 `requires` 判定 bins/env/scope 是否满足，把“加载不了”转化为“可定位的前置条件缺口”（缺失即明确反馈，而非静默降级）。
- **技能健康扫描工具** `scripts/py/scan_skill_health.py`：覆盖 3 个技能库，检测 frontmatter/正文可读性、references、命令、Python 库与平台差异，输出 JSONL。(`509f50c`)
- 整改报告：`docs/技能治理/2026-09-24_前置条件声明化整改报告.md`。

### Changed / Fixed

- **PATH 外工具检测**：`scan_skill_health.py` 新增 `KNOWN_INSTALL_LOCATIONS` 强制探测表与 `cmds_installed_no_path` 分类；`env_check.py` 补 codex / flutter / playwright 的 Windows 路径。实测命中“已安装但未加入 PATH”的 codex (0.155.0) / flutter (3.24.0) / playwright (1.63.0)，修正“工具已装却被判缺失”的盲区。(`752e409`)
- 修复 `verifier-hub` 的 `lib/xlsx.py` 中 argparse 裸 `%` 未转义（→ `%%`），xlsx 家族校验恢复。(`509f50c`)

### Verification

- 114 篇注入文件 PyYAML 解析全部合法、字段值与映射表一致（0 错误 / 0 不一致）。
- 63 篇运行时技能改前备份 vs 改后正文（frontmatter 之外）完全一致；BOM / CRLF 字节级保留（0 差异）。
- 幂等：重跑 scan 为 declared 114 / missing 0。
- 验证边界：文件层 / YAML 层校验通过；豆包 app 内实际技能路由与命令执行需客户端重新加载技能库后确认。

## 2026-09-21 — 方法论基线 v2.6.0

- 51 个官方可调用技能（core / governance / tech），13+1 步强制开发顺序，5S 交付治理与产品主导全 AI 交付，单一真相源与前端纯展示规则（基线快照，见 `AGENTS.md`）。
