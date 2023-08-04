from dataclasses import dataclass
from datetime import datetime, date, time
from decimal import Decimal


@dataclass
class Securities:
    """ Элемент блока данных `securities`
    """
    name: str
    decimals: int
    shortname: str
    annualhigh: Decimal
    annuallow: Decimal
    currencyid: str
    calcmode: str


@dataclass
class MarketData:
    """ Элемент блока данных `marketdata`
    """
    lastvalue: Decimal
    openvalue: Decimal
    currentvalue: Decimal
    lastchange: Decimal
    lastchangetoopenprc: Decimal
    lastchangetoopen: Decimal
    updatetime: time
    lastchangeprc: Decimal
    valtoday: Decimal
    monthchangeprc: Decimal
    yearchangeprc: Decimal
    seqnum: int
    systime: datetime
    time: time
    valtoday_usd: Decimal
    lastchangebp: Decimal
    monthchangebp: Decimal
    yearchangebp: Decimal
    capitalization: Decimal
    capitalization_usd: Decimal
    high: Decimal
    low: Decimal
    tradedate: date
    tradingsession: str
    voltoday: Decimal
