from typing import Optional
from pybit.unified_trading import HTTP
from bybit_session import BybitHttpSession
from bybit_types import Market, OrderSide, TradePair, OrderType, TPSLProperties, BybitResponse


class Derivatives(BybitHttpSession):
    def __init__(self, session: HTTP):
        super(Derivatives, self).__int__(session)

    def buy_limit(self,
                  trade_pair: TradePair,
                  qty: float,
                  price: float,
                  tp_sl: Optional[TPSLProperties] = None):
        return self._place_order(trade_pair, OrderSide.BUY, OrderType.LIMIT, qty, price, tp_sl)

    def sell_limit(self,
                   trade_pair: TradePair,
                   qty: float,
                   price: float,
                   tp_sl: Optional[TPSLProperties] = None):
        return self._place_order(trade_pair, OrderSide.SELL, OrderType.LIMIT, qty, price, tp_sl)

    def _place_order(self,
                     trade_pair: TradePair,
                     order_side: OrderSide,
                     order_type: OrderType,
                     qty: float,
                     price: float,
                     tp_sl: TPSLProperties = None):
        params = dict(
            category=Market.LINEAR.value,
            symbol=trade_pair.value,
            side=order_side.value,
            orderType=order_type.value,
            qty=str(qty),
            price=str(price)
        )
        if tp_sl and (tp_sl.take_profit or tp_sl.stop_loss):
            params.update(dict(
                tpslMode=tp_sl.mode.value,
                tpOrderType=tp_sl.order_type.value,
                takeProfit=str(tp_sl.take_profit) if tp_sl.take_profit else "",
                stopLoss=str(tp_sl.stop_loss) if tp_sl.stop_loss else ""
            ))

        data = self.session.place_order(**params)
        return BybitResponse(**data)
