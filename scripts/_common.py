import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

BREW_BASE_FILE = REPO_ROOT / "packages" / "base.Brewfile"

CONFIGS = {
    "home-macbook": {
        "package_file": REPO_ROOT / "packages" / "home-macbook.Brewfile",
        "package_manager": "brew",
        "ssh_dir": REPO_ROOT / "ssh" / "home",
        "git_email": "bbrown64506@gmail.com",
    },
    "work-macbook": {
        "package_file": REPO_ROOT / "packages" / "work-macbook.Brewfile",
        "package_manager": "brew",
        "ssh_dir": REPO_ROOT / "ssh" / "work",
        "git_email": "zacharyc.brown@veteransunited.com",
    },
    "home-desktop": {
        "package_file": REPO_ROOT / "packages" / "home-desktop.dnf.txt",
        "package_manager": "dnf",
        "ssh_dir": REPO_ROOT / "ssh" / "home",
        "git_email": "bbrown64506@gmail.com",
    },
}

SUBSYSTEMS = ["packages", "ssh", "config", "git", "shell"]


def usage(code=1):
    prog = sys.argv[0]
    print(f"Usage: {prog} <config> [{'|'.join(SUBSYSTEMS)}]")
    print("")
    print("Configurations:")
    print("  home-macbook   macOS laptop (personal)")
    print("  work-macbook   macOS laptop (work)")
    print("  home-desktop   Linux desktop (personal)")
    sys.exit(code)


def require(cmd):
    path = shutil.which(cmd)
    if path is None:
        print(f"Error: '{cmd}' is not installed.")
        sys.exit(1)
    return path


def run(args, **kwargs):
    subprocess.run(args, check=True, **kwargs)


def update_etc_shells(shell_path, *, present):
    shells_file = Path("/etc/shells")
    try:
        lines = shells_file.read_text().splitlines()
    except FileNotFoundError:
        lines = []
    has = shell_path in lines
    if present and not has:
        new = "\n".join(lines + [shell_path]) + "\n"
    elif not present and has:
        new = "\n".join(l for l in lines if l != shell_path) + "\n"
    else:
        return
    run(
        ["sudo", "tee", str(shells_file)],
        input=new,
        text=True,
        stdout=subprocess.DEVNULL,
    )


def read_package_list(path: Path):
    return [
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def parse_args():
    if len(sys.argv) < 2:
        usage()
    config_name = sys.argv[1]
    subsystem = sys.argv[2] if len(sys.argv) > 2 else ""
    cfg = CONFIGS.get(config_name)
    if cfg is None:
        usage()
    return cfg, subsystem


def dispatch(subsystem, actions):
    if subsystem == "":
        for action in actions.values():
            action()
    elif subsystem in actions:
        actions[subsystem]()
    else:
        usage()
