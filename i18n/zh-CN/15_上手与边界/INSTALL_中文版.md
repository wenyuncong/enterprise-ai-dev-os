# 安装 | Installation

> **源文件**：docs/公开材料/INSTALL.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应，不删章节；英文标识符、命令、代码块、门禁代号原样保留。

---

Enterprise AI Development OS 支持一条命令安装到现有项目。默认 `lite` 模式是推荐起点：只加入 AI 入口规则、文档模板和任务清单骨架，不会一次性复制完整 Skill 库。

## 一键安装 | One-Click Install

PowerShell：

```powershell
iwr -UseBasicParsing https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/ps1/install.ps1 | iex
```

Bash：

```bash
curl -fsSL https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/sh/install.sh | bash
```

## 完整安装 | Full Install

PowerShell：

```powershell
$u = "https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/ps1/install.ps1"
$s = Join-Path $env:TEMP "enterprise-ai-dev-os-install.ps1"
iwr -UseBasicParsing $u -OutFile $s
powershell -NoProfile -ExecutionPolicy Bypass -File $s -TargetPath . -Mode full
```

Bash：

```bash
curl -fsSL https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/sh/install.sh | bash -s -- --mode full
```

## 更新已有文件 | Update Existing Files

安装脚本默认不覆盖已有文件。只有当你明确要刷新生成的方法论文件时，才使用 `-Force` 或 `--force`。

## 验证 | Validate

完整安装之后执行：

```bash
python scripts/py/score_ai_development_readiness.py --project-root .
python scripts/py/audit_methodology.py --project-root .
```
