from bybit_session import BybitHttpSession
from pybit.unified_trading import HTTP


class Market(BybitHttpSession):
    def __init__(self, session: HTTP):
        super(Market, self).__init__(session)
