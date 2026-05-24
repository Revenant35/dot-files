import os
import shutil
import sys
from pathlib import Path
from sys import platform

from .logger import logger
from .rust import cargo_exists
from .shell import run_shell_command


def metapac_link():
    """Create a symlink from the platform config directory to the repo's metapac/ dir."""
    source = _metapac_dir_source()
    target = _metapac_dir_target()

    if not source.exists():
        logger.error(f"metapac source directory not found: {source}")
        sys.exit(1)

    if target.exists() and not target.is_symlink():
        logger.error(f"metapac target already exists and is not a symlink: {target}")
        sys.exit(1)

    if target.is_symlink() and target.resolve() == source.resolve():
        logger.info("metapac directory already linked... skipping.")
        return

    if target.resolve() == source.resolve():
        logger.info(f"Removing stale symlink at {target}")
        target.unlink()

    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(source)
    logger.info(f"Linked {source} -> {target}")
    return


def metapac_exists():
    return shutil.which("metapac") is not None


def metapac_install():
    if not cargo_exists():
        logger.error("cargo not found")
        sys.exit(1)

    if metapac_exists():
        logger.debug("metapac already installed")
        return

    logger.info("Installing metapac...")

    try:
        run_shell_command("cargo install metapac")
    except (OSError, Exception) as e:
        logger.error(f"Failed to install metapac: {e}")
        sys.exit(1)

    logger.info("metapac installed.")
    return


def metapac_sync():
    if not metapac_exists():
        logger.error("metapac not found")
        sys.exit(1)

    logger.info("Syncing packages...")

    try:
        run_shell_command("metapac sync --no-confirm")
        run_shell_command("metapac clean --no-confirm")
        _metapac_cleanup()
    except (OSError, Exception) as e:
        logger.error(f"Failed to sync packages: {e}")
        sys.exit(1)

    logger.info("Packages synced.")
    return


def metapac_update():
    if not metapac_exists():
        logger.error("metapac not found")
        sys.exit(1)

    logger.info("Updating packages...")

    try:
        run_shell_command("metapac update-all --no-confirm")
        _metapac_cleanup()
    except (OSError, Exception) as e:
        logger.error(f"Failed to update packages: {e}")
        sys.exit(1)

    logger.info("Packages updated.")
    return True


def _metapac_cleanup():
    logger.info("Cleaning up packages...")

    run_shell_command("metapac unmanaged")

    logger.info("Packages cleaned up.")


def _metapac_dir_source() -> Path:
    """Absolute path to the metapac/ directory tracked in this repo."""
    return Path(__file__).resolve().parents[2] / "metapac"


def _metapac_dir_target() -> Path:
    """Platform-specific directory where metapac expects its config."""
    if platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "metapac"
    elif platform == "win32":
        roaming = os.environ.get("APPDATA", "")
        return Path(roaming) / "metapac"
    else:  # Linux / other POSIX
        xdg = os.environ.get("XDG_CONFIG_HOME", "")
        base = Path(xdg) if xdg else Path.home() / ".config"
        return base / "metapac"
