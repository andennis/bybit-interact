from bybit import Bybit


def test_derivatives():
    bybit = Bybit()
    assert bybit.trade.derivatives
    assert bybit.trade.derivatives.session
    assert bybit.trade.derivatives.session == bybit._http_session
