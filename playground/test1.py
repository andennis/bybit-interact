import logging
from pybit.unified_trading import HTTP
from bybit import Bybit
from bybit_types import TradePair

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# Test
API_KEY = ""
API_SECRET = ""

bybit = Bybit(api_key=API_KEY, api_secret=API_SECRET)


def get_orderbook(category: str, cr_pair: str):
    session = HTTP(
        testnet=True,
        api_key=API_KEY,
        api_secret=API_SECRET,
    )
    return session.get_orderbook(category=category, symbol=cr_pair, limit=1)


if __name__ == '__main__':
    # res = get_orderbook("linear", "TONUSDT")
    # result = res["result"]
    # print("----- Asks -------")
    # for ask in reversed(result["a"]):
    #     print(ask)
    #
    # print("----- Bids -------")
    # for ask in result["b"]:
    #     print(ask)
    res = bybit.trade.derivatives.get_current_price(trade_pair=TradePair.TON_USDT)
    print(res)
