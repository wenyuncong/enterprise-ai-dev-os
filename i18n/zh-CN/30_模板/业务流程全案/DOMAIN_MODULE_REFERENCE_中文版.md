# 领域模块分解参考 | Domain Module Decomposition Reference

> **源文件**：docs/_templates/业务流程全案/DOMAIN_MODULE_REFERENCE.md
> **源版本**：1.0.0
> **译文日期**：2026-11-08
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

> **通用化自**：真实企业交付证据——通用职责类别，项目与业务名称已移除
> **适用时机**：为新企业级项目设计原子服务（atomic service）边界时

---

## 分解原则 | Decomposition Principles

1. **一个模块 = 一项业务能力** —— 不是一张表，也不是一个页面
2. **最多 3 个依赖** —— 任何模块若依赖超过 3 个其他模块，就应当拆分
3. **数据归属唯一** —— 每个数据集合只属于一个模块
4. **API 是唯一契约** —— 模块之间只通过已定义的 API 通信

---

## 参考类别地图 | Reference Category Map

把系统自己的模块映射到这些通用职责类别，而非假设一份固定模块清单：

```
┌─────────────────────────────────────────────────────────────┐
│  FOUNDATION — shared base, master/reference data, identity  │
├─────────────────────────────────────────────────────────────┤
│  CORE TRANSACTION — primary flows, asset state, execution   │
├─────────────────────────────────────────────────────────────┤
│  FINANCE — accounting, settlement, funds                    │
├─────────────────────────────────────────────────────────────┤
│  EXTENDED BUSINESS — channels, supply coordination, trade   │
├─────────────────────────────────────────────────────────────┤
│  OPERATIONS — reporting, output, collaboration, quality     │
├─────────────────────────────────────────────────────────────┤
│  PLATFORM — provisioning, agent capabilities, automation    │
└─────────────────────────────────────────────────────────────┘
```

> **层级对照**：FOUNDATION = 基座层；CORE TRANSACTION = 核心交易层；FINANCE = 财务层；EXTENDED BUSINESS = 扩展业务层；OPERATIONS = 运营层；PLATFORM = 平台层。

---

## 模块依赖规则 | Module Dependency Rules

| 规则 | 依据 |
|---|---|
| 基座模块不依赖任何模块 | 它们是依赖树的根 |
| 核心交易依赖基座 | 交易流程需要参考数据与身份数据 |
| 财务依赖核心交易 | 核算需要交易证据 |
| 扩展业务依赖核心 | 渠道需要交易历史 |
| 运营依赖上述全部 | 报表跨模块读取 |
| 平台依赖上述全部 | 预置治理全部租户 |

**反模式（anti-pattern）**：两个模块之间的循环依赖。修复：两者都依赖同一条事件总线。

---

*最后更新：2026-11-08 | 状态：通用——项目与业务名称已移除*
