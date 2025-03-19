This page is for anyone who wants to contribute to RedPlanet's code.

We assume you're familiar with GitHub and Git. If not, learn about them [here](https://docs.github.com/en/get-started/start-your-journey/hello-world){target="_blank"}.

If you're not comfortable with this process, feel free to contact us by email or open an issue on GitHub — we'd happy to implement your suggestions!


---

---
## [1] Developer Tools

---
### [1.1] Prerequisites

Any operating system should be fine:

| OS                         | Instructions                                                                                                                                                                                                                                                          |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Linux/MacOS                | Everything should work out of the box.                                                                                                                                                                                                                                |
| Windows                    | Please just use [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/about){target="_blank"}, it takes a few minutes to set up and will make anything programming-related exponentially easier.                                          |
| Nix (OS / package manager) | We use this ourselves since it offers the most reliable/reproducible/sandboxed development environment. Make sure flakes are enabled, and run `just activate-devshell` (or `nix develop`) to enter the development environment based on `flake.nix` and `flake.lock`. |

&nbsp;

Please install the following tools (these are fairly lightweight, easy to uninstall, and will never permanently alter you system in any way — I'd never ask you to install something I wouldn't be comfortable with on my own personal computer!):

1. [`uv` by Astral](https://docs.astral.sh/uv/getting-started/installation/){target="_blank"} for running/managing Python environments.
2. [`just` by Casey Rodarmor](https://just.systems/man/en/prerequisites.html){target="_blank"} as a lightweight/basic command runner, very similar to GNU Make / Makefiles. You can see the exact commands in the `.justfile`, or list the recipes by running `just`:

<!-- Self note: get the text below with `just > tmp.txt`, don't fuss with copying from terminal or screenshotting. -->

```toml
Available recipes:
    [Help]
    help              # List all recipes (or just run `just`).

    [Development shell via Nix package manager]
    activate-devshell # Activate interactive development shell with uv (remember to `exit` when done) — we recommend getting into the habit of using this recipe over plain `nix develop` since it incorporates guard rails against entering multi-nested devshells.
    update-flake      # Update flake. (check for `uv` updates in nixpkgs here: https://github.com/NixOS/nixpkgs/blob/nixpkgs-unstable/pkgs/by-name/uv/uv/package.nix )

    [Dependencies]
    sync-venv         # Sync the project's environment (`.venv/`) with exact dependencies in the lockfile (`uv.lock`), including installing this project in editable mode. If `.venv/` doesn't exist, it will be created.
    update-lockfile   # Update lockfile (`uv.lock`) with the latest versions of all dependencies. This does NOT install or modify `.venv/` — for that, see `sync-venv`.

    [Test]
    test              # Run tests.
    test-verbose      # Run tests, do not suppress print statements.

    [Website]
    serve-site        # Start the live-reloading docs server locally (see: http://localhost:8000/ ).
    deploy-site       # Deploy to GitHub Pages.

    [Publish]
    tag               # Create an annotated git tag with version from `pyproject.toml` — NOTE: this triggers a PyPI release when pushed! You should (1) update version manually in `pyproject.toml` and automatically in `uv.lock`, then commit; (2) push, then verify tests passing in GitHub Actions; (3) merge to main, then `just tag`; (4) double check, then push commit + tag.

    [misc]
    clean             # Clean up miscellaneous build/artifact files.
```

<!-- ![](https://files.catbox.moe/vnk61w.png) -->


&nbsp;

---
### [1.2] Install Project Locally

Run `just sync-venv` (which calls `uv sync --all-extras --all-groups` under the hood) to sync the project's environment (`.venv/`) with exact dependencies in the lockfile (`uv.lock`). This will also install `redplanet` in editable mode (corresponding to `pip install -e .`), so you can make changes to the code and see them reflected immediately. If `.venv/` doesn't exist, it will be created.


&nbsp;

---

---
## [2] How to Modify/Contribute Code

We assume you've followed the steps above to set up your development environment.

---
### [2.1] Experienced Users

For experienced users, here's a quick guide:

- Please make all changes on the `develop` branch.
- Ensure all tests are passing locally (`just test`) and in the GitHub Actions of your forked repository upon pushing.
- Make a pull request to the `develop` branch of the main repository.

&nbsp;

---
### [2.2] Beginners

For beginners, here's a step-by-step guide:

1. Fork the repository.
    1. Sign into your GitHub account, go to our repository, and click the ["Fork"](https://github.com/Humboldt-Penguin/redplanet/fork){target="_blank"} button in the top right corner.
    2. On your local machine, `git clone ...` your forked repository. Enter the repository with `cd redplanet`.
2. Make changes on the `develop` branch.
    1. By default you are on the `main` branch, which reflects the latest stable release. Switch to the development branch with `git checkout develop`, which contains the latest development changes.
    2. Create a new branch for your changes with `git checkout -b your-contribution-name`.
    3. Implement and commit your changes.
        - We encourage you to use [Conventional Commit Messages](https://www.conventionalcommits.org/){target="_blank"} (cheatsheets: [\[1\]](https://gist.github.com/Zekfad/f51cb06ac76e2457f11c80ed705c95a3){target="_blank"}, [\[2\]](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13){target="_blank"}) for best practices/standardization, although it's not required.
    4. Ensure all tests are still passing with `just test`.
    5. Push your changes to your fork with `git push origin your-contribution-name`. See the "Actions" tab on your forked repository to see if tests are passing on all python versions and platforms.
3. When your changes are ready to be incorporated into the main repository, make a pull request.
    1. Go to your forked repository on GitHub and click the "New pull request" button.
    2. Describe what you changed and why.
    3. Submit the pull request.
    4. We will review your changes and provide feedback if necessary.
