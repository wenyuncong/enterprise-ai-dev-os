# Project Constitution | 项目宪法

> 本文件是 AI-OS 的**不可违背原则**（spec-kit constitution 风格）。每条 MUST 都对应 `scripts/py/check_constitution.py` 里的一条机器校验；`--json` 输出可接 CI 门禁。
> 宪法是最高层约束，优先级高于普通规则和技能；任何交付若违反宪法，即使通过其他门禁也算未完成。

## MUST-1 Frontend Display Only | 前端纯展示

前端只负责渲染、采集输入、展示反馈；业务逻辑、计算、校验、状态转换、权限决策一律在服务端。
校验：扫描前端组件中的业务计算启发式（金额/价格/状态计算、权限判断）。

## MUST-2 Single Source Of Truth | 单一真相源

数据库 → 后端 API → 前端缓存，同一值绝不在两处用不同逻辑计算；字段定义集中，不在多个组件重复。
校验：规则入口声明存在 + 字段重复定义启发式。

## MUST-3 Library First | 库优先

任何自定义代码前，先查成熟开源库（npm/pip/maven）；禁止重复造轮子。
校验：规则入口声明存在。

## MUST-4 No Silent Failures | 无静默失败

每个错误都必须按严重级呈现（P0 弹窗 / P1 横幅 / P2 Toast / P3 控制台）；禁止空 catch、静默吞异常。
校验：复用 rule_lint 的 empty_catches 规则。

## MUST-5 Verification Before Done | 完成前验证

宣称"完成/修好/通过"必须有最后一次相关改动之后的新鲜证据（编译/API/浏览器/审计输出）。
校验：规则入口声明存在 + 证据采集器可运行。

## MUST-6 Destructive Ops Confirm | 破坏性操作确认

删除、迁移、批量替换、数据库或仓库级破坏操作必须先确认影响范围与回滚路径，P0 级必须弹窗确认。
校验：规则入口声明存在 + ACI 命令白名单存在。

## MUST-7 File Placement | 目录边界

脚本进 `scripts/`、SQL 进 `database/`、文档进 `docs/`、临时文件进 `temp/`；禁止项目根散落文件。
校验：复用 rule_lint 的 root_clutter 规则。

## MUST-8 No Hard-coded Locals | 禁止硬编码本地路径与颜色

可移植资产不得硬编码本地盘符路径；样式只用主题变量，禁止硬编码颜色。
校验：复用 rule_lint 的 drive_paths 与 hardcoded_colors 规则。
