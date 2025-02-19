{ pkgs, lib, config, inputs, ... }:

{

  services.mysql = {
      enable = true;
  };
}
