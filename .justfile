_default: help

[group("0. Help")]
[doc("List all recipes (or just run `just`).")]
help:
    @just --list --unsorted





## For more info on `nix develop`, see: https://nix.dev/manual/nix/2.18/command-ref/new-cli/nix3-develop.html
## > `nix develop` - run a bash shell that provides the build environment of a derivation
## The next two commands (`activate` and `deactivate` devshell) are based on the assumption that if $SHLVL > 1 then we're already in a nix interactive development shell. See more discussion in the following two links:
## [1] https://discourse.nixos.org/t/custom-prompts-or-shell-depth-indicator-for-nix-shell-nix-develop/29942
## [2] https://github.com/NixOS/nix/issues/6677

shlvl := env('SHLVL', '-1')
## ^ We have to access the user's SHLVL like this because entering a justfile increments SHLVL


[group("1. Nix tools")]
[doc("Activate interactive development shell with uv (remember to `exit` when done) -- we recommend getting into the habit of using this recipe over plain `nix develop` since it incorporates guard rails against entering multi-nested devshells.")]
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

[group("1. Nix tools")]
[doc("Update flake. (check for `uv` updates in nixpkgs here: https://github.com/NixOS/nixpkgs/blob/nixpkgs-unstable/pkgs/by-name/uv/uv/package.nix )")]
update-flake:
    nix flake update





## TODO: add commands for creating the venv from scratch using the lockfile (WITHOUT updating anything)

[group("2. Project management/development")]
[doc("Sync the project's environment (`.venv/`) with exact dependencies in the lockfile (`uv.lock`). If `.venv/` doesn't exist, it will be created. All dependency groups will be installed, including optional and development (see `pyproject.toml`).")]
sync-venv:
    @# For more info, see: https://docs.astral.sh/uv/reference/cli/#uv-sync
    uv sync --all-extras --all-groups

[group("2. Project management/development")]
[doc("Update lockfile (`uv.lock`) with the latest versions of all dependencies. This does NOT install or modify `.venv/` — for that, see `sync-venv`.")]
update-lockfile:
    @# For more info see: https://docs.astral.sh/uv/reference/cli/#uv-lock
    uv lock --upgrade





[group("3. Project tools")]
[doc("Run tests.")]
test:
    @# Note that we use `uv run` as opposed to `uv tool run` since the tool in question (pytest) should NOT be isolated from the project...
    @#     [Excerpt from docs:] "If you are running a tool in a project and the tool requires that your project is installed, e.g., when using pytest or mypy, you'll want to use uv run instead of uvx. Otherwise, the tool will be run in a virtual environment that is isolated from your project."
    @# For more info, search the docs for 'pytest': https://docs.astral.sh/uv/guides/tools/#running-tools
    uv run pytest

[group("3. Project tools")]
[doc("Run tests, do not suppress print statements.")]
test-verbose:
    uv run pytest -s

# TODO: change this to `uv run` (see comments in `test` recipe)
# [group("3. Project tools")]
# [doc("Check static types with `mypy`.")]
# type-check target=".":
#     uvx mypy {{target}}

[group("3. Project tools")]
[doc("Start the live-reloading docs server locally (see: http://localhost:8000/ ).")]
site-serve:
    uv run mkdocs serve





[group("misc")]
[doc("Clean up Python bytecode artifacts.")]
clean:
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type f -name "*.pyc" -exec rm -f {} +
    find . -type d -name ".mypy_cache" -exec rm -r {} +
    find . -type d -name ".pytest_cache" -exec rm -r {} +
