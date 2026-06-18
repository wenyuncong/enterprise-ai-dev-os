# Installation | 安装

Enterprise AI Development OS can be installed into an existing project with one command. The default `lite` mode is the recommended starting point: it adds the AI entrypoint, rules, documentation templates, and task backlog scaffold without copying the full skill library.

Enterprise AI Development OS 支持一条命令安装到现有项目。默认 `lite` 模式是推荐起点：只加入 AI 入口规则、文档模板和任务清单骨架，不会一次性复制完整 Skill 库。

## One-Click Install | 一键安装

PowerShell:

```powershell
iwr -UseBasicParsing https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/ps1/install.ps1 | iex
```

Bash:

```bash
curl -fsSL https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/sh/install.sh | bash
```

## Full Install | 完整安装

PowerShell:

```powershell
$u = "https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/ps1/install.ps1"
$s = Join-Path $env:TEMP "enterprise-ai-dev-os-install.ps1"
iwr -UseBasicParsing $u -OutFile $s
powershell -NoProfile -ExecutionPolicy Bypass -File $s -TargetPath . -Mode full
```

Bash:

```bash
curl -fsSL https://raw.githubusercontent.com/wenyuncong/enterprise-ai-dev-os/main/scripts/sh/install.sh | bash -s -- --mode full
```

## Update Existing Files | 更新已有文件

Installers do not overwrite existing files by default. Use `-Force` or `--force` when you intentionally want to refresh generated methodology files.

安装脚本默认不覆盖已有文件。只有明确需要刷新规则、模板或 Skill 时，才使用 `-Force` 或 `--force`。

## Validate | 验证

After full install:

```bash
python scripts/py/score_ai_development_readiness.py --project-root .
python scripts/py/audit_methodology.py --project-root .
```

