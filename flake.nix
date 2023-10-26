{
  description = "The Pfersel Discord bot";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
      packages = forAllSystems (system: {
        default = pkgs.${system}.python311Packages.callPackage ./default.nix { };
      });
      hydraJobs = forAllSystems (system: {
        default = self.packages.${system}.default;
      });
      nixosModules.default = import ./module.nix;

      devShells = forAllSystems (system: {
        default =
          let
            pythonEnv = pkgs.${system}.python311.withPackages (p: with p; [ (self.packages.${system}.default) ]);
          in

          pkgs.${system}.mkShell {
            packages = [ pythonEnv ];
            shellHook = ''
              export PYTHONPATH="${pythonEnv}/lib/python3.11/site-packages/"
            '';
          };
      });
    };
}
