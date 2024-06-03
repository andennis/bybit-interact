from functools import cached_property

from pybit.unified_trading import HTTP
from bybit_session import BybitHttpSession
from trade_derivatives import TradeDerivatives
from trade_spot import TradeSpot
from bybit_config import BybitConfig


class Trade(BybitHttpSession):
    def __init__(self, session: HTTP, config: BybitConfig):
        super(Trade, self).__init__(session)
        self._config = config

    @cached_property
    def derivatives(self):
        return TradeDerivatives(self.session, self._config)

    @cached_property
    def spot(self):
        return TradeSpot(self.session, self._config)
