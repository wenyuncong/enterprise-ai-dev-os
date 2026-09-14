# 命令入口与诊断地图 | Command Entry Points and Diagnosis Map

> **源文件**：skills/core/ai-command-executor/references/entrypoints.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-command-executor` 的配套参考文件中中文对照版，不是正式加载源。

---

## 1. 优先阅读的主要文档 | Primary documents to read first

- `{PROJECT_ROOT}/AGENTS.md`
- `{PROJECT_ROOT}/.trae/rules/project_rules.md`
- `{PROJECT_ROOT}/docs/全项目总控/` 或 `{PROJECT_ROOT}/docs/业务流程全案/` 下的当前任务包或执行记录

## 2. 获准入口的优先级 | Approved entrypoint priority

1. `{PROJECT_ROOT}/scripts/bat/gerp.bat`
2. `{PROJECT_ROOT}/scripts/bat` 下的直接批处理脚本
3. `{PROJECT_ROOT}/scripts/ps1` 下的辅助脚本
4. 仅当以上都不覆盖所需能力时，才使用自定义 shell 命令

## 3. 场景到入口的矩阵 | Scenario-to-entrypoint matrix

| 场景 | 首选入口 | 首查项 | 证据 |
| --- | --- | --- | --- |
| MySQL 连通性 | `scripts/bat/gerp.bat mysql test` | DB 主机 / 账号 / 进程 | 命令结果 |
| SQL 只读检查 | `scripts/bat/gerp.bat mysql exec gerp_enterprise "SHOW TABLES;"` | schema / 表 / 字段是否存在 | SQL 输出 |
| SQL 写入执行 | `database/` 下的确切 SQL 文件 + 对应的 MySQL 入口 | 目标 schema、是否需要备份、脚本路径 | SQL 文件 + 执行输出 |
| 后端编译 | `scripts/bat/gerp.bat maven compile [module]` | 模块路径、`pom.xml`、依赖状态 | 编译输出 |
| 后端打包 | `scripts/bat/maven-package.bat` | 模块 target、打包路径 | 打包输出 |
| 后端启动 | `scripts/bat/start-service.bat [service]` | 端口 / 进程 / 配置 / 延迟重启规则 | 运行时日志 |
| 前端开发 | `scripts/bat/frontend-dev.bat [app]` | 应用路径、端口、node 状态 | dev 输出 |
| 前端构建 | `scripts/bat/frontend-build.bat [app]` | 应用路径、依赖状态 | 构建输出 |
| 运行时诊断 | 现有脚本 + 对应日志路径 | 日志文件是否存在、第一个真实错误 | 日志摘录摘要 |

## 4. 常用直接脚本 | Common direct scripts

- `{PROJECT_ROOT}/scripts/bat/mysql-test.bat`
- `{PROJECT_ROOT}/scripts/bat/mysql-exec.bat`
- `{PROJECT_ROOT}/scripts/bat/maven-compile.bat`
- `{PROJECT_ROOT}/scripts/bat/maven-package.bat`
- `{PROJECT_ROOT}/scripts/bat/start-service.bat`
- `{PROJECT_ROOT}/scripts/bat/frontend-dev.bat`
- `{PROJECT_ROOT}/scripts/bat/frontend-build.bat`

## 5. 常用辅助脚本 | Common helper scripts

- `{PROJECT_ROOT}/scripts/ps1/mysql-functions.ps1`
- `{PROJECT_ROOT}/scripts/ps1/maven-functions.ps1`
- `{PROJECT_ROOT}/scripts/ps1/frontend-functions.ps1`

## 6. 常用日志位置 | Common log locations

- `{PROJECT_ROOT}/scripts/bat/logs`
- `{PROJECT_ROOT}/scripts/bat/logs/error`
- `{PROJECT_ROOT}/scripts/logs`
- 模块本地的 `target` 或运行时日志目录（仅在显式配置时）

## 7. 首查矩阵 | First-check matrix

| 检查类型 | 典型动作 |
| --- | --- |
| DB | `SHOW TABLES`、`DESCRIBE`、行数、schema 确认 |
| 代码 | `Test-Path`、`rg`、读配置、模块路径确认 |
| 运行时 | 端口、进程、PID、日志文件是否存在 |
| 任务边界 | 当前任务包、延迟重启规则、热点文件冲突 |

## 8. 诊断分类 | Diagnosis categories

| 分类 | 典型症状 | 必需的下一步 |
| --- | --- | --- |
| 环境问题 | 命令未找到、端口被占用、运行时缺失 | 修路径 / 端口 / 进程 |
| 脚本问题 | 获准脚本路径错误或参数不匹配 | 修正脚本用法或脚本资产 |
| 依赖问题 | 依赖包缺失、工具链未就绪 | 恢复依赖或环境 |
| 编译问题 | 编译错误、符号未解析 | 查看第一个编译错误与目标文件 |
| 运行时问题 | 服务启动后失败、HTTP 500 | 查看运行时日志与失败堆栈 |
| 数据 / 配置问题 | schema 错误、配置缺失、样例数据错误 | 核实 DB / 配置并修补来源 |

## 9. Git 路径提醒 | Git path reminder

如果 PowerShell 中 `git` 无法识别，检查：

- `where.exe git`
- `tools/tool-registry.json` 中登记的工具路径
- 包管理器的安装记录

在核实路径解析与本地工具注册表之前，禁止下结论说 “Git 未安装”。
