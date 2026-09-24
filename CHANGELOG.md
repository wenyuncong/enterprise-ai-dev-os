# Changelog

本项目的显著变更记录。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，日期为 Asia/Shanghai。

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
