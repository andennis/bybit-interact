import os
from typing import Optional
from pybit.unified_trading import HTTP
from trade import Trade
from market import Market
from functools import cached_property
from bybit_types import BBEnvVars
from bybit_config import BybitConfig


class Bybit:
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, testnet: bool = True):
        self._http_session = HTTP(
            api_key=api_key or os.environ.get(BBEnvVars.API_KEY.value),
            api_secret=api_secret or os.environ.get(BBEnvVars.API_SECRET.value),
            testnet=testnet,
            log_requests=True,
        )

    @cached_property
    def config(self) -> BybitConfig:
        return BybitConfig()

    @cached_property
    def trade(self):
        return Trade(self._http_session, self.config)

    @cached_property
    def market(self):
        return Market(self._http_session)
