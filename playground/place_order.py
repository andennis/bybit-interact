import logging

from pybit.unified_trading import HTTP
from bybit_types import Market, TradePair, TPSLProperties
from bybit import Bybit

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# Test
API_KEY = "addoY1N4m0HXdDSxx2"
API_SECRET = "GVk5DwZei44QTFGP8L85mgLXTKnrl30SDJiy"

bybit = Bybit(api_key=API_KEY, api_secret=API_SECRET)
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


def get_ticker(category: Market):
    return session.get_tickers(
        category=category.value,
        symbol=TradePair.TON_USDT.value,
    )


# def place_strategy_order(price: int, qty: int, profit: int, diff: int):
#     bybit.trade.derivatives.buy_limit(
#         trade_pair=TradePair.TON_USDT,
#         qty=qty,
#         price=price,
#         tp_sl=TPSLProperties(take_profit=price + profit))
#     bybit.trade.derivatives.sell_limit(
#         trade_pair=TradePair.TON_USDT,
#         qty=qty,
#         price=price,
#         tp_sl=TPSLProperties(take_profit=profit - diff - profit))


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
    last_price = bybit.trade.derivatives.get_last_price(TradePair.TON_USDT)
    trigger_price = last_price + 0.1
    order_price = trigger_price - 0.05
    res = bybit.trade.derivatives.buy_limit_conditional(
        trade_pair=TradePair.TON_USDT,
        qty=3,
        trigger_price=trigger_price,
        price=order_price,
        tp_sl=TPSLProperties(take_profit=order_price + 0.5, stop_loss=order_price - 0.1)
    )
    print(res)
