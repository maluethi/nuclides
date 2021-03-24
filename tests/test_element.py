import pytest

@pytest.fixture
def response():
    pass

def test_element_creation(response):
    from nuclides import Element

    Ti = Element('Ti')
    assert (Ti.name == 'Ti')
    assert (Ti.n_nuclides == 27)

    #assert (len(Ti.isomers) == 12)

    Ti2 = Element(Ti.Z)
    assert (Ti2.name == 'Ti')

    with pytest.raises(ValueError, match=r'XX'):
        Element('XX')

    with pytest.raises(ValueError, match=r'1234'):
        Element(1234)
