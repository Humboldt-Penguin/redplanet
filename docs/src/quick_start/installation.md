## Experienced Users

Install from [PyPI](https://pypi.org/project/redplanet/) with `pip install redplanet`.

We'd be happy to upload to conda-forge if anyone requests — feel free to [reach out directly](mailto:zain.eris.kamal@rutgers.edu) or [open an issue](https://github.com/Humboldt-Penguin/redplanet/issues/new).



&nbsp;

---
## Beginners

If you've never installed a Python package before, we'll walk you through the steps and concepts.

### bwaa

The standard tool for installing Python packages is `pip`, which downloads packages from the [Python Package Index (PyPI)](https://pypi.org/). To install `redplanet` from PyPI, run the following command:

```shell
pip install redplanet
pip install --upgrade redplanet  # to upgrade a pre-existing installation
```



&nbsp;

---

## Dependencies

<!-- inspired by: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#dependencies -->

??? info ""Installation Size""

    <!-- We provide an estimated size for each package for convenience (low: < 5MB, medium: 5-50MB, high: > 50MB). However, please note these are **rough estimates** and can vary based on your system and the specific dependencies required. -->

    For convenience, we provide an estimated size for each package — these are **ROUGH ESTIMATES** and can vary wildly based on your system and combinations of dependency groups:

    - **Low**: < 5MB
    - **Medium**: 5-50MB
    - **High**: > 50MB

    For reference, installing ALL dependencies *(including developer dependencies, which normal users will never need)* in a fresh Python environment takes ~1GB.


### Required Dependencies

Included in `pip install redplanet`

| Package                                                     | Purpose                                                      | Minimum Version | Installed Size |
| ----------------------------------------------------------- | ------------------------------------------------------------ | --------------- | -------------- |
| [numpy](https://pypi.org/project/numpy)                     | Essential numerical computing                                | 2.1.1           | High           |
| [pyshtools](https://pypi.org/project/pyshtools)             | Spherical harmonic operations (moho & magnetic field)        | 4.13.1          | Medium         |
| [pandas](https://pypi.org/project/pandas)                   | Tabular/2D data (GRS & magnetic source depths)               | 2.2.2           | High           |
| [python-calamine](https://pypi.org/project/python-calamine) | Excel file parsing (engine for pandas)                       | 0.3.1           | Low            |
| [cartopy](https://pypi.org/project/cartopy)                 | Defining the Martian ellipsoid and solving geodesic problems | 0.24.1          | Medium         |
| [scipy](https://pypi.org/project/scipy)                     | Scientific computing algorithms                              | 1.14.1          | High           |
| [xarray](https://pypi.org/project/xarray)                   | Multi-dimensional data handling                              | 2024.9.0        | Medium         |
| [xxhash](https://pypi.org/project/xxhash)                   | Fast hashing for data validation                             | 3.5.0           | Low            |


&nbsp;

### Optional Dependencies

For specific features, you'll need to install additional packages.


#### Interactive/Plotting (recommended)

`pip install "redplanet[interactive]"`

| Package                                           | Purpose                                 | Minimum Version | Installed Size |
| ------------------------------------------------- | --------------------------------------- | --------------- | -------------- |
| [jupyter](https://pypi.org/project/jupyter)       | Interactive notebooks, extremely useful | 1.1.1           | High           |
| [matplotlib](https://pypi.org/project/matplotlib) | Static 2D plots                         | 3.9.2           | Medium         |
| [plotly](https://pypi.org/project/plotly)         | Interactive 2D/3D plots                 | 5.24.1          | Medium         |


#### Reproduce Datasets

`pip install "redplanet[generate-datasets]"`

| Package                                         | Purpose                                               | Minimum Version | Installed Size |
| ----------------------------------------------- | ----------------------------------------------------- | --------------- | -------------- |
| [dask](https://pypi.org/project/dask)           | Parallel computing (large DEM datasets)               | 2024.9.0        | Medium         |
| [rioxarray](https://pypi.org/project/rioxarray) | Geospatial raster processing (reprojecting DEM maps)  | 0.17.0          | Medium         |
| [zarr](https://pypi.org/project/zarr)           | Chunked/compressed array storage (large DEM datasets) | 2.18.3          | Low            |


&nbsp;

Note: you can install both sets of optional dependencies with a single command: `pip install "redplanet[interactive,generate-datasets]"`.
