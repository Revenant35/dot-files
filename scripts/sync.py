#!/usr/bin/env python3

import sys

from lib.common import logger
from lib.metapac import metapac_sync


def main():
    metapac_sync()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        sys.exit(1)
