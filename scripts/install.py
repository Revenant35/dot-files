#!/usr/bin/env python3
import sys
from pathlib import Path

from _common import (
    BREW_BASE_FILE,
    REPO_ROOT,
    dispatch,
    parse_args,
    read_package_list,
    require,
    run,
    update_etc_shells,
)


def install_packages(cfg):
    print("=== Installing packages ===")
    pm = cfg["package_manager"]
    if pm == "brew":
        require("brew")
        run(["brew", "bundle", f"--file={BREW_BASE_FILE}"])
        run(["brew", "bundle", f"--file={cfg['package_file']}"])
    elif pm == "dnf":
        require("dnf")
        run(["sudo", "dnf", "install", "-y", *read_package_list(cfg["package_file"])])


def install_config():
    print("=== Stowing config files ===")
    require("stow")
    run(["stow", "."], cwd=REPO_ROOT / "config")


def install_git(cfg):
    print("=== Writing ~/.config/git/config.local ===")
    git_dir = Path.home() / ".config" / "git"
    git_dir.mkdir(parents=True, exist_ok=True)
    (git_dir / "config.local").write_text(
        f"[user]\n    email = {cfg['git_email']}\n"
    )


def decrypt_ssh(cfg):
    print("=== Decrypting SSH private key ===")
    age_file = cfg["ssh_dir"] / "id_ed25519.age"
    if not age_file.is_file():
        print(f"Error: SSH key file not found: {age_file}")
        sys.exit(1)
    ssh_dir = Path.home() / ".ssh"
    ssh_dir.mkdir(mode=0o700, exist_ok=True)
    ssh_dir.chmod(0o700)
    require("age")
    key_path = ssh_dir / "id_ed25519"
    run(["age", "-d", "-o", str(key_path), str(age_file)])
    key_path.chmod(0o600)


def install_ssh(cfg):
    decrypt_ssh(cfg)
    print("=== Stowing SSH files ===")
    require("stow")
    run(["stow", "."], cwd=cfg["ssh_dir"])


def add_shell(shell):
    print(f"=== Adding {shell} to shells ===")
    shell_path = require(shell)
    update_etc_shells(shell_path, present=True)
    run(["chsh", "-s", shell_path])


def main():
    cfg, subsystem = parse_args()
    actions = {
        "packages": lambda: install_packages(cfg),
        "config": install_config,
        "git": lambda: install_git(cfg),
        "ssh": lambda: install_ssh(cfg),
        "shell": lambda: add_shell("fish"),
    }
    dispatch(subsystem, actions)
    print("=== Done ===")


if __name__ == "__main__":
    main()
