from typing import Optional
from pybit.unified_trading import HTTP
from bybit_types import (
    Market,
    OrderSide,
    TradePair,
    OrderType,
    TPSLProperties,
)
from bybit_types import BybitResponse
from trade_base import BaseTrade
from exceptions import BybitException
from bybit_config import BybitConfig


class Derivatives(BaseTrade):
    def __init__(self, session: HTTP, config: BybitConfig):
        super(Derivatives, self).__init__(session, config)

    @property
    def market(self) -> Market:
        return Market.LINEAR

    def buy_limit(
        self,
        trade_pair: TradePair,
        qty: float,
        price: float,
        tp_sl: Optional[TPSLProperties] = None,
    ) -> BybitResponse:
        return self._place_order(
            trade_pair, OrderSide.BUY, OrderType.LIMIT, qty, price, tp_sl=tp_sl
        )

    def sell_limit(
        self,
        trade_pair: TradePair,
        qty: float,
        price: float,
        tp_sl: Optional[TPSLProperties] = None,
    ) -> BybitResponse:
        return self._place_order(
            trade_pair, OrderSide.SELL, OrderType.LIMIT, qty, price, tp_sl=tp_sl
        )

    def buy_limit_conditional(
        self,
        trade_pair: TradePair,
        trigger_price: float,
        qty: float,
        price: float,
        tp_sl: Optional[TPSLProperties] = None,
    ) -> BybitResponse:
        if not trigger_price:
            raise BybitException("trigger_price is required")
        if trigger_price < price:
            raise BybitException(
                "trigger_price must be greater or equal to the BUY limit price"
            )

        return self._place_order(
            trade_pair,
            OrderSide.BUY,
            OrderType.LIMIT,
            qty,
            price,
            trigger_price=trigger_price,
            tp_sl=tp_sl,
        )

    def sell_limit_conditional(
        self,
        trade_pair: TradePair,
        trigger_price: float,
        qty: float,
        price: float,
        tp_sl: Optional[TPSLProperties] = None,
    ) -> BybitResponse:
        if not trigger_price:
            raise BybitException("trigger_price is required")
        if trigger_price > price:
            raise BybitException(
                "trigger_price must be less or equal to the SELL limit price"
            )

        return self._place_order(
            trade_pair,
            OrderSide.SELL,
            OrderType.LIMIT,
            qty,
            price,
            trigger_price=trigger_price,
            tp_sl=tp_sl,
        )

    def reduce_long_position(
        self, trade_pair: TradePair, qty: float
    ) -> BybitResponse:
        return self._reduce_position(
            trade_pair, OrderSide.SELL, OrderType.MARKET, qty
        )

    def reduce_short_position(
        self, trade_pair: TradePair, qty: float
    ) -> BybitResponse:
        return self._reduce_position(
            trade_pair, OrderSide.BUY, OrderType.MARKET, qty
        )
