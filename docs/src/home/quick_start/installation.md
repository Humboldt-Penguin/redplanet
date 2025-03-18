## [1] System Requirements

RedPlanet is supported on the following platforms, as verified by our [tests via GitHub Actions](https://github.com/Humboldt-Penguin/redplanet/actions/workflows/test.yml){target="_blank"}:

- ^^Operating Systems^^ — Linux, MacOS, and Windows
- ^^Python Version^^ — 3.10 to 3.12
    - We plan to add support for 3.13 once [pyshtools is updated](https://github.com/SHTOOLS/SHTOOLS/pull/500){target="_blank"}.
    - To see the official support timeline for all versions of Python, look [here](https://devguide.python.org/versions){target="_blank"} or [here](https://endoflife.date/python){target="_blank"}.

Feel free to send an email or open an issue on GitHub if you're having installation issues or want to request support for earlier versions of Python. It might only take a few minutes to add compatibility.



&nbsp;

---

---
## [2] Installation

For beginners, I wrote a [Python Installation Guide](../../tutorials/install_python.md){target="_blank"} to explain the concepts, steps, and suggested tools for installing Python and packages *([relevant xkcd](https://www.explainxkcd.com/wiki/index.php/1987:_Python_Environment){target="_blank"})*.

&nbsp;

Past that, install from [PyPI](https://pypi.org/project/redplanet/){target="_blank"} with `pip install redplanet`.

We'd be happy to upload to conda-forge if anyone requests — feel free to send an email or open an issue on GitHub.



&nbsp;

---

---
## [3] Dependencies

<!-- format inspired by: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#dependencies -->

??? info ""Installation Size""

    <!-- We provide an estimated size for each package for convenience (low: < 5MB, medium: 5-50MB, high: > 50MB). However, please note these are ^^rough estimates^^ and can vary based on your system and the specific dependencies required. -->

    For convenience, we provide an estimated size for each package — these are ^^ROUGH ESTIMATES^^ and can vary wildly based on your system and combinations of dependency groups (e.g. `pyshtools` requires `scipy`, so we can't remove the latter without removing the former):

    - ^^Low^^: < 5MB
    - ^^Medium^^: 5-50MB
    - ^^High^^: > 50MB

    For reference, installing ALL dependencies *(including developer dependencies, which normal users will never need)* in a fresh Python environment takes ~1GB.

---
### [3.1] Required Dependencies

Included in `pip install redplanet`

<!-- TODO: Consider reorganizing in order of importance??? -->

| Package                                                                      | Purpose                                                      | Minimum Version | Installed Size |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------ | --------------- | -------------- |
| [numpy](https://pypi.org/project/numpy){target="_blank"}                     | Essential numerical computing                                | 2.1.1           | High           |
| [pyshtools](https://pypi.org/project/pyshtools){target="_blank"}             | Spherical harmonic operations (moho & magnetic field)        | 4.13.1          | Medium         |
| [pandas](https://pypi.org/project/pandas){target="_blank"}                   | Tabular/2D data (GRS & magnetic source depths)               | 2.2.2           | High           |
| [python-calamine](https://pypi.org/project/python-calamine){target="_blank"} | Excel file parsing (engine for pandas)                       | 0.3.1           | Low            |
| [cartopy](https://pypi.org/project/cartopy){target="_blank"}                 | Defining the Martian ellipsoid and solving geodesic problems | 0.24.1          | Medium         |
| [scipy](https://pypi.org/project/scipy){target="_blank"}                     | Scientific computing algorithms                              | 1.14.1          | High           |
| [xarray](https://pypi.org/project/xarray){target="_blank"}                   | Multi-dimensional data handling                              | 2024.9.0        | Medium         |
| [xxhash](https://pypi.org/project/xxhash){target="_blank"}                   | Fast hashing for data validation                             | 3.5.0           | Low            |


&nbsp;

---
### [3.2] Optional Dependencies

For specific features, you'll need to install additional packages.

&nbsp;

#### [3.2.1] Interactive/Plotting (recommended)

`pip install "redplanet[interactive]"`

| Package                                                            | Purpose                                 | Minimum Version | Installed Size |
| ------------------------------------------------------------------ | --------------------------------------- | --------------- | -------------- |
| [jupyter](https://pypi.org/project/jupyter){target="_blank"}       | Interactive notebooks, extremely useful | 1.1.1           | High           |
| [matplotlib](https://pypi.org/project/matplotlib){target="_blank"} | Static 2D plots                         | 3.9.2           | Medium         |
| [plotly](https://pypi.org/project/plotly){target="_blank"}         | Interactive 2D/3D plots                 | 5.24.1          | Medium         |

#### [3.2.2] Reproduce Datasets

`pip install "redplanet[generate-datasets]"`

| Package                                                          | Purpose                                               | Minimum Version | Installed Size |
| ---------------------------------------------------------------- | ----------------------------------------------------- | --------------- | -------------- |
| [dask](https://pypi.org/project/dask){target="_blank"}           | Parallel computing (large DEM datasets)               | 2024.9.0        | Medium         |
| [rioxarray](https://pypi.org/project/rioxarray){target="_blank"} | Geospatial raster processing (reprojecting DEM maps)  | 0.17.0          | Medium         |
| [zarr](https://pypi.org/project/zarr){target="_blank"}           | Chunked/compressed array storage (large DEM datasets) | 2.18.3          | Low            |


&nbsp;

---

Note: you can install both sets of optional dependencies with a single command: `pip install "redplanet[interactive,generate-datasets]"`.
