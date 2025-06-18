import pandas as pd

from datetime import datetime
from typing import Optional

from src.logger import logger_setup
# from src.processing import category_counter, filter_by_state, sort_by_date
# from src.utils import get_transactions_from_csv_file, get_transactions_from_excel_file, get_transactions_from_file
# from src.widget import check_validity_state, display_transactions
from src.utils import main_page, get_transactions_from_jsonfile, get_transactions_from_excel_file
from src.services import search_transactions_to_person
from src.reports import get_expenses_by_category

PATH_PREFIX = "data/"
logger = logger_setup("main")


def get_main_page_data(data_file: str, config_file: str) -> dict:
    """Возвращает данные в формате json для Веб-страницы. Главная"""
    operations = get_transactions_from_excel_file(PATH_PREFIX+data_file)
    user_config = get_transactions_from_jsonfile(PATH_PREFIX+config_file)

    return main_page(operations, user_config)


def get_transactions_to_person(data_file: str) -> list[dict]:
    """Возвращает данные в формате json для страницы Сервисы. Поиск переводов физическим лицам"""
    operations = get_transactions_from_excel_file(PATH_PREFIX+data_file)
    return search_transactions_to_person(operations)


def spending_by_category(data_file: str,
                         category: str,
                         date: Optional[str] = datetime.now()) -> pd.DataFrame:
    operations = get_transactions_from_excel_file(PATH_PREFIX + data_file)
    # categories = operations["Категория"].dropna().unique().tolist()
    # print(categories)
    return get_expenses_by_category(operations, category, date)


def main() -> None:
    """Основная часть программы!!!"""
    data_file = 'operations.xlsx'
    # Веб-страницы. Главная:
    # print(get_main_page_data(data_file, 'user_config.json'))

    # Сервисы. Поиск переводов физическим лицам
    # print(get_transactions_to_person(data_file)[:5:])

    # Отчеты. Траты по категории
    # Список категорий:
    # ['Супермаркеты', 'Различные товары', 'Переводы', 'Каршеринг', 'Пополнения', 'Канцтовары', 'Ж/д билеты', 'Фастфуд',
    #  'Дом и ремонт', 'Аптеки', 'Связь', 'Такси', 'Транспорт', 'Цветы', 'Развлечения', 'Госуслуги', 'Местный транспорт',
    #  'Другое', 'Бонусы', 'Топливо', 'Услуги банка', 'Сервис', 'ЖКХ', 'Детские товары', 'Косметика', 'Одежда и обувь',
    #  'НКО', 'Электроника и техника', 'Наличные', 'Сувениры', 'Мобильная связь', 'Медицина', 'Фото и видео',
    #  'Онлайн-кинотеатры', 'Авиабилеты', 'Образование', 'Рестораны', 'Частные услуги', 'Красота', 'Турагентства',
    #  'Книги', 'Отели', 'Кино', 'Спорттовары', 'Автоуслуги', 'Зарплата', 'Финансы', 'Искусство', 'Duty Free']
    category = "Фастфуд"
    date = "31.01.2020"
    print(spending_by_category(data_file, category, date))


if __name__ == "__main__":
    main()
