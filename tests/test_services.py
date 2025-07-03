import pandas as pd
import pytest

from src.services import search_transactions_to_person


@pytest.fixture
def test_data():
    return pd.DataFrame([
        {"Категория": "Переводы", "Описание": "Иван П."},
        {"Категория": "Переводы", "Описание": "Мария С."},
        {"Категория": "Переводы", "Описание": "ПЕРЕВОД ОТ ПОЛЬЗОВАТЕЛЯ"},
        {"Категория": "Еда", "Описание": "Иван П."},
        {"Категория": "Переводы", "Описание": "ivan p."},
        {"Категория": "Переводы", "Описание": None},
        {"Категория": "Переводы", "Описание": "Сергей А."},
        {"Категория": "Переводы", "Описание": "Олег"},
    ])


def test_search_transactions_to_person_valid(test_data):
    result = search_transactions_to_person(test_data)

    # Должны остаться только корректные ФИ (всего 3 записи)
    assert isinstance(result, list)
    assert len(result) == 3

    names = [r["Описание"] for r in result]
    assert "Иван П." in names
    assert "Мария С." in names
    assert "Сергей А." in names


def test_search_transactions_to_person_empty_input():
    empty_df = pd.DataFrame(columns=["Категория", "Описание"])
    result = search_transactions_to_person(empty_df)
    assert isinstance(result, list)
    assert result == []


def test_search_transactions_to_person_wrong_category():
    df = pd.DataFrame([
        {"Категория": "Еда", "Описание": "Иван П."},
        {"Категория": "Покупки", "Описание": "Мария С."}
    ])
    result = search_transactions_to_person(df)
    assert result == []
