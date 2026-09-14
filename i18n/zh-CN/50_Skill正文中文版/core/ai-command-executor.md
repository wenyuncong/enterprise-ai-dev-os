# `ai-command-executor` — 标准化命令执行引擎

> **源文件**：skills/core/ai-command-executor/SKILL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **注意**：本文件是中文对照版，不是 Skill 的正式加载源。正式源为英文 `skills/`。

```yaml
name: ai-command-executor
description: "Standardize command execution, environment checks, tool discovery, approved script usage, runtime diagnosis, logs, service start/stop, build verification, and evidence capture. Use before shell/CLI work, runtime debugging, or tool installation decisions."
```

**中文描述**：把命令执行、环境检查、工具发现、已批准脚本的使用、运行时诊断、日志、服务启停、构建验证与证据采集标准化。在任何 shell/CLI 操作、运行时排障或工具安装决策之前使用。

---

# ai-command-executor — Standardized Command Execution Engine | 标准化命令执行引擎

## Purpose | 用途

把执行请求转化为标准化、可审计的命令运行：

- 已批准入口的选择（优先使用既有脚本）
- 先检查后执行（check before execute）的核实
- 脚本/命令的执行记录
- 从日志与输出做根因诊断
- 最安全的下一步建议

本 Skill 只负责**执行与诊断**，不负责任务路由或项目排期。

## Rule | 规则

**当项目已经提供了已批准入口时，禁止发明新的命令流程。**

执行优先级：
1. 项目标准脚本（例如 `scripts/bat/`、`scripts/ps1/`、`scripts/py/`）
2. 项目内可复用的辅助脚本
3. 有明确理由并被记录的文档化单行命令
4. 只有在给出明确理由并留档时才使用自研 shell 命令

---

## Check-Before-Execute Protocol | 执行前检查

在运行任何命令之前，核实：

1. **目标**：用户想要的精确结果是什么？
2. **已批准脚本**：哪个既有脚本已经覆盖了这件事？
3. **环境事实**：执行前必须为真的前提有哪些？

| 检查项 | 示例 | 命令 |
|---|---|---|
| git 可用性 | `git` 是否在 PATH 上？ | `where git` 或检查已知路径 |
| Node.js 版本 | 工具所需的 Node 是否正确？ | `node --version` |
| Java 版本 | JDK 是否正确？ | `java --version` |
| 端口可用性 | 端口是否已被占用？ | `netstat -an` 或等价命令 |
| 进程状态 | 服务是否已在运行？ | `ps aux` 或等价命令 |
| 磁盘空间 | 构建所需空间是否充足？ | `df -h` 或等价命令 |

---

## Standard Workflow | 标准工作流

### Phase 1: Environment Verification | 阶段 1：环境核实
- 核实工具依赖是否可用
- **若有任何工具缺失 → 调用 ai-tool-bootstrapper 自动安装**
- 启动服务前检查端口可用性
- 确认工作目录与权限

### Phase 2: Script Selection | 阶段 2：脚本选择
- 检查 `scripts/` 目录是否已有现成方案
- 优先使用项目标准脚本，而不是临时命令
- 若没有现成脚本，把该命令保存为新的可复用脚本

### Phase 3: Execution | 阶段 3：执行
- 带合适参数运行命令
- 分别捕获 stdout 与 stderr
- 记录执行耗时与退出码

### Phase 4: Diagnosis | 阶段 4：诊断
- 解析输出，匹配已知错误模式
- 检查日志以获取更多上下文
- 分类：环境问题、代码问题，还是配置问题

### Phase 5: Recommendation | 阶段 5：建议
- 若成功：报告结果，给出验证步骤建议
- 若失败：归类根因、给出修复建议，并提供精确命令

---

## Working Tree Gate | 工作区（working-tree）门禁

在开始新任务之前，以及在提交已完成任务之前，核实工作区（working-tree）状态：

```
1. Check for unexpected dirty files
2. Stage only current task's files
3. Verify staged changes with diff
4. Classify untracked files as evidence, temp, or misplaced
```

**中文对照**：

1. 检查是否存在意料之外的脏文件。
2. 只暂存当前任务的文件。
3. 用 diff 核实已暂存的改动。
4. 把未跟踪文件归类为：证据、临时文件，或放错位置。

**规则**：
- 禁止对无关脏文件执行整仓库清理
- 只暂存当前任务文件，提交前必须核实
- 位于文档化目录下的未跟踪文件，视为可能有效的证据
- 若无关脏文件阻塞执行，用带描述性信息的说明显式 stash 它们

---

## Command Category Reference | 命令分类参考

| 类别 | 典型脚本前缀 | 示例 |
|---|---|---|
| 构建/编译 | `build-*`、`compile-*` | `build-backend.ps1`、`npm run build` |
| 服务启停 | `start-*`、`stop-*` | `start-server.ps1`、`docker-compose up` |
| 数据库 | `db-*`、`migrate-*` | `db-migrate.sh`、`mysql -e "..."` |
| 测试 | `test-*`、`run-tests-*` | `run-tests.sh`、`npm test` |
| 部署 | `deploy-*`、`release-*` | `deploy-staging.sh` |
| 健康检查 | `health-*`、`check-*` | `health-check.sh`、`curl /health` |

---

## Guardrails | 防护规则

- 禁止在同一工作区并行执行构建（共享输出目录）
- 未先检查端口之前，禁止假定服务没有在运行
- 若旧进程可能仍占用端口，禁止只凭健康检查端点下结论
- 前一步骤失败后，禁止跳过环境核实
- 未经用户明确确认，禁止使用破坏性（destructive）命令（`reset --hard`、`clean -fdx`）

## Maturity | 成熟度

**Stage**：Effective（有效）—— 从 28KB 的企业级命令执行工作流中提炼，含环境特定诊断。

## Integration with ai-tool-bootstrapper | 与 ai-tool-bootstrapper 的集成

当环境核实检测到工具缺失时，不要失败。改为：

1. 报告："Tool X not found"
2. 调用 ai-tool-bootstrapper 自动安装 X
3. 安装后重新核实
4. 继续执行

这样形成自愈环境：缺失工具被自动获取，而不是阻塞开发。

---

## Evolution History | 进化记录

- v1.0.0：从 gerp-command-executor 提炼（原始 28KB）
- v1.1.0：泛化为通用命令执行模式
- Source：Daily enterprise development environments with multi-service orchestrationr

---

## 译注

- 源文件末尾存在残留字符：`## Evolution History | 进化记录` 的 `Source` 行以 `orchestrationr` 结尾，其后还有一行孤立的 `r`（源文件第 142–143 行）。这是源文件的笔误/脏字符，本译文照抄 `Source` 行的英文原文，并删除孤立行；源文件未被改动。
- 源文件 H1 位于 `## Purpose` 之前、`## Rule` 之前；本译文保持源文件的章节顺序。
- 源文件 `## Working Tree Gate | 工作树闸门` 的标题按术语口径统一为「工作区（working-tree）门禁」，并按术语表要求保留英文 `working-tree`。
- `docker-compose up`（Compose V1 写法）与 `mysql -e "..."` 为源文件既有示例，本译文原样保留，未替换为 Compose V2 的 `docker compose up`。
- `skills/SKILL_MANIFEST.json` 中该 Skill 的 `maturity` 为 `verified`，正文 `## Maturity` 自述 Stage 为 `Effective`，两者口径不同，本译文如实保留原文。
