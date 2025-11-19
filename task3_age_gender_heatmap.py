"""Задание 3: тепловая карта показов/кликов по возрасту и полу.

Скрипт строит pivot table (Возраст x Пол) с суммой показов или кликов и визуализирует
ее через seaborn. Результат сохраняется в outputs/heatmap.png
"""
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_load import load_data


def main(path: str, value_col: str = 'Показы'):
    df = load_data(path)

    if 'Возраст' not in df.columns or 'Пол' not in df.columns:
        print('Требуются колонки "Возраст" и "Пол". Выход.')
        return

    pivot = pd.pivot_table(df, index='Возраст', columns='Пол', values=value_col, aggfunc='sum', fill_value=0)

    out_dir = 'outputs'
    os.makedirs(out_dir, exist_ok=True)

    pivot_csv = os.path.join(out_dir, 'age_gender_pivot.csv')
    pivot.to_csv(pivot_csv)
    print(f'Pivot сохранён: {pivot_csv}')

    plt.figure(figsize=(8, max(4, pivot.shape[0] * 0.5)))
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
    plt.title(f'Heatmap: {value_col} по возрасту и полу')
    plt.tight_layout()
    out_png = os.path.join(out_dir, 'age_gender_heatmap.png')
    plt.savefig(out_png)
    print(f'Heatmap сохранён: {out_png}')


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '2023-05-12_2023-06-12_client_login (1).csv'
    main(path)
