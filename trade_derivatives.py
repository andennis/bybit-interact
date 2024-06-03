from pybit.unified_trading import HTTP
from bybit_types import (
    Market,
    OrderSide,
    TradePair,
    OrderType,
)
from bybit_types import BybitResponse
from trade_base import TradeBase
from bybit_config import BybitConfig


class TradeDerivatives(TradeBase):
    def __init__(self, session: HTTP, config: BybitConfig):
        super(TradeDerivatives, self).__init__(session, config)

    @property
    def market(self) -> Market:
        return Market.LINEAR

    def reduce_long_position(
        self, trade_pair: TradePair, qty: float
    ) -> BybitResponse:
        return self._reduce_position(
            trade_pair, OrderSide.SELL, OrderType.MARKET, qty
        )

    def reduce_short_position(
        self, trade_pair: TradePair, qty: float
    ) -> BybitResponse:
        return self._reduce_position(
            trade_pair, OrderSide.BUY, OrderType.MARKET, qty
        )
