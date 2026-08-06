import sys

from enum import Enum
from typing import Optional


class Platform(Enum):
    MAC = "darwin"
    WINDOWS = "win32"
    LINUX = "linux"


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
