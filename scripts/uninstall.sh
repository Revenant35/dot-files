#!/bin/bash
set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Repository root is one level up from scripts/
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# --- Dependency checks ---

require() {
  command -v "$1" >/dev/null 2>&1 || { echo "Error: '$1' is not installed."; exit 1; }
}

# --- Configuration ---

CONFIG="${1:-}"
SUBSYSTEM="${2:-}"

case "$CONFIG" in
  home-macbook)
    PACKAGE_FILE="${REPO_ROOT}/packages/home-macbook.Brewfile"
    PACKAGE_MANAGER="brew"
    SSH_DIR="${REPO_ROOT}/ssh/home"
    ;;
  work-macbook)
    PACKAGE_FILE="${REPO_ROOT}/packages/work-macbook.Brewfile"
    PACKAGE_MANAGER="brew"
    SSH_DIR="${REPO_ROOT}/ssh/work"
    ;;
  home-desktop)
    PACKAGE_FILE="${REPO_ROOT}/packages/home-desktop.dnf.txt"
    PACKAGE_MANAGER="dnf"
    SSH_DIR="${REPO_ROOT}/ssh/home"
    ;;
  *)
    echo "Usage: $0 <config> [packages|ssh|config|git|shell]"
    echo ""
    echo "Configurations:"
    echo "  home-macbook   macOS laptop (personal)"
    echo "  work-macbook   macOS laptop (work)"
    echo "  home-desktop   Linux desktop (personal)"
    exit 1
    ;;
esac

# --- Functions ---

uninstall_packages() {
  echo "=== Uninstalling packages ==="
  case "$PACKAGE_MANAGER" in
    brew)
      require brew
      brew bundle cleanup --force --file="$PACKAGE_FILE"
      ;;
    dnf)
      require dnf
      sudo dnf remove -y $(grep -v '^#' "$PACKAGE_FILE" | grep -v '^$')
      ;;
  esac
}

uninstall_config() {
  echo "=== Unstowing config files ==="
  require stow
  (cd "${REPO_ROOT}/config" && stow -D .)
}

uninstall_git() {
  echo "=== Removing ~/.config/git/config.local ==="
  rm -f ~/.config/git/config.local
}

uninstall_ssh() {
  echo "=== Unstowing SSH files ==="
  require stow
  (cd "$SSH_DIR" && stow -D .)
  if [ -f ~/.ssh/id_ed25519 ]; then
    echo "=== Removing decrypted SSH private key ==="
    rm ~/.ssh/id_ed25519
  fi
}

remove_shell() {
  echo "=== Removing $1 from shells ==="
  local shell_path
  shell_path="$(which "$1" 2>/dev/null || true)"
  if [ -n "$shell_path" ] && grep -qx "$shell_path" /etc/shells; then
    sudo sed -i'' -e "\\|^${shell_path}$|d" /etc/shells
  fi
  chsh -s /bin/zsh
}

# --- Main ---

case "$SUBSYSTEM" in
  packages)
    uninstall_packages
    ;;
  ssh)
    uninstall_ssh
    ;;
  config)
    uninstall_config
    ;;
  git)
    uninstall_git
    ;;
  shell)
    remove_shell fish
    ;;
  "")
    remove_shell fish
    uninstall_ssh
    uninstall_git
    uninstall_config
    uninstall_packages
    ;;
  *)
    echo "Usage: $0 <config> [packages|ssh|config|git|shell]"
    exit 1
    ;;
esac

echo "=== Done ==="
