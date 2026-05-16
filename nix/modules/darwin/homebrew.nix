{ config, lib, pkgs, ... }:

{
  homebrew = {
    enable = true;

    casks = [
      "discord"
      "ghostty"
      "obsidian"
      "spotify"
      "zen-browser"
    ];
  };
}
