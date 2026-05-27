#!/usr/bin/env bash
# =============================================================================
# uninstall.sh — remove hckfetch from the system
# =============================================================================
#
# What this script does:
#   1. Removes hckfetch and hckfetch-wrap from the install prefix.
#   2. Removes the hckfetch block from ~/.bashrc and ~/.zshrc.
#   3. Optionally removes the log directory ~/.hckfetch_logs/.
#
# Usage:
#   ./uninstall.sh           — interactive mode (asks before deleting logs)
#   ./uninstall.sh --purge   — also delete all logs without asking
#
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()    { echo -e " ${CYAN}[*]${RESET} $*"; }
success() { echo -e " ${GREEN}[✓]${RESET} $*"; }
warn()    { echo -e " ${YELLOW}[!]${RESET} $*"; }

PURGE=0
for arg in "$@"; do
    [[ "$arg" == "--purge" ]] && PURGE=1
done

# ---------------------------------------------------------------------------
# Determine install prefix
# ---------------------------------------------------------------------------
if [[ "${EUID:-$(id -u)}" -eq 0 ]]; then
    INSTALL_PREFIX="/usr/local/bin"
else
    INSTALL_PREFIX="${HOME}/.local/bin"
fi

LOG_DIR="${HOME}/.hckfetch_logs"

# ---------------------------------------------------------------------------
# Step 1: Remove binaries
# ---------------------------------------------------------------------------
for script in hckfetch hckfetch-wrap; do
    target="${INSTALL_PREFIX}/${script}"
    if [[ -f "$target" ]]; then
        info "Removing ${target} ..."
        rm -f "$target"
        success "Removed ${target}."
    else
        warn "${target} not found — skipping."
    fi
done

# ---------------------------------------------------------------------------
# Step 2: Remove hckfetch block from rc files
# ---------------------------------------------------------------------------
MARKER_BEGIN="# ---- hckfetch: begin"
MARKER_END="# ---- hckfetch: end"

for rc in "${HOME}/.bashrc" "${HOME}/.zshrc"; do
    if [[ ! -f "$rc" ]]; then
        continue
    fi
    if ! grep -qF "$MARKER_BEGIN" "$rc" 2>/dev/null; then
        warn "${rc}: no hckfetch block found — skipping."
        continue
    fi
    info "Removing hckfetch block from ${rc} ..."

    # Use awk to delete lines between (and including) the two markers
    awk "
        /^${MARKER_BEGIN//\//\\/}/ { skip=1 }
        skip { if (/^${MARKER_END//\//\\/}/) { skip=0 } next }
        { print }
    " "$rc" > "${rc}.hckfetch_bak"
    mv "${rc}.hckfetch_bak" "$rc"
    success "Cleaned ${rc}."
done

# ---------------------------------------------------------------------------
# Step 3: Optionally remove log directory
# ---------------------------------------------------------------------------
if [[ -d "$LOG_DIR" ]]; then
    if [[ "$PURGE" -eq 1 ]]; then
        info "Removing log directory ${LOG_DIR}/ (--purge) ..."
        rm -rf "${LOG_DIR:?}"
        success "Log directory removed."
    else
        echo
        read -rp "$(echo -e " ${YELLOW}Remove log directory ${LOG_DIR}/? [y/N]${RESET} ")" yn
        case "$yn" in
            [yY]|[yY][eE][sS])
                info "Removing ${LOG_DIR}/ ..."
                rm -rf "${LOG_DIR:?}"
                success "Log directory removed."
                ;;
            *)
                warn "Log directory kept: ${LOG_DIR}"
                ;;
        esac
    fi
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo
echo -e " ${GREEN}${BOLD}hckfetch uninstalled.${RESET}"
echo -e " ${YELLOW}Tip:${RESET} reload your shell:  ${CYAN}source ~/.bashrc${RESET}"
echo
