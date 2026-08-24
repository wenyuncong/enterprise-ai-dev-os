# Autopilot Delivery Protocol | 全自动交付协议

> 目标驱动模式：用户只需告知业务目标。AI 负责计划、执行、验证、分批提交与结果报告。
> 本协议由用户于 2026-08-24 明确设定，替代逐轮确认制。

---

## 1. 协作模式 | Collaboration Mode

**用户提供**：业务目标、验收期望、关键约束（一次说清即可）。

**AI 自动完成（无需确认）**：

- 目标分析、计划拆解（todo 可见化）
- 代码/文档/Skill 的全部实现与修改
- 全量自动验证（审计脚本、场景回归、边界检查、语法检查、构建/运行证据）
- 按主题分批 `git commit`（conventional commits，验证全绿才提交）
- 变更摘要与证据报告

**必须停下来（带建议询问）**：

- 业务目标本身模糊、冲突或需要用户拍板方向
- 破坏性操作（删除/重命名/迁移/批量替换、数据库或仓库级破坏）
- 对外发布、对外承诺、许可/边界变更
- 无法自动判断的取舍——**必须给出明确建议与默认选项**，不让用户从零决策

## 2. 执行循环 | Execution Loop

```text
目标输入
  -> 计划（todo 列表）
  -> 执行（分批、可验证）
  -> 验证（audit + scenarios + boundary + 语法/构建 + 新鲜证据）
  -> 提交（conventional commits，按主题分批）
  -> 报告（改了什么、证据在哪、遗留提醒）
```

## 3. 提交规范 | Commit Rules

- 每个 commit 只含一个逻辑主题
- message 用 Conventional Commits：`feat|fix|docs|refactor|chore|test|perf(scope): 描述`
- 提交前必须：`audit_methodology.py`、`test_methodology_scenarios.py`、`check_open_source_boundary.py` 全绿
- 生成产物（适配器目录、安装器输出）不入库，靠 `.gitignore` 隔离

## 4. 质量护栏 | Quality Guardrails

- 任何"完成"声明必须有**最后一次相关变更之后**运行的新鲜证据（规则 0.9）
- 规则、Skill、模板或路由边界变化时，额外跑 `test_methodology_scenarios.py --project-root .`
- 命中未跟踪/未预期的文件先归类：入库、gitignore、或提醒用户，不留中间态

## 5. 协议自身的进化

本协议属于方法论资产，可在实践中修订；修订本身按上述提交规范入库。
