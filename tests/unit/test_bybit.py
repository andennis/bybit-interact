import os
import pytest
from unittest.mock import patch
from bybit import Bybit
from bybit_types import BBEnvVars


# @pytest.fixture()
# def bybit():
#     return Bybit()

@pytest.mark.parametrize("testnet", [True, False])
def test_session(testnet):
    bybit = Bybit(api_key="some_api_key", api_secret="some_secret", testnet=testnet)
    assert bybit._http_session
    assert bybit._http_session.api_key == "some_api_key"
    assert bybit._http_session.api_secret == "some_secret"
    assert bybit._http_session.testnet == testnet


@pytest.mark.parametrize("apy_key, api_secret", [(None, None), ("key1", "secret1")])
@patch.dict(os.environ, {BBEnvVars.API_KEY.value: "env_api_key", BBEnvVars.API_SECRET.value: "env_secret"})
def test_session_key_from_env(apy_key: str, api_secret: str):
    bybit = Bybit(api_key=apy_key, api_secret=api_secret, testnet=False)
    assert bybit._http_session
    assert bybit._http_session.api_key == (apy_key or "env_api_key")
    assert bybit._http_session.api_secret == (api_secret or "env_secret")


def test_bybit_testnet_on_by_default():
    bybit = Bybit()
    assert bybit._http_session
    assert bybit._http_session.testnet


def test_config():
    bybit = Bybit()
    assert bybit.config


def test_bybit_trade():
    bybit = Bybit()
    assert bybit.trade
    assert bybit.trade.session
    assert bybit.trade.session == bybit._http_session


def test_bybit_market():
    bybit = Bybit()
    assert bybit.market
    assert bybit.market.session
    assert bybit.market.session == bybit._http_session



