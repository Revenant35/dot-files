"""Cryptography utilities for dotfiles setup.

Provides helper functions for decrypting files using the `age` encryption tool.
"""

from pathlib import Path
from _logging import logger
from _shell import run_shell_command, assert_command_exists


def age_decrypt(src: Path, dest: Path) -> None:
    """Decrypt an age-encrypted file to a destination path.

    Prompts for a passphrase interactively. On failure, offers a retry loop
    until the user declines or decryption succeeds. The destination file is
    written with permissions 0o600 (owner read/write only).

    Args:
        src: Path to the age-encrypted source file.
        dest: Path where the decrypted output will be written.

    Raises:
        FileNotFoundError: If ``src`` does not exist.
        RuntimeError: If decryption fails and the user chooses not to retry.
        AssertionError: If the ``age`` command is not available on PATH.
    """
    logger.info(f"Decrypting {src} -> {dest}")

    if not src.exists():
        raise FileNotFoundError(f"Encrypted file not found: {src}")

    assert_command_exists("age")

    dest.parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            run_shell_command(f"age -d -o {dest} {src}")
            break
        except RuntimeError:
            logger.warning(f"Invalid passphrase for {src}")
            retry = input("Would you like to try again? [y/N] ").strip().lower()
            if retry != "y":
                raise

    dest.chmod(0o600)

    logger.info(f"Decrypted {src} -> {dest}")
