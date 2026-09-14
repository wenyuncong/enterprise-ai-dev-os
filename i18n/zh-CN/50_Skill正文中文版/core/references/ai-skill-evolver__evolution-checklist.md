# Skill 进化检查清单 | Skill Evolution Checklist

> **源文件**：skills/core/ai-skill-evolver/references/evolution-checklist.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-skill-evolver` 的配套参考文件中中文对照版，不是正式加载源。

---

## 证据来源 | Evidence sources

先阅读当前方法论 Skill 治理链：

- `AGENTS.md`
- `rules/AGENTS.md`
- `skills/SKILL_MANIFEST.json`
- `docs/全项目总控/MASTER_INDEX.md`
- `docs/全项目总控/TASK_BACKLOG.md`
- `docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- 当前任务日志、测试报告、审计输出，以及已获准的私有来源材料

## 决策树 | Decision tree

1. 该模式是否重复出现？
   - 否 -> 记录为观察项
   - 是 -> 继续
2. 该 Skill 只是被声明，还是已经生效？
   - 仅声明 -> 核实实际 Skill 资产是否存在且可被调用
   - 已生效 -> 进入进化决策
3. 现有 Skill 能否吸收它？
   - 能 -> 更新该 Skill
   - 不能 -> 创建新的 Skill 候选
4. 是否需要完整的 Skill？
   - 不需要 -> 创建或更新模板 / 文档 / 规则
   - 需要 -> 创建治理任务并更新 Skill 资产

## 必需的更新 | Required updates

- 归档表
- Skill 专属文档
- 任务条目或日志条目
- 如需要，项目或运行时的 `SKILL.md`
- 下一轮待办台账（backlog）
