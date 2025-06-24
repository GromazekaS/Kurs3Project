import os
from functools import wraps
from typing import Optional, Callable
from datetime import datetime
import pandas as pd

from src.logger import logger_setup


logger = logger_setup("decorators")


def export_to_excel(report_folder: str = "../reports"):
    """Сохранение отчета в файле со сгенерированным названием"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(data: pd.DataFrame, category: str, end_date: Optional[str] = None):
            # Вызов оригинальной функции
            result = func(data, category, end_date)

            # Преобразуем дату
            if end_date is None:
                end_dt = datetime.now()
            elif isinstance(end_date, str):
                end_dt = pd.to_datetime(end_date, dayfirst=True)
            else:
                end_dt = end_date

            # Формируем имя файла
            safe_category = category.replace(" ", "_")  # Убираем пробелы
            date_str = end_dt.strftime("%d-%m-%Y")
            filename = f"{safe_category}_на_{date_str}.xlsx"
            filepath = os.path.join(report_folder, filename)

            # Создаём папку при необходимости
            os.makedirs(report_folder, exist_ok=True)

            # Сохраняем результат
            result.to_excel(filepath, index=False)
            logger.info(f"[✓] Отчёт сохранён в: {filepath}")

            return result
        return wrapper
    return decorator


def default_export_to_excel(filename: str = "../reports/report.xlsx"):
    """Сохранение отчета в файле названием по умолчанию"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(data: pd.DataFrame, category: str, end_date: Optional[str] = None):
            # Вызов оригинальной функции
            result = func(data, category, end_date)

            # Формируем имя файла
            report_folder = "../reports"
            filename = "report.xlsx"
            filepath = os.path.join(report_folder, filename)

            # Создаём папку при необходимости
            os.makedirs(report_folder, exist_ok=True)

            # Сохраняем результат
            result.to_excel(filepath, index=False)
            logger.info(f"[✓] Отчёт сохранён в: {filepath}")

            return result
        return wrapper
    return decorator
