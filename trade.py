from functools import cached_property

from pybit.unified_trading import HTTP
from bybit_session import BybitHttpSession
from derivatives import Derivatives
from bybit_config import BybitConfig


class Trade(BybitHttpSession):
    def __init__(self, session: HTTP, config: BybitConfig):
        super(Trade, self).__init__(session)
        self._config = config

    @cached_property
    def derivatives(self):
        return Derivatives(self.session, self._config)
