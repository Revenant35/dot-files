#!/usr/bin/env python3

import sys

from lib.common import logger, stow_config, decrypt_ssh_key


def install():
    logger.info("Installing dotfiles")
    stow_config()
    decrypt_ssh_key()
    logger.info("Installation complete!.")


if __name__ == "__main__":
    try:
        install()
    except Exception as e:
        logger.error(f"Installation failed: {e}")
        sys.exit(1)
