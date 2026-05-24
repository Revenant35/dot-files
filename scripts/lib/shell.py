import subprocess

from .logger import logger


def run_shell_command(command):
    """Run a shell command, raising RuntimeError on failure.

    Args:
        command: The shell command string to execute.

    Raises:
        RuntimeError: If the command exits with a non-zero status or an OS error occurs.
    """
    logger.info(f"Running: {command}")

    try:
        subprocess.run(command, shell=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exception:
        raise RuntimeError(f"{command} failed: {exception}") from exception
