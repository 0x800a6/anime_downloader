#!/usr/bin/env bash
# Robust Anime Downloader Launcher Script

set -euo pipefail

# --- Prevent Sourcing ---
(return 0 2>/dev/null) && { echo "Do not source this script! Run it as ./run.sh"; return 1; }

# --- CONFIGURABLES ---
REPO_URL="https://github.com/0x800a6/anime_downloader"
VENV_DIR=".venv"
APP_ENTRY="src/main.py"
REQUIREMENTS="requirements.txt"
MIN_PYTHON="3.8"
LAUNCHER_VERSION="1.0.0"

# --- COLORS ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- GLOBALS ---
YES_MODE=0
RESET_VENV=0
UPDATE=0
DEV_MODE=0
CHECK_ONLY=0
SHOW_HELP=0
SHOW_VERSION=0
APP_ARGS=()

# --- UTILS ---
err() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
info() { echo -e "${GREEN}[INFO]${NC} $*"; }
success() { echo -e "${CYAN}[OK]${NC} $*"; }
prompt() { [[ $YES_MODE -eq 1 ]] && return 0; echo -en "${MAGENTA}[?]${NC} $*"; }

# Trap errors
trap 'err "Script failed at line $LINENO."' ERR

# --- BASH CHECK ---
if [ -z "${BASH_VERSION:-}" ]; then
  err "This script must be run with Bash."; exit 1
fi
if (( BASH_VERSINFO[0] < 4 )); then
  err "Bash 4.0+ required. You have $BASH_VERSION."; exit 1
fi

# --- ARGUMENT PARSING ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) SHOW_HELP=1; shift ;;
    -v|--version) SHOW_VERSION=1; shift ;;
    -y|--yes) YES_MODE=1; shift ;;
    -r|--reset-venv) RESET_VENV=1; shift ;;
    -u|--update) UPDATE=1; shift ;;
    -d|--dev) DEV_MODE=1; shift ;;
    -c|--check) CHECK_ONLY=1; shift ;;
    --) shift; APP_ARGS+=("$@") ; break ;;
    *) APP_ARGS+=("$1"); shift ;;
  esac
done

# --- HELP & VERSION ---
if (( SHOW_HELP )); then
  cat <<EOF
${CYAN}Anime Downloader Launcher${NC} (v$LAUNCHER_VERSION)
Usage: $0 [options] [-- [app args]]
Options:
  -h, --help         Show this help message and exit
  -v, --version      Show launcher version and exit
  -y, --yes          Non-interactive mode (auto-confirm prompts)
  -r, --reset-venv   Delete and recreate the Python virtual environment
  -u, --update       Update the repository (if git is available)
  -d, --dev          Run in development mode (no venv, use system Python)
  -c, --check        Run environment checks and exit
  --                 Pass all following arguments to the application
EOF
  exit 0
fi
if (( SHOW_VERSION )); then
  echo "Anime Downloader Launcher v$LAUNCHER_VERSION"; exit 0
fi

# --- BANNER ---
print_banner() {
  echo -e "${CYAN}========================================"
  echo -e "      Anime Downloader Launcher"
  echo -e "========================================${NC}"
  echo -e "${MAGENTA}Date: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
  echo -e "${BLUE}Project: $REPO_URL${NC}"
  echo -e "${CYAN}Launcher: v$LAUNCHER_VERSION${NC}"
  echo
}
print_banner

# --- REQUIRED COMMANDS ---
for cmd in awk grep python3 pip; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    err "Required command '$cmd' not found. Please install it."; exit 1
  fi
done
if ! command -v ffmpeg >/dev/null 2>&1; then
  warn "ffmpeg is not installed or not in PATH. Some features may not work."
else
  success "ffmpeg found: $(command -v ffmpeg)"
fi

# --- PYTHON VERSION CHECK ---
PYTHON_VERSION=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')
if [[ "${PYTHON_VERSION//./}" -lt "${MIN_PYTHON//./}" ]]; then
  err "Python $MIN_PYTHON+ required, found $PYTHON_VERSION."; exit 1
fi

# --- GIT UPDATE ---
if (( UPDATE )); then
  if [ -d .git ] && command -v git >/dev/null 2>&1; then
    info "Checking for updates..."
    git fetch origin >/dev/null 2>&1 || warn "Could not fetch updates."
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    BASE=$(git merge-base @ @{u})
    if [ "$LOCAL" = "$REMOTE" ]; then
      success "You are up to date."
    elif [ "$LOCAL" = "$BASE" ]; then
      warn "A new version is available."
      if (( YES_MODE )); then yn=Y; else prompt "Update now? [Y/n] "; read -r yn; yn=${yn:-Y}; fi
      if [[ "$yn" =~ ^[Yy]$ ]]; then
        git pull --rebase && success "Repository updated. Please re-run the script." && exit 0
      fi
    else
      warn "Local changes detected or branch is ahead. Skipping update."
    fi
  else
    warn "Not a git repository or git not found."
  fi
  exit 0
fi

# --- VENV HANDLING ---
if (( RESET_VENV )) && [ -d "$VENV_DIR" ]; then
  warn "Resetting Python virtual environment ($VENV_DIR)..."
  rm -rf "$VENV_DIR"
  success "Virtual environment removed."
fi

if (( ! DEV_MODE )) && [ ! -d "$VENV_DIR" ]; then
  warn "Python virtual environment ($VENV_DIR) not found."
  if (( YES_MODE )); then yn=Y; else prompt "Create one now? [Y/n] "; read -r yn; yn=${yn:-Y}; fi
  if [[ "$yn" =~ ^[Yy]$ ]]; then
    info "Creating virtual environment..."
    python3 -m venv "$VENV_DIR" || { err "Failed to create venv."; exit 1; }
    success "Virtual environment created."
    info "Installing dependencies from $REQUIREMENTS..."
    "$VENV_DIR/bin/pip" install --upgrade pip || { err "pip upgrade failed."; exit 1; }
    if [ -f "$REQUIREMENTS" ]; then
      "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS" || { err "Dependency install failed."; exit 1; }
      success "Dependencies installed."
    else
      warn "$REQUIREMENTS not found. Skipping dependency install."
    fi
  else
    warn "Proceeding without a virtual environment."
    DEV_MODE=1
  fi
fi

# --- PYTHON EXECUTABLE ---
if (( ! DEV_MODE )) && [ -x "$VENV_DIR/bin/python" ]; then
  PYTHON_EXEC="$VENV_DIR/bin/python"
  info "Using Python from virtual environment."
else
  PYTHON_EXEC="python3"
  warn "Using system Python. Consider creating a virtual environment for isolation."
fi

# --- REQUIREMENTS CHECK ---
if [ -f "$REQUIREMENTS" ] && [ -x "$VENV_DIR/bin/python" ] && (( ! DEV_MODE )); then
  if [ "$REQUIREMENTS" -nt "$VENV_DIR" ]; then
    warn "$REQUIREMENTS has changed since venv was created."
    if (( YES_MODE )); then yn=Y; else prompt "Update dependencies in venv? [Y/n] "; read -r yn; yn=${yn:-Y}; fi
    if [[ "$yn" =~ ^[Yy]$ ]]; then
      info "Updating dependencies..."
      "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS" || { err "Dependency update failed."; exit 1; }
      success "Dependencies updated."
    fi
  fi
fi

# --- PIP OUTDATED CHECK ---
if (( ! DEV_MODE )) && [ -x "$VENV_DIR/bin/pip" ]; then
  OUTDATED=$("$VENV_DIR/bin/pip" list --outdated --format=columns | grep -v 'Package' || true)
  if [[ -n "$OUTDATED" ]]; then
    warn "Some Python packages are outdated in venv."
    if (( YES_MODE )); then upyn=N; else prompt "Upgrade all packages? [y/N] "; read -r upyn; upyn=${upyn:-N}; fi
    if [[ "$upyn" =~ ^[Yy]$ ]]; then
      info "Upgrading all packages in venv..."
      "$VENV_DIR/bin/pip" list --outdated --format=freeze | cut -d= -f1 | xargs -n1 "$VENV_DIR/bin/pip" install -U
      success "All packages upgraded."
    fi
  fi
fi

# --- ENVIRONMENT SUMMARY ---
info "Environment summary:"
echo -e "  ${CYAN}Python:${NC} $($PYTHON_EXEC --version 2>&1)"
if command -v ffmpeg >/dev/null 2>&1; then
  echo -e "  ${CYAN}ffmpeg:${NC} $(ffmpeg -version | head -n1)"
else
  echo -e "  ${CYAN}ffmpeg:${NC} not found"
fi
if [ -f "$APP_ENTRY" ]; then
  APP_VERSION=$($PYTHON_EXEC "$APP_ENTRY" --version 2>/dev/null || echo "unknown")
  echo -e "  ${CYAN}Anime Downloader version:${NC} ${APP_VERSION}"
fi
echo -e "  ${CYAN}Virtualenv:${NC} $([[ -x "$VENV_DIR/bin/python" ]] && echo "yes" || echo "no")"
echo -e "  ${CYAN}Working dir:${NC} $(pwd)"
echo

if (( CHECK_ONLY )); then
  success "Environment check complete."
  exit 0
fi

# --- PAUSE BEFORE LAUNCH (unless --yes) ---
if (( ! YES_MODE )); then
  echo
  prompt "Press [Enter] to launch the Anime Downloader GUI..."
  read -r _
fi

# --- LAUNCH APP ---
info "Launching Anime Downloader GUI..."
exec "$PYTHON_EXEC" "$APP_ENTRY" "${APP_ARGS[@]}"
exit 0  # fallback, should never be reached
