from pybit.unified_trading import HTTP
from bybit_types import Market

# Test
API_KEY = ""
API_SECRET = ""


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


if __name__ == '__main__':
    res = place_order(Market.LINEAR, "TONUSDT", "Sell", "Limit", 5.829, 12, 6)
    print(res)
