{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    devkitNix.url = "github:bandithedoge/devkitNix";
    devkitNix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, devkitNix }: let
    pkgs = import nixpkgs { system = "x86_64-linux"; overlays = [ devkitNix.overlays.default ]; };
  in {
    devShells.x86_64-linux = rec {
      custom-install-finalize = pkgs.mkShell.override { stdenv = pkgs.devkitNix.stdenvARM; } {};
      cif = custom-install-finalize;
    };

    packages.x86_64-linux = rec {
      custom-install-finalize = pkgs.devkitNix.stdenvARM.mkDerivation rec {
        name = "custom-install-finalize";
        src = builtins.path { path = ./.; name = name; };

        makeFlags = [ "TARGET=${name}" ];

        installPhase = ''
          mkdir $out
          cp ${name}.3dsx $out
        '';
      };
      cif = custom-install-finalize;
    };
  };
}
