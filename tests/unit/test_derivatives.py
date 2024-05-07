from unittest.mock import patch
import pytest

from bybit import Bybit
from bybit_types import TradePair, BybitResponse, Market, OrderSide, OrderType


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
        result = bybit.trade.derivatives.buy_limit(TradePair.TON_USDT, 1, 5.86)
        assert result
        assert result.retCode == 0
        assert result.retMsg == 'OK'
        mock_place_order.assert_called_once_with(
            category=Market.LINEAR.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.BUY.value,
            orderType=OrderType.LIMIT.value,
            qty="1",
            price="5.86"
        )


def test_sell_limit(bybit: Bybit):
    data = {'retCode': 0, 'retMsg': 'OK'}
    with patch.object(bybit.trade.derivatives.session, "place_order", return_value=data) as mock_place_order:
        result = bybit.trade.derivatives.sell_limit(TradePair.TON_USDT, 2, 5.81)
        assert result
        assert result.retCode == 0
        assert result.retMsg == 'OK'
        mock_place_order.assert_called_once_with(
            category=Market.LINEAR.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.SELL.value,
            orderType=OrderType.LIMIT.value,
            qty="2",
            price="5.81"
        )
