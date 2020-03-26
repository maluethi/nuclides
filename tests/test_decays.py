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


def test_decay_range(response):
    from nuclides.decays import Alpha

    for br in [-1, 0., 2.]:
        with pytest.raises(ValueError, match=r'Branching*'):
            Alpha(half_life=1, branching_ratio=br)

    for hl in [-1000, 0]:
        with pytest.raises(ValueError, match=r'Half*'):
            Alpha(half_life=hl, branching_ratio=0.5)


def test_decay_logic(response):
    from nuclides.decays import Alpha

    with pytest.raises(ValueError, match=r'Branching*'):
        Alpha(half_life=1)

    with pytest.raises(ValueError, match=r'Half*'):
        Alpha(branching_ratio=0.2)


def test_alpha(response):
    from nuclides.decays import Alpha

    a = Alpha(half_life=2, branching_ratio=0.5)

    assert a.dN == -2
    assert a.dZ == -2


def test_beta(response):
    from nuclides.decays import BetaMinus, BetaPlus

    bm = BetaMinus(half_life=2, branching_ratio=0.5)
    assert bm.dZ == 1
    assert bm.dN == -1

    bp = BetaPlus(half_life=2, branching_ratio=0.5)
    assert bp.dZ == -1
    assert bp.dN == 1


def test_proton_neutron(response):
    from nuclides.decays import NNeutronDecay, NProtonDecay

    nd = NProtonDecay(half_life=1, branching_ratio=0.1, n_protons=1)
    assert nd.dZ == -1
    assert nd.dN == 0
    assert nd.name == 'p'

    nd = NProtonDecay(half_life=1, branching_ratio=0.1, n_protons=2)
    assert nd.dZ == -2
    assert nd.dN == 0
    assert nd.name == '2p'

    pd = NNeutronDecay(half_life=1, branching_ratio=0.1, n_neutrons=1)
    assert pd.dZ == 0
    assert pd.dN == -1
    assert pd.name == 'n'

    pd = NNeutronDecay(half_life=1, branching_ratio=0.1, n_neutrons=2)
    assert pd.dZ == 0
    assert pd.dN == -2
    assert pd.name == '2n'


def test_Igamma(response):
    from nuclides.decays import Igamma

    meta = Igamma(half_life=2, branching_ratio=0.3)
    assert meta.dZ == 0
    assert meta.dN == 0


def test_mode_parser(response):
    from nuclides.decays import _dec_parser

    cases_betap = [' b+', 'b+', 'b+p', 'b+2p', 'b+3p', 'b+4p', 'b+a', 'b+d', 'b+pa', 'b+sf', '2b+']
    cases_betam = [' b-', 'b-', 'b-n', 'b-2n', 'b-3n', 'b-4n', 'b-a', 'b-d', 'b-pa', 'b-sf', '2b-', 'b-t']
    cases_e_ec_ep = ['e+', 'ec', 'ec+b+', 'is', 'it']
    cases_heavy = ['p', 'n', 'sf']

    for el in cases_betam + cases_betap:
        _dec_parser(el)

