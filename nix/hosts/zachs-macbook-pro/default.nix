{ config, lib, pkgs, inputs, username, ... }:

{
  imports = [
    ../../modules/darwin/homebrew.nix
    ../../modules/darwin/system-preferences.nix
  ];

  nixpkgs.overlays = [ inputs.claude-code.overlays.default ];

  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  environment.systemPackages = with pkgs; [
    # CLI tools
    age
    bat
    delta
    eza
    fastfetch
    fd
    fish
    fzf
    gh
    htop
    jq
    lazygit
    ripgrep
    starship
    stow
    tealdeer
    tree
    zoxide

    # Media
    ffmpeg

    # Node.js
    nodejs
    nodePackages.pnpm

    # Fonts
    nerd-fonts.jetbrains-mono

    # Apps
    claude-code
  ];

  programs.fish.enable = true;

  networking.hostName = "Zachs-MacBook-Pro";

  system.primaryUser = username;
  system.stateVersion = 5;
}
