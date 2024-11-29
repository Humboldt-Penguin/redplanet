import pytest
import numpy as np

from redplanet import Craters



def test_getall():
    df = Craters.get()
    assert df.shape[0] == 2072
    assert df.equals(Craters.get_dataset())


def test_getall_with_params():
    df = Craters.get(
        lon      = [-180,180],
        lat      = [-90,90],
        diameter = [0,9999],
    )
    assert df.shape[0] == 2072


def test_getall_with_params_plon():
    df = Craters.get(
        lon      = [0,360],
        lat      = [-90,90],
        diameter = [0,9999],
    )
    assert df.shape[0] == 2072


def test_get_filtered():
    df = Craters.get(
        lon      = [-60,60],
        lat      = [-30,30],
        diameter = [100,200],
    )
    assert df.shape[0] == 64


def test_get_aged():
    df = Craters.get(has_age=True)
    assert df.shape[0] == 73


def test_get_named():
    df = Craters.get(name=['Copernicus', 'Henry'])
    assert df.shape[0] == 2
