from src.logger import logger_setup
from src.utils import main_page, get_transactions_from_jsonfile, get_transactions_from_excel_file
from src.services import search_transactions_to_person
from src.reports import spending_by_category

PATH_PREFIX = "data/"
logger = logger_setup("main")


def main() -> None:
    """Основная часть программы!!!"""
    data_file = 'operations.xlsx'
    config_file = 'user_config.json'
    operations = get_transactions_from_excel_file(PATH_PREFIX + data_file)
    user_config = get_transactions_from_jsonfile(PATH_PREFIX + config_file)
    # Веб-страницы. Главная:
    print(main_page(operations, user_config))

    # Сервисы. Поиск переводов физическим лицам
    print(search_transactions_to_person(operations)[:5:])

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
    print(spending_by_category(operations, category, date))


if __name__ == "__main__":
    main()
