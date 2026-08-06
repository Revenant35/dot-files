"""
brew.py - Shared Homebrew helper functions
"""

import os
import subprocess


BREWFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Brewfile")
TARGET = os.path.expanduser("~/.Brewfile")


def check_homebrew() -> bool:
    return subprocess.run(["which", "brew"], capture_output=True).returncode == 0


def install_homebrew():
    print("Homebrew not found. Installing...")
    install_cmd = (
        '/bin/bash -c "$(curl -fsSL '
        'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    )
    subprocess.run(install_cmd, shell=True, check=True)
    # Add Homebrew to PATH for Apple Silicon
    homebrew_bin = "/opt/homebrew/bin"
    if os.path.isdir(homebrew_bin):
        os.environ["PATH"] = homebrew_bin + ":" + os.environ.get("PATH", "")


def brewfile_exists() -> bool:
    return os.path.exists(os.path.expanduser("~/.Brewfile"))


def brew_update():
    print("Updating Homebrew...")
    subprocess.run(["brew", "update"], check=True)


def brew_bundle():
    print("Installing new packages from Brewfile...")
    subprocess.run(["brew", "bundle", "--global"], check=False)


def brew_cleanup():
    print("Cleaning up packages not in Brewfile...")
    subprocess.run(["brew", "bundle", "--global", "cleanup", "--force"], check=True)


def brew_upgrade():
    print("Upgrading outdated packages...")
    subprocess.run(["brew", "upgrade"], check=True)


def link_brewfile():
    if os.path.islink(TARGET):
        existing = os.readlink(TARGET)
        if existing == BREWFILE:
            print(f"~/.Brewfile is already linked to {BREWFILE}")
            return
        print(f"Replacing existing symlink: {TARGET} -> {existing}")
        os.remove(TARGET)
    elif os.path.exists(TARGET):
        backup = TARGET + ".bak"
        print(f"Backing up existing ~/.Brewfile to {backup}")
        os.rename(TARGET, backup)

    os.symlink(BREWFILE, TARGET)
    print(f"Linked {TARGET} -> {BREWFILE}")


def install_brew_packages():
    print("=== Brewfile install ===\n")
    if not check_homebrew():
        install_homebrew()
    link_brewfile()
    brew_bundle()
    brew_cleanup()
    print("\nDone.")


def update_brew_packages():
    print("=== Brewfile update ===\n")
    if not check_homebrew():
        raise RuntimeError("Homebrew is not installed. Run install.py first.")
    if not brewfile_exists():
        raise RuntimeError("~/.Brewfile not found. Run install.py first.")
    brew_update()
    brew_bundle()
    brew_cleanup()
    brew_upgrade()
    print("\nDone.")
