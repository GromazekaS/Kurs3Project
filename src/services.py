import pandas as pd
import re
from src.logger import logger_setup
from src.utils import get_transactions_from_excel_file

from pprint import pprint


logger = logger_setup("services")


def search_transactions_to_person(data: pd.DataFrame) -> list[dict]:
    # 1. Отбираем по категории "Переводы"
    filtered = data[data["Категория"] == "Переводы"]

    # 2. Применяем фильтр по описанию: имя и инициал (например: Иван П.)
    # Паттерн: одно слово с заглавной + пробел + одна заглавная + точка
    name_pattern = re.compile(r"^[А-Я][а-я]+ [А-Я]\.$")

    # 3. Применяем фильтрацию с использованием .str.match + .fillna("")
    filtered = filtered[filtered["Описание"].fillna("").str.match(name_pattern)]
    # print(filtered.head(5))

    # 4. Преобразуем в JSON
    return filtered.to_dict(orient="records")


def main() -> None:
    """Локальная проверка работы функций"""
    data = get_transactions_from_excel_file('../data/operations.xlsx')
    result = search_transactions_to_person(data)
    pprint(result[-5::])


if __name__ == '__main__':
    main()
