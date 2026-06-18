<#
.SYNOPSIS
    企业级全AI开发方法论 — 多工具部署脚本
    将 skills/ 和 rules/ 一键部署到多个 AI 编程工具目录

.DESCRIPTION
    从 adapters.json 读取工具映射表，为每个工具：
    1. 创建 skills/ 的符号链接（不改动源文件，永远同步）
    2. 复制 rules/AGENTS.md 到工具的规则文件位置

.PARAMETER Tool
    指定目标工具（codex, trae, qoder, codebuddy, claude, cursor, copilot, windsurf, lingma）
    使用 "all" 部署到所有已验证工具

.PARAMETER DryRun
    仅显示将要执行的操作，不实际执行

.PARAMETER Force
    覆盖已存在的符号链接和文件

.PARAMETER ProjectRoot
    项目根目录，默认为脚本所在目录的上级

.EXAMPLE
    .\deploy.ps1 -Tool all
    .\deploy.ps1 -Tool trae -DryRun
    .\deploy.ps1 -Tool codex,qoder -Force
#>

param(
    [string]$Tool = "all",
    [switch]$DryRun,
    [switch]$Force,
    [string]$ProjectRoot = $null
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $ProjectRoot) { $ProjectRoot = Resolve-Path (Join-Path $scriptDir "..") }
$adaptersPath = Join-Path $scriptDir "adapters.json"

Write-Host "=== AI Tool Deploy ===" -ForegroundColor Cyan
Write-Host "Project Root: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# ─── Load adapter config ───────────────────────────────────────
if (-not (Test-Path $adaptersPath)) {
    Write-Error "adapters.json not found at $adaptersPath"
    exit 1
}
$config = Get-Content $adaptersPath -Raw | ConvertFrom-Json

# ─── Determine target tools ────────────────────────────────────
$targetTools = @()
if ($Tool -eq "all") {
    $targetTools = $config.tools.PSObject.Properties | ForEach-Object { $_.Name }
} else {
    $targetTools = $Tool -split "," | ForEach-Object { $_.Trim() }
}

# ─── Source paths ──────────────────────────────────────────────
$srcSkills = Join-Path $ProjectRoot "skills"
$srcRulesFile  = Join-Path $ProjectRoot "rules" "AGENTS.md"

if (-not (Test-Path $srcSkills)) {
    Write-Error "Source skills/ not found: $srcSkills"
    exit 1
}
if (-not (Test-Path $srcRulesFile)) {
    Write-Error "Source rules/AGENTS.md not found: $srcRulesFile"
    exit 1
}

# ─── Helper functions ──────────────────────────────────────────
function Invoke-DeployStep {
    param($Description, $ScriptBlock)
    if ($DryRun) {
        Write-Host "  [DRY] $Description" -ForegroundColor Yellow
        $true
    } else {
        Write-Host "  $Description" -ForegroundColor Gray
        try {
            & $ScriptBlock
            $true
        } catch {
            Write-Warning "  FAILED: $_"
            $false
        }
    }
}

function New-SymlinkSafe {
    param($Path, $Target)
    try {
        New-Item -ItemType SymbolicLink -Path $Path -Target $Target -Force:$Force -ErrorAction Stop | Out-Null
        Write-Host "    OK (symlink)" -ForegroundColor DarkGreen
    } catch {
        try {
            New-Item -ItemType Junction -Path $Path -Target $Target -Force:$Force -ErrorAction Stop | Out-Null
            Write-Host "    OK (junction)" -ForegroundColor DarkYellow
        } catch {
            throw "Symlink/junction failed. Run as admin or enable Developer Mode for symlink support."
        }
    }
}

# ─── Deploy per tool ───────────────────────────────────────────
$results = @{}
foreach ($toolName in $targetTools) {
    $toolCfg = $config.tools.$toolName
    if (-not $toolCfg) {
        Write-Warning "Tool not found in adapters.json: $toolName"
        $results[$toolName] = $false
        continue
    }

    Write-Host "[$toolName] $($toolCfg.name)" -ForegroundColor Green

    # ── Skills symlink ─────────────────────────────────────────
    $toolSkillsDir = Join-Path $ProjectRoot $toolCfg.skills_dir

    $skillOk = Invoke-DeployStep "Skills: skills/ -> $($toolCfg.skills_dir)" {
        $parent = Split-Path -Parent $toolSkillsDir
        if (-not (Test-Path $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }

        if (Test-Path $toolSkillsDir) {
            if ($Force) {
                if ((Get-Item $toolSkillsDir).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                    (Get-Item $toolSkillsDir).Delete()
                } else {
                    Remove-Item $toolSkillsDir -Recurse -Force
                }
            } else {
                Write-Host "    (exists, use -Force to overwrite)" -ForegroundColor DarkGray
                return
            }
        }

        New-SymlinkSafe -Path $toolSkillsDir -Target $srcSkills
    }

    # ── Rules copy ─────────────────────────────────────────────
    $toolRulesTarget = Join-Path $ProjectRoot $toolCfg.rules_file
    $toolRulesNormalized = [System.IO.Path]::GetFullPath($toolRulesTarget)
    $srcRulesNormalized = [System.IO.Path]::GetFullPath($srcRulesFile)

    # Skip self-copy
    if ($toolRulesNormalized -eq $srcRulesNormalized) {
        Write-Host "  Rules: source = target, skip (already in place)" -ForegroundColor DarkGray
        $results[$toolName] = $skillOk
        continue
    }

    Invoke-DeployStep "Rules: AGENTS.md -> $($toolCfg.rules_file)" {
        $rulesDir = Split-Path -Parent $toolRulesTarget
        if ($rulesDir -and -not (Test-Path $rulesDir)) {
            New-Item -ItemType Directory -Path $rulesDir -Force | Out-Null
        }

        if (Test-Path $toolRulesTarget) {
            if ($Force) {
                Remove-Item $toolRulesTarget -Force
            } else {
                # Compare content - if identical, skip
                $existingContent = Get-Content $toolRulesTarget -Raw
                $sourceContent = Get-Content $srcRulesFile -Raw
                if ($existingContent.Trim() -eq $sourceContent.Trim()) {
                    Write-Host "    OK (identical, skip)" -ForegroundColor DarkGray
                    return
                }
                Write-Host "    (differs, use -Force to overwrite)" -ForegroundColor DarkGray
                return
            }
        }

        Copy-Item -Path $srcRulesFile -Destination $toolRulesTarget -Force
        Write-Host "    OK (copied)" -ForegroundColor DarkGreen
    }

    $results[$toolName] = $skillOk
}

# ─── Summary ───────────────────────────────────────────────────
Write-Host ""
Write-Host "=== Deploy Summary ===" -ForegroundColor Cyan
foreach ($kv in $results.GetEnumerator()) {
    $icon = if ($kv.Value) { "[OK]" } else { "[FAIL]" }
    $color = if ($kv.Value) { "Green" } else { "Red" }
    Write-Host "  $icon $($kv.Key)" -ForegroundColor $color
}

if ($DryRun) {
    Write-Host "`nDry run complete. Remove -DryRun to execute." -ForegroundColor Yellow
} else {
    Write-Host "`nDeploy complete." -ForegroundColor Cyan
    $deployedDirs = $targetTools | Where-Object { $results[$_] } | ForEach-Object {
        $cfg = $config.tools.$_
        "  $($cfg.skills_dir)"
    }
    Write-Host "Skills synced to:" -ForegroundColor Gray
    $deployedDirs | ForEach-Object { Write-Host $_ -ForegroundColor DarkGray }
}
