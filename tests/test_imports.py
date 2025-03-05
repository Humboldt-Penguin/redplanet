from importlib import import_module
from importlib.metadata import version
import pytest

# Dictionary declaring all dependency groups and their packages
dependencies = {
    'Dependencies: required': [
        'cartopy',
        'numpy',
        'pandas',
        'pyshtools',
        'python-calamine',
        'scipy',
        'xarray',
        'xxhash',
    ],
    'Dependencies (optional): "interactive"': [
        'jupyter',
        'matplotlib',
        'plotly',
    ],
    'Dependencies (optional): "generate-datasets"': [
        'dask',
        'rioxarray',
        'zarr',
    ],
}

def test__import_dependencies():
    for group_name, packages in dependencies.items():
        print(f'\n\t- {group_name}')
        for package in packages:
            try:
                imported_package = import_module(package)
                print(f'\t\t> {package} = {version(package)}')
            except ImportError:
                print(f'\t\t> {package} = NOT AVAILABLE')
