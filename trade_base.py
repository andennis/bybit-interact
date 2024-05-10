from bybit_session import BybitHttpSession
from pybit.unified_trading import HTTP
from exceptions import BybitException
from bybit_types import Market, TradePair, MarketPrice


class BaseTrade(BybitHttpSession):
    def __init__(self, session: HTTP):
        super(BaseTrade, self).__init__(session)

    def get_current_price(self, trade_pair: TradePair) -> MarketPrice:
        response = self.session.get_orderbook(category=Market.LINEAR.value, symbol=trade_pair.value, limit=1)
        if response["retCode"] != 0:
            raise BybitException(f"Derivatives.get_current_price failed: {response['retMsg']}, "
                                 f"code: {response['retCode']}")

        return MarketPrice(
            ask=float(response["result"]["a"][0][0]),
            bid=float(response["result"]["b"][0][0])
        )
