#!/usr/bin/env python3

import sys

from lib.common import logger, stow_config, decrypt_ssh_key
from lib.metapac import metapac_exists, metapac_install, metapac_link
from lib.rust import cargo_exists, rust_install
from lib.metapac import metapac_sync


def install():
    logger.info("Installing dotfiles")
    if not cargo_exists():
        rust_install()
    else:
        logger.info("cargo already installed... skipping.")

    if not metapac_exists():
        metapac_install()
    else:
        logger.info("metapac already installed... skipping.")

    metapac_link()

    metapac_sync()

    stow_config()

    decrypt_ssh_key()

    logger.info("Installation complete!.")


if __name__ == "__main__":
    try:
        install()
    except Exception as e:
        logger.error(f"Installation failed: {e}")
        sys.exit(1)
