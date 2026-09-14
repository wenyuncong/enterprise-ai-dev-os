# 轻量规则运行时 | Rule Runtime Lite

> **源文件**：docs/公开材料/RULE_RUNTIME_LITE.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

---

Rule Runtime Lite 是让项目规则可执行的未来设计方向。当前开源方法论不依赖它才能使用，它也不是已经完成的完整实现。

## 目标 | Goal

把选定的文档规则转成小型、可测试的检查，可在 AI 辅助改代码之前、过程中或之后执行。

## 非目标 | Non-Goals

- 不做大型 AI 平台重写
- 不做模型生命周期管理
- 不做 Kubernetes 调度器
- 不做区块链审计存储
- 不做物理门禁集成
- 不声称所有业务规则都能自动验证

## 运行阶段 | Runtime Stages

| 阶段 | 用途 | 示例 |
|---|---|---|
| 生成前 | 在 AI 写文件之前加载约束 | 必需 Skill、文件存放位置、禁止路径 |
| 生成中 | 给 AI 提供可调用或可推理的结构化检查 | 路径策略、Schema 清单、适配器目标校验 |
| 生成后 | 在「完成」之前验证输出 | 审计脚本、边界检查、运行时验证 |
| 进化 | 把重复失败转成更强的规则 | 增加规则、模板、Skill 或测试 |

## 最小可行规则类型 | Minimum Viable Rule Types

从便宜、确定性强、有用的规则开始：

| 类型 | 示例 | 实现路径 |
|---|---|---|
| 路径规则 | 私有目录中不放文件，不提交生成的适配器产物 | Python 审计 |
| 结构规则 | 必需的 `docs/_templates/` 与 `skills/` 资产存在 | Python 审计 |
| 清单规则 | 每个 `SKILL.md` 都在 `SKILL_MANIFEST.json` 中登记 | Python 审计 |
| 文本残留规则 | 不含硬编码的本地路径或历史仓库名 | Python 审计 |
| 适配器规则 | 已验证的适配器能无错误地 dry-run | PowerShell dry-run |

AST 或 Tree-sitter 规则以后有用，但应当在简单确定性检查已证明有可测量价值之后再加入。

## 规则文件草案 | Rule File Sketch

```yaml
rules:
  - id: no_private_paths
    severity: error
    scope:
      include:
        - README.md
        - docs/**
        - skills/**
      exclude:
        - docs/公开材料/**
    check:
      type: text_pattern
      deny:
        - "[A-Z]:\\\\"
        - "legacy-private-repo-name"
    fix_hint: "Move private paths to non-public notes or replace with portable placeholders."
```

这是设计草案，不是已经承诺的引擎接口。

## 公开版与高级版边界 | Public / Advanced Boundary

适合开源：

- 规则 Schema 草案
- 简单的确定性审计
- 使用脱敏夹具（fixture）的示例
- 适配器验证报告

可能的高级/商业层：

- 团队策略包
- 规则命中分析
- 多仓库治理看板
- MCP / 工具调用审计网关
- 企业审批工作流

## 首个实现候选 | First Implementation Candidate

最安全的首次实现不是 AST，而是围绕本仓库已经在用的检查做一个小的规则运行器：

```text
rule config -> deterministic checks -> JSON report -> README/site badge or release evidence
```

这样能让项目保持脚踏实地，避免在证据出现之前就构建一个过大的平台。
