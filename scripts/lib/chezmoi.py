import shutil
import sys

from .logger import logger
from .shell import run_shell_command


def chezmoi_initialize():
    try:
        run_shell_command("chezmoi init --apply git@github.com:Revenant35/dotfiles.git")
    except (OSError, Exception) as e:
        logger.error(f"Failed to initialize chezmoi: {e}")
        sys.exit(1)


def chezmoi_exists():
    return shutil.which("chezmoi") is not None
