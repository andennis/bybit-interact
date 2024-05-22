from bybit_session import BybitHttpSession
from pybit.unified_trading import HTTP
from exceptions import BybitException
from bybit_types import Market, TradePair
from bybit_config import BybitConfig


class BaseTrade(BybitHttpSession):
    def __init__(self, session: HTTP, config: BybitConfig):
        super(BaseTrade, self).__init__(session)
        self._config = config

    @property
    def config(self):
        return self._config

    @property
    def market(self) -> Market:
        raise NotImplemented("The property 'market' must be implemented")

    def get_last_price(self, trade_pair: TradePair) -> float:
        response = self.session.get_tickers(category=self.market.value, symbol=trade_pair.value)
        if response["retCode"] != 0:
            raise BybitException(f"Derivatives.get_last_price failed: {response['retMsg']}, "
                                 f"code: {response['retCode']}")
        return float(response["result"]["list"][0]["lastPrice"])

    # def get_current_price(self, trade_pair: TradePair) -> MarketPrice:
    #     response = self.session.get_orderbook(category=self.market.value, symbol=trade_pair.value, limit=1)
    #     if response["retCode"] != 0:
    #         raise BybitException(f"Derivatives.get_current_price failed: {response['retMsg']}, "
    #                              f"code: {response['retCode']}")
    #
    #     return MarketPrice(
    #         ask=float(response["result"]["a"][0][0]),
    #         bid=float(response["result"]["b"][0][0])
    #     )
