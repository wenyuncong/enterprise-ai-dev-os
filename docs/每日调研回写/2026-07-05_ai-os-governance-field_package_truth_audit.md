# 2026-07-05 AI-OS 治理发现回写

> 来源: atomic runtime | 审计案例: `field_package_truth_audit`
> 生成时间: 2026-07-02T10:07:19
> 证据文件: `evidence\erp_production\field_package_truth_audit\result.json`

## 审计摘要

- 扫描: 1574 前端 + 5000 后端 + 928 数据库
- 候选: 249
- 已报告: 100
- 适用规则: field_package_primary_source, legacy_debt_boundary, single_truth_backend_first

## 发现分布

- review: 100

## 抽样发现 (前 10)

- `frontend/gerp-web/src/composables/useBaseTableColumnConfig.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]
- `frontend/gerp-web/src/composables/useBaseTableSelection.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]
- `frontend/gerp-web/src/composables/useCustomFieldValues.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]
- `frontend/gerp-web/src/composables/useFeatureGate.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]
- `frontend/gerp-web/src/composables/useSalesCostInsightColumns.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]
- `frontend/gerp-web/src/composables/useTableConfig.alias.test.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]
- `frontend/gerp-web/src/composables/useTableConfig.order.test.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]
- `frontend/gerp-web/src/composables/useTableConfig.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]
- `frontend/gerp-web/src/constants/businessModuleCommonParams.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]
- `frontend/gerp-web/src/services/documentCalculationService.ts` — static_field_or_column_config_without_obvious_field_package_contract [review]

## 后续动作

- [ ] 人工复核抽样发现
- [ ] 确认后升级为 CasePack 修复任务
- [ ] 如发现新的模式问题，回写到 Skill 体系

---
*由 ai-os governance writeback bridge 自动生成*
