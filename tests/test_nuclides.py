#!/usr/bin/env python

"""Tests for `nuclides` package."""

import pytest


from nuclides import nuclides


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')



def test_nuclide_gen(response):
    from nuclides.nuclide import Nuclide

    nuc = Nuclide('Ti-48')
    assert nuc.Z == 22
    assert nuc.N == 26
    assert nuc.name == 'Ti'
    assert nuc.stable == True

    nuc = Nuclide('Ti48')
    assert nuc.N == 26
    assert nuc.name == 'Ti'

    nuc = Nuclide('48Ti')
    assert nuc.N == 26
    assert nuc.name == 'Ti'

    nuc = Nuclide(name='Ti', N=28)
    assert nuc.name == 'Ti'
    assert nuc.N == 28

    nuc = Nuclide(Z=92, N=123)
    assert nuc.name == 'U'
    assert nuc.Z == 92
    assert nuc.N == 123

    with pytest.raises(ValueError, match=r'does*'):
        nuc = Nuclide(Z=92, N=92)

    with pytest.raises(ValueError, match=r'exist*'):
        nuc = Nuclide(name='U', N=92)
