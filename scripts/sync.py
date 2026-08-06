#!/usr/bin/env python3

import argparse

from _logging import logger
from _brew import brew_sync
from _stow import stow
from _ssh import decrypt_ssh_key


def sync():
    logger.info("Installing dotfiles")
    brew_sync()
    stow()
    decrypt_ssh_key()
    logger.info("Installation complete!.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync dotfiles")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("brew", help="Run brew sync")
    subparsers.add_parser("stow", help="Run stow")
    subparsers.add_parser("ssh", help="Decrypt SSH key")

    args = parser.parse_args()

    if args.command == "brew":
        brew_sync()
    elif args.command == "stow":
        stow()
    elif args.command == "ssh":
        decrypt_ssh_key()
    else:
        sync()
