{ inputs, ... }:

{
  flake.darwinConfigurations =
    let
      mkDarwinConfiguration = { hostname, system, username }:
        inputs.nix-darwin.lib.darwinSystem {
          inherit system;
          specialArgs = { inherit inputs username; };
          modules = [
            ../hosts/${hostname}
          ];
        };
    in
    {
      "Zachs-MacBook-Pro" = mkDarwinConfiguration {
        hostname = "zachs-macbook-pro";
        system = "aarch64-darwin";
        username = "zachbrown";
      };
    };
}
