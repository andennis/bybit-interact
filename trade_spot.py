from pybit.unified_trading import HTTP
from bybit_types import Market
from trade_base import TradeBase
from bybit_config import BybitConfig


class TradeSpot(TradeBase):
    def __init__(self, session: HTTP, config: BybitConfig):
        super(TradeSpot, self).__init__(session, config)

    @property
    def market(self) -> Market:
        return Market.SPOT
