# 字段治理检查清单 | Field Governance Checklist

> **源文件**：skills/governance/ai-field-package-governor/references/field-governance-checklist.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-field-package-governor` 的配套参考文件中中文对照版，不是正式加载源。

---

## 向任何页面新增字段之前 | Before adding a field to any page

- [ ] 数据库：列已在 schema 中存在，类型已核实（`DESCRIBE table`）
- [ ] 元数据：字段已在中央元数据注册表中登记，含 label、type、validation
- [ ] 配置：默认可见性、排序、必填状态已定义
- [ ] 消费方：已识别所有引用该实体的页面

## 修改字段之前 | Before modifying a field

- [ ] 数据库：列类型与元数据声明一致
- [ ] 全部消费方：追踪每一个使用该字段的页面 / 组件
- [ ] 不会破坏页面本地覆盖（检查是否有硬编码 label / 列）

## 创建新页面之前 | Before creating a new page

- [ ] 复用检查：是否已有可渲染该实体的共享组件？
- [ ] `businessCode` / `entityKey` 已在元数据层定义
- [ ] 所有字段都从元数据消费，而非硬编码
- [ ] 字段标签来自元数据层，而非页面本地字符串

## 报表治理 | Report governance

- [ ] 标准列表 / 图表报表使用带 `reportCode` 的共享报表引擎
- [ ] 仅在元数据驱动方式不足时才使用自定义报表页
- [ ] 报表权限由后端引擎强制，而非前端组件
- [ ] 关系字段自动从主数据导入（`productId` → `productName`）

## 反模式 | Anti-patterns

- 在页面文件中硬编码字段标签
- 同一实体的多个页面之间出现重复的筛选 / 表单定义
- 把 `page_config` 当作字段定义的主来源
- 新增数据库列却未做元数据登记
