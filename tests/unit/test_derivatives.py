from unittest.mock import patch
import pytest

from bybit import Bybit
from bybit_types import TradePair, BybitResponse, Market, OrderSide, OrderType
from bybit_types import TPSLMode, TPOrderType, TPSLProperties


@pytest.mark.parametrize("data", [
    {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': 10}, 'retExtInfo': {"p1": 3}, 'time': 100},
    {'retCode': 1}
])
def test_bybit_response(data: dict):
    result = BybitResponse(**data)
    assert result.retCode == data['retCode']
    assert result.retMsg == data.get('retMsg', "")
    assert result.result == data.get('result', {})
    assert result.retExtInfo == data.get('retExtInfo', {})
    assert result.time == data.get('time', 0)


@pytest.fixture
def bybit() -> Bybit:
    return Bybit()


def test_buy_limit(bybit: Bybit):
    data = {'retCode': 0, 'retMsg': 'OK'}
    with patch.object(bybit.trade.derivatives.session, "place_order", return_value=data) as mock_place_order:
        result = bybit.trade.derivatives.buy_limit(TradePair.TON_USDT, 1.001, 5.8625)
        assert result
        assert result.retCode == 0
        assert result.retMsg == 'OK'
        mock_place_order.assert_called_once_with(
            category=Market.LINEAR.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.BUY.value,
            orderType=OrderType.LIMIT.value,
            qty="1.001",
            price="5.8625"
        )


@pytest.mark.parametrize("tp_sl", [
    TPSLProperties(take_profit=6.5001, stop_loss=5.8501),
    TPSLProperties(take_profit=6.5002),
    TPSLProperties(stop_loss=5.8502)
])
def test_buy_limit_with_tpsl(bybit: Bybit, tp_sl: TPSLProperties):
    data = {'retCode': 0, 'retMsg': 'OK'}
    with patch.object(bybit.trade.derivatives.session, "place_order", return_value=data) as mock_place_order:
        result = bybit.trade.derivatives.buy_limit(TradePair.TON_USDT, 1.001, 5.8625, tp_sl)
        assert result
        assert result.retCode == 0
        assert result.retMsg == 'OK'
        mock_place_order.assert_called_once_with(
            category=Market.LINEAR.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.BUY.value,
            orderType=OrderType.LIMIT.value,
            qty="1.001",
            price="5.8625",
            # Stop loss / Take profit
            tpslMode=tp_sl.mode.value,
            tpOrderType=tp_sl.order_type.value,
            takeProfit=str(tp_sl.take_profit) if tp_sl.take_profit else "",
            stopLoss=str(tp_sl.stop_loss) if tp_sl.stop_loss else ""
        )


def test_sell_limit(bybit: Bybit):
    data = {'retCode': 0, 'retMsg': 'OK'}
    with patch.object(bybit.trade.derivatives.session, "place_order", return_value=data) as mock_place_order:
        result = bybit.trade.derivatives.sell_limit(TradePair.TON_USDT, 2.0012, 5.8101)
        assert result
        assert result.retCode == 0
        assert result.retMsg == 'OK'
        mock_place_order.assert_called_once_with(
            category=Market.LINEAR.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.SELL.value,
            orderType=OrderType.LIMIT.value,
            qty="2.0012",
            price="5.8101"
        )


@pytest.mark.parametrize("tp_sl", [
    TPSLProperties(take_profit=5.7001, stop_loss=5.8301),
    TPSLProperties(take_profit=5.7001),
    TPSLProperties(stop_loss=5.8301)
])
def test_sell_limit_with_tpsl(bybit: Bybit, tp_sl: TPSLProperties):
    data = {'retCode': 0, 'retMsg': 'OK'}
    with patch.object(bybit.trade.derivatives.session, "place_order", return_value=data) as mock_place_order:
        result = bybit.trade.derivatives.sell_limit(TradePair.TON_USDT, 2.0012, 5.8101, tp_sl)
        assert result
        assert result.retCode == 0
        assert result.retMsg == 'OK'
        mock_place_order.assert_called_once_with(
            category=Market.LINEAR.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.SELL.value,
            orderType=OrderType.LIMIT.value,
            qty="2.0012",
            price="5.8101",
            # Stop loss / Take profit
            tpslMode=tp_sl.mode.value,
            tpOrderType=tp_sl.order_type.value,
            takeProfit=str(tp_sl.take_profit) if tp_sl.take_profit else "",
            stopLoss=str(tp_sl.stop_loss) if tp_sl.stop_loss else ""
        )
