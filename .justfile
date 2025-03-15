_default: help

[group("Help")]
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


[group("Development shell via Nix package manager")]
[doc("Activate interactive development shell with uv (remember to `exit` when done) — we recommend getting into the habit of using this recipe over plain `nix develop` since it incorporates guard rails against entering multi-nested devshells.")]
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

[group("Development shell via Nix package manager")]
[doc("Update flake. (check for `uv` updates in nixpkgs here: https://github.com/NixOS/nixpkgs/blob/nixpkgs-unstable/pkgs/by-name/uv/uv/package.nix )")]
update-flake:
    nix flake update





## TODO: add commands for creating the venv from scratch using the lockfile (WITHOUT updating anything)

[group("Dependencies")]
[doc("Sync the project's environment (`.venv/`) with exact dependencies in the lockfile (`uv.lock`), both optional and development groups. If `.venv/` doesn't exist, it will be created.")]
sync-venv:
    @# For more info, see: https://docs.astral.sh/uv/reference/cli/#uv-sync
    @#   Note: `--all-extras` and `--all-groups` refer to the optional (`[project.optional-dependencies]`) and development (`[dependency-groups]`) dependencies in `pyproject.toml`, respectively. For more info, see commit `b25359d`.
    uv sync --all-extras --all-groups

[group("Dependencies")]
[doc("Update lockfile (`uv.lock`) with the latest versions of all dependencies. This does NOT install or modify `.venv/` — for that, see `sync-venv`.")]
update-lockfile:
    @# For more info see: https://docs.astral.sh/uv/reference/cli/#uv-lock
    uv lock --upgrade





[group("Test")]
[doc("Run tests.")]
test:
    @# Note that we use `uv run` as opposed to `uv tool run` since the tool in question (pytest) should NOT be isolated from the project...
    @#     [Excerpt from docs:] "If you are running a tool in a project and the tool requires that your project is installed, e.g., when using pytest or mypy, you'll want to use uv run instead of uvx. Otherwise, the tool will be run in a virtual environment that is isolated from your project."
    @# For more info/tips/guidance, search the docs for 'pytest': https://docs.astral.sh/uv/guides/tools/#running-tools
    uv run -- pytest tests/

[group("Test")]
[doc("Run tests, do not suppress print statements.")]
test-verbose:
    uv run -- pytest tests/ -s

# TODO: change this to `uv run` (see comments in `test` recipe)
# [group("Test")]
# [doc("Check static types with `mypy`.")]
# type-check target=".":
#     uvx mypy {{target}}





[group("Website")]
[doc("Start the live-reloading docs server locally (see: http://localhost:8000/ ).")]
serve-site:
    uv run -- mkdocs serve --config-file docs/mkdocs.yml

[group("Website")]
[doc("Deploy to GitHub Pages.")]
deploy-site:
    uv run -- mkdocs gh-deploy --config-file docs/mkdocs.yml --no-history
    just _clean_site





[group("Publish")]
[doc("Create an annotated git tag with the version extracted from `pyproject.toml` — NOTE: this triggers a PyPI release when pushed! Always push the plain commit first and ensure tests are passing in GitHub Actions: https://github.com/Humboldt-Penguin/redplanet/actions")]
tag:
    #!/usr/bin/env bash
    set -euo pipefail
    version=$(uv run -- python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")
    version="v${version}"
    echo "Create tag \"$version\"? [y/n]"
    read -r response
    if [ "$response" != "y" ]; then
        echo "Exiting without creating tag."
        exit
    fi
    git tag -a "$version"
    # Self note: always use annotated tags over lightweight tags, even if the message is empty -- see [1] for an explanation, and [2] for useful commands/reference
    #   [1] https://stackoverflow.com/a/4971817
    #   [2] https://stackoverflow.com/a/25996877
    echo "- Push this tag: \`git push origin $version\`"
    echo "- Push all tags: \`git push --tags\`"
    echo "- Delete this tag locally (no 'amend' option): \`git tag -d $version\`"





[group("misc")]
[doc("Clean up Python bytecode artifacts + website build files.")]
clean:
    just _clean_python
    just _clean_site



# Clean up Python bytecode artifacts.
_clean_python:
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type f -name "*.pyc" -exec rm -f {} +
    find . -type d -name ".mypy_cache" -exec rm -r {} +
    find . -type d -name ".pytest_cache" -exec rm -r {} +

# Clean up website build files.
_clean_site:
    rm -rf docs/site/
