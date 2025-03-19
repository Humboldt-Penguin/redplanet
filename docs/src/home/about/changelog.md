## [1] Planned Features

- Breaking changes
    - (None currently planned)
- Major features
    - [ ] Plotting (with hillshade background...?)
    - [ ] Add MAVEN magnetometer module
- Minor changes/updates
    - [ ] Update crater database with new [IAU additions](https://planetarynames.wr.usgs.gov/SearchResults?Target=20_Mars&Feature%20Type=9_Crater,%20craters){target="_blank"}
        - Redplanet currently uses a database up to 2024-11-26 with 1218 craters -- as of 2025-02-27, there are 1231 craters (13 additions).
- Software/implementation changes
    - [ ] Publish to conda forge ([tutorial](https://www.pyopensci.org/python-package-guide/tutorials/publish-conda-forge.html#how-to-publish-your-package-on-conda-forge))
    - [ ] Add GitHub actions for CI/CD
        - Specifically, GH actions for [running tests with uv](https://docs.astral.sh/uv/guides/integration/github/#syncing-and-running), and [publishing the site](https://squidfunk.github.io/mkdocs-material/publishing-your-site/#with-github-actions) (see justfile for more specific commands!)
    - [ ] Switch from `pandas` to `polars` to save a lot of space and slight performance improvements (move pandas to optional dependecy group)
    - [ ] Change all `loader` modules so they have an additional semi-private method which returns the respective `GriddedData` object, which is then assigned to the global variable by the `load()`/`load(...)`/`_load()` method. This is more clean and extensible in edge cases, e.g. `Crust.moho` wants the pysh topo model to make a crthick model (kind of).
    - [ ] Move `DatasetManager` to `redplanet.helper_functions`?


&nbsp;

---
## [2] Changelog

RedPlanet follows the [Semantic Versioning](https://semver.org/){target="_blank"} standard. In short, this means that version numbers follow the pattern `MAJOR.MINOR.PATCH`, where `MAJOR` is incremented for breaking changes (i.e. not backwards compatible), `MINOR` is incremented for new features, and `PATCH` is incremented for bug fixes.


??? info "Complete rewrite in 2024 September & deleting v1.0.0"

    I completely rewrote this project in 2024 September, erasing the entire git history and restarting from scratch. On PyPI, I deleted the only version which which was ever published (v1.0.0), so it's impossible to download now (as opposed to "yanking" which would allow for downloading if the exact version were accidentally requested). An archive of the old repo is available here: https://github.com/Humboldt-Penguin/redplanet_archive-240910


&nbsp;

---

self note:

- Take inspiration from the following:
    - [mihon](https://mihon.app/changelogs/) (this is much more comprehensible)
    - [shtools](https://shtools.github.io/SHTOOLS/release-notes-v4.html)
    - [uv (but this is only on github) — but tbh, i don't really love these...? it's always been a bit confusing to parse](https://github.com/astral-sh/uv/blob/main/CHANGELOG.md)
