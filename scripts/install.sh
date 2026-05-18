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

BREW_BASE_FILE="${REPO_ROOT}/packages/base.Brewfile"

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
    echo "Usage: $0 <config> [packages|ssh|config|shell]"
    echo ""
    echo "Configurations:"
    echo "  home-macbook   macOS laptop (personal)"
    echo "  work-macbook   macOS laptop (work)"
    echo "  home-desktop   Linux desktop (personal)"
    exit 1
    ;;
esac

# --- Functions ---

install_packages() {
  echo "=== Installing packages ==="
  case "$PACKAGE_MANAGER" in
    brew)
      require brew
      brew bundle --file="$BREW_BASE_FILE"
      brew bundle --file="$PACKAGE_FILE"
      ;;
    dnf)
      require dnf
      sudo dnf install -y $(grep -v '^#' "$PACKAGE_FILE" | grep -v '^$')
      ;;
  esac
}

install_config() {
  echo "=== Stowing config files ==="
  require stow
  (cd "${REPO_ROOT}/config" && stow .)
}

decrypt_ssh() {
  echo "=== Decrypting SSH private key ==="
  local age_file="${SSH_DIR}/id_ed25519.age"
  if [ ! -f "$age_file" ]; then
    echo "Error: SSH key file not found: $age_file"
    exit 1
  fi
  mkdir -p -m 700 ~/.ssh
  require age
  age -d -o ~/.ssh/id_ed25519 "$age_file"
  chmod 600 ~/.ssh/id_ed25519
}

install_ssh() {
  decrypt_ssh
  require stow
  echo "=== Stowing SSH files ==="
  (cd "$SSH_DIR" && stow .)
}

add_shell() {
  echo "=== Adding $1 to shells ==="
  require "$1"
  local shell_path
  shell_path="$(which "$1")"
  if ! grep -qx "$shell_path" /etc/shells; then
    echo "$shell_path" | sudo tee -a /etc/shells
  fi
  chsh -s "$shell_path"
}

# --- Main ---

case "$SUBSYSTEM" in
  packages)
    install_packages
    ;;
  ssh)
    install_ssh
    ;;
  config)
    install_config
    ;;
  shell)
    add_shell fish
    ;;
  "")
    install_packages
    install_config
    install_ssh
    add_shell fish
    ;;
  *)
    echo "Usage: $0 <config> [packages|ssh|config|shell]"
    exit 1
    ;;
esac

echo "=== Done ==="
