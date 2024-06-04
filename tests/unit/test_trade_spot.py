from bybit import Bybit
from bybit_types import Market
from trade_spot import TradeSpot


def test_spot(bybit: Bybit):
    assert bybit.trade
    assert bybit.trade.spot
    assert isinstance(bybit.trade.spot, TradeSpot)
    assert bybit.trade.spot.market == Market.SPOT
    assert bybit.trade.spot.session
    assert bybit.trade.spot.config
