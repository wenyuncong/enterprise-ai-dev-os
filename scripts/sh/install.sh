#!/usr/bin/env bash
set -euo pipefail

TARGET="."
MODE="lite"
SOURCE_PATH=""
FORCE="0"
DEPLOY_ADAPTERS="0"
ADAPTER_TOOL="verified"
ZIP_URL="https://github.com/wenyuncong/enterprise-ai-dev-os/archive/refs/heads/main.zip"

usage() {
  cat <<'EOF'
Enterprise AI Development OS installer

Usage:
  install.sh [--target PATH] [--mode lite|full] [--source PATH] [--force]
             [--deploy-adapters] [--adapter-tool verified]

Defaults:
  --target .
  --mode lite
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:?missing value for --target}"
      shift 2
      ;;
    --mode)
      MODE="${2:?missing value for --mode}"
      shift 2
      ;;
    --source)
      SOURCE_PATH="${2:?missing value for --source}"
      shift 2
      ;;
    --force)
      FORCE="1"
      shift
      ;;
    --deploy-adapters)
      DEPLOY_ADAPTERS="1"
      shift
      ;;
    --adapter-tool)
      ADAPTER_TOOL="${2:?missing value for --adapter-tool}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ "$MODE" != "lite" && "$MODE" != "full" ]]; then
  echo "--mode must be lite or full" >&2
  exit 2
fi

step() {
  printf '[enterprise-ai-dev-os] %s\n' "$1"
}

abs_path() {
  mkdir -p "$1"
  (cd "$1" && pwd -P)
}

copy_path_safe() {
  local src="$1"
  local dest="$2"
  local label="$3"

  if [[ ! -e "$src" ]]; then
    printf '  [SKIP] %s (source missing)\n' "$label"
    return
  fi

  mkdir -p "$(dirname "$dest")"
  if [[ -e "$dest" ]]; then
    if [[ "$FORCE" != "1" ]]; then
      printf '  [KEEP] %s (already exists; use --force to overwrite)\n' "$label"
      return
    fi
    rm -rf "$dest"
  fi

  if [[ -d "$src" ]]; then
    cp -R "$src" "$dest"
  else
    cp "$src" "$dest"
  fi
  printf '  [OK]   %s\n' "$label"
}

get_source_root() {
  if [[ -n "$SOURCE_PATH" ]]; then
    local resolved
    resolved="$(cd "$SOURCE_PATH" && pwd -P)"
    if [[ ! -f "$resolved/AGENTS.md" ]]; then
      echo "Source path does not look like enterprise-ai-dev-os: $resolved" >&2
      exit 1
    fi
    printf '%s\n' "$resolved"
    return
  fi

  local tmp zip source
  tmp="$(mktemp -d "${TMPDIR:-/tmp}/enterprise-ai-dev-os.XXXXXX")"
  zip="$tmp/source.zip"
  step "Downloading source package" >&2

  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$ZIP_URL" -o "$zip"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$ZIP_URL" -O "$zip"
  else
    echo "curl or wget is required" >&2
    exit 1
  fi

  if command -v unzip >/dev/null 2>&1; then
    unzip -q "$zip" -d "$tmp"
  else
    python3 - "$zip" "$tmp" <<'PY'
import sys, zipfile
with zipfile.ZipFile(sys.argv[1]) as z:
    z.extractall(sys.argv[2])
PY
  fi

  source="$(find "$tmp" -maxdepth 2 -name AGENTS.md -type f -print -quit)"
  if [[ -z "$source" ]]; then
    echo "Downloaded archive does not contain AGENTS.md" >&2
    exit 1
  fi
  dirname "$source"
}

TARGET="$(abs_path "$TARGET")"
SOURCE_ROOT="$(get_source_root)"

step "Installing $MODE mode into $TARGET"

if [[ "$MODE" == "lite" ]]; then
  copy_path_safe "$SOURCE_ROOT/lite/rules/AGENTS.md" "$TARGET/AGENTS.md" "Root AI entrypoint"
  copy_path_safe "$SOURCE_ROOT/lite/rules" "$TARGET/rules" "Lite rules"
  copy_path_safe "$SOURCE_ROOT/lite/docs/_templates" "$TARGET/docs/_templates" "Lite documentation templates"
else
  copy_path_safe "$SOURCE_ROOT/AGENTS.md" "$TARGET/AGENTS.md" "Root AI entrypoint"
  copy_path_safe "$SOURCE_ROOT/CLAUDE.md" "$TARGET/CLAUDE.md" "Claude Code entrypoint"
  copy_path_safe "$SOURCE_ROOT/rules" "$TARGET/rules" "Rules"
  copy_path_safe "$SOURCE_ROOT/skills" "$TARGET/skills" "Official skills"
  copy_path_safe "$SOURCE_ROOT/docs/_templates" "$TARGET/docs/_templates" "Documentation templates"
  copy_path_safe "$SOURCE_ROOT/tools" "$TARGET/tools" "Adapter tools"
  copy_path_safe "$SOURCE_ROOT/scripts/py" "$TARGET/scripts/py" "Audit scripts"
  copy_path_safe "$SOURCE_ROOT/scripts/js" "$TARGET/scripts/js" "CLI scripts"
fi

copy_path_safe "$TARGET/docs/_templates/全项目总控/TASK_BACKLOG_TEMPLATE.md" "$TARGET/docs/全项目总控/TASK_BACKLOG.md" "Task backlog scaffold"

for dir in "docs/每日调研回写" "docs/测试验收报告"; do
  if [[ ! -d "$TARGET/$dir" ]]; then
    mkdir -p "$TARGET/$dir"
    printf '  [OK]   %s/\n' "$dir"
  fi
done

if [[ "$DEPLOY_ADAPTERS" == "1" ]]; then
  if [[ -f "$TARGET/tools/deploy.ps1" ]] && command -v powershell >/dev/null 2>&1; then
    step "Deploying adapters: $ADAPTER_TOOL"
    powershell -NoProfile -ExecutionPolicy Bypass -File "$TARGET/tools/deploy.ps1" -ProjectRoot "$TARGET" -Tool "$ADAPTER_TOOL" -Force
  else
    printf '  [SKIP] Adapter deploy requires full mode and PowerShell\n'
  fi
fi

printf '\nEnterprise AI Development OS installed.\n'
printf 'Next: open your AI coding tool in this project and ask it to read AGENTS.md.\n'
printf 'Validate later with: python scripts/py/score_ai_development_readiness.py --project-root .\n'

