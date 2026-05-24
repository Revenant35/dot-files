#!/usr/bin/env python3

import sys

from lib.logger import logger
from lib.metapac import metapac_update


def main():
    metapac_update()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Update failed: {e}")
        sys.exit(1)
