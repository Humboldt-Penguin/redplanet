import pytest
import numpy as np

from redplanet import Craters



def test_getall():
    x = Craters.get()
    assert len(x) == 2072
    assert len(x[0]) == 22


def test_getall_as_df():
    x = Craters.get(as_df=True)
    assert x.shape == (2072, 22)


def test_getall_confirm_range():
    x = Craters.get()
    y = Craters.get(
        lon = [-180, 180],
        lat = [-90, 90],
        diameter = [0,9999],
    )
    z = Craters.get(
        lon = [0, 360],
        lat = [-90, 90],
        diameter = [0,9999],
    )
    assert x == y == z


def test_get_filtered():
    x = Craters.get(
        lon = [-30, 0],
        lat = [0, 30],
        diameter = [100,200],
    )
    assert len(x) == 9


def test_get_aged():
    x = Craters.get(
        has_age = True,
    )
    assert len(x) == 73


def test_get_named():
    x = Craters.get(name=['Copernicus', 'Henry'])
    assert len(x) == 2
