#!/usr/bin/env python3

from lib.logger import logger
from lib.metapac import metapac_exists, metapac_install, metapac_link
from lib.rust import cargo_exists, rust_install
from lib.chezmoi import chezmoi_initialize
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

    chezmoi_initialize()

    logger.info("Installation complete!.")


if __name__ == "__main__":
    install()
