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


def test_nuclide_checks(response):
    from nuclides.nuclide import Nuclide
    from nuclides.decays import Alpha, BetaMinus

    dec1 = Alpha(10, 0.2)
    dec2 = BetaMinus(100, 0.7)
    dec3 = BetaMinus(1000, 0.2)

    with pytest.raises(ValueError, match=r'Total*'):
        Nuclide(name='MAL', Z=10, N=5, mass=10.1, decays=[dec3, dec2, dec1])

    with pytest.raises(ValueError, match=r'Nuclide*'):
        Nuclide(name='MAL', Z=10, N=5, mass=10.1, stable=True, decays=[dec3, dec2, dec1])

    with pytest.raises(ValueError, match=r'No*'):
        Nuclide(name='MAL', Z=10, N=5, mass=10.1, stable=False, decays=[])


def test_nuclide_gen(response):
    from nuclides.nuclide import Nuclide
    from nuclides.decays import Alpha, BetaMinus

    dec1 = Alpha(10, 0.2)
    dec2 = BetaMinus(100, 0.7)
    dec3 = BetaMinus(1000, 0.1)

    nuc = Nuclide(name='MAL', Z=10, N=5, mass=10.1, decays=[dec3, dec2, dec1])

    assert nuc.mass_defect == 10.1
    assert nuc.Z == 10
    assert nuc.N == 5
    assert nuc.name == 'MAL'

    # check sorting
    assert nuc.decays[0].half_life == 100
    assert nuc.decays[1].half_life == 10
    assert nuc.decays[2].half_life == 1000



