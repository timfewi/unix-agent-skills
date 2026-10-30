{
  config,
  lib,
  pkgs,
  ...
}:
let
  rootURL = lib.concatMapStringsSep "/" lib.escapeURL (lib.splitString "/" config.devenv.root);
  locked = builtins.getFlake "git+file://${rootURL}";
  project = locked // (import ./flake.nix).outputs (locked.inputs // { self = project; });
  shell = project.devShells.${pkgs.stdenv.hostPlatform.system}.default;
in
{
  # Reuse the locked Flake toolchain, including compiler and setup hooks.
  devenv.latestVersion = "2.4.0";
  inputsFrom = [ shell ];
  inherit (shell) stdenv;
}
