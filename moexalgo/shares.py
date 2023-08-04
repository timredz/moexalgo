import pandas

from moexalgo import session
from moexalgo.session import Session
from moexalgo.tickers import _Ticker
from moexalgo.models.common import OrderBookItem
from moexalgo.utils import result_deserializer, is_interactive


class Share(_Ticker):
    """ Акция
    """
    _PATH = 'engines/stock/markets/shares'

    def info(self, *fields: str):
        fields = fields or ['SHORTNAME', 'LOTSIZE', 'STATUS', 'DECIMALS', 'MINSTEP',
                            'ISSUESIZE', 'ISIN', 'LATNAME', 'CURRENCYID', 'SECTYPE', 'LISTLEVEL']
        return super().info(*fields)

    def orderbook(self, cs: Session = None):
        """ Текущий стакан лучших цен, список элементов или `pandas.DataFrame` """
        with Session((cs or session.default)._client) as client:
            items = client.get_objects(self._PATH, f'boards/{self.boardid}/securities/{self.secid}/orderbook',
                                       lambda data: result_deserializer(data, 'orderbook'))
            if is_interactive():
                return pandas.DataFrame([dict((name, value) for name, value in order.items())
                                         for order in reversed(items['orderbook'])])
            return [OrderBookItem(**dict((name.lower(), value) for name, value in order.items()))
                    for order in reversed(items['orderbook'])]


def get(name: str) -> Share:
    return Share(name)
