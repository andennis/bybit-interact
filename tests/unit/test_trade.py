from bybit import Bybit
from bybit_types import Market


def test_derivatives():
    bybit = Bybit()
    assert bybit.trade.derivatives
    assert bybit.trade.derivatives.session
    assert bybit.trade.derivatives.session == bybit._http_session
    assert bybit.trade.derivatives.market == Market.LINEAR


def test_spot():
    bybit = Bybit()
    assert bybit.trade.spot
    assert bybit.trade.spot.session
    assert bybit.trade.spot.session == bybit._http_session
    assert bybit.trade.spot.market == Market.SPOT
