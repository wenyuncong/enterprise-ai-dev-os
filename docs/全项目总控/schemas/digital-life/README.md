# AI-OS 数字生命核心协议 Schema

本目录存放数字生命智能体 P0/P1 阶段的机器可读协议。它们不是运行时代码，也不是页面说明，而是 AI-OS runtime 后续实现原子服务、原子编排和聚合接口时必须遵守的契约。

## 边界

- 理论母体：本目录定义协议和约束。
- AI-OS runtime：读取或生成等价 Schema，落地后端原子服务、编排和接口。
- GERP：作为真实业务场景验证这些协议是否可用。

## Schema 清单

| 文件 | 对象 | 用途 |
|---|---|---|
| `authority-profile.schema.json` | `AuthorityProfile` | 公有云、私有云、完全离线身份权威 |
| `life-identity.schema.json` | `LifeIdentity` | 数字生命全局身份、公钥、证书、登记状态 |
| `genome-manifest.schema.json` | `GenomeManifest` | 数字生命引用的基因原子清单 |
| `installed-atom-set.schema.json` | `InstalledAtomSet` | 某个运行节点已安装且可调用的原子集合 |
| `birth-certificate.schema.json` | `BirthCertificate` | 出生证书，绑定身份、权威、初始基因清单 |
| `lifecycle-event.schema.json` | `LifecycleEvent` | 生命周期事件、状态迁移、证据引用 |

## 强制原则

1. 基因库不属于单个数字生命内部硬逻辑。
2. 数字生命只保存基因引用、安装集合、运行状态和成长档案。
3. 公有云权威必须可被企业私有权威或完全离线权威替代。
4. 每个状态变化、身份变化、基因安装和外部动作都必须能写入证据。
5. 后续实现必须保持原子服务 + 原子编排 + 聚合接口。

