import os

import requests
from dotenv import load_dotenv
from pprint import pprint

from data.downloaded_data import currencies_vs_usd, stocks_from_user_list
from src.logger import logger_setup

logger = logger_setup("external_api")

load_dotenv()


def get_currencies_rates(currency: str) -> dict:
    """Вернуть текущий курс по валюте с https://api.apilayer.com"""
    # Для возможности тестирования приходится присвоение api-ключа делать внутри функции,
    # иначе придется светить его в тестах
    apilayer_api_key = os.getenv("API_KEY")

    # Возвращает только валюты относительно USD независимо от параметров после "?"
    url = f"https://api.apilayer.com/currency_data/live?base=RUB&symbols=EUR,USD"
    headers = {"apikey": apilayer_api_key}
    payload: dict[str, str] = {}

    # API запрос
    response = requests.request("GET", url, headers=headers, data=payload)
    status_code = response.status_code
    print(f"Статус запроса курса конвертации: {status_code}")

    # Имитация запроса по API
    # result = currencies_vs_usd

    result = response.json()

    # pprint(result)
    result = {'RUBUSD': result['quotes']['USDRUB'],
              'RUBEUR': round(result['quotes']['USDRUB']/result['quotes']['USDEUR'], 2)
              }
    logger.info(f"Результат запроса: {result}")
    return result


def get_symbols_rates(symbol: str) -> list:
    """Вернуть список актуальной информации по тикерам с сайта https://api.marketstack.com/v2/eod/latest"""
    # Для возможности тестирования приходится присвоение api-ключа делать внутри функции,
    # иначе придется светить его в тестах
    apilayer_api_key = os.getenv("MARKETSTACK_API_KEY")

    # url = f"https://api.apilayer.com/currency_data/convert?to={currency}&from={form_currency}&amount={amount}"
    # url = f"https://api.currencylayer.com/live?access_key={apilayer_api_key}&source=RUB&currencies={currency}"
    # "AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"
    url = f"https://api.marketstack.com/v2/eod/latest?access_key={apilayer_api_key}&symbols={symbol}"
    headers = {"apikey": apilayer_api_key}
    payload: dict[str, str] = {}

    # API запрос
    response = requests.request("GET", url)
    status_code = response.status_code
    print(f"Статус запроса курса конвертации: {status_code}")

    # Имитация запроса по API
    # response = stocks_from_user_list
    # result = stocks_from_user_list

    result = response.json()

    # pprint(result)
    stocks = []
    for stock in result['data']:
        brief = {'stock': stock['symbol'], 'price': stock['close']}
        stocks.append(brief)
    logger.info(f"Результат запроса: {stocks}")
    return stocks


# !!!КОЛИЧЕСТВО ЗАПРОСОВ ОГРАНИЧЕНО 100 В МЕСЯЦ работаем с файлом

# Вызов функции конвертации 12`000 руб в $
# print(convert_currency("12000", "RUB", "USD"))

# Вызов информации по списку тикеров
# print(get_symbols_rates("AAPL,AMZN,GOOGL,MSFT,TSLA"))

# Вызов обменного курса мировых валют к USD
# print(get_currencies_rates("USD"))