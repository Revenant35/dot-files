# dotfiles

Zach Brown's macOS dotfiles, managed with [GNU Stow](https://www.gnu.org/software/stow/) and automated via Python.

## Bootstrap

On a fresh machine, run:

```bash
curl -fsSL https://raw.githubusercontent.com/Revenant35/dot-files/main/install.sh | bash
```

This will:

1. Clone the repo to `~/.dotfiles`
2. Install [Homebrew](https://brew.sh) if not already present
3. Install all packages and apps from the `Brewfile` via `brew bundle`
4. Symlink configs into `~/.config` and `~/.ssh` via `stow`
5. Decrypt the SSH private key (`ssh/id_ed25519.age`) using `age`

> **Note:** `git` and `python3` must be available before running the one-liner.
> On macOS, running `git` for the first time will prompt you to install Xcode Command Line Tools, which provides both.

To clone to a custom location, set `DOTFILES_DIR` before running:

```bash
DOTFILES_DIR=~/code/dotfiles curl -fsSL https://raw.githubusercontent.com/Revenant35/dot-files/main/install.sh | bash
```

## Manual usage

```bash
git clone --recurse-submodules https://github.com/Revenant35/dot-files.git ~/.dotfiles
python3 ~/.dotfiles/scripts/sync.py
```

Individual steps can also be run in isolation:

```bash
python3 scripts/sync.py brew   # Homebrew only
python3 scripts/sync.py stow   # Symlinks only
python3 scripts/sync.py ssh    # SSH key decryption only
```

## Structure

```
.
├── install.sh          # Remote bootstrap script (curl | bash)
├── Brewfile            # All Homebrew packages and casks
├── config/             # XDG config files — stowed to ~/.config
│   ├── bat/
│   ├── fish/
│   ├── gh/
│   ├── ghostty/
│   ├── git/
│   ├── lazygit/
│   ├── opencode/
│   └── starship/
├── ssh/                # SSH config — stowed to ~/.ssh
│   ├── config
│   ├── id_ed25519.age  # Encrypted private key (age)
│   └── id_ed25519.pub
└── scripts/            # Sync automation
    ├── sync.py         # Entry point
    ├── _brew.py        # Homebrew install and bundle
    ├── _stow.py        # GNU stow wrapper
    ├── _ssh.py         # SSH key decryption
    ├── _crypto.py      # age decryption helper
    ├── _shell.py       # subprocess utilities
    ├── _platform.py    # OS detection
    ├── _common.py      # Shared path utility
    └── _logging.py     # Colored logger
```

## Dependencies

| Tool | Purpose | Auto-installed |
|------|---------|----------------|
| Homebrew | Package manager | Yes (by `install.sh`) |
| GNU stow | Symlink manager | Yes (via Brewfile) |
| age | SSH key decryption | Yes (via Brewfile) |
| git | Clone and version control | No — required before bootstrap |
| python3 | Run sync scripts | No — required before bootstrap |

## Adding new configs

1. Place the config file under `config/` (for `~/.config` targets) or `ssh/` (for `~/.ssh` targets), mirroring the exact path it should land at.
2. Run `python3 scripts/sync.py stow` to create the symlink.
3. Commit the file — the symlink is re-created from scratch on every sync.

## Adding Homebrew packages

Add the formula or cask to `Brewfile`, then run:

```bash
python3 scripts/sync.py brew
```

The sync will install new entries and remove anything no longer listed.
