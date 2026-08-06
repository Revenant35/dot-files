from pathlib import Path

def get_dotfile_root() -> Path:
    """Returns the path to the root of the dotfile repository."""
    return Path(__file__).resolve().parents[1]
