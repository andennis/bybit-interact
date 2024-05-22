from bybit_types import TradePair


class BybitConfig:
    def __init__(self):
        self._trade_pairs = {
            TradePair.TON_USDT: False
        }

    def is_hedge_mode(self, trade_pair: TradePair) -> bool:
        return self._trade_pairs[trade_pair] if trade_pair in self._trade_pairs else False
