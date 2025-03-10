import pytest

from redplanet import Crust



def test_substitute_docstrings():
    ## direct substitutions
    assert 'Get the underlying dataset' in Crust.topo.get_dataset.__doc__

    ## citations (read from bib file)
    assert 'Goddard Space Flight Center' in Crust.topo.load.__doc__

    ## multiple
    assert '{' not in Crust.topo.get.__doc__
