"""
Примеры использования функций для заданий 4-8
"""

import pandas as pd


# ======= ПРИМЕР 1: Загрузка и подготовка данных =======

def example_data_loading():
    """Пример загрузки и подготовки данных"""
    print("=== ПРИМЕР 1: Загрузка данных ===\n")
    
    # Загрузка файлов
    transactions = pd.read_csv('transactions.csv')
    gender_train = pd.read_csv('gender_train.csv')
    tr_mcc_codes = pd.read_csv('tr_mcc_codes.csv')
    tr_types = pd.read_csv('tr_types.csv')
    
    print(f"Исходные данные:")
    print(f"  transactions: {transactions.shape}")
    print(f"  gender_train: {gender_train.shape}")
    print(f"  tr_mcc_codes: {tr_mcc_codes.shape}")
    print(f"  tr_types: {tr_types.shape}")
    
    # Объединение
    transactions = pd.merge(transactions, gender_train, how='left')
    transactions = pd.merge(transactions, tr_mcc_codes, how='inner')
    transactions = pd.merge(transactions, tr_types, how='inner')
    
    print(f"\nПосле объединения: {transactions.shape}")
    print(f"Столбцы: {list(transactions.columns)}")
    
    return transactions


# ======= ПРИМЕР 2: Задание 4 - Статистика по типам =======

def example_task4_statistics():
    """Пример вычисления среднего и медианы"""
    print("\n=== ПРИМЕР 2: Задание 4 - Статистика ===\n")
    
    transactions = example_data_loading()
    
    # Топ-10 регионов
    top10_regions = transactions.groupby('region')['amount'].sum().nlargest(10)
    print("Топ-10 регионов по сумме транзакций:")
    print(top10_regions)
    
    # Статистика для топ-10
    top10_region_list = top10_regions.index.tolist()
    subset = transactions[transactions['region'].isin(top10_region_list)]
    
    stats = subset.groupby('tr_type')['amount'].agg(['mean', 'median', 'count'])
    print(f"\nСтатистика по типам транзакций (топ-10 регионов):")
    print(stats.head(10))


# ======= ПРИМЕР 3: Задание 5 - Разница по полам =======

def example_task5_gender_difference():
    """Пример вычисления разницы по полам"""
    print("\n=== ПРИМЕР 3: Задание 5 - Разница по полам ===\n")
    
    transactions = example_data_loading()
    
    # Траты (amount < 0)
    spendings = transactions[transactions['amount'] < 0]
    avg_spending = spendings.groupby('gender')['amount'].mean()
    
    print("Средние траты по полам:")
    print(avg_spending)
    
    # Модуль разницы
    if len(avg_spending) >= 2:
        diff = abs(avg_spending.iloc[0] - avg_spending.iloc[1])
        print(f"\nМодуль разницы в тратах: {diff:.2f}")
    
    # Поступления (amount > 0)
    incomes = transactions[transactions['amount'] > 0]
    avg_income = incomes.groupby('gender')['amount'].mean()
    
    print("\nСредние поступления по полам:")
    print(avg_income)
    
    if len(avg_income) >= 2:
        diff = abs(avg_income.iloc[0] - avg_income.iloc[1])
        print(f"\nМодуль разницы в поступлениях: {diff:.2f}")


# ======= ПРИМЕР 4: Задание 6 - Макс доход по типам =======

def example_task6_max_income():
    """Пример анализа максимального дохода"""
    print("\n=== ПРИМЕР 4: Задание 6 - Макс доход ===\n")
    
    transactions = example_data_loading()
    
    # Только поступления
    incomes = transactions[transactions['amount'] > 0]
    
    # Макс доход по типам и полам
    max_income = incomes.groupby(['gender', 'tr_type'])['amount'].max().reset_index()
    max_income = max_income.rename(columns={'amount': 'max_income'})
    
    print("Максимальный доход по типам и полам:")
    print(max_income.head(10))
    
    # Топ-10 с наименьшим макс доходом для каждого пола
    for gender in max_income['gender'].unique():
        subset = max_income[max_income['gender'] == gender]
        top_10_least = subset.nsmallest(10, 'max_income')
        print(f"\nПол {gender}: 10 типов с наименьшим макс доходом")
        print(top_10_least[['tr_type', 'max_income']])


# ======= ПРИМЕР 5: Задание 7 - Разница по MCC =======

def example_task7_mcc_difference():
    """Пример анализа MCC категорий"""
    print("\n=== ПРИМЕР 5: Задание 7 - Разница по MCC ===\n")
    
    transactions = example_data_loading()
    
    # Только траты
    spendings = transactions[transactions['amount'] < 0].copy()
    spendings['abs_amount'] = abs(spendings['amount'])
    
    # Сумма затрат по MCC и полу
    mcc_gender = spendings.groupby(['gender', 'mcc_code', 'mcc_description'])['abs_amount'].sum().reset_index()
    
    # Пивотируем
    pivot = mcc_gender.pivot_table(
        index=['mcc_code', 'mcc_description'],
        columns='gender',
        values='abs_amount',
        fill_value=0
    )
    
    # Разница
    cols = pivot.columns.tolist()
    if len(cols) >= 2:
        pivot['difference'] = abs(pivot[cols[0]] - pivot[cols[1]])
    else:
        pivot['difference'] = pivot[cols[0]]
    
    # Топ-10
    top_10 = pivot.nlargest(10, 'difference')
    print("Топ-10 MCC категорий с наибольшей разницей в тратах:")
    print(top_10)


# ======= ПРИМЕР 6: Задание 8 - Ночные транзакции =======

def example_task8_night_transactions():
    """Пример анализа ночных транзакций"""
    print("\n=== ПРИМЕР 6: Задание 8 - Ночные транзакции ===\n")
    
    transactions = example_data_loading()
    
    # Выделение часа
    if transactions['tr_datetime'].dtype == 'object':
        transactions['tr_datetime'] = pd.to_datetime(transactions['tr_datetime'])
    
    transactions['tr_hour'] = transactions['tr_datetime'].dt.hour
    
    print(f"Диапазон часов: {transactions['tr_hour'].min()}-{transactions['tr_hour'].max()}")
    
    # Ночные траты (00:00-06:00, часы 0-5)
    night_spendings = transactions[
        (transactions['tr_hour'].isin(range(0, 6))) & 
        (transactions['amount'] < 0)
    ]
    
    print(f"\nВсего ночных траты: {len(night_spendings)}")
    
    # По полам
    by_gender = night_spendings.groupby('gender').size()
    print("\nНочные траты по полам:")
    print(by_gender)
    
    # По часам
    by_hour = night_spendings.groupby('tr_hour').size()
    print("\nНочные траты по часам:")
    print(by_hour)


# ======= ПРИМЕР 7: Сохранение результатов =======

def example_save_results():
    """Пример сохранения результатов в CSV"""
    print("\n=== ПРИМЕР 7: Сохранение результатов ===\n")
    
    transactions = example_data_loading()
    
    # Пример 1: Сохранить статистику по типам
    stats = transactions.groupby('tr_type')['amount'].agg(['mean', 'median', 'count'])
    stats.to_csv('task4_statistics.csv')
    print("✓ Сохранено: task4_statistics.csv")
    
    # Пример 2: Сохранить статистику по полам
    by_gender = transactions.groupby('gender')['amount'].describe()
    by_gender.to_csv('task5_gender_stats.csv')
    print("✓ Сохранено: task5_gender_stats.csv")
    
    # Пример 3: Сохранить MCC анализ
    spendings = transactions[transactions['amount'] < 0]
    mcc_stats = spendings.groupby(['gender', 'mcc_code', 'mcc_description'])['amount'].agg(['sum', 'count'])
    mcc_stats.to_csv('task7_mcc_analysis.csv')
    print("✓ Сохранено: task7_mcc_analysis.csv")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ - ЗАДАНИЯ 4-8")
    print("="*70)
    
    try:
        # Запуск всех примеров
        example_data_loading()
        example_task4_statistics()
        example_task5_gender_difference()
        example_task6_max_income()
        example_task7_mcc_difference()
        example_task8_night_transactions()
        example_save_results()
        
        print("\n" + "="*70)
        print("✓ ВСЕ ПРИМЕРЫ ВЫПОЛНЕНЫ УСПЕШНО!")
        print("="*70)
        
    except FileNotFoundError:
        print("\n❌ ОШИБКА: Файлы данных не найдены!")
        print("Убедитесь, что в рабочей директории находятся:")
        print("  - transactions.csv")
        print("  - gender_train.csv")
        print("  - tr_mcc_codes.csv")
        print("  - tr_types.csv")
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
