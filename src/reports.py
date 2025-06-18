import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional

from src.logger import logger_setup
from src.utils import get_transactions_from_excel_file

from pprint import pprint


logger = logger_setup("services")


def get_expenses_by_category(data: pd.DataFrame,
                             category: str,
                             end_date: Optional[str] = datetime.now()) -> pd.DataFrame:
    """
    Эффективная фильтрация транзакций по категории и трехмесячному периоду.

    :param df: DataFrame с колонками "Категория" и "Дата платежа"
    :param category: Название категории
    :param end_date: Конечная дата (строка или datetime)
    :return: Отфильтрованный DataFrame
    """
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date, dayfirst=True)

    # Вычисляем месяцы для фильтрации
    end_period = end_date.to_period("M")
    start_period = (end_date - relativedelta(months=2)).to_period("M")

    # Фильтрация по категории
    filtered = data[data["Категория"] == category].copy()

    # Преобразуем "Дата платежа" в period("M"), чтобы сравнивать по месяцам
    filtered["Дата платежа"] = pd.to_datetime(filtered["Дата платежа"], errors='coerce', dayfirst=True)
    filtered["Месяц платежа"] = filtered["Дата платежа"].dt.to_period("M")

    # Фильтрация по месячному периоду
    mask = (filtered["Месяц платежа"] >= start_period) & (filtered["Месяц платежа"] <= end_period)
    return filtered[mask].drop(columns=["Месяц платежа"])


def main() -> None:
    """Локальная проверка работы функций"""
    data = get_transactions_from_excel_file('../data/operations.xlsx')
    result = get_expenses_by_category(data, "Фастфуд", "31.01.2020")
    print(result[-5::])


if __name__ == '__main__':
    main()
