import pytest
from moexalgo import Market, Ticker, Share, Index
from moexalgo.models.common import Candle


def test_tickers_creation():
    eq = Market('EQ')
    moex = Ticker('MOEX')
    assert isinstance(moex, Share)
    assert moex.boardid == eq.boardid == 'TQBR'
    assert moex.market == eq

    ndx = Market('index')
    imoex = Ticker('IMOEX')
    assert isinstance(imoex, Index)
    assert imoex.boardid == ndx.boardid == 'SNDX'
    assert imoex.market == ndx


def test_tickers_iter():
    moex = Ticker('MOEX')
    assert isinstance(moex.orderbook(), list)
    it = moex.candles('2020-01-01', limit=100)
    assert isinstance(next(it), Candle)
    assert len([item for item in it]) == 99


if __name__ == '__main__':
    pytest.main()
