from pybit.unified_trading import HTTP

# Test
API_KEY = ""
API_SECRET = ""


def get_orderbook(category: str, cr_pair: str):
    session = HTTP(
        testnet=True,
        api_key=API_KEY,
        api_secret=API_SECRET,
    )
    return session.get_orderbook(category=category, symbol=cr_pair, limit=5)


if __name__ == '__main__':
    res = get_orderbook("spot", "ETHUSDT")
    # print(res)

    result = res["result"]
    print("----- Asks -------")
    for ask in reversed(result["a"]):
        print(ask)

    print("----- Bids -------")
    for ask in result["b"]:
        print(ask)
