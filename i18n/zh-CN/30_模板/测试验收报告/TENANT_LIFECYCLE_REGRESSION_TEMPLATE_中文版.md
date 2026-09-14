# 租户生命周期回归 | Tenant Lifecycle Regression

> **源文件**：docs/_templates/测试验收报告/TENANT_LIFECYCLE_REGRESSION_TEMPLATE.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

---

用于租户初始化、重建、恢复、迁移、运行时配置（runtime profile）、权限或跨租户隔离改动时填写本记录。

## 测试范围 | Test Scope

| 项目 | 取值 |
| --- | --- |
| 环境（Environment） | |
| 版本 / 提交（Version / commit） | |
| 目标租户（Target tenant(s)） | |
| 对照租户（Control tenant(s)） | |
| 报告范围（Report scope） | |
| 证据目录（Evidence directory） | |
| 允许写入（Writes allowed） | 是 / 否；精确范围： |
| 已执行的初始化 / 重建 / 恢复 | 无 / [记录] |

## 生命周期检查 | Lifecycle Checks

| 阶段 | 期望 | 实际 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| 认证（Authenticate） | 目标租户可以认证 | | Pass / Fail | |
| 加载配置（Load profile） | 正确的运行时与权限配置加载 | | Pass / Fail | |
| 初始化 / 重建（Initialize / rebuild） | 仅声明的租户状态被改动 | | Pass / Fail / N/A | |
| 执行业务流（Execute flow） | 受影响的业务或能力流程可运行 | | Pass / Fail | |
| 回读（Readback） | 权威回读（authoritative readback）的事实与期望结果一致 | | Pass / Fail | |
| 审计（Audit） | 动作、操作人、租户与版本被记录 | | Pass / Fail | |
| 回滚 / 残留（Rollback / residue） | 恢复或残留检查通过 | | Pass / Fail / N/A | |

## 隔离断言 | Isolation Assertions

| 断言 | 期望 | 实际 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| 目标租户只能看到自己的数据 | 隔离（Isolated） | | Pass / Fail | |
| 对照租户保持不变 | 未改动（Unchanged） | | Pass / Fail | |
| 跨租户访问被拒绝 | 拒绝（Denied） | | Pass / Fail | |
| 报表与计数使用声明的范围 | 限定范围（Scoped） | | Pass / Fail | |

## 决策 | Decision

```text
回归结果（Regression result）：pass / blocked
P0 / P1 / P2 findings：
残留数据或运行时状态（Residual data or runtime state）：
产品验收（Product acceptance）：accept / revise / reject / not requested
```

---

## 译注 | Translation Notes

- 「决策」节的 ```text 块是**状态取值脚手架**，不是代码：标签文字已译出并保留英文括注，`pass / blocked`、`accept / revise / reject / not requested`、`N/A`、`P0 / P1 / P2` 等状态与分级代号保持英文原样。
- 「结果」列的 `Pass / Fail` 是判定代号，按门禁代号口径不译。
