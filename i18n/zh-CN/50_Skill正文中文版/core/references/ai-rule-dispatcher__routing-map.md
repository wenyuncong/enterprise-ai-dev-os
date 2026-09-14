# AI 原生方法论路由地图 | AI-Native Methodology Routing Map

> **源文件**：skills/core/ai-rule-dispatcher/references/routing-map.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-rule-dispatcher` 的配套参考文件中中文对照版，不是正式加载源。

---

## 1. 权威规则层 | Authoritative rule layer

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/rules/AGENTS.md`

这两份文件定义先检查后执行（check-before-execute）、执行边界、重启时机与全项目级约束。

## 2. 当前任务线层级 | Current line hierarchy

### 2.1 当前企业主线 | Current enterprise mainline

通过以下文件冻结当前执行线：

- `{PROJECT_ROOT}/docs/全项目总控/TASK_BACKLOG.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- `{PROJECT_ROOT}/docs/业务流程全案/` 下的当前任务包

当前顺序：

1. 分类任务
2. 加载必需的规则与 Skill
3. 核实当前状态
4. 把工作拆解为批次
5. 通过既有工具或脚本执行
6. 验证运行时 / 测试
7. 回写证据与进化记录

### 2.2 支撑线与特殊线 | Support and special lines

- 治理支撑线 -> 方法论、规则、Skill、审计脚本
- 产品完成线 -> 文档、发布套件、打包、证据
- 运行时支撑线 -> 环境、工具、构建、部署、验证
- 领域实现线 -> 数据库、后端、前端、集成

## 3. 主要文档路由 | Primary document routing

| 任务类型 | 首批文档 |
| --- | --- |
| 全项目治理 / 规划 | `docs/全项目总控/MASTER_INDEX.md` + `docs/全项目总控/TASK_BACKLOG.md` |
| 当前企业执行线 | `docs/业务流程全案/` 下的当前任务包 |
| 业务流程下的本地执行包 | `docs/业务流程全案` 下的相关包 |
| 命令 / 运行时 / 编译 | `AGENTS.md` + `scripts/` |
| 产品设计预冻结 | `docs/架构决策记录/` 下的相关 ADR |
| 竞品 / 市场 | `docs/` 下现有的 `竞品 / 对标 / 调研` 文档 |

## 4. 主导 Skill 路由表 | Lead-skill routing map

| 主导任务类型 | 主导 Skill | 常用支撑 Skill |
| --- | --- | --- |
| 总控规划 / 派单 / 回填 | `ai-chief-planner` | `ai-task-decomposer` |
| 复杂任务拆分 | `ai-task-decomposer` | `ai-chief-planner` |
| 命令执行 / 运行时诊断 | `ai-command-executor` | `ai-rule-dispatcher` |
| 路由 / 规则 / 文档歧义 | `ai-rule-dispatcher` | `ai-chief-planner` |
| 竞品对标 | `ai-competitor-analyst` | `ai-reference-researcher` |
| 边界 / 真相源冲突 | `ai-domain-boundary-mapper` | `ai-architect-governor` |
| 流程收口审计 | `ai-flow-closure-audit` | `ai-chief-planner` |
| 前端可用性 / 易用性审计 | `ai-frontend-audit` | `ai-ui-ux-governor` |
| UI/UX 改进 | `ai-ui-ux-governor` | `ai-frontend-audit` |

## 5. 首查模板 | First-check templates

| 情形 | 首查项 |
| --- | --- |
| 与 DB 相关 | 表 / 字段 / 行数 / schema 确认 |
| 与代码相关 | 文件是否存在、路由 / controller / service 检索 |
| 与运行时相关 | 获准脚本入口、日志路径、端口、进程 |
| 与文档相关 | 现有包、执行记录、认领池行（claim-pool row）、主任务表行 |
| 主线歧义 | 该任务属于当前主线、支撑线还是特殊线 |

## 6. 必需的路由输出 | Required routing output

每个路由答复都应当给出：

1. 任务线判断
2. 主导 Skill
3. 支撑 Skill
4. 权威文档
5. 首批事实检查
6. 安全执行顺序
7. 禁止跨越的边界
