from pybit.unified_trading import HTTP
from bybit_types import Market, TradePair, TPSLProperties
from bybit import Bybit

# Test
API_KEY = "ZUVBoaokntFM67YEOi"
API_SECRET = "la5oef31bt1Y5y0D4uuj2epMKrOveYI6fWdd"

bybit = Bybit(api_key=API_KEY, api_secret=API_SECRET)


def place_order(category: Market, symbol: str, side: str, order_type: str, price: float, amount: int, take_profit: float):
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
        # tpslMode="Full",
        # tpOrderType="Market",
        # takeProfit=str(take_profit),
        # orderLinkId="andennis-test2",
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
    # res = place_order(Market.LINEAR, "TONUSDT", "Sell", "Limit", 5.829, 12, 6)
    # res = bybit.trade.derivatives.sell_limit(trade_pair=TradePair.TON_USDT, qty=3, price=5.7875)
    # res = bybit.trade.derivatives.buy_limit(trade_pair=TradePair.TON_USDT, qty=3, price=5.7815)
    res = bybit.trade.derivatives.sell_limit(
        trade_pair=TradePair.TON_USDT,
        qty=3,
        price=5.8,
        tp_sl=TPSLProperties(take_profit=5.6, stop_loss=5.9))
    print(res)
