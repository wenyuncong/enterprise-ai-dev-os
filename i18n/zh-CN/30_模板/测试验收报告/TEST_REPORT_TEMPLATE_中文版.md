# 测试与验收报告模板 | Testing & Acceptance Report Template

> **源文件**：docs/_templates/测试验收报告/TEST_REPORT_TEMPLATE.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

---

## 测试报告：[功能 / 模块 / 发布版本] | Test Report: [Feature/Module/Release]

**版本（Version）**：[X.Y.Z]
**测试日期（Test Date）**：YYYY-MM-DD
**测试环境（Test Environment）**：[本地（Local）/ 预发布（Staging）/ 生产（Production）]
**测试人（Tester）**：[姓名 / AI 智能体]

---

## 测试摘要 | Test Summary

| 指标 | 取值 |
|---|---|
| 用例总数（Total Test Cases） | N |
| 通过（Passed） | N |
| 失败（Failed） | N |
| 阻塞（Blocked） | N |
| 通过率（Pass Rate） | XX% |

## 测试用例 | Test Cases

### TC-001：[正常路径] | TC-001: [Happy Path]
- **步骤（Steps）**：[逐步操作]
- **期望（Expected）**：[应当发生什么]
- **实际（Actual）**：[实际发生了什么]
- **状态（status）**：[PASS / FAIL]
- **证据（Evidence）**：[截图 / curl 输出 / 日志]

### TC-002：[边界用例] | TC-002: [Edge Case]
[...]

## 回归检查 | Regression Check

| 已有功能 | 状态（status） | 备注 |
|---|---|---|
| [功能 1] | PASS | — |
| [功能 2] | PASS | — |

## 发现的问题 | Issues Found

| ID | 严重级别 | 描述 | 复现步骤 | 状态（status） |
|---|---|---|---|---|
| BUG-001 | P0 | [...] | [...] | 待处理（Open） |
| BUG-002 | P2 | [...] | [...] | 已修复（Fixed） |

## 验收 | Acceptance

- [ ] 所有 P0/P1 用例通过
- [ ] 已有功能无回归
- [ ] 性能在可接受范围内
- [ ] 文档已更新

**结论（Decision）**：[接受（ACCEPTED）/ 拒绝（REJECTED）/ 有条件接受（CONDITIONAL）]

---

## 译注 | Translation Notes

- `PASS / FAIL`、`P0`–`P3`、`TC-*`、`BUG-*` 为判定代号与用例编号，原样保留。
- 「状态（status）」保留 `status` 键名；「阻塞（Blocked）」对应术语表的 `blocked` 状态名，正文中保留英文括注。
