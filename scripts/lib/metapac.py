import shutil

from .logger import logger
from .rust import cargo_exists
from .shell import run_shell_command


def metapac_exists():
    return shutil.which("metapac") is not None

def metapac_install():
    if not cargo_exists():
        logger.error("cargo not found")
        return False

    if metapac_exists():
        logger.debug("metapac already installed")
        return True

    logger.info("Installing metapac...")

    try:
        run_shell_command("cargo install metapac")
    except (OSError, Exception) as e:
        logger.error(f"Failed to install metapac: {e}")
        return False

    logger.info("metapac installed.")
    return True

def metapac_sync():
    if not metapac_exists():
        logger.error("metapac not found")
        return False

    logger.info("Syncing packages...")

    try:
        run_shell_command("metapac sync --no-confirm")
        run_shell_command("metapac clean --no-confirm")
        _metapac_cleanup()
    except (OSError, Exception) as e:
        logger.error(f"Failed to sync packages: {e}")
        return False

    logger.info("Packages synced.")
    return True

def metapac_update():
    if not metapac_exists():
        logger.error("metapac not found")
        return False

    logger.info("Updating packages...")

    try:
        run_shell_command("metapac update-all --no-confirm")
        _metapac_cleanup()
    except (OSError, Exception) as e:
        logger.error(f"Failed to update packages: {e}")
        return False

    logger.info("Packages updated.")
    return True

def _metapac_cleanup():
    logger.info("Cleaning up packages...")

    run_shell_command("metapac unmanaged")

    logger.info("Packages cleaned up.")