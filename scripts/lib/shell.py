import shlex
import subprocess

from .logger import logger


def run_shell_command(command):
    command_args = shlex.split(command)

    logger.info(f"Running: {command}")

    try:
        subprocess.run(command_args, check=True)
    except (OSError, subprocess.CalledProcessError) as exception:
        logger.error(exception)
        logger.error(f"${command} failed")
        raise exception
