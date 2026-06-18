# 部署运维手册 — Deployment & Operations Guide

> **Template Version**: v1.0
> **Project**: [PROJECT_NAME]
> **Last Updated**: [DATE]

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

### 3.1 测试服务器发布
1. 代码合并到 [TEST_BRANCH]
2. CI流水线自动构建: [CI_URL]
3. 自动部署到测试环境
4. 冒烟测试验证: [SMOKE_TEST_CHECKLIST]

### 3.2 生产服务器发布
1. 创建 release tag: `git tag vX.Y.Z`
2. 触发生产流水线: [PROD_PIPELINE]
3. 数据库迁移检查: [DB_MIGRATION_CHECK]
4. 灰度发布 / 蓝绿部署
5. 监控告警确认

---

## 4. 回滚方案 | Rollback Plan

### 触发条件
- 关键API错误率 > [THRESHOLD]
- 页面加载失败率 > [THRESHOLD]
- 数据库迁移失败

### 回滚步骤
1. 停止当前部署
2. 恢复到上一个已知良好的版本: [ROLLBACK_CMD]
3. 数据库回滚（如果适用）
4. 验证关键功能
5. 通知相关方: [NOTIFICATION_LIST]

---

## 5. 监控与告警 | Monitoring & Alerts

| 指标 | 监控方式 | 告警阈值 | 通知渠道 |
|---|---|---|---|
| API响应时间 | [TOOL] | > [THRESHOLD]ms | [CHANNEL] |
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

### 重启服务
```bash
[SYSTEMCTL_CMD]
```

### 查看日志
```bash
[LOG_CMD]
```

### 数据库连接
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
