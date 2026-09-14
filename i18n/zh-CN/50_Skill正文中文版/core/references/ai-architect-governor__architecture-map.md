# 架构治理地图 | Architecture Governance Map

> **源文件**：skills/core/ai-architect-governor/references/architecture-map.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-architect-governor` 的配套参考文件中中文对照版，不是正式加载源。

---

## 优先阅读的主要文档 | Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/docs/全项目总控/MASTER_INDEX.md`
- `{PROJECT_ROOT}/docs/架构决策记录/` 下的领域地图或系统边界文档
- `{PROJECT_ROOT}/docs/业务流程全案/` 下的业务流程文档
- `{PROJECT_ROOT}/docs/部署运维手册/` 下的部署 / 运行时归属文档

## 典型架构问题 | Typical architecture questions

1. 哪个领域是业务唯一真相源？
2. 哪个领域只是入口层？
3. 哪个领域只是使能 / 增强层？
4. 谁拥有身份、租户、组织与权限主体？
5. 哪些对象可以跨领域，按什么方向跨？
6. 哪个领域收口财务 / 结算 / 报表真相？
7. 哪些设置是全局、租户级或渠道级？
8. 哪个对象归属哪个 schema / 主表 / 主服务？

## 跨领域治理检查清单 | Cross-domain governance checklist

### A. 边界 | Boundary

- 涉及领域
- 主要归属方
- 禁止重复归属
- 入口 vs 真相 vs 增强的区分

### B. 身份与租户 | Identity and tenant

- 登录主体
- 租户范围
- 角色 / 权限注入
- 当领域存在多种身份类型时的外部用户 / 内部用户 / 合作伙伴主体拆分

### C. 数据归属 | Data ownership

- 主数据源
- 单据源
- 对象归属方
- 状态回写归属方
- 报表 / 财务收口归属方

### D. 对象落位 | Object landing

- 主表
- 主服务
- schema 落位
- 允许写入方
- 禁止写入方

### E. 链路设计 | Chain design

- 入口
- 传递对象
- 下游真相表
- 回写路径
- 失败 / 降级处理

## 预期产出物 | Expected artifacts

- 领域边界矩阵
- 架构决策说明
- 对象级归属地图
- schema 落位矩阵
- 主链归属地图
- 后续任务清单
