from typing import Generator
from unittest.mock import MagicMock, patch

import pytest


stocks_json = {'data': [{"adj_close": 196.45,
           "adj_high": 200.37,
           "adj_low": 195.7,
           "adj_open": 199.73,
           "adj_volume": 51447349.0,
           "asset_type": "Stock",
           "close": 196.45,
           "date": "2025-06-13T00:00:00+0000",
           "dividend": 0.0,
           "exchange": "XNAS",
           "exchange_code": "NASDAQ",
           "high": 200.37,
           "low": 195.7,
           "name": "Apple Inc",
           "open": 199.73,
           "price_currency": "USD",
           "split_factor": 1.0,
           "symbol": "AAPL",
           "volume": 51362400.0},
          {"adj_close": 212.1,
           "adj_high": 214.05,
           "adj_low": 209.62,
           "adj_open": 209.96,
           "adj_volume": 29337763.0,
           "asset_type": "Stock",
           "close": 212.1,
           "date": "2025-06-13T00:00:00+0000",
           "dividend": 0.0,
           "exchange": "XNAS",
           "exchange_code": "NASDAQ",
           "high": 214.05,
           "low": 209.62,
           "name": "Amazon.com Inc",
           "open": 209.96,
           "price_currency": "USD",
           "split_factor": 1.0,
           "symbol": "AMZN",
           "volume": 29337763.0}],
           "pagination": {"count": 2, "limit": 100, "offset": 0, "total": 2}}


@pytest.fixture(autouse=True)
def mock_entire_logger() -> Generator[MagicMock, None, None]:
    with patch("src.logger.logging.getLogger") as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        yield mock_logger


@pytest.fixture
def transactions_test() -> list[dict]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]
