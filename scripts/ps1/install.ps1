<#
.SYNOPSIS
    One-click installer for Enterprise AI Development OS.

.DESCRIPTION
    Installs the portable rules, templates, and optional skills into an
    existing project. The default lite mode is intentionally small and safe:
    it adds the AI session entrypoint, rule file, documentation templates, and
    task backlog scaffold.

.PARAMETER TargetPath
    Project path to install into. Defaults to the current directory.

.PARAMETER Mode
    lite or full. Lite installs minimal rules and templates. Full installs the
    complete rules, official skills, adapter tools, and audit scripts.

.PARAMETER SourcePath
    Optional local source repository path. Used for development/testing.

.PARAMETER Force
    Overwrite existing target files.

.PARAMETER DeployAdapters
    After full install, run tools/deploy.ps1 to generate adapter files.
#>

param(
    [string]$TargetPath = ".",
    [ValidateSet("lite", "full")]
    [string]$Mode = "lite",
    [string]$SourcePath = "",
    [string]$RepositoryZipUrl = "https://github.com/wenyuncong/enterprise-ai-dev-os/archive/refs/heads/main.zip",
    [switch]$Force,
    [switch]$DeployAdapters,
    [string]$AdapterTool = "verified"
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "[enterprise-ai-dev-os] $Message" -ForegroundColor Cyan
}

function Resolve-FullPath {
    param([string]$Path)
    $item = Get-Item -LiteralPath $Path -ErrorAction SilentlyContinue
    if ($item) { return $item.FullName }
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }
    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Path))
}

function Copy-PathSafe {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Label
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        Write-Host "  [SKIP] $Label (source missing)" -ForegroundColor Yellow
        return
    }

    $parent = Split-Path -Parent $Destination
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    if (Test-Path -LiteralPath $Destination) {
        if (-not $Force) {
            Write-Host "  [KEEP] $Label (already exists; use -Force to overwrite)" -ForegroundColor DarkYellow
            return
        }
        Remove-Item -LiteralPath $Destination -Recurse -Force
    }

    $sourceItem = Get-Item -LiteralPath $Source
    if ($sourceItem.PSIsContainer) {
        Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
    } else {
        Copy-Item -LiteralPath $Source -Destination $Destination -Force
    }
    Write-Host "  [OK]   $Label" -ForegroundColor Green
}

function Get-SourceRoot {
    if ($SourcePath) {
        $resolved = Resolve-FullPath $SourcePath
        if (-not (Test-Path -LiteralPath (Join-Path $resolved "AGENTS.md"))) {
            throw "SourcePath does not look like enterprise-ai-dev-os: $resolved"
        }
        return $resolved
    }

    $tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("enterprise-ai-dev-os-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
    $zipPath = Join-Path $tempRoot "source.zip"

    Write-Step "Downloading source package"
    Invoke-WebRequest -UseBasicParsing -Uri $RepositoryZipUrl -OutFile $zipPath
    Expand-Archive -LiteralPath $zipPath -DestinationPath $tempRoot -Force

    $source = Get-ChildItem -LiteralPath $tempRoot -Directory |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "AGENTS.md") } |
        Select-Object -First 1

    if (-not $source) {
        throw "Downloaded archive does not contain AGENTS.md"
    }

    return $source.FullName
}

$target = Resolve-FullPath $TargetPath
if (-not (Test-Path -LiteralPath $target)) {
    New-Item -ItemType Directory -Path $target -Force | Out-Null
}

$sourceRoot = Get-SourceRoot
Write-Step "Installing $Mode mode into $target"

if ($Mode -eq "lite") {
    Copy-PathSafe -Source (Join-Path $sourceRoot "lite/rules/AGENTS.md") -Destination (Join-Path $target "AGENTS.md") -Label "Root AI entrypoint"
    Copy-PathSafe -Source (Join-Path $sourceRoot "lite/rules") -Destination (Join-Path $target "rules") -Label "Lite rules"
    Copy-PathSafe -Source (Join-Path $sourceRoot "lite/docs/_templates") -Destination (Join-Path $target "docs/_templates") -Label "Lite documentation templates"
} else {
    Copy-PathSafe -Source (Join-Path $sourceRoot "AGENTS.md") -Destination (Join-Path $target "AGENTS.md") -Label "Root AI entrypoint"
    Copy-PathSafe -Source (Join-Path $sourceRoot "CLAUDE.md") -Destination (Join-Path $target "CLAUDE.md") -Label "Claude Code entrypoint"
    Copy-PathSafe -Source (Join-Path $sourceRoot "rules") -Destination (Join-Path $target "rules") -Label "Rules"
    Copy-PathSafe -Source (Join-Path $sourceRoot "skills") -Destination (Join-Path $target "skills") -Label "Official skills"
    Copy-PathSafe -Source (Join-Path $sourceRoot "docs/_templates") -Destination (Join-Path $target "docs/_templates") -Label "Documentation templates"
    Copy-PathSafe -Source (Join-Path $sourceRoot "tools") -Destination (Join-Path $target "tools") -Label "Adapter tools"
    Copy-PathSafe -Source (Join-Path $sourceRoot "scripts/py") -Destination (Join-Path $target "scripts/py") -Label "Audit scripts"
    Copy-PathSafe -Source (Join-Path $sourceRoot "scripts/js") -Destination (Join-Path $target "scripts/js") -Label "CLI scripts"
}

$backlogTemplate = Join-Path $target "docs/_templates/全项目总控/TASK_BACKLOG_TEMPLATE.md"
$backlogFile = Join-Path $target "docs/全项目总控/TASK_BACKLOG.md"
Copy-PathSafe -Source $backlogTemplate -Destination $backlogFile -Label "Task backlog scaffold"

foreach ($dir in @("docs/每日调研回写", "docs/测试验收报告")) {
    $path = Join-Path $target $dir
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "  [OK]   $dir/" -ForegroundColor Green
    }
}

if ($DeployAdapters) {
    $deploy = Join-Path $target "tools/deploy.ps1"
    if (-not (Test-Path -LiteralPath $deploy)) {
        Write-Host "  [SKIP] Adapter deploy requires full mode" -ForegroundColor Yellow
    } else {
        Write-Step "Deploying adapters: $AdapterTool"
        & powershell -NoProfile -ExecutionPolicy Bypass -File $deploy -ProjectRoot $target -Tool $AdapterTool -Force
    }
}

Write-Host ""
Write-Host "Enterprise AI Development OS installed." -ForegroundColor Green
Write-Host "Next: open your AI coding tool in this project and ask it to read AGENTS.md."
Write-Host "Validate later with: python scripts/py/score_ai_development_readiness.py --project-root ."
