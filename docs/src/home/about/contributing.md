TODO

- How to install/use `uv`
    - RedPlanet is developed using the [Nix package manager](https://nixos.org/){target="_blank"}, which provides a fully declarative (see `flake.nix`), reproducible (see `flake.lock`), and reliable development environment.
    - On other systems, prerequisites are:
        - `uv`
            - Installation instructions in their [docs](https://docs.astral.sh/uv/){target="_blank"} — on Windows, I highly suggest using WSL, it takes a few minutes to setup but will save a ton of headache down the road.
        - `just`
            - Simple task runner similar to GNU Make and Makefiles (see next section for more info).

- Explanation of justfile
    - Run `just` to see all options... (insert image)
    - Run tests with `just test` (insert image)


We encourage you to use [Conventional Commit Messages](https://www.conventionalcommits.org/){target="_blank"} (cheatsheets: [\[1\]](https://gist.github.com/Zekfad/f51cb06ac76e2457f11c80ed705c95a3){target="_blank"}, [\[2\]](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13){target="_blank"}) for best practices/standardization, although it's not required.
