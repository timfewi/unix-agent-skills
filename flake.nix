{
  description = "unix-agent-skills: small, isolated agent skills for Linux and macOS";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/7a0f122f5090cf4c2ade2a13a0e229d4e19ba71f";

  outputs =
    { self, nixpkgs }:
    let
      inherit (nixpkgs) lib;
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = lib.genAttrs systems;
      directories =
        path: lib.attrNames (lib.filterAttrs (_: kind: kind == "directory") (builtins.readDir path));
      # skills/<domain>/<skill> flattened to <skill>, the layout every harness
      # discovers. The validator rejects duplicate names; this guard covers
      # consumers that build without running the checks.
      entries = lib.concatMap (
        domain:
        map (name: {
          inherit name;
          path = ./skills + "/${domain}/${name}";
        }) (directories (./skills + "/${domain}"))
      ) (directories ./skills);
      skills =
        lib.throwIf (lib.length (lib.unique (map (entry: entry.name) entries)) != lib.length entries)
          "unix-agent-skills: skill names must be unique across domains"
          (lib.listToAttrs (map (entry: lib.nameValuePair entry.name entry.path) entries));
    in
    {
      # Skill name -> directory, for consumers that select individual skills.
      lib.skills = skills;

      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        rec {
          skills = pkgs.linkFarm "unix-agent-skills" (
            lib.mapAttrsToList (name: path: { inherit name path; }) self.lib.skills
          );
          default = skills;
        }
      );

      checks = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          catalog =
            pkgs.runCommand "unix-agent-skills-check"
              {
                # Darwin builds use the system ps and pgrep.
                nativeBuildInputs = [
                  pkgs.python3
                  pkgs.ruff
                  pkgs.shellcheck
                ]
                ++ lib.optional pkgs.stdenv.isLinux pkgs.procps;
                src = self;
              }
              ''
                cp -r "$src" source
                chmod -R u+w source
                cd source
                export PYTHONDONTWRITEBYTECODE=1
                python3 scripts/validate.py
                python3 -m unittest discover -s tests -p 'test_*.py'
                ruff check --no-cache scripts tests
                ruff format --check --no-cache scripts tests
                shellcheck skills/*/*/scripts/*.sh
                touch "$out"
              '';
        }
      );

      devShells = forAllSystems (system: {
        default = nixpkgs.legacyPackages.${system}.mkShell {
          packages = with nixpkgs.legacyPackages.${system}; [
            python3
            ruff
            shellcheck
            nixfmt
            statix
            deadnix
          ];
        };
      });

      formatter = forAllSystems (system: nixpkgs.legacyPackages.${system}.nixfmt-tree);
    };
}
