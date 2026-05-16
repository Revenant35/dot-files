set fish_greeting

if status is-interactive
# Commands to run in interactive sessions can go here
  # -- Starship --
  starship init fish | source
  enable_transience

  # -- lazygit --
  export XDG_CONFIG_HOME="$HOME/.config"

  # -- Nix --
  abbr -a drs "sudo darwin-rebuild switch"

  # -- zoxide --
  abbr -a cd z
  zoxide init fish | source

  # -- eza --
  abbr -a ls "eza --color=always --long --git --no-filesize --icons=always --no-time --no-user --no-permissions"

  # -- bat --
  abbr -a cat bat

  # -- fzf --
  fzf --fish | source

  # -- fastfetch --
  abbr -a ff fastfetch

  # -- pnpm --
  abbr -a npm pnpm
  abbr -a nx "pnpm nx"

  # -- age --
  abbr -a ssh-unlock "age -d -o ~/.ssh/id_ed25519 id_ed25519.age"
end
