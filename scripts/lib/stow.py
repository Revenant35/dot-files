import shutil

from .common import get_dotfile_root, get_environment
from .logger import logger
from .shell import run_shell_command


def stow():
    """Stow all config directories for the current environment.

    Raises:
        RuntimeError: If the environment is unrecognized or stow is not installed.
        FileNotFoundError: If a stow source directory does not exist.
    """
    env = get_environment()

    if env is None:
        raise RuntimeError("Unknown environment, cannot determine config directories to stow")

    if not shutil.which("stow"):
        raise RuntimeError("stow not found")

    logger.info("Stowing directories...")

    _stow_dir(get_dotfile_root() / "config" / "common")
    _stow_dir(get_dotfile_root() / "config" / env.value)
    _stow_dir(get_dotfile_root() / "ssh" / env.value)

    logger.info("Directories stowed.")


def _stow_dir(source):
    """Run stow for a single source directory, targeting $HOME.

    Args:
        source: Path to the directory to stow.

    Raises:
        FileNotFoundError: If the source directory does not exist.
        RuntimeError: If the stow command fails.
    """
    if not source.exists():
        raise FileNotFoundError(f"Stow source directory not found: {source}")

    logger.info(f"Stowing {source}...")
    run_shell_command(f"cd {source} && stow .")
