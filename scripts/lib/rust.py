import os
import shutil
import sys
from pathlib import Path

from .logger import logger
from .shell import run_shell_command


def cargo_exists():
    return shutil.which("cargo") is not None


def rust_install():
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
