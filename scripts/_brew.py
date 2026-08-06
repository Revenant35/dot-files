"""Homebrew helper functions for dotfiles setup.

Provides helpers for installing Homebrew and managing packages via brew bundle,
using the Brewfile in the dotfiles repository directly.
"""

import os

from pathlib import Path
from _logging import logger
from _shell import run_shell_command, assert_command_exists, command_exists
from _common import get_dotfile_root


_BREWFILE = get_dotfile_root() / "Brewfile"
_GLOBAL_BREWFILE = Path.home() / ".Brewfile"
_HOMEBREW_INSTALL_URL = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
_HOMEBREW_BIN = "/opt/homebrew/bin"


def _brew_global_link_exists() -> bool:
    """Check whether ~/.Brewfile exists and is a symlink pointing to the local Brewfile."""
    return (
        _GLOBAL_BREWFILE.is_symlink()
        and _GLOBAL_BREWFILE.resolve() == _BREWFILE.resolve()
    )


def _link_brew_global() -> None:
    """Symlink ~/.Brewfile to the dotfiles Brewfile.

    Removes any existing file or symlink at ~/.Brewfile before creating the
    new symlink, so that `brew bundle` (without --file) picks up the dotfiles
    Brewfile automatically.
    """
    if _GLOBAL_BREWFILE.is_symlink():
        _GLOBAL_BREWFILE.unlink()
        logger.info(f"Removed existing symlink {_GLOBAL_BREWFILE}")
    elif _GLOBAL_BREWFILE.exists():
        backup = _GLOBAL_BREWFILE.with_suffix(".bak")
        _GLOBAL_BREWFILE.rename(backup)
        logger.info(f"Backed up existing {_GLOBAL_BREWFILE} to {backup}")

    _GLOBAL_BREWFILE.symlink_to(_BREWFILE)
    logger.info(f"Linked {_GLOBAL_BREWFILE} -> {_BREWFILE}")


def _install_homebrew() -> None:
    """Download and run the official Homebrew install script.

    After installation, adds the Homebrew bin directory to PATH for the
    current process (relevant on Apple Silicon where brew lives in
    /opt/homebrew).
    """
    run_shell_command(f'/bin/bash -c "$(curl -fsSL {_HOMEBREW_INSTALL_URL})"')

    if Path(_HOMEBREW_BIN).is_dir():
        os.environ["PATH"] = _HOMEBREW_BIN + ":" + os.environ.get("PATH", "")
        logger.info(f"Added {_HOMEBREW_BIN} to PATH")

    assert_command_exists("brew")


def _brew_update() -> None:
    """Run brew update."""
    logger.info("Updating Homebrew")
    run_shell_command("brew update")


def _brew_bundle() -> None:
    """Install packages from the dotfiles Brewfile."""
    logger.info(f"Installing packages from {_BREWFILE}")
    run_shell_command(f"brew bundle --file={_BREWFILE}")


def _brew_cleanup() -> None:
    """Remove packages not listed in the dotfiles Brewfile."""
    logger.info("Removing packages not in Brewfile")
    run_shell_command(f"brew bundle --file={_BREWFILE} cleanup --force")


def _brew_upgrade() -> None:
    """Upgrade all outdated packages."""
    logger.info("Upgrading outdated packages")
    run_shell_command("brew upgrade")


def brew_sync() -> None:
    """Ensure installed packages match the Brewfile."""
    if not command_exists("brew"):
        logger.info("Homebrew not found, installing")
        _install_homebrew()

    if not _BREWFILE.exists():
        raise RuntimeError(f"Brewfile not found: {_BREWFILE}")

    if not _brew_global_link_exists():
        logger.info(f"Linking {_GLOBAL_BREWFILE} -> {_BREWFILE}")
        _link_brew_global()

    _brew_update()
    _brew_bundle()
    _brew_cleanup()
    _brew_upgrade()
