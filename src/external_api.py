import os

import requests
from dotenv import load_dotenv
from pprint import pprint

from data.downloaded_data import currencies_vs_usd, stocks_from_user_list
from src.logger import logger_setup

logger = logger_setup("external_api")

load_dotenv()


def convert_currency(amount: str, form_currency: str, to_currency: str) -> float:
    """Вернуть сумму после конвертации по текущему курсу на https://api.apilayer.com"""
    # Для возможности тестирования приходится присвоение api-ключа делать внутри функции,
    # иначе придется светить его в тестах
    apilayer_api_key = os.getenv("API_KEY")

    url = f"https://api.apilayer.com/currency_data/convert?to={to_currency}&from={form_currency}&amount={amount}"

    headers = {"apikey": apilayer_api_key}
    payload: dict[str, str] = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    result = response.json()
    # {
    # 'success': True,
    # 'query': {'from': 'EUR', 'to': 'RUB', 'amount': 100},
    # 'info': {'timestamp': 1746107344, 'quote': 92.657461},
    # 'result': 9265.7461}
    print(f"Статус запроса курса конвертации: {status_code}")
    print(f"Результат запроса: {result}")
    return float(result["result"])


def calculate_transaction_amount(transaction: dict, dist_currency: str = "RUB") -> float:
    """Пересчет суммы транзакции в заданной валюте"""
    # pprint(transaction)
    amount = transaction["operationAmount"]["amount"]
    from_cur = transaction["operationAmount"]["currency"]["code"]
    if from_cur == dist_currency:
        res = float(amount)
        print(f"Конвертация не требуется. {amount} {dist_currency}")
    else:
        logger.info(f"Отправляем запрос на конвертацию {amount} {from_cur} в {dist_currency}")
        res = convert_currency(amount, from_cur, dist_currency)
        # По идее надо округлять до 2 цифр после запятой, но с финансовой точки зрения это будет некорректно
        # result = round(convert_currency(amount, from_cur, dist_currency), 2)
        logger.info(f"Получен ответ: {res}.")

    return res

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
    # response = requests.request("GET", url, headers=headers, data=payload)

    # Имитация запроса по API
    response = currencies_vs_usd

    # status_code = response.status_code
    # result = response.json()
    result = currencies_vs_usd
    # pprint(result)
    result = {'RUBUSD': result['quotes']['USDRUB'],
              'RUBEUR': round(result['quotes']['USDRUB']/result['quotes']['USDEUR'], 2)
              }
    # print(f"Статус запроса курса конвертации: {status_code}")
    logger.info(f"Результат запроса: {result}")
    return result


def get_symbols_rates(symbol: str) -> list:
    """Вернуть список актуальной информации с сайта https://api.marketstack.com/v2/eod/latest"""
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
    # response = requests.request("GET", url)

    # Имитация запроса по API
    response = stocks_from_user_list


    # status_code = response.status_code
    # result = response.json()
    result = stocks_from_user_list
    # pprint(result)
    stocks = []
    for stock in result['data']:
        brief = {'stock': stock['symbol'], 'price': stock['close']}
        stocks.append(brief)
    # print(f"Статус запроса курса конвертации: {status_code}")
    logger.info(f"Результат запроса: {stocks}")
    return stocks


# !!!КОЛИЧЕСТВО ЗАПРОСОВ ОГРАНИЧЕНО 100 В МЕСЯЦ работаем с файлом

# Вызов функции конвертации 12`000 руб в $
# print(convert_currency("12000", "RUB", "USD"))

# Вызов информации по списку тикеров
# print(get_symbols_rates("AAPL,AMZN,GOOGL,MSFT,TSLA"))

# Вызов обменного курса мировых валют к USD
# print(get_currencies_rates("USD"))