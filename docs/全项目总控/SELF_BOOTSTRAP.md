# 数字生命系统自举能力说明

> 数字生命不是被部署的——它自我部署。不是被配置的——它自我治理。

## 核心原则

传统软件：人写 Dockerfile → 人写部署脚本 → 人配置策略 → 人运维。

数字生命：基因原子 → 原子编排 → 自举执行 → 证据闭环。

## 自举原子清单

### infra.* — 基础设施自举

数字生命拥有以下 L1 原子（无 LLM 依赖），可自行完成部署：

```text
编排流程:
  dockerfile.generate(manifest) → compose.generate(services) → package.offline(src) → package.verify(pkg)
```

| 步骤 | 原子 | 输入 | 输出 |
|---|---|---|---|
| 1 | `infra.dockerfile.generate` | 服务清单 | Dockerfile |
| 2 | `infra.compose.generate` | 多服务清单 | docker-compose.yml |
| 3 | `infra.package.offline` | 项目源码目录 | 离线部署包（tar.gz + 清单） |
| 4 | `infra.package.verify` | 部署包路径 | 完整性校验结果 |

### policy.* — 策略自举

数字生命不需要外部 OPA 二进制，使用 Python 原生策略评估：

```text
编排流程:
  rego.generate(policy_pack) → evaluate(policy_pack, input) → validate_bundle(policy_pack)
```

| 步骤 | 原子 | 输入 | 输出 |
|---|---|---|---|
| 1 | `policy.rego.generate` | PolicyPack | Rego 策略代码 |
| 2 | `policy.evaluate` | PolicyPack + 输入数据 | allow/deny + 匹配规则 |
| 3 | `policy.validate_bundle` | PolicyPack | 结构校验 + 警告 |

## 自举演示

数字生命 agent 收到"部署到 Docker"任务后：

1. **读取自身清单**：从 `GenomeManifest` 和 `InstalledAtomSet` 获取服务列表
2. **编排 infra 原子**：
   - `infra.dockerfile.generate(mode="offline")` → Dockerfile
   - `infra.compose.generate(services=[...])` → docker-compose.yml
   - `infra.package.offline(source_dir=".")` → aios-offline.tar.gz
   - `infra.package.verify(package_path="aios-offline.tar.gz")` → ✅ valid
3. **证据记录**：每个步骤写入 evidence
4. **自我部署**：`docker-compose up`

数字生命 agent 收到"评估策略"任务后：

1. **加载策略**：从 PolicyPack 读取
2. **编排 policy 原子**：
   - `policy.validate_bundle(policy_pack)` → ✅ valid
   - `policy.evaluate(policy_pack, input)` → allowed/denied
   - `policy.rego.generate(policy_pack)` → 可审计的 Rego 代码
3. **证据记录**：决策轨迹可回溯

## 为什么不是手工实现

| 手工实现 | 原子自举 |
|---|---|
| Dockerfile 写死在仓库 | 数字生命按需生成 |
| OPA 外部二进制依赖 | Python 原生评估，零外部依赖 |
| 部署脚本和代码耦合 | 原子可独立升级、独立测试 |
| 策略硬编码在 if/else | 策略声明式，可版本化 |
| 人跑部署流程 | 数字生命自主编排 |

## 符合项目规则

- ✅ 原子服务：每个 infra/policy 原子独立可测试
- ✅ 原子编排：`dockerfile.generate → compose.generate → package.offline → package.verify`
- ✅ 聚合接口：可暴露为 `/api/v1/infra/deploy` 和 `/api/v1/policy/evaluate`
- ✅ 证据闭环：每步写入 evidence
- ✅ 治理原子化：阈值和策略不硬编码
- ✅ 私有化离线：`infra.dockerfile.generate(mode="offline")` 生成完全离线部署包