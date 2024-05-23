import pytest
from bybit_config import BybitConfig
from bybit_types import BBEnvVars, TradePair


@pytest.mark.parametrize("is_hedge_mode", [True, False])
def test_hedge_mode_envs(is_hedge_mode: bool):
    config = BybitConfig()
    config._trade_pairs[TradePair.TON_USDT] = is_hedge_mode
    assert config.is_hedge_mode(TradePair.TON_USDT) == is_hedge_mode


