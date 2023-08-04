import moexalgo.session

moexalgo.session.USE_HTTPS = False

from moexalgo import Market, Ticker, Index, Share

eq = Market('EQ')
print(eq)

moex = Ticker('MOEX')
print(moex)

for item in moex.orderbook():
    print(item)

for item in moex.candles('2023-01-01', limit=10000):
    print(item)