_default: help

[doc('List all recipes (or just run `just`).')]
[group('0. Help')]
help:
    @just --list





## For more info on `nix develop`, see: https://nix.dev/manual/nix/2.18/command-ref/new-cli/nix3-develop.html
## > `nix develop` - run a bash shell that provides the build environment of a derivation
## The next two commands (`activate` and `deactivate` devshell) are based on the assumption that if $SHLVL > 1 then we're already in a nix interactive development shell. See more discussion in the following two links:
## [1] https://discourse.nixos.org/t/custom-prompts-or-shell-depth-indicator-for-nix-shell-nix-develop/29942
## [2] https://github.com/NixOS/nix/issues/6677

shlvl := env('SHLVL', '-1')
## ^ We have to access the user's SHLVL like this because entering a justfile increments SHLVL


[doc('Activate interactive development shell (remember to `exit` when done!) -- we recommend getting in the habit of using this to avoid accidentally entering multi-nested devshells.')]
[group('1. Access UV Development Environment')]
activate-devshell:
    #!/usr/bin/env bash
    set -euo pipefail
    # Error: $SHLVL doesn't exist
    if [ "{{shlvl}}" -eq -1 ]; then
        echo "ERROR: Environment variable \$SHLVL not found, this is unexpected, not sure what to do."
        echo "Exiting without any changes."
        exit
    fi
    # Error: Already in dev shell
    if [ "{{shlvl}}" -gt 1 ]; then
        echo "ERROR: You are already in an interactive development shell."
        echo "Exiting without any changes."
        exit
    fi
    # Activate environment
    nix develop

