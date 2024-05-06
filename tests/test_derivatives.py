from bybit import Bybit
from bybit_types import TradePair

# Test
API_KEY = ""
API_SECRET = ""


def test_buy_limit():
    bybit = Bybit(api_key=API_KEY, api_secret=API_SECRET, testnet=True)
    result = bybit.trade.derivatives.buy_limit(TradePair.TON_USDT, 1, 5.86)
    assert result
    assert result.retCode == 0


def test_sell_limit():
    bybit = Bybit(api_key=API_KEY, api_secret=API_SECRET, testnet=True)
    result = bybit.trade.derivatives.sell_limit(TradePair.TON_USDT, 1, 5.81)
    assert result
    assert result.retCode == 0
