{
  description = "Pure functional and typing utilities";
  inputs = {
    arch-lint = {
      url = "gitlab:dmurciaatfluid/arch_lint";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nixpkgs.url = "github:nixos/nixpkgs";
    nix_filter.url = "github:numtide/nix-filter";
  };
  outputs = {
    self,
    arch-lint,
    nixpkgs,
    nix_filter,
  }: let
    metadata = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).project;
    path_filter = nix_filter.outputs.lib;
    src = path_filter {
      root = self;
      include = [
        "mypy.ini"
        "pyproject.toml"
        (path_filter.inDirectory metadata.name)
        (path_filter.inDirectory "tests")
      ];
    };
    out = system: python_version:
      import ./build {
        inherit src python_version;
        nixpkgs =
          nixpkgs.legacyPackages."${system}"
          // {
            arch-lint = arch-lint.packages."${system}";
          };
      };
    supported = ["python38" "python39" "python310" "python311"];
    python_outs = system:
      (builtins.listToAttrs (map (name: {
          inherit name;
          value = out system name;
        })
        supported))
      // {build_with_python = out system;};
    systems = [
      "aarch64-darwin"
      "aarch64-linux"
      "x86_64-darwin"
      "x86_64-linux"
    ];
    forAllSystems = nixpkgs.lib.genAttrs systems;
  in {
    packages = forAllSystems python_outs;
    defaultPackage = self.packages;
  };
}
