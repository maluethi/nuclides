import pytest

@pytest.fixture
def response():
    pass

def test_get_name(response):
    from nuclides.util import _get_name

    res = _get_name(92)
    assert res == 'U'

    with pytest.raises(ValueError, match=r'1000*'):
        res = _get_name(1000)

    with pytest.raises(ValueError, match=r'-1*'):
        res = _get_name(-1)


def test_get_Z(response):
    from nuclides.util import _get_Z

    res = _get_Z('U')
    assert res == 92

    with pytest.raises(ValueError, match=r'rop*'):
        res = _get_Z('rop')

    with pytest.raises(ValueError, match=r'12*'):
        res = _get_Z(12)


def test_check_N(response):
    from nuclides.util import _check_N_exists

    res = _check_N_exists(22, name='Ti')
    assert res == True

    res = _check_N_exists(22, Z=92)
    assert res == False

    with pytest.raises(ValueError, match=r'Not*'):
        res = _check_N_exists(12)


def test_get_nuc_info(response):
    from nuclides.util import _get_nuc_info

    res = _get_nuc_info(75, 110)
    assert res['stable'] == True
