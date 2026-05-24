import subprocess
import sys

from .logger import logger


def run_shell_command(command):
    logger.info(f"Running: {command}")

    try:
        subprocess.run(command, shell=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exception:
        logger.error(exception)
        logger.error(f"${command} failed")
        sys.exit(1)
