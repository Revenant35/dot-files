#!/usr/bin/env python3

import sys

from lib.logger import logger
from lib.metapac import metapac_exists, metapac_install, metapac_link
from lib.rust import cargo_exists, rust_install
from lib.metapac import metapac_sync
from lib.stow import stow


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

    stow()

    logger.info("Installation complete!.")


if __name__ == "__main__":
    try:
        install()
    except Exception as e:
        logger.error(f"Installation failed: {e}")
        sys.exit(1)
