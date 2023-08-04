import pytest
from moexalgo import Market


def test_markets_creation():
    eq = Market('EQ')
    assert eq == Market('EQ')
    assert eq == Market('shares')
    assert eq == Market('shares/TQBR')
    assert eq == Market('shares', 'TQBR')
    index = Market('index')
    assert index != eq
    assert index == Market('index', 'SNDX')


if __name__ == '__main__':
    pytest.main()
