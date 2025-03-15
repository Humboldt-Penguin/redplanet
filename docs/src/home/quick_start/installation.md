RedPlanet is currently officially supported for Python 3.10 to 3.12 (3.13 will be supported once [pyshtools updates](https://github.com/SHTOOLS/SHTOOLS/pull/500){target="_blank"}), and works on Linux, MacOS, and Windows (as verified by [our CI/CD tests](https://github.com/Humboldt-Penguin/redplanet/actions){target="_blank"}).

Send an email if you'd like to request support for earlier versions of Python, it might only take a few minutes to add compatibility.

To see the Python foundation's support status for all versions, look [here](https://devguide.python.org/versions){target="_blank"} or [here](https://endoflife.date/python){target="_blank"}.


&nbsp;

---
## [1] Experienced Users

Install from [PyPI](https://pypi.org/project/redplanet/){target="_blank"} with `pip install redplanet`.

We'd be happy to upload to conda-forge if anyone requests — feel free to [reach out directly](mailto:zain.eris.kamal@rutgers.edu) or [open an issue](https://github.com/Humboldt-Penguin/redplanet/issues/new){target="_blank"}.



&nbsp;

---
## [2] Beginners

If you've never installed a Python package before, we'll walk you through the steps and concepts.

### [2.1] bwaa

The standard tool for installing Python packages is `pip`, which downloads packages from the [Python Package Index (PyPI)](https://pypi.org/){target="_blank"}. To install `redplanet` from PyPI, run the following command:

```shell
pip install redplanet
pip install --upgrade redplanet  # to upgrade a pre-existing installation
```



&nbsp;

---

## [3] Dependencies

<!-- format inspired by: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#dependencies -->

??? info ""Installation Size""

    <!-- We provide an estimated size for each package for convenience (low: < 5MB, medium: 5-50MB, high: > 50MB). However, please note these are **rough estimates** and can vary based on your system and the specific dependencies required. -->

    For convenience, we provide an estimated size for each package — these are **ROUGH ESTIMATES** and can vary wildly based on your system and combinations of dependency groups (e.g. `pyshtools` requires `scipy`, so we can't remove the latter without removing the former):

    - **Low**: < 5MB
    - **Medium**: 5-50MB
    - **High**: > 50MB

    For reference, installing ALL dependencies *(including developer dependencies, which normal users will never need)* in a fresh Python environment takes ~1GB.


### [3.1] Required Dependencies

Included in `pip install redplanet`

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

### [3.2] Optional Dependencies

For specific features, you'll need to install additional packages.


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

Note: you can install both sets of optional dependencies with a single command: `pip install "redplanet[interactive,generate-datasets]"`.
