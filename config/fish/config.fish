set fish_greeting

# Add Homebrew to PATH
if test -x /opt/homebrew/bin/brew
  eval (/opt/homebrew/bin/brew shellenv)
end

# -- .NET --
if test -d /opt/homebrew/opt/dotnet@8
  fish_add_path /opt/homebrew/opt/dotnet@8/bin
  set -gx DOTNET_ROOT /opt/homebrew/opt/dotnet@8/libexec
end

if status is-interactive
# Commands to run in interactive sessions can go here

  # Clean up old abbreviations that were migrated to aliases
  for a in (abbr --list)
      abbr --erase $a
  end

  # -- Starship --
  starship init fish | source
  enable_transience

  # -- lazygit --
  export XDG_CONFIG_HOME="$HOME/.config"

  # -- Nix --
  alias drs="sudo darwin-rebuild switch"

  # -- zoxide --
  alias cd=z
  zoxide init fish | source

  # -- eza --
  alias ls="eza --color=always --long --git --no-filesize --icons=always --no-time --no-user --no-permissions"

  # -- bat --
  alias cat=bat

  # -- fzf --
  fzf --fish | source

  # -- fastfetch --
  alias ff=fastfetch

  # -- pnpm --
  alias npm=pnpm
  alias nx="pnpm nx"

  # -- age --
  alias ssh-unlock="age -d -o ~/.ssh/id_ed25519 id_ed25519.age"
end
