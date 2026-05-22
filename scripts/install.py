#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path
from logger import logger
from shell import run_shell_command

def cargo_exists():
    return shutil.which("cargo") is not None

def metapac_exists():
    return shutil.which("metapac") is not None

def install_rust():
    logger.info("Installing Rust toolchain...")

    # Download and run rustup installer noninteractively
    run_shell_command("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")

    cargo_home = Path.home() / ".cargo"
    cargo_bin = str(cargo_home / "bin")

    # Make cargo available in current process
    os.environ["PATH"] = cargo_bin + os.pathsep + os.environ["PATH"]

    # Verify installation
    if not cargo_exists():
        logger.error("cargo was not found after rustup install")
        sys.exit(1)

def install_metapac():
    logger.info("Installing metapac...")
    run_shell_command("cargo install metapac")

def main():
    if not cargo_exists():
        install_rust()
    else:
        logger.info("cargo already installed")

    if not metapac_exists():
        install_metapac()
    else:
        logger.info("metapac already installed")

    logger.info("Done.")


if __name__ == "__main__":
    main()