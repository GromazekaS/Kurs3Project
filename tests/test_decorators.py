import unittest
from unittest.mock import patch, MagicMock

import os
import pandas as pd
from datetime import datetime
from src.decorators import export_to_excel, default_export_to_excel  # замени на свой модуль

class TestExportDecorators(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({"Категория": ["Тест"], "Дата платежа": ["01.01.2021"]})

    @patch("src.decorators.os.makedirs")
    @patch("src.decorators.pd.DataFrame.to_excel")
    @patch("src.decorators.logger")
    def test_export_to_excel_decorator_with_str_date(self, mock_logger, mock_to_excel, mock_makedirs):
        @export_to_excel("../test_reports")
        def dummy_func(data, category, end_date=None):
            return data

        category = "Тест Категория"
        end_date = "15.03.2021"

        result = dummy_func(self.df, category, end_date)

        # Проверки
        mock_makedirs.assert_called_once_with("../test_reports", exist_ok=True)
        mock_to_excel.assert_called_once()

        args, kwargs = mock_to_excel.call_args
        filepath = args[0]
        self.assertIn("Тест_Категория_на_15-03-2021.xlsx", filepath)
        mock_logger.info.assert_called()

        self.assertTrue(result.equals(self.df))

    @patch("src.decorators.os.makedirs")
    @patch("src.decorators.pd.DataFrame.to_excel")
    @patch("src.decorators.logger")
    def test_export_to_excel_decorator_with_none_date(self, mock_logger, mock_to_excel, mock_makedirs):
        @export_to_excel("../test_reports")
        def dummy_func(data, category, end_date=None):
            return data

        result = dummy_func(self.df, "Без даты", None)

        mock_makedirs.assert_called_once()
        mock_to_excel.assert_called_once()
        mock_logger.info.assert_called_once()

        self.assertTrue(result.equals(self.df))

    @patch("src.decorators.os.makedirs")
    @patch("src.decorators.pd.DataFrame.to_excel")
    @patch("src.decorators.logger")
    def test_default_export_to_excel(self, mock_logger, mock_to_excel, mock_makedirs):
        @default_export_to_excel()
        def dummy_func(data, category, end_date=None):
            return data

        result = dummy_func(self.df, "Категория", "10.01.2020")

        mock_makedirs.assert_called_once_with("../reports", exist_ok=True)
#        mock_to_excel.assert_called_once_with("../reports/report.xlsx", index=False)
        expected_path = os.path.normpath("../reports/report.xlsx")
        args, kwargs = mock_to_excel.call_args
        actual_path = os.path.normpath(args[0])

        assert actual_path == expected_path
        assert kwargs == {'index': False}
        mock_logger.info.assert_called_once()

        self.assertTrue(result.equals(self.df))

if __name__ == "__main__":
    unittest.main()
