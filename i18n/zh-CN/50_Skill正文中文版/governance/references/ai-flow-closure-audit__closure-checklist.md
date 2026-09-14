# 流程收口检查清单 | Flow Closure Checklist

> **源文件**：skills/governance/ai-flow-closure-audit/references/closure-checklist.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-flow-closure-audit` 的配套参考文件中中文对照版，不是正式加载源。

---

## 优先阅读的主要文档 | Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- `{PROJECT_ROOT}/docs/全项目总控/AI_NATIVE_DELIVERY_LOOP.md`
- `{PROJECT_ROOT}/docs/业务流程全案/` 下的相关流程文档
- `{PROJECT_ROOT}/docs/测试验收报告/` 下的最新验证报告

## 典型链路类别 | Typical chain categories

- O2C：订单到收款（order to cash）
- S2P：采购到付款（source to pay）
- R2R：记录到报告（record to report）
- L2C：线索到收款（lead to cash）
- 生产履约（production fulfillment）
- WMS / TMS 执行
- SaaS 订阅生命周期（SaaS subscription lifecycle）

## 审计检查清单 | Audit checklist

### A. 基本事实 | Basic facts

- 页面存在
- 路由 / 菜单存在
- API 存在
- 表存在
- 参数存在

### B. 主要行为 | Main behavior

- 新建 / 保存
- 提交 / 审核
- 下游推送
- 状态流转
- 回写 / 对账

### C. 扩展收口 | Extended closure

- 报表 / 历史 / 台账支持
- 导出或查询支持
- 权限 / 参数门禁
- 跨模块一致性

### D. 证据 | Evidence

- SQL
- API 日志
- UI 截图
- 需要时的编译或运行时验证
- 执行回填引用

## 预期产出物 | Expected artifacts

- 收口证据表
- 差距清单
- 验收检查清单
- 回归任务清单
- 任务日志与回填引用
