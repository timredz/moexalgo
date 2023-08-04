from dataclasses import dataclass
from datetime import time, datetime


@dataclass
class OrderBookItem:
    """ Активные заявки """
    secid: str
    boardid: str
    buysell: str
    price: float
    quantity: int
    seqnum: int
    updatetime: time
    decimals: int


@dataclass
class Candle:
    """ Свеча """
    open: float
    close: float
    high: float
    low: float
    value: float
    volume: int
    begin: datetime
    end: datetime
