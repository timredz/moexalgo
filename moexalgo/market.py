from __future__ import annotations

import re

from moexalgo import session
from moexalgo.session import Session
from moexalgo.utils import result_deserializer, is_interactive, pandas

_AVAILABLE = {'index': dict(), 'shares': dict()}
_ALIASES = {
    'index': ('index', 'SNDX'),
    'shares': ('shares', 'TQBR'),
    'EQ': ('shares', 'TQBR'),
}


def market_for(secid: str, boardid: str, cs: Session = None):
    for _, boards in _AVAILABLE.items():
        if market := boards.get(boardid):
            if market.securities_for(secid, cs):
                return market


class Market:
    """ Раздел биржевого рынока
    """
    name: str
    boardid: str
    _fields: dict[str, dict[str, dict]] = None
    _values: dict[str, dict[str, dict]] = None

    def __new__(cls, name: str, boardid: str = None):
        if boardid is None:
            name_, boardid = _ALIASES.get(name, (None, None))
            if boardid is not None:
                name = name_
            else:
                name, *args = re.split('\W', name)
                if args:
                    boardid = args[0]
        if name not in _AVAILABLE:
            raise NotImplementedError(f"Market {name} is not supported")
        market = _AVAILABLE.setdefault(name, dict())
        if boardid not in market:
            market[boardid] = super().__new__(cls)
            market[boardid].name = name
            market[boardid].boardid = boardid
        return market[boardid]

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}/{self.boardid}')"

    def _ensure_loaded(self, cs: Session = None):
        if self._fields is None or self._values is None:
            with Session((cs or session.default)._client) as client:
                self._fields = client.get_objects(
                    'engines/stock/markets', f'{self.name}/boards/{self.boardid}/securities/columns',
                    lambda data: result_deserializer(data, key=lambda item: item['name']))
                self._values = client.get_objects(
                    'engines/stock/markets', f'{self.name}/boards/{self.boardid}/securities/',
                    lambda data: result_deserializer(data, key=lambda item: item['SECID']))

    def ticker_info(self, secid: str, cs: Session = None):
        """ Информация о заданном инструменте """
        self._ensure_loaded(cs)
        marketdata = self._values['marketdata'].get(secid)
        securities = self._values['securities'].get(secid)
        if securities or marketdata:
            return dict(securities=securities, marketdata=marketdata)

    def securities(self, cs: Session = None):
        """ Справочная информация всех инструментах рынка """
        self._ensure_loaded(cs)
        if is_interactive():
            return pandas.DataFrame(self._values['securities'].values())
        else:
            return list(self._values['securities'].values())

    def marketdata(self, cs: Session = None):
        """ Статистическая информация всех инструментах рынка """
        self._ensure_loaded(cs)
        if is_interactive():
            return pandas.DataFrame(self._values['marketdata'].values())
        else:
            return list(self._values['marketdata'].values())

    tickers = securities
    stats = marketdata
