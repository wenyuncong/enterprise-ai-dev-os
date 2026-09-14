# 治理 | Governance

> **源文件**：GOVERNANCE.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件对应的是英文正式源 `GOVERNANCE.md`（仓库根目录），中文版为叠加对照层。

---

Enterprise AI Development OS 以可移植的方法论与适配器框架的形态维护。

## 维护者职责 | Maintainer Responsibilities

维护者负责：

- 保护开源边界
- 审阅兼容性声明
- 保持 `skills/` 与 `rules/AGENTS.md` 为正式源
- 让生成的适配器产物不进入版本控制
- 要求合并前完成验证

## 唯一真相源 | Source Of Truth

正式源：

- `rules/AGENTS.md`
- `skills/`
- `skills/SKILL_MANIFEST.json`
- `docs/_templates/`
- `tools/adapters.json`
- `tools/deploy.ps1`

生成的产物不是唯一真相源。

## 决策规则 | Decision Rules

公开声明之前先取得证据：

- 工具适配器需要官方文档或实际行为作为依据
- 新增 Skill 需要清晰的触发条件与工作流
- 面向发布的文档必须不包含私有路径与私有策略
- 审计失败阻断发布

## 兼容性状态 | Compatibility Status

兼容性状态在 `tools/adapters.json` 中管理：

- `verified`
- `experimental`
- `pending-verification`

没有书面证据，不得把某个工具的兼容性状态提升为 `verified`。
