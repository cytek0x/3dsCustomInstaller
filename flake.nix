{
  description = "custominstall";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    pyctr.url = "github:ihaveamac/pyctr/master";
    pyctr.inputs.nixpkgs.follows = "nixpkgs";
    hax-nur.url = "github:ihaveamac/nur-packages/master";
    hax-nur.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      pyctr,
      hax-nur,
    }:
    let
      systems = [
        "x86_64-linux"
        "i686-linux"
        "x86_64-darwin"
        "aarch64-darwin"
        "aarch64-linux"
        "armv6l-linux"
        "armv7l-linux"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      legacyPackages = forAllSystems (
        system:
        (import ./default.nix {
          pkgs = import nixpkgs { inherit system; };
          pyctr = pyctr.packages.${system}.pyctr;
          save3ds = hax-nur.packages.${system}.save3ds;
        })
        // {
          default = self.legacyPackages.${system}.custominstall;
        }
      );
      packages = forAllSystems (
        system: nixpkgs.lib.filterAttrs (_: v: nixpkgs.lib.isDerivation v) self.legacyPackages.${system}
      );
    };
}
