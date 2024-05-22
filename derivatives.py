from typing import Optional
from pybit.unified_trading import HTTP
from bybit_types import Market, OrderSide, TradePair, OrderType, TPSLProperties, BybitResponse, PositionIdx
from bybit_types import TriggerDirection
from trade_base import BaseTrade
from exceptions import BybitException
from bybit_config import BybitConfig


class Derivatives(BaseTrade):
    def __init__(self, session: HTTP, config: BybitConfig):
        super(Derivatives, self).__init__(session, config)

    @property
    def market(self) -> Market:
        return Market.LINEAR

    def buy_limit(self,
                  trade_pair: TradePair,
                  qty: float,
                  price: float,
                  tp_sl: Optional[TPSLProperties] = None):
        return self._place_order(trade_pair, OrderSide.BUY, OrderType.LIMIT, qty, price, tp_sl=tp_sl)

    def sell_limit(self,
                   trade_pair: TradePair,
                   qty: float,
                   price: float,
                   tp_sl: Optional[TPSLProperties] = None):
        return self._place_order(trade_pair, OrderSide.SELL, OrderType.LIMIT, qty, price, tp_sl=tp_sl)

    def buy_limit_conditional(self,
                              trade_pair: TradePair,
                              trigger_price: float,
                              qty: float,
                              price: float,
                              tp_sl: Optional[TPSLProperties] = None):
        if not trigger_price:
            raise BybitException("trigger_price is required")
        if trigger_price < price:
            raise BybitException("trigger_price must be greater or equal to the BUY limit price")

        return self._place_order(
            trade_pair,
            OrderSide.BUY,
            OrderType.LIMIT,
            qty,
            price,
            trigger_price=trigger_price,
            tp_sl=tp_sl
        )

    def sell_limit_conditional(self,
                               trade_pair: TradePair,
                               trigger_price: float,
                               qty: float,
                               price: float,
                               tp_sl: Optional[TPSLProperties] = None):
        if not trigger_price:
            raise BybitException("trigger_price is required")
        if trigger_price > price:
            raise BybitException("trigger_price must be less or equal to the SELL limit price")

        return self._place_order(
            trade_pair,
            OrderSide.SELL,
            OrderType.LIMIT,
            qty,
            price,
            trigger_price=trigger_price,
            tp_sl=tp_sl
        )

    def _place_order(self,
                     trade_pair: TradePair,
                     order_side: OrderSide,
                     order_type: OrderType,
                     qty: float,
                     price: float,
                     trigger_price: float = None,
                     tp_sl: TPSLProperties = None):
        params = dict(
            category=self.market.value,
            symbol=trade_pair.value,
            side=order_side.value,
            orderType=order_type.value,
            qty=str(qty),
            price=str(price)
        )

        # positionIdx is required if the current position mode for the given trade pair is set to the Hedge Mode
        if self.config.is_hedge_mode(trade_pair):
            params["positionIdx"] = PositionIdx.HEDGE_BUY.value if order_side == OrderSide.BUY else PositionIdx.HEDGE_SELL.value

        if trigger_price:
            last_price = self.get_last_price(trade_pair)
            params.update(dict(
                triggerPrice=str(trigger_price),
                triggerDirection=TriggerDirection.RAISES.value if trigger_price > last_price else TriggerDirection.FALLS.value
            ))

        if tp_sl and (tp_sl.take_profit or tp_sl.stop_loss):
            params.update(dict(
                tpslMode=tp_sl.mode.value,
                tpOrderType=tp_sl.order_type.value,
                takeProfit=str(tp_sl.take_profit) if tp_sl.take_profit else "",
                stopLoss=str(tp_sl.stop_loss) if tp_sl.stop_loss else ""
            ))

        data = self.session.place_order(**params)
        return BybitResponse(**data)
