from __future__ import annotations

import re
import weakref
from datetime import date

from moexalgo import session
from moexalgo.market import Market
from moexalgo.models.common import Candle
from moexalgo.session import Session
from moexalgo.utils import is_interactive, pandas, result_deserializer


class _Ticker:
    """ Инструмент
    """
    _PATH = 'API main path part, must be defined in superclasses'

    secid: str
    boardid: str

    def __new__(cls, secid: str, boardid: str = None):
        if boardid is None:
            secid, *args = re.split('\W', secid)
            if args:
                boardid = args[0]
        market = Market(cls._PATH.split('/')[-1], boardid)
        if market.ticker_info(secid):
            inst = super().__new__(cls)
            inst.secid = secid
            inst.boardid = market.boardid
            inst._r_market = weakref.ref(market)
            return inst
        raise LookupError(f"Cannot found ticker: ({secid}, {boardid or ''})")

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.secid}/{self.boardid}')"

    @property
    def market(self):
        """ Раздел рынка в который входит инструмент """
        return self._r_market()

    def info(self, *fields, cs: Session = None):
        """ Возвращает информацию об инструменте, словарь или `pandas.DataFrame` """
        if self.market:
            if info := self.market.ticker_info(self.secid):
                if securities := info.get('securities'):
                    fields = fields or tuple(self.market._fields['securities'].keys())
                    titles = self.market._fields['securities']
                    index, title, value = zip(*[(name, titles[name]['title'], value)
                                                for name, value in securities.items() if name in fields])
                    if is_interactive():
                        return pandas.DataFrame(index=index, data=dict(title=title, value=value))
                    else:
                        return dict(zip(index, value))

    def candles(self, from_date: str | date, till_date: str | date = None, interval=60,
                offset=0, limit=500, cs: Session = None):
        """ Возвращает итератор или `pandas.DataFrame` свечей инструмента по заданным параметрам.

        Args:
            from_date: Дата начала диапазона выдачи данных
            till_date: Дата конца диапазона выдачи данных
            interval: Интервал в минутах 1, 10, 60
            offset: Начальная позиция в последовательности записей
            limit: Максимальное количество записей в результате
            cs: Клиентская сессия
        Returns:
            Объекты типа `Candles`
        """
        assert interval in (1, 10, 60), f"Interval {interval}m not implemented"
        from_date = date.fromisoformat(from_date) if isinstance(from_date, str) else from_date
        till_date = date.fromisoformat(till_date) if isinstance(till_date, str) else till_date
        options = dict(**{'from': from_date.isoformat()}, interval=interval)
        if till_date:
            options['till'] = till_date.isoformat()

        def candles_gen():
            start = offset
            with Session((cs or session.default)._client) as client:
                while True:
                    options['start'] = start
                    items = client.get_objects(self._PATH, f'boards/{self.boardid}/securities/{self.secid}/candles',
                                               lambda data: result_deserializer(data, 'candles'), **options)
                    if candles := items.get('candles'):
                        for item in candles:
                            yield item
                            start += 1
                            if start >= offset + limit:
                                return
                    else:
                        return

        def normalized_gen():
            for item in candles_gen():
                yield Candle(**dict((name.lower(), value) for name, value in item.items()))

        if is_interactive():
            return pandas.DataFrame([candle for candle in candles_gen()])
        return normalized_gen()
