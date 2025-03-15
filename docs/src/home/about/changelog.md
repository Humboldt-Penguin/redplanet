TODO

---

# Roadmap/todo (maybe move this elsewhere?)

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

---

# Explaining Versioning Scheme

RedPlanet uses a modified version of [Semantic Versioning](https://semver.org/){target="_blank"}.

??? note "*Why modify SemVer?*"

    In short, we find the "major" category is too broad.

    For example, under SemVer, both of the following changes would be considered "major" (i.e. breaking changes, not backwards compatible):

    1. Consider the return type of the function `Crust.topo.get(lon, lat)` when both inputs are floats, e.g. `x = Crust.topo.get(lon=0, lat=0)`.
        - Currently, the return type is a singleton numpy array (i.e. `type(x) == np.ndarray`, and `x.ndim == 0`).
        - In an update, the return type is changed to a float value (i.e. `type(x) == float`), which is the result of calling `.item()` on the output of the previous case. This will only affect a subset of users, and the fix for them would be trivial.
    2. An update redesigns the package so `Crust.topo` is no longer a valid namespace and the new "topography" module uses a different dataset and accessing function. Users will have to completely rewrite/rethink their usage.

    We want a way for users to differentiate between these two cases. Thus we introduce the `epoch` category which is better suited for example 2 above.

Our versions are in the format `epoch.major.minor-patch` (`#.#.#-@`), where:

- `patch` (letter) indicates a bug fix, performance improvement, dependency update, and/or cosmetic change with no changes to observed inputs/outputs.
    - e.g. `x.x.x` -> `x.x.x-a`; or `x.x.x-a` -> `x.x.x-b`
    - => You can update patches without much thought.
- `minor` (number) indicates a new feature that IS backwards compatible.
    - e.g. `x.x.1-b` -> `x.x.2`
    - => You can update minor versions without much thought. Additionally, check the changelog for new features that may enhance your workflow.
- `major` (number) indicates a breaking change that is NOT backwards compatible.
    - e.g. `x.1.2-c` -> `x.2.0`
    - => Check for new features/improvements, and if you'd like to use them, you may need to update your code.
- `epoch` (number) draws a user's attention to a notable/significant change, such as a complete rewrite or a change in the underlying philosophy of the package.
    - e.g. `1.2.3-d` -> `2.0.0`
    - => Older epochs might become depracated. If you see a new epoch is available, you should read the release notes even if your code is running fine and you have no need to upgrade. We try to bump epochs only when absolutely necessary, such as being forced to migrate dataset download links to a new host.

---

# Changelog

...


self note:

- Take inspiration from the following:
    - [mihon](https://mihon.app/changelogs/) (this is much more comprehensible)
    - [shtools](https://shtools.github.io/SHTOOLS/release-notes-v4.html)
    - [uv (but this is only on github) — but tbh, i don't really love these...? it's always been a bit confusing to parse](https://github.com/astral-sh/uv/blob/main/CHANGELOG.md)
