"""Утилита для загрузки и предобработки CSV-данных рекламной выборки.

Функция:
    load_data(path) -> pd.DataFrame

Что делает:
 - читает CSV с разделителем ';'
 - парсит колонку 'Дата' в datetime
 - приводит числовые колонки (Показы, Клики, Расход) к числовым типам
 - заменяет дефис '-' и пустые значения на NaN

Возвращает очищенный DataFrame.
"""
from typing import Optional
import pandas as pd


def load_data(path: str, encoding: Optional[str] = "utf-8") -> pd.DataFrame:
    """Загрузить CSV и выполнить минимальную очистку.

    Аргументы:
        path: путь к CSV-файлу
        encoding: кодировка (по умолчанию utf-8)

    Возвращает:
        pd.DataFrame
    """
    # Читаем файл. В файле числа в некоторых колонках используют запятую как десятичный разделитель.
    df = pd.read_csv(path, sep=';', encoding=encoding, dtype=str)

    # Парсим даты (формат D.M.Y)
    if 'Дата' in df.columns:
        df['Дата'] = pd.to_datetime(df['Дата'], dayfirst=True, errors='coerce')

    # Колонки с числами: "Показы", "Клики"
    for col in ['Показы', 'Клики']:
        if col in df.columns:
            df[col] = df[col].replace({'-': None, '': None})
            df[col] = pd.to_numeric(df[col].str.replace(',', '.', regex=False), errors='coerce')

    # Расход: заменить запятую на точку и приводим к float
    spend_col = 'Расход (руб.)'
    if spend_col in df.columns:
        df[spend_col] = df[spend_col].replace({'-': None, '': None})
        df[spend_col] = df[spend_col].str.replace(',', '.', regex=False)
        df[spend_col] = pd.to_numeric(df[spend_col], errors='coerce')

    # Конверсии: привести '-' в NaN
    if 'Конверсии' in df.columns:
        df['Конверсии'] = df['Конверсии'].replace({'-': None, '': None})

    # Удалим полностью пустые строки (все значения NaN)
    df = df.dropna(how='all')

    return df


if __name__ == '__main__':
    # маленький самопроверочный запуск
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else '2023-05-12_2023-06-12_client_login (1).csv'
    df = load_data(path)
    print('\nФайл загружен. Формат и первые строки:')
    print(df.info())
    print(df.head())
