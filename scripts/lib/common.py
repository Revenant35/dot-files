import logging
import shutil
import socket
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Optional


class Platform(Enum):
    MAC = "darwin"
    WINDOWS = "win32"
    LINUX = "linux"


class Environment(Enum):
    WORK = "work"
    HOME = "home"


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    message_format = "=> %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + message_format + reset,
        logging.INFO: grey + message_format + reset,
        logging.WARNING: yellow + message_format + reset,
        logging.ERROR: red + message_format + reset,
        logging.CRITICAL: bold_red + message_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


WORK_HOSTNAMES = ["VU-D4RW65L6QG"]
HOME_HOSTNAMES = ["Zachs-MacBook-Pro", "fedora"]

logger = logging.getLogger("DotfileInstaller")
logger.setLevel(logging.DEBUG)

_info_handler = logging.StreamHandler(sys.stdout)
_info_handler.setLevel(logging.DEBUG)
_info_handler.addFilter(lambda record: record.levelno <= logging.INFO)
_info_handler.setFormatter(CustomFormatter())

_error_handler = logging.StreamHandler(sys.stderr)
_error_handler.setLevel(logging.DEBUG)
_error_handler.addFilter(lambda record: record.levelno > logging.INFO)
_error_handler.setFormatter(CustomFormatter())

logger.addHandler(_info_handler)
logger.addHandler(_error_handler)


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


def decrypt_ssh_key() -> None:
    """Decrypts the ssh key.

    Raises:
        FileNotFoundError: If the encrypted source file does not exist.
        RuntimeError: If 'age' is not installed or the decryption command fails.
    """
    logger.info("Decrypting SSH key...")

    env = get_environment()

    if env is None:
        raise RuntimeError("Unknown environment, cannot determine config directories to stow")

    ssh_dir = get_dotfile_root() / "ssh" / env.value
    age_file = ssh_dir / "id_ed25519.age"
    decrypted_key = Path.home() / ".ssh" / "id_ed25519"

    if not age_file.exists():
        raise FileNotFoundError(f"Encrypted file not found: {age_file}")

    if decrypted_key.exists():
        logger.info("SSH key already decrypted... skipping")
        return

    if shutil.which("age") is None:
        raise RuntimeError("'age' is not installed or not on PATH")

    decrypted_key.parent.mkdir(parents=True, exist_ok=True)
    run_shell_command(f"age -d -o {decrypted_key} {age_file}")
    decrypted_key.chmod(0o600)

    logger.info("SSH key successfully decrypted")


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


def stow_config():
    """Stow all config directories for the current environment.

    Raises:
        RuntimeError: If the environment is unrecognized or stow is not installed.
        FileNotFoundError: If a stow source directory does not exist.
    """
    env = get_environment()

    if env is None:
        raise RuntimeError("Unknown environment, cannot determine config directories to stow")

    if not shutil.which("stow"):
        raise RuntimeError("stow not found")

    logger.info("Stowing directories...")

    _stow_dir(get_dotfile_root() / "config" / "common")
    _stow_dir(get_dotfile_root() / "config" / env.value)
    _stow_dir(get_dotfile_root() / "ssh" / env.value)

    logger.info("Directories stowed.")


def _stow_dir(source):
    """Run stow for a single source directory, targeting $HOME.

    Args:
        source: Path to the directory to stow.

    Raises:
        FileNotFoundError: If the source directory does not exist.
        RuntimeError: If the stow command fails.
    """
    if not source.exists():
        raise FileNotFoundError(f"Stow source directory not found: {source}")

    logger.info(f"Stowing {source}...")
    run_shell_command(f"cd {source} && stow .")

