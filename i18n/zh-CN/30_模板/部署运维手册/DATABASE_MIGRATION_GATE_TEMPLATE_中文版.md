# 数据库迁移一致性门禁 | Database Migration Consistency Gate

> **源文件**：docs/_templates/部署运维手册/DATABASE_MIGRATION_GATE_TEMPLATE.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

---

用于 Schema、种子数据（seed）、参数基线或租户数据迁移。**部署任务成功或 API 返回成功都不能替代本门禁。**

## 迁移标识 | Migration Identity

| 项目 | 取值 |
| --- | --- |
| 迁移 ID（Migration ID） | |
| 目标版本（Target version） | |
| 源路径（Source path） | |
| 依赖 / 执行顺序（Dependency / execution order） | |
| 校验和（Checksum） | |
| 替换或取代关系（Replacement or supersession relation） | 无 / [记录] |

## 环境登记 | Environment Registration

| 环境 | 已登记 | 注册表 / 清单路径 | 提交或版本 |
| --- | --- | --- | --- |
| 测试 / 预发布（Test / staging） | 是 / 否 | | |
| 生产（Production） | 是 / 否 | | |

## 安全与恢复 | Safety and Recovery

| 检查 | 结果 | 证据 |
| --- | --- | --- |
| 幂等或受保护的前置条件 | Pass / Fail / N/A | |
| 重复或已被取代的迁移被阻止 | Pass / Fail / N/A | |
| 恢复路径（Recovery path） | Pass / Fail | |
| 备份 / 补偿迁移 / 回退点 | | |

## 执行历史 | Execution History

| 环境 | 状态（status） | 完成时间 | 操作人 / 任务 | 提交 / 版本 | 证据 |
| --- | --- | --- | --- | --- | --- |
| 测试 / 预发布（Test / staging） | | | | | |
| 生产（Production） | | | | | |

## 迁移后检查 | Post-Migration Checks

| 范围 | 检查 | 结果 | 证据 |
| --- | --- | --- | --- |
| Schema | 表、列、索引、约束 | Pass / Fail | |
| 种子 / 参数（Seed / parameters） | 必需的行与取值 | Pass / Fail | |
| 运行时配置（Runtime profile） | 编译后的配置反映该迁移 | Pass / Fail | |
| 租户范围（Tenant scope） | 目标租户被改动；无关租户未改动 | Pass / Fail | |
| 业务流程（Business flow） | 受影响流程仍能闭环 | Pass / Fail | |

## 决策 | Decision

```text
迁移门禁（Migration gate）：pass / blocked
缺失证据或阻塞项（Missing evidence or blockers）：
恢复决策（Recovery decision）：
发布决策（Release decision）：
```

---

## 译注 | Translation Notes

- 「决策」节的 ```text 块是**状态取值脚手架**，不是代码：标签文字已译出并保留英文括注，`pass / blocked` 状态代号保持英文原样。
- `Pass / Fail / N/A` 为门禁判定代号，按门禁代号口径不译；`Schema` 在数据库语境下保留英文（见术语表第 6 节）。
