# 贡献指南 | Contributing

> **源文件**：CONTRIBUTING.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件对应的是英文正式源 `CONTRIBUTING.md`（仓库根目录），中文版为叠加对照层。

---

感谢你考虑为 Enterprise AI Development OS 作出贡献。

## 可以贡献什么 | What To Contribute

适合首次贡献的方向：

- 修正含义不清的规则或文档
- 改进已有的 Skill
- 补充验证示例
- 改进工具适配器
- 为某个工具版本补充兼容性证据
- 在不削弱边界检查的前提下改进审计脚本

请勿提交：

- 私有客户/项目材料
- 未脱敏的截图、日志或本机路径
- 生成的适配器产物，例如 `.trae/`、`.qoder/`、`.cursor/`、`.agents/`
- 大型原始归档或照抄的第三方仓库
- 没有证据的工具集成声明

## 贡献流程 | Contribution Flow

1. Fork 该仓库。
2. 从 `main` 创建分支。
3. 做一处聚焦的改动。
4. 运行必需检查。
5. 使用 PR 模板提交 pull request。

## 必需检查 | Required Checks

在提交 pull request 之前运行这些命令：

```powershell
py scripts/py/audit_methodology.py --project-root .
py scripts/py/check_open_source_boundary.py --project-root .
py scripts/py/score_ai_development_readiness.py --project-root .
powershell -NoProfile -ExecutionPolicy Bypass -File tools/deploy.ps1 -Tool verified -DryRun
```

若改动网站，还需检查：

```powershell
node -e "const fs=require('fs'); const html=fs.readFileSync('site/index.html','utf8'); if(!html.includes('Enterprise AI Development OS')) process.exit(1); console.log('site ok')"
```

## 更新规则 | Updating Rules

规则存放于 `rules/AGENTS.md`。如果你修改规则：

- 保持规则与具体工具无关
- 不得加入私有项目路径
- 生成的适配器产物不得进入版本控制
- 仅在 `AGENTS.md` 和 `CLAUDE.md` 确有需要、要有意识地镜像规则入口时才更新它们
- 运行审计脚本

## 更新 Skill | Updating Skills

Skill 位于 `skills/` 下。

每个 Skill 应当包含：

- 一个 `SKILL.md`
- 清晰的触发条件
- 工作流或检查清单指引
- 防护规则
- 仅在确有需要时提供的引用

如果你新增、删除或重命名 Skill，请更新：

- `skills/SKILL_MANIFEST.json`
- `docs/全项目总控/MASTER_INDEX.md`
- 必要时更新相关的兼容性或适配器文档

## 更新工具适配器 | Updating Tool Adapters

适配器源文件位于：

- `tools/adapters.json`
- `tools/deploy.ps1`
- `docs/TOOL_ADAPTERS.md`
- `docs/COMPATIBILITY.md`

禁止提交生成的适配器目录。如果某个工具需要不同的生成布局，请更新 `tools/deploy.ps1`，并记录已验证的行为。

适配器状态规则：

- `verified`：官方文档或实际行为证明规则路径与加载行为
- `experimental`：大概率可用，但仍需按版本验证
- `pending-verification`：尚不得作出公开支持声明

## 开源边界 | Open-Source Boundary

本仓库有意排除私有策略、原始归档、过程日志、本机工具状态和未脱敏案例材料。参见：

- `docs/公开材料/OPEN_SOURCE_PACKAGE.md`
- `docs/公开材料/OPEN_SOURCE_READINESS.md`
- `docs/全项目总控/DISCLOSURE_BOUNDARY.md`

有疑问时，先开 issue 再提交材料。

## Pull Request 期望 | Pull Request Expectations

一个 PR 应当包含：

- 改了什么
- 为什么改
- 哪些检查通过了
- 是否改变了兼容性声明或公开声明
- 仅在截图安全且相关时才附截图

优先选择小而聚焦的 PR。
