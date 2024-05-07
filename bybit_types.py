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


@dataclass
class BybitResponse:
    retCode: int
    retMsg: str = ""
    result: dict = field(default_factory=dict)
    retExtInfo: dict = field(default_factory=dict)
    time: int = 0
