from unittest.mock import patch, PropertyMock
import pytest

from trade_base import TradeBase
from bybit_types import Market
from bybit_config import BybitConfig
from pybit.unified_trading import HTTP
from bybit_types import (
    BybitResponse,
    TradePair,
    OrderType,
    OrderSide,
    PositionIdx,
    TPSLProperties,
    TriggerDirection,
)
from exceptions import BybitException


class FakeTrade(TradeBase):
    def __init__(self, session: HTTP, config: BybitConfig):
        super(FakeTrade, self).__init__(session, config)

    @property
    def market(self) -> Market:
        raise NotImplemented("The property must be mocked")


@pytest.fixture(params=[Market.LINEAR, Market.SPOT], ids=["Linear", "Spot"])
def trade(request) -> FakeTrade:
    session = HTTP(api_key="123", api_secret="321", testnet=False)
    with patch(
        "test_trade_base.FakeTrade.market", new_callable=PropertyMock
    ) as mock_market:
        mock_market.return_value = request.param
        yield FakeTrade(session, BybitConfig())


@pytest.mark.parametrize(
    "data",
    [
        {
            "retCode": 0,
            "retMsg": "OK",
            "result": {"orderId": 10},
            "retExtInfo": {"p1": 3},
            "time": 100,
        },
        {"retCode": 1},
    ],
)
def test_bybit_response(data: dict):
    result = BybitResponse(**data)
    assert result.retCode == data["retCode"]
    assert result.retMsg == data.get("retMsg", "")
    assert result.result == data.get("result", {})
    assert result.retExtInfo == data.get("retExtInfo", {})
    assert result.time == data.get("time", 0)


def test_get_last_price_ok(trade: FakeTrade):
    data = {
        "retCode": 0,
        "retMsg": "OK",
        "result": {
            "list": [{"lastPrice": 6.23}],
        },
    }
    with patch.object(
        trade.session, "get_tickers", return_value=data
    ) as mock_get_tickers:
        result = trade.get_last_price(TradePair.TON_USDT)
        assert result == data["result"]["list"][0]["lastPrice"]
        mock_get_tickers.assert_called_once_with(
            category=trade.market.value,
            symbol=TradePair.TON_USDT.value,
        )


def test_get_last_price_failed(trade: FakeTrade):
    data = {"retCode": 1, "retMsg": "some error"}
    with patch.object(trade.session, "get_tickers", return_value=data):
        with pytest.raises(BybitException):
            trade.get_last_price(TradePair.TON_USDT)


@pytest.mark.parametrize("hedge_mode", [True, False])
def test_buy_limit(trade: FakeTrade, hedge_mode: bool):
    data = {"retCode": 0, "retMsg": "OK"}
    with patch.object(trade.config, "is_hedge_mode", return_value=hedge_mode):
        with patch.object(
            trade.session, "place_order", return_value=data
        ) as mock_place_order:
            result = trade.buy_limit(TradePair.TON_USDT, 1.001, 5.8625)
            assert result
            assert result.retCode == 0
            assert result.retMsg == "OK"
            params = dict(
                category=trade.market.value,
                symbol=TradePair.TON_USDT.value,
                side=OrderSide.BUY.value,
                orderType=OrderType.LIMIT.value,
                qty="1.001",
                price="5.8625",
            )
            if hedge_mode:
                params["positionIdx"] = PositionIdx.HEDGE_BUY.value
            mock_place_order.assert_called_once_with(**params)


@pytest.mark.parametrize(
    "tp_sl",
    [
        TPSLProperties(take_profit=6.5001, stop_loss=5.8501),
        TPSLProperties(take_profit=6.5002),
        TPSLProperties(stop_loss=5.8502),
    ],
)
def test_buy_limit_with_tpsl(trade: TradeBase, tp_sl: TPSLProperties):
    data = {"retCode": 0, "retMsg": "OK"}
    with patch.object(
        trade.session, "place_order", return_value=data
    ) as mock_place_order:
        result = trade.buy_limit(TradePair.TON_USDT, 1.001, 5.8625, tp_sl=tp_sl)
        assert result
        assert result.retCode == 0
        assert result.retMsg == "OK"
        mock_place_order.assert_called_once_with(
            category=trade.market.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.BUY.value,
            orderType=OrderType.LIMIT.value,
            qty="1.001",
            price="5.8625",
            # Stop loss / Take profit
            tpslMode=tp_sl.mode.value,
            tpOrderType=tp_sl.order_type.value,
            takeProfit=str(tp_sl.take_profit) if tp_sl.take_profit else "",
            stopLoss=str(tp_sl.stop_loss) if tp_sl.stop_loss else "",
        )


@pytest.mark.parametrize("hedge_mode", [True, False])
def test_sell_limit(trade: TradeBase, hedge_mode: bool):
    data = {"retCode": 0, "retMsg": "OK"}
    with patch.object(trade.config, "is_hedge_mode", return_value=hedge_mode):
        with patch.object(
            trade.session, "place_order", return_value=data
        ) as mock_place_order:
            result = trade.sell_limit(TradePair.TON_USDT, 2.0012, 5.8101)
            assert result
            assert result.retCode == 0
            assert result.retMsg == "OK"
            params = dict(
                category=trade.market.value,
                symbol=TradePair.TON_USDT.value,
                side=OrderSide.SELL.value,
                orderType=OrderType.LIMIT.value,
                qty="2.0012",
                price="5.8101",
            )
            if hedge_mode:
                params["positionIdx"] = PositionIdx.HEDGE_SELL.value
            mock_place_order.assert_called_once_with(**params)


@pytest.mark.parametrize(
    "tp_sl",
    [
        TPSLProperties(take_profit=5.7001, stop_loss=5.8301),
        TPSLProperties(take_profit=5.7001),
        TPSLProperties(stop_loss=5.8301),
    ],
)
def test_sell_limit_with_tpsl(trade: TradeBase, tp_sl: TPSLProperties):
    data = {"retCode": 0, "retMsg": "OK"}
    with patch.object(
        trade.session, "place_order", return_value=data
    ) as mock_place_order:
        result = trade.sell_limit(
            TradePair.TON_USDT, 2.0012, 5.8101, tp_sl=tp_sl
        )
        assert result
        assert result.retCode == 0
        assert result.retMsg == "OK"
        mock_place_order.assert_called_once_with(
            category=trade.market.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.SELL.value,
            orderType=OrderType.LIMIT.value,
            qty="2.0012",
            price="5.8101",
            # Stop loss / Take profit
            tpslMode=tp_sl.mode.value,
            tpOrderType=tp_sl.order_type.value,
            takeProfit=str(tp_sl.take_profit) if tp_sl.take_profit else "",
            stopLoss=str(tp_sl.stop_loss) if tp_sl.stop_loss else "",
        )


@pytest.mark.parametrize(
    "last_price, trigger_price, trigger_direction, order_price",
    [
        (5.5, 5.4, TriggerDirection.FALLS, 5.4),
        (5.5, 5.45, TriggerDirection.FALLS, 5.4),
        (5.5, 5.6, TriggerDirection.RAISES, 5.55),
    ],
)
def test_buy_limit_conditional(
    trade: FakeTrade,
    last_price: float,
    trigger_price: float,
    trigger_direction: TriggerDirection,
    order_price: float,
):
    data = {"retCode": 0, "retMsg": "OK"}
    qyt = 2.55
    tp_sl = TPSLProperties(
        take_profit=order_price + 0.5, stop_loss=order_price - 0.1
    )
    with (
        patch.object(trade, "get_last_price", return_value=last_price),
        patch.object(
            trade.session, "place_order", return_value=data
        ) as mock_place_order,
    ):
        result = trade.buy_limit_conditional(
            TradePair.TON_USDT, trigger_price, qyt, order_price, tp_sl=tp_sl
        )
        assert result
        assert result.retCode == 0
        assert result.retMsg == "OK"
        mock_place_order.assert_called_once_with(
            category=trade.market.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.BUY.value,
            orderType=OrderType.LIMIT.value,
            qty=str(qyt),
            price=str(order_price),
            # trigger price
            triggerPrice=str(trigger_price),
            triggerDirection=trigger_direction.value,
            # Stop loss / Take profit
            tpslMode=tp_sl.mode.value,
            tpOrderType=tp_sl.order_type.value,
            takeProfit=str(tp_sl.take_profit),
            stopLoss=str(tp_sl.stop_loss),
        )


def test_buy_limit_conditional_trigger_price_less_limit(trade: FakeTrade):
    with pytest.raises(BybitException):
        trade.buy_limit_conditional(TradePair.TON_USDT, 5.5, 5, 5.6)


@pytest.mark.parametrize(
    "last_price, trigger_price, trigger_direction, order_price",
    [
        (5.5, 5.6, TriggerDirection.RAISES, 5.7),
        (5.5, 5.6, TriggerDirection.RAISES, 5.6),
        (5.5, 5.4, TriggerDirection.FALLS, 5.6),
    ],
)
def test_sell_limit_conditional(
    trade: FakeTrade,
    last_price: float,
    trigger_price: float,
    trigger_direction: TriggerDirection,
    order_price: float,
):
    data = {"retCode": 0, "retMsg": "OK"}
    qyt = 2.55
    tp_sl = TPSLProperties(
        take_profit=order_price - 0.5, stop_loss=order_price + 0.1
    )
    with (
        patch.object(trade, "get_last_price", return_value=last_price),
        patch.object(
            trade.session, "place_order", return_value=data
        ) as mock_place_order,
    ):
        result = trade.sell_limit_conditional(
            TradePair.TON_USDT, trigger_price, qyt, order_price, tp_sl=tp_sl
        )
        assert result
        assert result.retCode == 0
        assert result.retMsg == "OK"
        mock_place_order.assert_called_once_with(
            category=trade.market.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.SELL.value,
            orderType=OrderType.LIMIT.value,
            qty=str(qyt),
            price=str(order_price),
            # trigger price
            triggerPrice=str(trigger_price),
            triggerDirection=trigger_direction.value,
            # Stop loss / Take profit
            tpslMode=tp_sl.mode.value,
            tpOrderType=tp_sl.order_type.value,
            takeProfit=str(tp_sl.take_profit),
            stopLoss=str(tp_sl.stop_loss),
        )


def test_sell_limit_conditional_trigger_price_greater_limit(trade: FakeTrade):
    with pytest.raises(BybitException):
        trade.sell_limit_conditional(TradePair.TON_USDT, 5.6, 5, 5.5)
