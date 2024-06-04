import pytest
from bybit import Bybit


@pytest.fixture
def bybit() -> Bybit:
    return Bybit()
