"""Stow utilities for dotfiles setup.

Provides helpers for symlinking dotfile config directories into the home
directory using GNU stow.
"""

from pathlib import Path
from _logging import logger
from _shell import run_shell_command, assert_command_exists
from _common import get_dotfile_root


def _stow(src: Path, dest: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Stow source directory not found: {src}")

    if not src.is_dir():
        raise NotADirectoryError(f"Stow source is not a directory: {src}")

    if dest.exists() and not dest.is_dir():
        raise NotADirectoryError(f"Stow destination is not a directory: {dest}")

    if not dest.exists():
        dest.mkdir(parents=True, exist_ok=True)

    logger.info(f"Stowing {src} -> {dest}")
    run_shell_command(f"stow --dir={src} --target={dest} .")


def stow_directories() -> None:
    """Stow all config directories into the home directory.

    Raises:
        RuntimeError: If ``stow`` is not installed or a stow command fails.
        FileNotFoundError: If a stow source directory does not exist.
    """
    assert_command_exists("stow")

    root = get_dotfile_root()
    home = Path.home()

    logger.info("Stowing config directories")

    _stow(root / "config", home / ".config")
    _stow(root / "ssh", home / ".ssh")

    logger.info("Directories stowed")
