import logging

from pybit.unified_trading import HTTP
from bybit_types import Market, TradePair, TPSLProperties
from bybit import Bybit

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# Test
API_KEY = ""
API_SECRET = ""
# bybit = Bybit(api_key=API_KEY, api_secret=API_SECRET)

bybit = Bybit(testnet=True)
bybit.config._trade_pairs[TradePair.TON_USDT] = True


def place_order(category: Market, symbol: str, side: str, order_type: str, price: float, amount: int,
                take_profit: float = None, trigger_price: float = None):
    session = HTTP(
        testnet=True,
        api_key=API_KEY,
        api_secret=API_SECRET,
    )

    return session.place_order(
        category=category.value,
        symbol=symbol,
        side=side,  # "Buy",
        orderType=order_type,  # "Limit",
        qty=str(amount),
        price=str(price),
        triggerPrice=str(trigger_price),
        triggerDirection=2,
        positionIdx=1
        # tpslMode="Full",
        # tpOrderType="Market",
        # takeProfit=str(take_profit),
        # orderLinkId="andennis-test2",
    )


if __name__ == '__main__':
    # res = place_order(Market.LINEAR, "TONUSDT", "Sell", "Limit", 6.5, 12, trigger_price=6.5)
    # res = bybit.trade.derivatives.sell_limit(trade_pair=TradePair.TON_USDT, qty=3, price=5.7875)
    # res = bybit.trade.derivatives.buy_limit(trade_pair=TradePair.TON_USDT, qty=3, price=5.7815)
    # res = bybit.trade.derivatives.sell_limit(
    #     trade_pair=TradePair.TON_USDT,
    #     qty=3,
    #     price=5.8,
    #     tp_sl=TPSLProperties(take_profit=5.6, stop_loss=5.9))

    # res = get_ticker(Market.LINEAR)
    # print(res)
    # print(res["result"]["list"][0]["lastPrice"])

    # print(bybit.trade.derivatives.get_last_price(TradePair.TON_USDT))

    # last_price = bybit.trade.derivatives.get_last_price(TradePair.TON_USDT)
    # trigger_price = last_price + 0.1
    # order_price = trigger_price - 0.05
    # res = bybit.trade.derivatives.buy_limit_conditional(
    #     trade_pair=TradePair.TON_USDT,
    #     qty=3,
    #     trigger_price=trigger_price,
    #     price=order_price,
    #     tp_sl=TPSLProperties(take_profit=order_price + 0.5, stop_loss=order_price - 0.1)
    # )

    res = bybit.trade.derivatives.reduce_short_position(TradePair.TON_USDT, 7)
    print(res)
