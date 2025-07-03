import pytest
from unittest.mock import patch, MagicMock
from src import external_api


# -------- get_currencies_rates --------
@patch("src.external_api.requests.request")
@patch("src.external_api.logger")
@patch("src.external_api.os.getenv", return_value="fake_api_key")
def test_get_currencies_rates(mock_getenv, mock_logger, mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "quotes": {
            "USDRUB": 90.0,
            "USDEUR": 1.2
        }
    }
    mock_request.return_value = mock_response

    result = external_api.get_currencies_rates("USD")

    assert isinstance(result, dict)
    assert result["RUBUSD"] == 90.0
    assert result["RUBEUR"] == round(90.0 / 1.2, 2)
    mock_logger.info.assert_called()


# -------- get_symbols_rates --------
@patch("src.external_api.requests.request")
@patch("src.external_api.logger")
@patch("src.external_api.os.getenv", return_value="fake_api_key")
def test_get_symbols_rates(mock_getenv, mock_logger, mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {"symbol": "AAPL", "close": 190.5},
            {"symbol": "AMZN", "close": 120.0}
        ]
    }
    mock_request.return_value = mock_response

    result = external_api.get_symbols_rates("AAPL,AMZN")

    assert isinstance(result, list)
    assert result == [
        {"stock": "AAPL", "price": 190.5},
        {"stock": "AMZN", "price": 120.0}
    ]
    mock_logger.info.assert_called()

