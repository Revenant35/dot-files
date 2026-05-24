import os
import shutil
from pathlib import Path

from .common import Platform, get_platform, get_dotfile_root, logger, run_shell_command
from .rust import cargo_exists


def metapac_link():
    """Create a symlink from the platform config directory to the repo's metapac/ dir.

    Raises:
        FileNotFoundError: If the metapac source directory does not exist.
        RuntimeError: If the target path exists and is not a symlink.
    """
    source = get_dotfile_root() / "metapac"
    target = _metapac_dir_target()

    if not source.exists():
        raise FileNotFoundError(f"metapac source directory not found: {source}")

    if target.exists() and not target.is_symlink():
        raise RuntimeError(f"metapac target already exists and is not a symlink: {target}")

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
    """Install metapac via cargo.

    Raises:
        RuntimeError: If cargo is not found or the installation fails.
    """
    if not cargo_exists():
        raise RuntimeError("cargo not found")

    if metapac_exists():
        logger.debug("metapac already installed")
        return

    logger.info("Installing metapac...")
    run_shell_command("cargo install metapac")
    logger.info("metapac installed.")
    return


def metapac_sync():
    """Sync packages using metapac.

    Raises:
        RuntimeError: If metapac is not found or the sync fails.
    """
    if not metapac_exists():
        raise RuntimeError("metapac not found")

    logger.info("Syncing packages...")
    run_shell_command("metapac sync --no-confirm")
    run_shell_command("metapac clean --no-confirm")
    _metapac_cleanup()
    logger.info("Packages synced.")
    return


def metapac_update():
    """Update all packages using metapac.

    Raises:
        RuntimeError: If metapac is not found or the update fails.
    """
    if not metapac_exists():
        raise RuntimeError("metapac not found")

    logger.info("Updating packages...")
    run_shell_command("metapac update-all --no-confirm")
    _metapac_cleanup()
    logger.info("Packages updated.")
    return True


def _metapac_cleanup():
    logger.info("Cleaning up packages...")

    run_shell_command("metapac unmanaged")

    logger.info("Packages cleaned up.")


def _metapac_dir_target() -> Path:
    """Platform-specific directory where metapac expects its config."""
    platform = get_platform()
    if platform == Platform.MAC:
        return Path.home() / "Library" / "Application Support" / "metapac"
    elif platform == Platform.WINDOWS:
        roaming = os.environ.get("APPDATA", "")
        return Path(roaming) / "metapac"
    else:  # Linux / other POSIX
        xdg = os.environ.get("XDG_CONFIG_HOME", "")
        base = Path(xdg) if xdg else Path.home() / ".config"
        return base / "metapac"
