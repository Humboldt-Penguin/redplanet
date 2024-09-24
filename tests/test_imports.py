from importlib import import_module
from importlib.metadata import version
import pytest

# Dictionary declaring all dependency groups and their packages
dependencies = {
    'Dependencies: required': [
        'dask',
        'numpy',
        'pandas',
        'pyshtools',
        'scipy',
        'xarray',
        'xxhash',
        'zarr',
    ],
    'Dependencies: "crs" (optional)': [
        'rioxarray',
    ],
    'Dependencies: "plot" (optional)': [
        'matplotlib',
        'plotly',
    ],
    'Dependencies: "dev" (optional)': [
        'jupyter',
    ],
}

def test_import_dependencies():
    for group_name, packages in dependencies.items():
        print(f'\n\t- {group_name}')
        for package in packages:
            try:
                imported_package = import_module(package)
                print(f'\t\t> {package} = {version(package)}')
            except ImportError:
                print(f'\t\t> {package} = NOT AVAILABLE')