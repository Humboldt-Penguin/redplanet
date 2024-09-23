_default: help

[group('0. Help')]
[doc('List all recipes (or just run `just`).')]
help:
    @just --list --unsorted





## For more info on `nix develop`, see: https://nix.dev/manual/nix/2.18/command-ref/new-cli/nix3-develop.html
## > `nix develop` - run a bash shell that provides the build environment of a derivation
## The next two commands (`activate` and `deactivate` devshell) are based on the assumption that if $SHLVL > 1 then we're already in a nix interactive development shell. See more discussion in the following two links:
## [1] https://discourse.nixos.org/t/custom-prompts-or-shell-depth-indicator-for-nix-shell-nix-develop/29942
## [2] https://github.com/NixOS/nix/issues/6677

shlvl := env('SHLVL', '-1')
## ^ We have to access the user's SHLVL like this because entering a justfile increments SHLVL


[group('1. Access UV Development Environment')]
[doc('Activate interactive development shell (remember to `exit` when done!) -- we recommend getting in the habit of using this to avoid accidentally entering multi-nested devshells.')]
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





[group('2. Developer tools')]
[doc('Run tests.')]
test:
    @# Note that we use `uv run` as opposed to `uv tool run` since the tool in question (pytest) should NOT be isolated from the project...
    @#     [Excerpt from docs:] "If you are running a tool in a project and the tool requires that your project is installed, e.g., when using pytest or mypy, you'll want to use uv run instead of uvx. Otherwise, the tool will be run in a virtual environment that is isolated from your project."
    @# For more info, search the docs for 'pytest': https://docs.astral.sh/uv/guides/tools/#running-tools
    uv run pytest

[group('2. Developer tools')]
[doc('Run tests, do not suppress print statements.')]
test-verbose:
    uv run pytest -s

[group('2. Developer tools')]
[doc('Clean up Python bytecode artifacts.')]
clean:
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type f -name "*.pyc" -exec rm -f {} +
    find . -type d -name ".mypy_cache" -exec rm -r {} +
    find . -type d -name ".pytest_cache" -exec rm -r {} +

[group('2. Developer tools')]
[doc('Check static types with `mypy`.')]
type-check:
    uvx mypy .
