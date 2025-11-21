"""
Мастер-скрипт для выполнения заданий 4-8
Объединяет все тапсырмалар (задания) в одной программе
"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def load_data():
    """Загрузка всех необходимых данных"""
    print("Загрузка данных...")
    
    # Загружаем основные файлы
    transactions = pd.read_csv('transactions.csv')
    gender_train = pd.read_csv('gender_train.csv')
    tr_mcc_codes = pd.read_csv('tr_mcc_codes.csv')
    tr_types = pd.read_csv('tr_types.csv')
    
    print(f"✓ Транзакции: {transactions.shape[0]} строк")
    print(f"✓ Пол: {gender_train.shape[0]} строк")
    print(f"✓ MCC коды: {tr_mcc_codes.shape[0]} строк")
    print(f"✓ Типы транзакций: {tr_types.shape[0]} строк")
    
    return transactions, gender_train, tr_mcc_codes, tr_types


def prepare_merged_data(transactions, gender_train, tr_mcc_codes, tr_types):
    """Объединение всех таблиц согласно инструкции"""
    print("\nОбъединение таблиц...")
    
    # Левое объединение с gender_train
    transactions = pd.merge(transactions, gender_train, how='left')
    print(f"✓ После left join с gender_train: {transactions.shape[0]} строк")
    
    # Внутреннее объединение с tr_mcc_codes
    transactions = pd.merge(transactions, tr_mcc_codes, how='inner')
    print(f"✓ После inner join с tr_mcc_codes: {transactions.shape[0]} строк")
    
    # Внутреннее объединение с tr_types
    transactions = pd.merge(transactions, tr_types, how='inner')
    print(f"✓ После inner join с tr_types: {transactions.shape[0]} строк")
    
    print(f"\nИтого: {transactions.shape} (ожидается 999584 строк)")
    
    return transactions


# ============== ЗАДАНИЕ 4 ==============
def task4(transactions):
    """Среднее и медиана по amount для типов транзакций"""
    print("\n" + "="*60)
    print("ЗАДАНИЕ 4: Среднее и медиана по amount")
    print("="*60)
    
    # Часть 1: Топ регионы
    print("\n--- ЧАСТЬ 1: Топ-10 регионов ---")
    top10_regions = transactions.groupby('region')['amount'].sum().nlargest(10).index.tolist()
    print(f"Топ-10 регионов: {top10_regions}")
    
    transactions_top10 = transactions[transactions['region'].isin(top10_regions)]
    result1 = transactions_top10.groupby('tr_type')['amount'].agg(['mean', 'median'])
    result1.columns = ['среднее', 'медиана']
    print("\nСреднее и медиана по типам транзакций в топ-10 регионах:")
    print(result1)
    
    # Часть 2: По полу
    print("\n--- ЧАСТЬ 2: По полу из всех данных ---")
    result2 = transactions.groupby(['gender', 'tr_type'])['amount'].agg(['mean', 'median'])
    print("\nСреднее и медиана по полу и типам транзакций:")
    print(result2)
    
    return result1, result2


# ============== ЗАДАНИЕ 5 ==============
def task5(transactions):
    """Разница между средними тратами и поступлениями по полам"""
    print("\n" + "="*60)
    print("ЗАДАНИЕ 5: Разница в тратах и поступлениях по полам")
    print("="*60)
    
    # Часть 1: Траты
    print("\n--- ЧАСТЬ 1: Среднее по тратам ---")
    spendings = transactions[transactions['amount'] < 0].copy()
    avg_spending = spendings.groupby('gender')['amount'].mean()
    print("Средние траты по полам:")
    print(avg_spending)
    
    if len(avg_spending) == 2:
        diff_spending = abs(avg_spending.iloc[0] - avg_spending.iloc[1])
        print(f"\n✓ Модуль разницы в тратах: {diff_spending:.2f}")
    
    # Часть 2: Поступления
    print("\n--- ЧАСТЬ 2: Среднее по поступлениям ---")
    incomes = transactions[transactions['amount'] > 0].copy()
    avg_income = incomes.groupby('gender')['amount'].mean()
    print("Средние поступления по полам:")
    print(avg_income)
    
    if len(avg_income) == 2:
        diff_income = abs(avg_income.iloc[0] - avg_income.iloc[1])
        print(f"\n✓ Модуль разницы в поступлениях: {diff_income:.2f}")
    
    return avg_spending, avg_income


# ============== ЗАДАНИЕ 6 ==============
def task6(transactions):
    """Максимальный доход по типам транзакций для разных полов"""
    print("\n" + "="*60)
    print("ЗАДАНИЕ 6: Макс доход по типам и полам")
    print("="*60)
    
    # Часть 1: Макс доход по типам
    print("\n--- ЧАСТЬ 1: Топ-10 типов с наименьшим макс доходом ---")
    income_trans = transactions[transactions['amount'] > 0].copy()
    max_income = income_trans.groupby(['gender', 'tr_type'])['amount'].max().reset_index()
    max_income.columns = ['gender', 'tr_type', 'max_income']
    
    result = {}
    for gender in max_income['gender'].unique():
        gender_data = max_income[max_income['gender'] == gender]
        top_10 = gender_data.nsmallest(10, 'max_income')
        result[gender] = top_10
        print(f"\nПол: {gender}")
        print(top_10[['tr_type', 'max_income']])
    
    # Часть 2: Общие типы
    print("\n--- ЧАСТЬ 2: Типы транзакций в обоих полах ---")
    genders = list(result.keys())
    if len(genders) >= 2:
        types1 = set(result[genders[0]]['tr_type'])
        types2 = set(result[genders[1]]['tr_type'])
        common = types1.intersection(types2)
        print(f"Общие типы: {common}")
        print(f"Количество общих типов: {len(common)}")
    
    return result


# ============== ЗАДАНИЕ 7 ==============
def task7(transactions):
    """Топ-10 категорий с наибольшей разницей в тратах по полам"""
    print("\n" + "="*60)
    print("ЗАДАНИЕ 7: Разница в тратах по MCC категориям")
    print("="*60)
    
    # Часть 1: Суммы по категориям
    print("\n--- ЧАСТЬ 1: Суммы затрат по MCC ---")
    spendings = transactions[transactions['amount'] < 0].copy()
    spending_mcc = spendings.groupby(['gender', 'mcc_code', 'mcc_description'])['amount'].sum().reset_index()
    spending_mcc['total_spending'] = abs(spending_mcc['amount'])
    print(f"Всего категорий: {spending_mcc['mcc_code'].nunique()}")
    print("\nПримеры:")
    print(spending_mcc.head(10))
    
    # Часть 2: Топ-10 по разнице
    print("\n--- ЧАСТЬ 2: Топ-10 категорий с наибольшей разницей ---")
    spending_pivot = spending_mcc.pivot_table(
        index=['mcc_code', 'mcc_description'],
        columns='gender',
        values='total_spending',
        fill_value=0
    )
    
    genders = list(spending_pivot.columns)
    if len(genders) >= 2:
        spending_pivot['diff'] = abs(spending_pivot[genders[0]] - spending_pivot[genders[1]])
    else:
        spending_pivot['diff'] = spending_pivot.iloc[:, 0]
    
    top_10_mcc = spending_pivot.nlargest(10, 'diff')
    print("\nТоп-10 MCC категорий с наибольшей разницей:")
    for idx, row in top_10_mcc.iterrows():
        mcc_code, mcc_desc = idx
        print(f"{mcc_code}: {mcc_desc}")
        print(f"  Разница: {row['diff']:.2f}")
    
    return spending_mcc, top_10_mcc


# ============== ЗАДАНИЕ 8 ==============
def task8(transactions):
    """Анализ ночных транзакций со тратами по полам"""
    print("\n" + "="*60)
    print("ЗАДАНИЕ 8: Ночные транзакции (00:00-06:00)")
    print("="*60)
    
    # Часть 1: Выделение часа
    print("\n--- ЧАСТЬ 1: Выделение часа из datetime ---")
    if transactions['tr_datetime'].dtype == 'object':
        transactions['tr_datetime'] = pd.to_datetime(transactions['tr_datetime'])
    
    transactions['tr_hour'] = transactions['tr_datetime'].dt.hour
    print("Часы выделены успешно")
    print(f"Диапазон часов: {transactions['tr_hour'].min()}-{transactions['tr_hour'].max()}")
    
    # Часть 2: Ночные траты
    print("\n--- ЧАСТЬ 2: Ночные траты по полам (00:00-06:00) ---")
    night_trans = transactions[
        (transactions['tr_hour'].isin(range(0, 6))) & 
        (transactions['amount'] < 0)
    ]
    
    result = night_trans.groupby('gender').size()
    print("\nКоличество ночных транзакций со тратами по полам:")
    print(result)
    
    # Статистика
    all_spendings = transactions[transactions['amount'] < 0]
    percentage = (len(night_trans) / len(all_spendings) * 100) if len(all_spendings) > 0 else 0
    print(f"\nВсего ночных транзакций со тратами: {len(night_trans)}")
    print(f"Процент от всех транзакций со тратами: {percentage:.2f}%")
    
    # По часам
    print("\nРаспределение по часам:")
    by_hour = night_trans.groupby('tr_hour').size()
    print(by_hour)
    
    return night_trans


def main():
    """Главная функция"""
    print("\n" + "="*60)
    print("КОМПЛЕКСНЫЙ АНАЛИЗ ТРАНЗАКЦИЙ - ЗАДАНИЯ 4-8")
    print("="*60)
    
    try:
        # Загрузка данных
        transactions, gender_train, tr_mcc_codes, tr_types = load_data()
        
        # Подготовка объединенной таблицы
        transactions = prepare_merged_data(transactions, gender_train, tr_mcc_codes, tr_types)
        
        # Выполнение заданий
        result4 = task4(transactions)
        result5 = task5(transactions)
        result6 = task6(transactions)
        result7 = task7(transactions)
        result8 = task8(transactions)
        
        print("\n" + "="*60)
        print("✓ ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
        print("="*60)
        
    except FileNotFoundError as e:
        print(f"\n❌ ОШИБКА: Файл не найден - {e}")
        print("\nУбедитесь, что в рабочей директории находятся файлы:")
        print("  - transactions.csv")
        print("  - gender_train.csv")
        print("  - tr_mcc_codes.csv")
        print("  - tr_types.csv")
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
