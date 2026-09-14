# 部署运维手册 | Deployment & Operations Guide

> **源文件**：docs/_templates/部署运维手册/DEPLOYMENT_TEMPLATE.md
> **源版本**：v1.0（源文件标注 `Template Version: v1.0`）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。

> **模板版本（Template Version）**：v1.0
> **项目（Project）**：[PROJECT_NAME]
> **最后更新（Last Updated）**：[DATE]

---

## 1. 服务器清单 | Server Inventory

| 服务器 | IP/域名 | 角色 | OS | 规格 |
|---|---|---|---|---|
| 测试服务器 | [TEST_SERVER] | 开发测试 | [OS] | [SPECS] |
| 预发布服务器 | [STAGING_SERVER] | 预发布验证 | [OS] | [SPECS] |
| 生产服务器 | [PROD_SERVER] | 生产环境 | [OS] | [SPECS] |

---

## 2. 服务清单 | Service Inventory

| 服务 | 端口 | 部署路径 | 启动命令 | 健康检查 |
|---|---|---|---|---|
| [FRONTEND] | [PORT] | [PATH] | [CMD] | [HEALTH_URL] |
| [BACKEND] | [PORT] | [PATH] | [CMD] | [HEALTH_URL] |
| [DATABASE] | [PORT] | — | — | [CHECK_CMD] |

---

## 3. 发布流程 | Release Process

### 3.1 测试服务器发布 | Test Server Release
1. 代码合并到 [TEST_BRANCH]
2. CI 流水线自动构建：[CI_URL]
3. 自动部署到测试环境
4. 冒烟测试验证：[SMOKE_TEST_CHECKLIST]

### 3.2 生产服务器发布 | Production Server Release
1. 创建 release tag：`git tag vX.Y.Z`
2. 触发生产流水线：[PROD_PIPELINE]
3. 数据库迁移检查：[DB_MIGRATION_CHECK]
4. 灰度发布 / 蓝绿部署
5. 监控告警确认

---

## 4. 回滚方案 | Rollback Plan

### 触发条件 | Trigger Conditions
- 关键 API 错误率 > [THRESHOLD]
- 页面加载失败率 > [THRESHOLD]
- 数据库迁移失败

### 回滚步骤 | Rollback Steps
1. 停止当前部署
2. 恢复到上一个已知良好的版本：[ROLLBACK_CMD]
3. 数据库回滚（如果适用）
4. 验证关键功能
5. 通知相关方：[NOTIFICATION_LIST]

---

## 5. 监控与告警 | Monitoring & Alerts

| 指标 | 监控方式 | 告警阈值 | 通知渠道 |
|---|---|---|---|
| API 响应时间 | [TOOL] | > [THRESHOLD]ms | [CHANNEL] |
| 错误率 | [TOOL] | > [THRESHOLD]% | [CHANNEL] |
| 磁盘使用率 | [TOOL] | > [THRESHOLD]% | [CHANNEL] |
| 内存使用率 | [TOOL] | > [THRESHOLD]% | [CHANNEL] |

---

## 6. 备份策略 | Backup Strategy

| 数据 | 频率 | 保留天数 | 存储位置 |
|---|---|---|---|
| 数据库 | [FREQUENCY] | [DAYS] | [LOCATION] |
| 文件存储 | [FREQUENCY] | [DAYS] | [LOCATION] |
| 配置文件 | [FREQUENCY] | [DAYS] | [LOCATION] |

---

## 7. 环境变量 | Environment Variables

| 变量名 | 测试环境 | 生产环境 | 说明 |
|---|---|---|---|
| [VAR_NAME] | [TEST_VALUE] | [PROD_VALUE] | [DESCRIPTION] |

---

## 8. 常见运维任务 | Common Operations

### 重启服务 | Restart Service
```bash
[SYSTEMCTL_CMD]
```

### 查看日志 | View Logs
```bash
[LOG_CMD]
```

### 数据库连接 | Database Connection
```bash
[DB_CMD]
```

---

## 9. 紧急联系 | Emergency Contacts

| 角色 | 姓名 | 联系方式 |
|---|---|---|
| 运维负责人 | [NAME] | [CONTACT] |
| 开发负责人 | [NAME] | [CONTACT] |
| DBA | [NAME] | [CONTACT] |

---

## 译注 | Translation Notes

- 源文件正文已是中文，标题为「中文 | English」形式；本译文补齐文件头、把源文件未带英文的子标题（3.1、3.2、触发条件、回滚步骤、重启服务、查看日志、数据库连接）补上英文对照，并统一标识符前后的空格，未改动语义。
- 所有全大写方括号占位符（`[PROJECT_NAME]`、`[TEST_SERVER]`、`[THRESHOLD]` 等）属代码型占位符，按口径原样保留；`[NAME]`、`[CONTACT]`、`[DESCRIPTION]` 同理。
- `bash` 代码块原样保留，未译。
