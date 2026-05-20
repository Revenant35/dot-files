#!/usr/bin/env python3
import shutil
import subprocess
from pathlib import Path

from _common import (
    REPO_ROOT,
    dispatch,
    parse_args,
    read_package_list,
    require,
    run,
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
    require("stow")
    print("=== Unstowing SSH files ===")
    run(["stow", "-D", "."], cwd=cfg["ssh_dir"])
    key = Path.home() / ".ssh" / "id_ed25519"
    if key.is_file():
        print("=== Removing decrypted SSH private key ===")
        key.unlink()


def remove_shell(shell):
    print(f"=== Removing {shell} from shells ===")
    shell_path = shutil.which(shell)
    shells_file = Path("/etc/shells")
    if shell_path and shells_file.exists():
        lines = shells_file.read_text().splitlines()
        if shell_path in lines:
            new_content = "\n".join(l for l in lines if l != shell_path) + "\n"
            subprocess.run(
                ["sudo", "tee", str(shells_file)],
                input=new_content,
                text=True,
                check=True,
                stdout=subprocess.DEVNULL,
            )
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
    order = ["shell", "ssh", "git", "config", "packages"]
    dispatch(subsystem, actions, order)
    print("=== Done ===")


if __name__ == "__main__":
    main()
