import json
import datetime

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from src.external_api import get_currencies_rates, get_symbols_rates
from src.logger import logger_setup

from pprint import pprint


logger = logger_setup("utils")

def get_transactions_from_jsonfile(path: str) -> dict:
    """Прочитать json-файл по указанному пути, вернуть список транзакций"""
    # Если try не выполнится, функция вернет пустой список
    data = []
    try:
        # Пробуем открыть файл
        logger.info(f"Считываем файл {path}")
        with open(path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        # Проверка структуры данных
        # logger.info("Проверяем структуру считанных данных в файле")
        # if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        #     logger.info("Успешно загружено {} записей".format(len(data)))
        # else:
        #     logger.warning("Файл имеет некорректную структуру")
        #     data = []

    except FileNotFoundError:
        logger.error("Файл не найден")
    except json.JSONDecodeError:
        logger.error("Ошибка разбора JSON")
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
    logger.info("Завершение обработки файла")
    return data


def get_transactions_from_excel_file(path: str) -> pd.DataFrame:
    """Прочитать excel-файл по указанному пути, вернуть список транзакций"""
    # Если try не выполнится, функция вернет пустой список
    # result_list = []
    excel_data = pd.DataFrame()
    try:
        # Пробуем открыть файл
        logger.info(f"Считываем файл excel {path}")
        excel_data = pd.read_excel(path, dtype=str)

        excel_data["Номер карты"] = (
            excel_data["Номер карты"]
            .str.replace("*", "", regex=False)  # Удалить *
        )

        # Преобразуем считанные строковые данные в дробные
        excel_data["Сумма операции"] = (
            excel_data["Сумма операции"]
            .str.replace(" ", "", regex=False)  # Удалить пробелы
            .str.replace(",", ".", regex=False)  # Заменить запятые на точки
            .astype(float)
        )

        excel_data["Сумма платежа"] = (
            excel_data["Сумма платежа"]
            .str.replace(" ", "", regex=False)  # Удалить пробелы
            .str.replace(",", ".", regex=False)  # Заменить запятые на точки
            .astype(float)
        )

        excel_data["Бонусы (включая кэшбэк)"] = (
            excel_data["Бонусы (включая кэшбэк)"]
            .str.replace(" ", "", regex=False)  # Удалить пробелы
            .str.replace(",", ".", regex=False)  # Заменить запятые на точки
            .astype(float)
        )

        excel_data["Округление на инвесткопилку"] = (
            excel_data["Округление на инвесткопилку"]
            .str.replace(" ", "", regex=False)  # Удалить пробелы
            .str.replace(",", ".", regex=False)  # Заменить запятые на точки
            .astype(float)
        )

        excel_data["Сумма операции с округлением"] = (
            excel_data["Сумма операции с округлением"]
            .str.replace(" ", "", regex=False)  # Удалить пробелы
            .str.replace(",", ".", regex=False)  # Заменить запятые на точки
            .astype(float)
        )

        # Преобразуем считанные строковые данные в целые (кэшбэк может быть только целым)
        excel_data["Кэшбэк"] = pd.to_numeric(excel_data["Кэшбэк"], errors="coerce").fillna(0).astype(int)

        # logger.info(f"Считано {len(result_list)} записей")
    except FileNotFoundError:
        logger.error("Файл не найден")
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
    logger.info("Завершение обработки файла")
    return excel_data


def greeting() -> str:
    """Вернуть строку-приветствие в зависимости от текущего локального времени суток"""
    hour = datetime.datetime.now().hour
    if hour < 5 or hour > 23: return "Доброй ночи"
    if hour < 11: return "Доброе утро"
    if hour < 17: return "Добрый день"
    return "Добрый вечер"


def brief_info(data: pd.DataFrame) -> str:
    # Требуется дополнительная фильтрация по неисполненным операциям (FAILED)?
    result = data.groupby("Номер карты", as_index=False)[["Сумма платежа", "Кэшбэк"]].sum()
    result = result.rename(columns={
        "Номер карты": "last_digits",
        "Сумма платежа": "total_spent",
        "Кэшбэк": "cashback"
    })
    return result.to_json(orient="records", force_ascii=False)


def top_five_transactions(data: pd.DataFrame) -> list[dict]:
    top_5_expenses = data.sort_values(by="Сумма платежа", ascending=False).head(5)
    result = []
    for i in range(len(top_5_expenses)):
        # print(top_5_expenses.iloc[i])
        row = {
            "date": top_5_expenses.iloc[i]["Дата платежа"],
            "amount": float(top_5_expenses.iloc[i]["Сумма платежа"]),
            "category": top_5_expenses.iloc[i]["Категория"],
            "description": top_5_expenses.iloc[i]["Описание"]
        }
        result.append(row)
    return result


# def get_currency_rates(user_currencies: list) -> list[dict]:
#     print(user_currencies)
#     return []
#
#
# def get_stock_prices(user_stocks: list) -> list[dict]:
#     print(user_stocks)
#     return []


def main_page(data: DataFrame, user_config: dict):
    json_answer= {"greeting" : greeting(),
                  "cards" : brief_info(data),
                  "top_transactions" : top_five_transactions(data),
                  "currency_rates" : get_currencies_rates(",".join(user_config["user_currencies"])),
                  "stock_prices" : get_symbols_rates(",".join(user_config["user_stocks"]))
                  }
    return json_answer


def main():
    """Локальная проверка функций"""
    user_config_filename = 'user_config.json'
    datafile = 'operations.xlsx'
    filepath = '../data/'
    operations = get_transactions_from_excel_file(filepath+datafile)
    user_config = get_transactions_from_jsonfile(filepath+user_config_filename)
    # print(user_config)

    # Страница "Главная"
    main_page_data = main_page(operations, user_config)
    pprint(main_page_data)



if __name__ == "__main__":
    main()
