#!/usr/bin/env bash
# Bootstrap script for Zach Brown's dotfiles.
#
# Usage (one-liner):
#   curl -fsSL https://raw.githubusercontent.com/Revenant35/dot-files/main/install.sh | bash
#
# Or clone manually and run:
#   bash install.sh

set -euo pipefail

DOTFILES_REPO="https://github.com/Revenant35/dot-files.git"
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/.dotfiles}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

log()  { printf '=> %s\n' "$*"; }
die()  { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------------------
# Preflight checks
# ---------------------------------------------------------------------------

# macOS only — sync.py has platform detection but the Homebrew bootstrap is
# Apple Silicon-specific and the overall setup targets macOS.
if [[ "$(uname -s)" != "Darwin" ]]; then
  die "This bootstrap script only supports macOS."
fi

# git is required to clone. On a fresh Mac, running git triggers the Xcode
# Command Line Tools install prompt automatically.
if ! command -v git &>/dev/null; then
  die "git not found. Install Xcode Command Line Tools first: xcode-select --install"
fi

# python3 is required to run sync.py. It ships with macOS (or via CLT) and
# uses only stdlib — no extra install step needed.
if ! command -v python3 &>/dev/null; then
  die "python3 not found. It should be available after installing Xcode Command Line Tools."
fi

# ---------------------------------------------------------------------------
# Clone or update the repo
# ---------------------------------------------------------------------------

if [[ -d "$DOTFILES_DIR/.git" ]]; then
  log "Dotfiles already cloned at $DOTFILES_DIR — pulling latest"
  git -C "$DOTFILES_DIR" pull --ff-only
  git -C "$DOTFILES_DIR" submodule update --init --recursive
else
  log "Cloning dotfiles into $DOTFILES_DIR"
  git clone --recurse-submodules "$DOTFILES_REPO" "$DOTFILES_DIR"
fi

# ---------------------------------------------------------------------------
# Hand off to the Python sync entrypoint
# ---------------------------------------------------------------------------

log "Running sync"
python3 "$DOTFILES_DIR/scripts/sync.py"

log "Done. Open a new shell to pick up all changes."
