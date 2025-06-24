import json
from typing import Any
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest
from pandas import DataFrame

from src.utils import get_transactions_from_excel_file, get_transactions_from_jsonfile


def test_get_transactions_from_valid_file(transactions_test: list[dict[str, Any]]) -> None:
    mock_data = json.dumps(transactions_test)
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_transactions_from_jsonfile("dummy_path.json")
        assert result == transactions_test


def test_get_transactions_file_not_found() -> None:
    with patch("builtins.open", side_effect=FileNotFoundError()):
        result = get_transactions_from_jsonfile("not_found.json")
        assert result == []


def test_get_transactions_invalid_json() -> None:
    with (
        patch("builtins.open", mock_open(read_data="INVALID_JSON")),
        patch("json.load", side_effect=json.JSONDecodeError("msg", "", 0)),
    ):
        result = get_transactions_from_jsonfile("invalid.json")
        assert result == []


def test_get_transactions_invalid_structure() -> None:
    bad_structure = json.dumps({"not": "a list"})
    with patch("builtins.open", mock_open(read_data=bad_structure)):
        result = get_transactions_from_jsonfile("bad_struct.json")
        assert result == []


@pytest.fixture
def mock_csv_data() -> list[list[str]]:
    return [
        ["id", "state", "date", "amount", "currency_code", "currency_name", "from", "to", "description"],
        [
            "650703",
            "EXECUTED",
            "2023-09-05T11:30:32Z",
            "16210",
            "Sol",
            "PEN",
            "Счет 58803664561298323391",
            "Счет 39745660563456619397",
            "Перевод организации",
        ],
        [
            "5447107",
            "EXECUTED",
            "2021-11-01T03:49:47Z",
            "18924",
            "Peso",
            "MXN",
            "Visa 1750234568535711",
            "Mastercard 1365460456366991",
            "Перевод с карты на карту",
        ],
    ]


@pytest.fixture
def mock_excel_data() -> DataFrame:
    return pd.DataFrame(
        [
            {
                "id": "650703",
                "state": "EXECUTED",
                "date": "2023-09-05T11:30:32Z",
                "amount": "16210",
                "currency_code": "Sol",
                "currency_name": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            },
            {
                "id": "5447107",
                "state": "EXECUTED",
                "date": "2021-11-01T03:49:47Z",
                "amount": "18924",
                "currency_code": "Peso",
                "currency_name": "MXN",
                "from": "Visa 1750234568535711",
                "to": "Mastercard 1365460456366991",
                "description": "Перевод с карты на карту",
            },
        ]
    )


@patch("src.utils.pd.read_excel")
def test_get_transactions_from_excel_file_success(mock_read_excel: MagicMock, mock_excel_data: DataFrame) -> None:
    mock_read_excel.return_value = mock_excel_data

    result = get_transactions_from_excel_file("fake_path.xlsx")
    assert len(result) == 2
    assert result[0]["id"] == "650703"
    assert result[0]["state"] == "EXECUTED"
    assert result[0]["date"] == "2023-09-05T11:30:32Z"
    assert result[0]["operationAmount"]["amount"] == "16210"
    assert result[0]["operationAmount"]["currency"]["code"] == "Sol"
    assert result[0]["operationAmount"]["currency"]["name"] == "PEN"
    assert result[0]["from"] == "Счет 58803664561298323391"
    assert result[0]["to"] == "Счет 39745660563456619397"
    assert result[0]["description"] == "Перевод организации"


@patch("src.utils.logger")
@patch("src.utils.pd.read_excel", side_effect=FileNotFoundError)
def test_get_transactions_from_excel_file_file_not_found(mock_read_excel: MagicMock, mock_logger: MagicMock) -> None:
    result = get_transactions_from_excel_file("nonexistent_file.xlsx")
    assert result == []
    mock_logger.error.assert_called_with("Файл не найден")


@patch("src.utils.logger")
@patch("src.utils.pd.read_excel", side_effect=Exception("Непредвиденная ошибка"))
def test_get_transactions_from_excel_file_generic_error(mock_read_excel: MagicMock, mock_logger: MagicMock) -> None:
    result = get_transactions_from_excel_file("error_file.xlsx")
    assert result == []
    mock_logger.error.assert_called_with("Произошла ошибка: Непредвиденная ошибка")
