
import os
import sys
import matplotlib.pyplot as plt
from data_load import load_data


def main(path: str):
    df = load_data(path)

    if 'Дата' not in df.columns:
        print('В файле нет колонки "Дата". Выход.')
        return

    # Группируем по дате
    agg = df.groupby('Дата', as_index=True)[['Показы', 'Клики']].sum()

    # Создаём выходную папку
    out_dir = 'outputs'
    os.makedirs(out_dir, exist_ok=True)

    # Сохраняем агрегат
    agg_csv = os.path.join(out_dir, 'time_series_agg.csv')
    agg.to_csv(agg_csv, index=True)
    print(f'Агрегированные данные сохранены: {agg_csv}')

    # Рисуем: пытаемся использовать seaborn (если установлен), иначе используем доступный matplotlib-стиль
    try:
        import seaborn as sns
        sns.set_theme(style='darkgrid')
    except Exception:
        # fallback: выбрать известный стиль из available или 'classic'
        available = plt.style.available
        fallback = 'ggplot' if 'ggplot' in available else (available[0] if available else 'classic')
        plt.style.use(fallback)
    fig, ax = plt.subplots(figsize=(10, 5))
    if 'Показы' in agg.columns:
        ax.plot(agg.index, agg['Показы'], label='Показы', marker='o')
    if 'Клики' in agg.columns:
        ax.plot(agg.index, agg['Клики'], label='Клики', marker='o')

    ax.set_title('Показы и клики по датам')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Число')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    out_png = os.path.join(out_dir, 'time_series.png')
    fig.savefig(out_png)
    print(f'График сохранён: {out_png}')


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '2023-05-12_2023-06-12_client_login (1).csv'
    main(path)
