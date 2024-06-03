from typing import Optional
from bybit_session import BybitHttpSession
from pybit.unified_trading import HTTP
from exceptions import BybitException
from bybit_types import (
    Market,
    TradePair,
    BybitResponse,
    PositionIdx,
    TriggerDirection,
    OrderSide,
    OrderType,
)
from bybit_types import TPSLProperties
from bybit_config import BybitConfig


class TradeBase(BybitHttpSession):
    def __init__(self, session: HTTP, config: BybitConfig):
        super(TradeBase, self).__init__(session)
        self._config = config

    @property
    def config(self):
        return self._config

    @property
    def market(self) -> Market:
        raise NotImplemented("The property 'market' must be implemented")

    def get_last_price(self, trade_pair: TradePair) -> float:
        response = self.session.get_tickers(
            category=self.market.value, symbol=trade_pair.value
        )
        if response["retCode"] != 0:
            raise BybitException(
                f"Derivatives.get_last_price failed: {response['retMsg']}, "
                f"code: {response['retCode']}"
            )
        return float(response["result"]["list"][0]["lastPrice"])

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

    def _place_order(
        self,
        trade_pair: TradePair,
        order_side: OrderSide,
        order_type: OrderType,
        qty: float,
        price: float,
        trigger_price: float = None,
        tp_sl: TPSLProperties = None,
    ):
        params = dict(
            category=self.market.value,
            symbol=trade_pair.value,
            side=order_side.value,
            orderType=order_type.value,
            qty=str(qty),
            price=str(price),
        )

        # positionIdx is required if the current position mode for the given trade pair is set to the Hedge Mode
        if self.config.is_hedge_mode(trade_pair):
            params["positionIdx"] = (
                PositionIdx.HEDGE_BUY.value
                if order_side == OrderSide.BUY
                else PositionIdx.HEDGE_SELL.value
            )

        if trigger_price:
            last_price = self.get_last_price(trade_pair)
            params.update(
                dict(
                    triggerPrice=str(trigger_price),
                    triggerDirection=(
                        TriggerDirection.RAISES.value
                        if trigger_price > last_price
                        else TriggerDirection.FALLS.value
                    ),
                )
            )

        if tp_sl and (tp_sl.take_profit or tp_sl.stop_loss):
            params.update(
                dict(
                    tpslMode=tp_sl.mode.value,
                    tpOrderType=tp_sl.order_type.value,
                    takeProfit=(
                        str(tp_sl.take_profit) if tp_sl.take_profit else ""
                    ),
                    stopLoss=str(tp_sl.stop_loss) if tp_sl.stop_loss else "",
                )
            )

        data = self.session.place_order(**params)
        return BybitResponse(**data)

    def _reduce_position(
        self,
        trade_pair: TradePair,
        order_side: OrderSide,
        order_type: OrderType,
        qty: float,
    ):
        params = dict(
            category=self.market.value,
            symbol=trade_pair.value,
            side=order_side.value,
            orderType=order_type.value,
            qty=str(qty),
            reduceOnly=True,
        )
        # positionIdx is required if the current position mode for the given trade pair is set to the Hedge Mode
        if self.config.is_hedge_mode(trade_pair):
            params["positionIdx"] = (
                PositionIdx.HEDGE_BUY.value
                if order_side == OrderSide.SELL
                else PositionIdx.HEDGE_SELL.value
            )

        data = self.session.place_order(**params)
        return BybitResponse(**data)

    # def get_current_price(self, trade_pair: TradePair) -> MarketPrice:
    #     response = self.session.get_orderbook(category=self.market.value, symbol=trade_pair.value, limit=1)
    #     if response["retCode"] != 0:
    #         raise BybitException(f"Derivatives.get_current_price failed: {response['retMsg']}, "
    #                              f"code: {response['retCode']}")
    #
    #     return MarketPrice(
    #         ask=float(response["result"]["a"][0][0]),
    #         bid=float(response["result"]["b"][0][0])
    #     )
