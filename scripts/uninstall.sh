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

# --- Functions ---

uninstall_packages() {
  echo "=== Uninstalling packages ==="
  case "$(uname -s)" in
    Darwin)
      require brew
      brew bundle cleanup --force --file="${REPO_ROOT}/packages/home.Brewfile"
      ;;
    Linux)
      require dnf
      sudo dnf remove -y $(grep -v '^#' "${REPO_ROOT}/packages/home.dnf.txt" | grep -v '^$')
      ;;
    *)
      echo "Error: Unsupported OS '$(uname -s)'."; exit 1
      ;;
  esac
}

uninstall_config() {
  echo "=== Unstowing config files ==="
  require stow
  (cd "${REPO_ROOT}/config" && stow -D .)
}

uninstall_ssh() {
  echo "=== Unstowing SSH files ==="
  require stow
  (cd "${REPO_ROOT}/ssh" && stow -D .)
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

case "${1:-}" in
  packages)
    uninstall_packages
    ;;
  ssh)
    uninstall_ssh
    ;;
  config)
    uninstall_config
    ;;
  shell)
    remove_shell fish
    ;;
  "")
    remove_shell fish
    uninstall_ssh
    uninstall_config
    uninstall_packages
    ;;
  *)
    echo "Usage: $0 [packages|ssh|config|shell]"
    exit 1
    ;;
esac

echo "=== Done ==="
