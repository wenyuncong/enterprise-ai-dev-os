<#
.SYNOPSIS
    Smoke tests for tools/deploy.ps1 and tools/adapters.json.
    Pure pwsh assertions, no external test framework. Dry-run only:
    these tests never write to user-level or project adapter paths.

.USAGE
    pwsh -NoProfile -File scripts/ps1/test_deploy.ps1
    Exit code 0 = all tests passed, 1 = failures.
#>
$ErrorActionPreference = "Stop"
$script:failures = @()

function Assert($condition, $message) {
    if (-not $condition) {
        $script:failures += $message
        Write-Host "  [FAIL] $message" -ForegroundColor Red
    } else {
        Write-Host "  [OK]   $message" -ForegroundColor Green
    }
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$adapters = Join-Path $root "tools\adapters.json"
$deploy = Join-Path $root "tools\deploy.ps1"

Write-Host "=== deploy.ps1 / adapters.json smoke tests ===" -ForegroundColor Cyan
Write-Host "Root: $root"

# 1. adapters.json is valid JSON with required structure
try {
    $config = Get-Content $adapters -Raw | ConvertFrom-Json
    Assert ($null -ne $config.tools) "adapters.json parses and has tools"
    Assert ($null -ne $config.globalTargets) "adapters.json has globalTargets"
    $gt = $config.globalTargets.PSObject.Properties | Where-Object { $_.Name -eq "codex" -or $_.Name -eq "claude" }
    Assert ($gt.Count -eq 2) "globalTargets registers codex and claude"
    Assert ($config.globalTargets.codex.path -like "~/*") "codex global target uses user-level path"
    Assert ($config.globalTargets.claude.path -like "~/*") "claude global target uses user-level path"
    Assert (Test-Path (Join-Path $root $config.globalTargets.codex.source)) "codex global source exists"
} catch {
    Assert $false "adapters.json valid: $($_.Exception.Message)"
}

# 2. -Scope global dry run touches only global targets
$globalOut = & pwsh -NoProfile -File $deploy -Scope global -DryRun 2>&1 | Out-String
Assert ($globalOut -match "\[codex\] global rules") "global dry-run lists codex target"
Assert ($globalOut -match "\[claude\] global rules") "global dry-run lists claude target"
Assert ($globalOut -match "\[DRY\]") "global dry-run does not write files"
Assert ($globalOut -notmatch "Skills: skills/ ->") "global scope skips project skills deploy"

# 3. -Scope project dry run lists adapters
$projOut = & pwsh -NoProfile -File $deploy -Tool verified -Scope project -DryRun 2>&1 | Out-String
Assert ($projOut -match "Adapter Deploy") "project dry-run runs"
Assert ($projOut -notmatch "Global User-Level") "project scope skips global deploy"

# 4. -Scope both dry run includes both
$bothOut = & pwsh -NoProfile -File $deploy -Tool verified -Scope both -DryRun 2>&1 | Out-String
Assert ($bothOut -match "Adapter Deploy") "both scope includes project deploy"
Assert ($bothOut -match "Global User-Level") "both scope includes global deploy"

Write-Host ""
if ($script:failures.Count -eq 0) {
    Write-Host "ALL TESTS PASSED ($($script:failures.Count) failures)" -ForegroundColor Green
    exit 0
} else {
    Write-Host "$($script:failures.Count) TEST(S) FAILED" -ForegroundColor Red
    exit 1
}
