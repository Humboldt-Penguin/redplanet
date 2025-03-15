import pytest
import numpy as np

from redplanet import Craters



def test_getall():
    assert Craters.get().shape == (2072, 22)


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

def test_get_asdict():
    d = Craters.get(
        name    = 'Henry',
        as_dict = True,
    )
    assert len(d) == 1
    assert d[0].get('id') == '10-0-003901'

    d = Craters.get(
        name    = ['Copernicus', 'Henry'],
        as_dict = True,
    )
    assert len(d) == 2
    assert d[0].get('id') == '04-1-001446'
    assert d[1].get('id') == '10-0-003901'
