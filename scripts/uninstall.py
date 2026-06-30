#!/usr/bin/env python3
import shutil
from pathlib import Path

from _common import (
    REPO_ROOT,
    dispatch,
    parse_args,
    read_package_list,
    require,
    run,
    update_etc_shells,
)


def uninstall_packages(cfg):
    print("=== Uninstalling packages ===")
    pm = cfg["package_manager"]
    if pm == "brew":
        require("brew")
        run(["brew", "bundle", "cleanup", "--force", f"--file={cfg['package_file']}"])
    elif pm == "dnf":
        require("dnf")
        run(["sudo", "dnf", "remove", "-y", *read_package_list(cfg["package_file"])])


def uninstall_config():
    print("=== Unstowing config files ===")
    require("stow")
    run(["stow", "-D", "."], cwd=REPO_ROOT / "config")


def uninstall_git():
    print("=== Removing ~/.config/git/config.local ===")
    (Path.home() / ".config" / "git" / "config.local").unlink(missing_ok=True)


def uninstall_ssh(cfg):
    print("=== Unstowing SSH files ===")
    require("stow")
    run(["stow", "-D", "."], cwd=cfg["ssh_dir"])
    print("=== Removing decrypted SSH private key ===")
    (Path.home() / ".ssh" / "id_ed25519").unlink(missing_ok=True)


def remove_shell(shell):
    print(f"=== Removing {shell} from shells ===")
    shell_path = shutil.which(shell)
    if shell_path:
        update_etc_shells(shell_path, present=False)
    run(["chsh", "-s", "/bin/zsh"])


def main():
    cfg, subsystem = parse_args()
    actions = {
        "shell": lambda: remove_shell("fish"),
        "ssh": lambda: uninstall_ssh(cfg),
        "git": uninstall_git,
        "config": uninstall_config,
        "packages": lambda: uninstall_packages(cfg),
    }
    dispatch(subsystem, actions)
    print("=== Done ===")


if __name__ == "__main__":
    main()
