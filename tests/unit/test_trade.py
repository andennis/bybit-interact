from bybit import Bybit
from trade import Trade


def test_trade():
    bybit = Bybit()
    assert bybit.trade
    assert isinstance(bybit.trade, Trade)
