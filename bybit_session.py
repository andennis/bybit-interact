from pybit.unified_trading import HTTP


class BybitHttpSession:
    def __init__(self, http_session: HTTP):
        self._session = http_session

    @property
    def session(self) -> HTTP:
        return self._session
