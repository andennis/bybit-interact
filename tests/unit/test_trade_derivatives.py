from unittest.mock import patch
import pytest

from bybit import Bybit
from bybit_types import (
    TradePair,
    Market,
    OrderSide,
    OrderType,
    PositionIdx,
)
from trade_derivatives import TradeDerivatives


def test_market_linear(bybit: Bybit):
    assert bybit.trade
    assert bybit.trade.derivatives
    assert isinstance(bybit.trade.derivatives, TradeDerivatives)
    assert bybit.trade.derivatives.market == Market.LINEAR
    assert bybit.trade.derivatives.session
    assert bybit.trade.derivatives.config


@pytest.mark.parametrize("hedge_mode", [True, False])
def test_reduce_long_position(bybit: Bybit, hedge_mode):
    data = {"retCode": 0, "retMsg": "OK"}
    with (
        patch.object(bybit.config, "is_hedge_mode", return_value=hedge_mode),
        patch.object(
            bybit.trade.derivatives.session, "place_order", return_value=data
        ) as mock_place_order,
    ):
        result = bybit.trade.derivatives.reduce_long_position(
            TradePair.TON_USDT, 4.1
        )

        assert result
        assert result.retCode == 0
        assert result.retMsg == "OK"

        params = dict(
            category=Market.LINEAR.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.SELL.value,
            orderType=OrderType.MARKET.value,
            qty="4.1",
            reduceOnly=True,
        )
        if hedge_mode:
            params["positionIdx"] = PositionIdx.HEDGE_BUY.value

        mock_place_order.assert_called_once_with(**params)


@pytest.mark.parametrize("hedge_mode", [True, False])
def test_reduce_short_position(bybit: Bybit, hedge_mode):
    data = {"retCode": 0, "retMsg": "OK"}
    with (
        patch.object(bybit.config, "is_hedge_mode", return_value=hedge_mode),
        patch.object(
            bybit.trade.derivatives.session, "place_order", return_value=data
        ) as mock_place_order,
    ):
        result = bybit.trade.derivatives.reduce_short_position(
            TradePair.TON_USDT, 4.1
        )

        assert result
        assert result.retCode == 0
        assert result.retMsg == "OK"

        params = dict(
            category=Market.LINEAR.value,
            symbol=TradePair.TON_USDT.value,
            side=OrderSide.BUY.value,
            orderType=OrderType.MARKET.value,
            qty="4.1",
            reduceOnly=True,
        )
        if hedge_mode:
            params["positionIdx"] = PositionIdx.HEDGE_SELL.value

        mock_place_order.assert_called_once_with(**params)
