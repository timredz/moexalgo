from dataclasses import dataclass
from datetime import datetime, date, time
from decimal import Decimal


@dataclass
class Securities:
    """ Элемент блока данных `securities`
    """
    shortname: str  #
    prevprice: Decimal
    lotsize: int  #
    facevalue: Decimal
    status: str  #
    boardname: str
    decimals: int  #
    secname: Decimal
    remarks: str
    marketcode: str
    instrid: str
    sectorid: str
    minstep: Decimal  #
    prevwaprice: Decimal
    faceunit: str
    prevdate: date
    issuesize: int  #
    isin: str  #
    latname: str  #
    regnumber: str
    prevlegalcloseprice: Decimal
    currencyid: str  #
    sectype: str  #
    listlevel: int  #
    settledate: date


@dataclass
class MarketData:
    """ Элемент блока данных `marketdata`
    """
    bid: Decimal
    biddepth: int
    offer: Decimal
    offerdepth: int
    spread: Decimal
    biddeptht: int
    offerdeptht: int
    open: Decimal
    low: Decimal
    high: Decimal
    last: Decimal
    lastchange: Decimal
    lastchangeprcnt: Decimal
    qty: int
    value: Decimal
    value_usd: Decimal
    waprice: Decimal
    lastcngtolastwaprice: Decimal
    waptoprevwapriceprcnt: Decimal
    waptoprevwaprice: Decimal
    closeprice: Decimal
    marketpricetoday: Decimal
    marketprice: Decimal
    lasttoprevprice: Decimal
    numtrades: int
    voltoday: int
    valtoday: int
    valtoday_usd: int
    etfsettleprice: Decimal
    tradingstatus: str
    updatetime: time
    lastbid: Decimal
    lastoffer: Decimal
    lcloseprice: Decimal
    lcurrentprice: Decimal
    marketprice2: Decimal
    numbids: int
    numoffers: int
    change: Decimal
    time: time
    highbid: Decimal
    lowoffer: Decimal
    priceminusprevwaprice: Decimal
    openperiodprice: Decimal
    seqnum: int
    systime: datetime
    closingauctionprice: Decimal
    closingauctionvolume: Decimal
    issuecapitalization: Decimal
    issuecapitalization_updatetime: time
    etfsettlecurrency: str
    valtoday_rur: int
    tradingsession: str