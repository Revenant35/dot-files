"""Stow utilities for dotfiles setup.

Provides helpers for symlinking dotfile config directories into the home
directory using GNU stow.
"""

from pathlib import Path
from _logging import logger
from _shell import run_shell_command, assert_command_exists
from _common import get_dotfile_root


def stow() -> None:
    """Stow all config directories into the home directory.

    Raises:
        RuntimeError: If ``stow`` is not installed or a stow command fails.
        FileNotFoundError: If a stow source directory does not exist.
    """
    assert_command_exists("stow")

    root = get_dotfile_root()
    home = Path.home()
    directories = [
        root / "config",
        root / "ssh",
    ]

    logger.info("Stowing config directories")

    for directory in directories:
        if not directory.exists():
            raise FileNotFoundError(f"Stow source directory not found: {directory}")

        logger.info(f"Stowing {directory} -> {home}")
        run_shell_command(f"stow --dir={directory} --target={home} .")

    logger.info("Config directories stowed")
