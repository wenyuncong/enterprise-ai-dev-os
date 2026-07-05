# 2026-07-05 AI-OS 治理发现回写

> 来源: ai-os runtime | 审计案例: `document_action_backend_truth_audit`
> 生成时间: 2026-07-05T14:44:10.626015
> 证据文件: `evidence\gerp_enterprise_mainline\document_action_backend_truth_audit\result.json`

## 审计摘要

- 扫描: 0 前端 + 4592 后端 + 0 数据库
- 真值信号文件: 55
- Gap 发现: 623
- 适用规则: single_truth_backend_first

## 发现分布

- review: 100

## 抽样发现 (前 10)

- `backend\gerp-admin\src\main\java\com\gerp\admin\controller\AdminRoleController.java` — direct_db_write_in_controller [review]
- `backend\gerp-admin\src\main\java\com\gerp\admin\controller\AdminTenantController.java` — direct_db_write_in_controller [review]
- `backend\gerp-admin\src\main\java\com\gerp\admin\controller\AdminUserController.java` — direct_db_write_in_controller [review]
- `backend\gerp-admin\src\main\java\com\gerp\admin\controller\ConfigCenterController.java` — direct_db_write_in_controller [review]
- `backend\gerp-admin\src\main\java\com\gerp\admin\controller\DevOpsController.java` — direct_db_write_in_controller [review]
- `backend\gerp-admin\src\main\java\com\gerp\admin\controller\PlatformConfigController.java` — direct_db_write_in_controller [review]
- `backend\gerp-admin\src\main\java\com\gerp\admin\controller\ProfileController.java` — direct_db_write_in_controller [review]
- `backend\gerp-admin\src\main\java\com\gerp\admin\controller\TranslationOverrideController.java` — direct_db_write_in_controller [review]
- `backend\gerp-admin\src\main\java\com\gerp\admin\service\AlertService.java` — direct_db_write_in_controller [review]
- `backend\gerp-admin\src\main\java\com\gerp\admin\service\OpsBaselineService.java` — direct_db_write_in_controller [review]

## 后续动作

- [ ] 人工复核抽样发现
- [ ] 确认后升级为 CasePack 修复任务
- [ ] 如发现新的模式问题，回写到 Skill 体系

---
*由 ai-os governance writeback bridge 自动生成*
