#!/usr/bin/env bash
# =============================================================================
# install.sh — hckfetch installation script
# =============================================================================
#
# What this script does:
#   1. Copies 'hckfetch' and 'hckfetch-wrap' to ~/.local/bin/ (or
#      /usr/local/bin/ when run as root).
#   2. Creates the log directory ~/.hckfetch_logs/.
#   3. Appends shell aliases for tracked tools to ~/.bashrc / ~/.zshrc.
#   4. Appends an auto-launch line to the rc file so hckfetch runs on every
#      new terminal (suppressed if HCKFETCH_SILENT=1 is set).
#   5. Sets correct permissions on installed files.
#
# Run as a normal user (recommended):
#   ./install.sh
#
# Run as root (system-wide install):
#   sudo ./install.sh
#
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()    { echo -e " ${CYAN}[*]${RESET} $*"; }
success() { echo -e " ${GREEN}[✓]${RESET} $*"; }
warn()    { echo -e " ${YELLOW}[!]${RESET} $*"; }
error()   { echo -e " ${RED}[✗]${RESET} $*" >&2; }

# ---------------------------------------------------------------------------
# Resolve source directory (where install.sh lives)
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# Determine install prefix
# ---------------------------------------------------------------------------
if [[ "${EUID:-$(id -u)}" -eq 0 ]]; then
    INSTALL_PREFIX="/usr/local/bin"
else
    INSTALL_PREFIX="${HOME}/.local/bin"
    mkdir -p "$INSTALL_PREFIX"
fi

# ---------------------------------------------------------------------------
# Make sure INSTALL_PREFIX is on PATH; warn if not
# ---------------------------------------------------------------------------
if ! echo ":${PATH}:" | grep -q ":${INSTALL_PREFIX}:"; then
    warn "${INSTALL_PREFIX} is not in your PATH."
    warn "Add the following line to your shell rc file:"
    warn "  export PATH=\"\$PATH:${INSTALL_PREFIX}\""
fi

# ---------------------------------------------------------------------------
# List of tools hckfetch will track
# ---------------------------------------------------------------------------
TRACKED_TOOLS=(
    nmap
    metasploit
    burpsuite
    sqlmap
    hydra
    john
    aircrack-ng
    gobuster
    nikto
    wireshark
    hashcat
    wfuzz
    ffuf
    crackmapexec
    enum4linux
)

# ---------------------------------------------------------------------------
# Step 1: Copy hckfetch and hckfetch-wrap to INSTALL_PREFIX
# ---------------------------------------------------------------------------
info "Installing hckfetch and hckfetch-wrap to ${INSTALL_PREFIX}/ ..."

for script in hckfetch hckfetch-wrap; do
    src="${SCRIPT_DIR}/${script}"
    if [[ ! -f "$src" ]]; then
        error "Source file not found: ${src}"
        exit 1
    fi
    cp "$src" "${INSTALL_PREFIX}/${script}"
    chmod +x "${INSTALL_PREFIX}/${script}"
done

success "Installed hckfetch and hckfetch-wrap."

# ---------------------------------------------------------------------------
# Step 2: Create log directory
# ---------------------------------------------------------------------------
LOG_DIR="${HOME}/.hckfetch_logs"
info "Creating log directory ${LOG_DIR}/ ..."
mkdir -p "$LOG_DIR"
chmod 700 "$LOG_DIR"
success "Log directory ready."

# ---------------------------------------------------------------------------
# Detect shell rc files to patch
# ---------------------------------------------------------------------------
RC_FILES=()
[[ -f "${HOME}/.bashrc"  ]] && RC_FILES+=("${HOME}/.bashrc")
[[ -f "${HOME}/.zshrc"   ]] && RC_FILES+=("${HOME}/.zshrc")

# If neither exists yet, fall back to bashrc
if [[ ${#RC_FILES[@]} -eq 0 ]]; then
    warn "No ~/.bashrc or ~/.zshrc found. Creating ~/.bashrc."
    touch "${HOME}/.bashrc"
    RC_FILES+=("${HOME}/.bashrc")
fi

# ---------------------------------------------------------------------------
# Build the block of text we will append to each rc file
# ---------------------------------------------------------------------------
build_rc_block() {
    local tool_list_str
    # Build alias lines
    local alias_lines=""
    for tool in "${TRACKED_TOOLS[@]}"; do
        alias_lines+="alias ${tool}='hckfetch-wrap ${tool}'\n"
    done

    cat << RCBLOCK
# ---- hckfetch: begin --------------------------------------------------------
# Auto-added by hckfetch install.sh — do not edit this block manually.
# To uninstall, run: uninstall.sh  (or remove this block and the files below)

# Tool tracking aliases
$(printf '%b' "$alias_lines")
# Auto-display hckfetch on new terminal (suppress with: export HCKFETCH_SILENT=1)
if [[ "\${HCKFETCH_SILENT:-0}" != "1" ]] && command -v hckfetch &>/dev/null; then
    hckfetch --no-logo
fi
# ---- hckfetch: end ----------------------------------------------------------
RCBLOCK
}

RC_BLOCK="$(build_rc_block)"

# ---------------------------------------------------------------------------
# Step 3 & 4: Append aliases + auto-launch to each rc file
# ---------------------------------------------------------------------------
MARKER_BEGIN="# ---- hckfetch: begin"
MARKER_END="# ---- hckfetch: end"

for rc in "${RC_FILES[@]}"; do
    # Idempotent: skip if block already present
    if grep -qF "$MARKER_BEGIN" "$rc" 2>/dev/null; then
        warn "${rc}: hckfetch block already present — skipping."
        continue
    fi
    info "Patching ${rc} ..."
    {
        echo ""
        echo "$RC_BLOCK"
    } >> "$rc"
    success "Patched ${rc}."
done

# ---------------------------------------------------------------------------
# Step 5: Summary
# ---------------------------------------------------------------------------
echo
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║   hckfetch installed successfully!  🎉       ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════╝${RESET}"
echo
echo -e " ${BOLD}Next steps:${RESET}"
echo -e "   1. Reload your shell:  ${CYAN}source ~/.bashrc${RESET}"
echo -e "   2. Run the dashboard:  ${CYAN}hckfetch${RESET}"
echo -e "   3. See help:           ${CYAN}hckfetch --help${RESET}"
echo -e "   4. Reset logs:         ${CYAN}hckfetch --reset${RESET}"
echo
echo -e " ${BOLD}Tracked tools:${RESET} ${TRACKED_TOOLS[*]}"
echo -e " ${BOLD}Log directory:${RESET} ${LOG_DIR}"
echo -e " ${BOLD}Installed to: ${RESET} ${INSTALL_PREFIX}"
echo
echo -e " ${YELLOW}Tip:${RESET} set ${BOLD}HCKFETCH_SILENT=1${RESET} to suppress auto-display on terminal open."
echo -e " ${YELLOW}Tip:${RESET} to uninstall, run ${BOLD}./uninstall.sh${RESET}"
echo
