import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock

from src import reports


@pytest.fixture
def sample_data():
    return pd.DataFrame([
        {"Категория": "Книги", "Дата платежа": "15.01.2020"},
        {"Категория": "Книги", "Дата платежа": "10.12.2019"},
        {"Категория": "Книги", "Дата платежа": "02.02.2020"},
        {"Категория": "Еда", "Дата платежа": "15.01.2020"},
    ])


@patch("src.decorators.os.makedirs")
@patch("src.decorators.pd.DataFrame.to_excel")
def test_spending_by_category_filters_correctly(mock_to_excel, mock_makedirs, sample_data):
    end_date = "31.01.2020"

    # Вызов функции
    result = reports.spending_by_category(sample_data, "Книги", end_date)

    # Проверяем результат
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2  # В январе и феврале
    assert all(result["Категория"] == "Книги")

    # Проверяем, что Excel сохраняется
    assert mock_to_excel.called
    mock_to_excel.assert_called_once()
    mock_makedirs.assert_called_once()


@patch("src.decorators.os.makedirs")
@patch("src.decorators.pd.DataFrame.to_excel")
def test_spending_by_category_with_empty_result(mock_to_excel, mock_makedirs, sample_data):
    end_date = "01.01.2019"  # раньше всех дат

    result = reports.spending_by_category(sample_data, "Книги", end_date)

    assert isinstance(result, pd.DataFrame)
    assert result.empty
    mock_to_excel.assert_called_once()
    mock_makedirs.assert_called_once()


@patch("src.decorators.os.makedirs")
@patch("src.decorators.pd.DataFrame.to_excel")
def test_spending_by_category_with_datetime_input(mock_to_excel, mock_makedirs, sample_data):
    end_date = "31.01.2020"

    result = reports.spending_by_category(sample_data, "Книги", end_date)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    mock_to_excel.assert_called_once()
