import shutil
import sys

from .common import get_dotfile_root, get_environment
from .logger import logger
from .shell import run_shell_command


def stow():
    env = get_environment()

    if env is None:
        logger.error("Unknown environment, cannot determine config directories to stow")
        sys.exit(1)

    if not shutil.which("stow"):
        logger.error("stow not found")
        sys.exit(1)

    logger.info("Stowing directories...")

    try:
        _stow_dir(get_dotfile_root() / "config" / "common")
        _stow_dir(get_dotfile_root() / "config" / env.value)
        _stow_dir(get_dotfile_root() / "ssh" / env.value)
    except (OSError, Exception) as e:
        logger.error(f"Failed to stow directories: {e}")
        sys.exit(1)

    logger.info("Directories stowed.")


def _stow_dir(source):
    """Run stow for a single source directory, targeting $HOME."""
    if not source.exists():
        logger.error(f"Stow source directory not found: {source}")
        sys.exit(1)

    logger.info(f"Stowing {source}...")
    run_shell_command(f"cd {source} && stow .")

