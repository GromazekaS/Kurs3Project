from src.logger import logger_setup
from src.processing import category_counter, filter_by_state, sort_by_date
from src.utils import get_transactions_from_csv_file, get_transactions_from_excel_file, get_transactions_from_file
from src.widget import check_validity_state, display_transactions

PATH_PREFIX = "data/"
logger = logger_setup("main")


def main() -> None:
    """Основная часть программы!!!"""
    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
        "О каких транзакциях Вы желаете получить информацию:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )
    menu = ["operations.json", "transactions.csv", "transactions_excel.xlsx"]
    menu_choice = int(input("Выберите необходимый пункт меню (1/2/3): "))

    filename = menu[menu_choice - 1]
    logger.info(f"Пользователь выбрал загрузить транзакции из {filename}")
    get_transactions = {
        "operations.json": get_transactions_from_file,
        "transactions.csv": get_transactions_from_csv_file,
        "transactions_excel.xlsx": get_transactions_from_excel_file,
    }
    print(f"Загружаю список транзакций из {PATH_PREFIX + filename}")
    transactions = get_transactions[filename](PATH_PREFIX + filename)
    logger.info(f"Загружено {len(transactions)} транзакций")

    logger.info("Запрашиваем параметр фильтра по статусу транзакции")
    state_checked = False
    while not state_checked:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        state = input("[E]XECUTED/[C]ANCELED/[P]ENDING: ").upper()
        state_checked = check_validity_state(state)
        print(f"Статус: {state_checked}")
        if not state_checked:
            print(f"Статус операции {state} недоступен.")
            state_checked = False

    logger.info(f"Фильтрую транзакции по статусу {state_checked}")
    transactions_by_state = filter_by_state(transactions, state_checked)
    print(len(transactions_by_state))
    logger.info(f"После фильтрации по статусу транзакции осталось {len(transactions_by_state)} записей")
    if len(transactions_by_state) == 0:
        print("Нет транзакций подходящих под выбранные условия")
    else:
        logger.info("Сортировка списка транзакций по дате")
        print("Отсортировать операции по дате?")
        sort_choice = input("Да[Y] / Нет[N]: ")
        if sort_choice in ["y", "Y"]:
            print("Отсортировать по возрастанию?")
            asc_choice = input("Да[Y] / Нет[N]: ")
            if asc_choice in ["y", "Y"]:
                logger.info("Транзакции отсортированы по возрастанию")
                reverse = False
            else:
                logger.info("Транзакции отсортированы по убыванию")
                reverse = True
            transactions_by_state = sort_by_date(transactions_by_state, reverse)
        else:
            logger.info("Транзакции остались без сортировки")

        logger.info("Сортировка по валюте")
        print("Выводить только рублевые транзакции?")
        currency_choice = input("Да[Y] / Нет[N]: ")
        if currency_choice in ["y", "Y"]:
            transactions_by_state = [
                x for x in transactions_by_state if x["operationAmount"]["currency"]["code"] == "RUB"
            ]
            logger.info(f"Оставляем только рублевые операции {len(transactions_by_state)}")

        cat_list = []
        categories = category_counter(transactions_by_state, [])
        print(f"Вывести все категории? - {sum(categories.values())} записей")
        cat_choice = input("Да[Y] / Нет[N]: ")
        if cat_choice in ["y", "Y"]:
            display_transactions(transactions_by_state, "")
        else:
            print("Выберите категории для отображения:")
            for index, category in enumerate(categories):
                print(f"{index + 1}. Вывести категорию '{category}' - {categories[category]} записей")
                cat_list.append(category)
            output_cat_list_choice = input("Введите номер категорий для вывода: ").strip()
            display_transactions(transactions_by_state, cat_list[(int(output_cat_list_choice) - 1)])


if __name__ == "__main__":
    main()
