{ lib, pkgs, config, ... }:
with lib;
let
  cfg = config.services.pfersel;
  appEnv = pkgs.python310.withPackages (p: with p; [ (pkgs.python310Packages.callPackage ./default.nix { }) ]);
in
{
  options.services.pfersel = {
    enable = mkEnableOption "pfersel";
    dataDir = mkOption {
      type = types.path;
      default = "/var/lib/pfersel";
      description = lib.mdDoc ''
        Data directory
      '';
    };
    discord = {
      tokenFile = mkOption {
        type = types.path;
        default = null;
        description = mdDoc ''
          File containing the Bot Token to authenticate to Discord.
        '';
      };

    };
  };

  config = mkIf (cfg.enable) {
    users.users.pfersel = {
      isSystemUser = true;
      group = "pfersel";
    };
    users.groups.pfersel = { };
    systemd.tmpfiles.rules = [
      "d '${cfg.dataDir}' 0700 pfersel pfersel - -"
    ];

    systemd.services.pfersel = {
      enable = true;
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      environment = {
        TOKEN_FILE = cfg.discord.tokenFile;
      };
      serviceConfig = {
        WorkingDirectory = cfg.dataDir;
        ExecStart = "${appEnv}/bin/python -m pfersel";
        User = "pfersel";
        Group = "pfersel";
      };
    };
  };
}
