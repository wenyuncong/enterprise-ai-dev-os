# 2026-07-05 AI-OS 治理发现回写

> 来源: ai-os runtime | 审计案例: `frontend_truth_leak_audit`
> 生成时间: 2026-07-05T14:44:08.699290
> 证据文件: `evidence\gerp_enterprise_mainline\frontend_truth_leak_audit\result.json`

## 审计摘要

- 扫描: 226 前端 + 0 后端 + 0 数据库
- 已报告: 207
- 适用规则: single_truth_backend_first

## 发现分布

- review: 100

## 抽样发现 (前 10)

- `frontend\gerp-admin-web\src\App.vue` — computed_with_block_body [review]
- `frontend\gerp-admin-web\src\components\layout\AdminLayout.vue` — computed_with_block_body [review]
- `frontend\gerp-admin-web\src\components\layout\AdminLayout.vue` — computed_with_block_body [review]
- `frontend\gerp-admin-web\src\components\layout\AdminLayout.vue` — computed_with_block_body [review]
- `frontend\gerp-admin-web\src\components\layout\AdminLayout.vue` — computed_with_block_body [review]
- `frontend\gerp-admin-web\src\views\ai\AiCenter.vue` — computed_with_block_body [review]
- `frontend\gerp-admin-web\src\views\devops\ProductFeatureLedgerPage.vue` — computed_with_block_body [review]
- `frontend\gerp-admin-web\src\views\devops\Troubleshoot.vue` — computed_with_block_body [review]
- `frontend\gerp-admin-web\src\views\devops\Troubleshoot.vue` — computed_with_block_body [review]
- `frontend\gerp-admin-web\src\views\devops\Troubleshoot.vue` — price_in_computed [review]

## 后续动作

- [ ] 人工复核抽样发现
- [ ] 确认后升级为 CasePack 修复任务
- [ ] 如发现新的模式问题，回写到 Skill 体系

---
*由 ai-os governance writeback bridge 自动生成*
