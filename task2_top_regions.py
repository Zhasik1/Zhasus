"""Задание 2: топ регионов по показам/кликам.

Скрипт считает суммарные показатели по колонке 'Регион таргетинга' и сохраняет
топ-N в CSV и в виде горизонтальной столбчатой диаграммы.
"""
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
from data_load import load_data


def main(path: str, top_n: int = 20):
    df = load_data(path)
    region_col = 'Регион таргетинга'

    if region_col not in df.columns:
        print(f'В файле нет колонки "{region_col}". Выход.')
        return

    # Агрегируем
    agg = df.groupby(region_col, as_index=True)[['Показы', 'Клики']].sum()
    agg = agg.sort_values('Клики', ascending=False).fillna(0)

    out_dir = 'outputs'
    os.makedirs(out_dir, exist_ok=True)

    top_df = agg.head(top_n)
    top_csv = os.path.join(out_dir, 'top_regions.csv')
    top_df.to_csv(top_csv)
    print(f'Топ регионов сохранён в: {top_csv}')

    # Построение: использовать seaborn, если есть, иначе fallback на доступный matplotlib-стиль
    try:
        import seaborn as sns
        sns.set_theme()
    except Exception:
        available = plt.style.available
        fallback = 'ggplot' if 'ggplot' in available else (available[0] if available else 'classic')
        plt.style.use(fallback)
    fig, ax = plt.subplots(figsize=(10, max(6, top_n * 0.4)))
    top_df['Клики'].sort_values().plot.barh(ax=ax, color='tab:blue')
    ax.set_title(f'Top {top_n} регионов по кликам')
    ax.set_xlabel('Клики')
    plt.tight_layout()
    out_png = os.path.join(out_dir, 'top_regions.png')
    fig.savefig(out_png)
    print(f'График топ регионов сохранён: {out_png}')


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '2023-05-12_2023-06-12_client_login (1).csv'
    main(path)
