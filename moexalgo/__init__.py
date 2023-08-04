from __future__ import annotations

import re

from .market import Market
from .indices import Index
from .shares import Share


def Ticker(secid: str, boardid: str = None) -> Index | Share:
    """ Резолвер тикера """
    if boardid is None:
        secid, *args = re.split('\W', secid)
        if args:
            boardid = args[0]
    shares = Market('shares', boardid)
    if shares.ticker_info(secid):
        return Share(secid, shares.boardid)
    indices = Market('index', boardid)
    if indices.ticker_info(secid):
        return Index(secid, indices.boardid)
    raise LookupError(f"Cannot found ticker: `{secid}`")
