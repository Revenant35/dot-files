"""Shell utilities for dotfiles setup.

Provides helpers for running shell commands and checking for required tools
on the system PATH.
"""

import subprocess
import shutil


def run_shell_command(command: str) -> None:
    """Run a shell command, raising RuntimeError on failure.

    Args:
        command: The shell command string to execute.

    Raises:
        RuntimeError: If the command exits with a non-zero status or an OS error occurs.
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exception:
        raise RuntimeError(f"{command} failed: {exception}") from exception


def command_exists(command: str) -> bool:
    """Return True if the given command is available on PATH.

    Args:
        command: The name of the command to look up.
    """
    return shutil.which(command) is not None


def assert_command_exists(command: str) -> None:
    """Raise RuntimeError if the given command is not available on PATH.

    Args:
        command: The name of the command to check.

    Raises:
        RuntimeError: If ``command`` is not found on PATH.
    """
    if not command_exists(command):
        raise RuntimeError(f"{command} is not installed or not on PATH")
