"""SSH key management utilities for dotfiles setup.

Provides helpers for decrypting and installing SSH keys from age-encrypted
files stored in the dotfiles repository.
"""

from pathlib import Path
from _logging import logger
from _crypto import age_decrypt
from _common import get_dotfile_root


def decrypt_ssh_key() -> None:
    """Decrypt the age-encrypted SSH private key into ~/.ssh/id_ed25519.

    Reads the encrypted key from ``<dotfile_root>/id_ed25519.age`` and writes
    the decrypted result to ``~/.ssh/id_ed25519`` with 0o600 permissions.

    Raises:
        FileNotFoundError: If the encrypted key file does not exist in the
            dotfiles root.
    """
    logger.info("Decrypting SSH key")

    src = get_dotfile_root() / "ssh" / "id_ed25519.age"
    dest = Path.home() / ".ssh" / "id_ed25519"

    try:
        age_decrypt(src, dest)
    except RuntimeError as e:
        logger.error(f"SSH key decryption aborted: {e}")
        return

    logger.info("SSH key decrypted")
