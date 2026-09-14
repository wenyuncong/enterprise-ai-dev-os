# 安全政策 | Security Policy

> **源文件**：SECURITY.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件对应的是英文正式源 `SECURITY.md`（仓库根目录），中文版为叠加对照层。

---

## 支持的版本 | Supported Versions

`main` 分支是受支持的开发线。

## 报告漏洞 | Reporting A Vulnerability

在维护者有机会审查之前，请勿公开披露漏洞。

如果该仓库已启用 GitHub 私有漏洞报告（private vulnerability reporting），请使用该渠道报告。如果尚未启用，请开一个最小化的 issue 说明需要私下报告，但不得发布 secrets、利用细节、客户数据或私有路径。

## 应当报告的内容 | What To Report

请报告：

- 可能泄露私有文件的脚本
- 边界检查的绕过方式
- 不安全的生成适配器行为
- 意外包含 secrets、本机路径、私有归档或未脱敏材料
- 供应链或工作流风险

## 开源边界事件 | Open-Source Boundary Incidents

如果某次贡献意外包含了私有材料：

1. 停止合并或发布相关改动。
2. 从 PR 中移除该材料。
3. 运行 `py scripts/py/check_open_source_boundary.py --project-root .`。
4. 询问维护者是否需要进行历史清理。

## 必需的本地检查 | Required Local Checks

```powershell
py scripts/py/audit_methodology.py --project-root .
py scripts/py/check_open_source_boundary.py --project-root .
```
