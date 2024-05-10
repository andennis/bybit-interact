from enum import Enum
from dataclasses import dataclass, field


class Market(Enum):
    SPOT = "spot"
    LINEAR = "linear"


class OrderSide(Enum):
    BUY = "Buy"
    SELL = "Sell"


class TradePair(Enum):
    TON_USDT = "TONUSDT"


class OrderType(Enum):
    MARKET = "Market"
    LIMIT = "Limit"
    UNKNOWN = "UNKNOWN"


class TriggerDirection(Enum):
    # Triggered when market price rises to trigger price
    RAISES = 1
    # Triggered when market price falls to trigger price
    FALLS = 2


# Identify position in different position modes
class PositionIdx(Enum):
    ONE_WAY = 0
    HEDGE_BUY = 1
    HEDGE_SELL = 2


class TPSLMode(Enum):
    FULL = "Full"
    PARTIAL = "Partial"


class TPOrderType(Enum):
    MARKET = "Market"
    LIMIT = "Limit"


class BBEnvVars(Enum):
    API_KEY = "BYBIT_APY_KEY"
    API_SECRET = "BYBIT_API_SECRET"


@dataclass
class TPSLProperties:
    mode: TPSLMode = TPSLMode.FULL
    order_type: TPOrderType = TPOrderType.MARKET
    take_profit: float = None
    stop_loss: float = None


@dataclass
class BybitResponse:
    retCode: int
    retMsg: str = ""
    result: dict = field(default_factory=dict)
    retExtInfo: dict = field(default_factory=dict)
    time: int = 0


@dataclass
class MarketPrice:
    ask: float
    bid: float

    def __int__(self, ask: float, bid: float):
        self.ask = ask
        self.bid = bid
