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

install_packages() {
  echo "=== Installing packages ==="
  case "$(uname -s)" in
    Darwin)
      require brew
      brew bundle --file="${REPO_ROOT}/packages/home.Brewfile"
      ;;
    Linux)
      require dnf
      sudo dnf install -y $(grep -v '^#' "${REPO_ROOT}/packages/home.dnf.txt" | grep -v '^$')
      ;;
    *)
      echo "Error: Unsupported OS '$(uname -s)'."; exit 1
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
  mkdir -p -m 700 ~/.ssh
  require age
  age -d -o ~/.ssh/id_ed25519 "${REPO_ROOT}/ssh/id_ed25519.age"
  chmod 600 ~/.ssh/id_ed25519
}

install_ssh() {
  decrypt_ssh
  require stow
  echo "=== Stowing SSH files ==="
  (cd "${REPO_ROOT}/ssh" && stow .)
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

case "${1:-}" in
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
    echo "Usage: $0 [--only-packages|--only-ssh|--only-config|--only-shell]"
    exit 1
    ;;
esac

echo "=== Done ==="
