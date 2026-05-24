import shutil
import socket
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

from .logger import logger
from .shell import run_shell_command

class Platform(Enum):
    MAC = "darwin"
    WINDOWS = "win32"
    LINUX = "linux"


class Environment(Enum):
    WORK = "work"
    HOME = "home"


WORK_HOSTNAMES = ["VU-D4RW65L6QG"]
HOME_HOSTNAMES = ["Zachs-MacBook-Pro"]


def get_hostname() -> str:
    """Returns the current machine's hostname."""
    return socket.gethostname()


def is_work() -> bool:
    """Returns True if the current machine is a work machine."""
    return get_hostname() in WORK_HOSTNAMES


def is_home() -> bool:
    """Returns True if the current machine is a home machine."""
    return get_hostname() in HOME_HOSTNAMES


def get_environment() -> Optional[Environment]:
    """Returns the current Environment, or None if unrecognized."""
    if is_work():
        return Environment.WORK
    if is_home():
        return Environment.HOME
    return None


def get_platform() -> Optional[Platform]:
    """Returns the current Platform, or None if unrecognized."""
    for platform in Platform:
        if sys.platform == platform.value:
            return platform
    return None


def is_mac() -> bool:
    """Returns True if the current platform is macOS."""
    return get_platform() == Platform.MAC


def is_windows() -> bool:
    """Returns True if the current platform is Windows."""
    return get_platform() == Platform.WINDOWS


def is_linux() -> bool:
    """Returns True if the current platform is Linux."""
    return get_platform() == Platform.LINUX


def get_dotfile_root() -> Path:
    """Returns the path to the root of the dotfile repository."""
    return Path(__file__).resolve().parents[2]


def decrypt_age_file(age_file: Path, output_path: Path, mode: int = 0o600) -> None:
    """Decrypts an age-encrypted file to a specific filepath.

    Args:
        age_file: Path to the .age encrypted source file.
        output_path: Destination path for the decrypted output.
        mode: File permission mode to apply to the output (default: 0o600).
    """

    if not age_file.exists():
        logger.error(f"Error: Encrypted file not found: {age_file}")
        sys.exit(1)

    if shutil.which("age") is None:
        logger.error("Error: 'age' is not installed or not on PATH")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    run_shell_command(f"age -d -o {output_path} {age_file}")
    output_path.chmod(mode)