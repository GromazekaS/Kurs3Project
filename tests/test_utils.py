import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from datetime import datetime

from src import utils  # путь к твоему модулю

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.sample_df = pd.DataFrame({
            "Номер карты": ["1234", "5678"],
            "Сумма платежа": [100.5, 200.0],
            "Кэшбэк": [10, 20],
            "Категория": ["Книги", "Еда"],
            "Дата платежа": ["01.01.2021", "02.02.2021"],
            "Описание": ["Книга", "Фастфуд"]
        })

    # -------- get_transactions_from_jsonfile --------
    @patch("src.utils.open", new_callable=mock_open, read_data='[{"a": 1}]')
    @patch("src.utils.logger")
    def test_get_transactions_json_success(self, mock_logger, mock_file):
        result = utils.get_transactions_from_jsonfile("somefile.json")
        self.assertEqual(result, [{"a": 1}])
        mock_logger.info.assert_called()

    @patch("src.utils.open", side_effect=FileNotFoundError)
    @patch("src.utils.logger")
    def test_get_transactions_json_file_not_found(self, mock_logger, mock_file):
        result = utils.get_transactions_from_jsonfile("missing.json")
        self.assertEqual(result, [])
        mock_logger.error.assert_called_with("Файл не найден")

    @patch("src.utils.open", new_callable=mock_open, read_data='INVALID_JSON')
    @patch("src.utils.logger")
    def test_get_transactions_json_decode_error(self, mock_logger, mock_file):
        result = utils.get_transactions_from_jsonfile("bad.json")
        self.assertEqual(result, [])
        mock_logger.error.assert_called()

    # -------- get_transactions_from_excel_file --------
    @patch("src.utils.pd.read_excel")
    @patch("src.utils.logger")
    def test_get_transactions_from_excel_file(self, mock_logger, mock_read_excel):
        df = pd.DataFrame({
            "Номер карты": ["****1234"],
            "Сумма операции": ["1 234,56"],
            "Сумма платежа": ["1 111,11"],
            "Бонусы (включая кэшбэк)": ["12,00"],
            "Округление на инвесткопилку": ["1,00"],
            "Сумма операции с округлением": ["1234,00"],
            "Кэшбэк": ["5"]
        })
        mock_read_excel.return_value = df

        result = utils.get_transactions_from_excel_file("some_excel.xlsx")
        self.assertEqual(result.shape[0], 1)
        self.assertIn("Сумма платежа", result.columns)
        self.assertAlmostEqual(result["Сумма платежа"].iloc[0], 1111.11)

    # -------- greeting --------
    @patch("src.utils.datetime")
    def test_greeting_morning(self, mock_dt):
        mock_dt.datetime.now.return_value = datetime(2024, 1, 1, 8)
        self.assertEqual(utils.greeting(), "Доброе утро")

    @patch("src.utils.datetime")
    def test_greeting_evening(self, mock_dt):
        mock_dt.datetime.now.return_value = datetime(2024, 1, 1, 21)
        self.assertEqual(utils.greeting(), "Добрый вечер")

    @patch("src.utils.datetime")
    def test_greeting_night(self, mock_dt):
        mock_dt.datetime.now.return_value = datetime(2024, 1, 1, 1)
        self.assertEqual(utils.greeting(), "Доброй ночи")

    # -------- brief_info --------
    def test_brief_info(self):
        result = utils.brief_info(self.sample_df)
        self.assertIsInstance(result, str)
        self.assertIn('"last_digits"', result)
        self.assertIn('"total_spent"', result)

    # -------- top_five_transactions --------
    def test_top_five_transactions(self):
        result = utils.top_five_transactions(self.sample_df)
        self.assertEqual(len(result), 2)
        self.assertIn("category", result[0])
        self.assertIn("amount", result[0])

    # -------- main_page --------
    @patch("src.utils.get_currencies_rates", return_value={"USD": 90})
    @patch("src.utils.get_symbols_rates", return_value={"AAPL": 190})
    @patch("src.utils.greeting", return_value="Доброе утро")
    @patch("src.utils.brief_info", return_value="[]")
    @patch("src.utils.top_five_transactions", return_value=[])
    def test_main_page(self, mock_top, mock_brief, mock_greet, mock_curr, mock_stocks):
        user_config = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
        result = utils.main_page(self.sample_df, user_config)
        self.assertIn("greeting", result)
        self.assertIn("currency_rates", result)
        self.assertEqual(result["currency_rates"], {"USD": 90})

