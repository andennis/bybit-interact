from functools import cached_property

from pybit.unified_trading import HTTP
from bybit_session import BybitHttpSession
from derivatives import Derivatives


class Trade(BybitHttpSession):
    def __init__(self, session: HTTP):
        super(Trade, self).__int__(session)

    @cached_property
    def derivatives(self):
        return Derivatives(self.session)
