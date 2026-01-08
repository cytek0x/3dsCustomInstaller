{
  pkgs ? import <nixpkgs> { },
  # just so i can use the same pinned version as the flake...
  pyctr ? (
    let
      flakeLock = builtins.fromJSON (builtins.readFile ./flake.lock);
      pyctr-repo = import (builtins.fetchTarball (
        with flakeLock.nodes.pyctr.locked;
        {
          url = "https://github.com/${owner}/${repo}/archive/${rev}.tar.gz";
        }
      )) { inherit pkgs; };
    in
    pyctr-repo.pyctr
  ),
  save3ds ? (
    let
      flakeLock = builtins.fromJSON (builtins.readFile ./flake.lock);
      hax-nur-repo = import (builtins.fetchTarball (
        with flakeLock.nodes.hax-nur.locked;
        {
          url = "https://github.com/${owner}/${repo}/archive/${rev}.tar.gz";
        }
      )) { inherit pkgs; };
    in
    hax-nur-repo.save3ds
  ),
}:

rec {
  custominstall = pkgs.python3Packages.callPackage ./package.nix {
    inherit pyctr save3ds;
  };
}
