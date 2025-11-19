"""Задание 4: Среднее и медиана по amount для транзакций"""
import os
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Ensure outputs directory exists
os.makedirs('outputs', exist_ok=True)

def task4_part1(transactions, top10_regions):
    """
    Найдите среднее арифметическое и медиану по столбцу amount 
    для каждого типа транзакций из топ-10 в Задании 2.
    """
    print("\n=== ЗАДАНИЕ 4, ЧАСТЬ 1 ===")
    print("Среднее и медиана по amount для типов транзакций из топ-10 регионов")
    
    # Фильтруем транзакции из топ-10 регионов
    transactions_top10 = transactions[transactions['region'].isin(top10_regions['region'])]
    
    # Группируем по типу транзакции и считаем среднее и медиану
    result = transactions_top10.groupby('tr_type')['amount'].agg(['mean', 'median'])
    result.columns = ['среднее', 'медиана']
    
    print(result)
    print(f"\nВсего типов транзакций: {len(result)}")
    # Save result
    result.to_csv('outputs/task4_part1.csv')

    # Plot mean and median for types (if not too many)
    try:
        ax = result.plot(kind='bar', rot=45, figsize=(10, 6), title='Task4 Part1: mean and median by tr_type')
        ax.set_ylabel('amount')
        plt.tight_layout()
        plt.savefig('outputs/task4_part1.png')
        plt.close()
    except Exception:
        # plotting best-effort; ignore on failure
        pass

    return result


def task4_part2(transactions, gender_data):
    """
    Найдите среднее арифметическое и медиану по столбцу amount 
    для каждого типа транзакций, совершенных клиентами из Задания 3.
    """
    print("\n=== ЗАДАНИЕ 4, ЧАСТЬ 2 ===")
    print("Среднее и медиана по amount для типов транзакций клиентов из Задания 3")
    
    # Объединяем с gender_data по customer_id (left join)
    transactions_with_gender = pd.merge(
        transactions, 
        gender_data[['customer_id', 'gender']], 
        on='customer_id', 
        how='left'
    )
    
    # Группируем по типу транзакции и считаем среднее и медиану
    result = transactions_with_gender.groupby('tr_type')['amount'].agg(['mean', 'median'])
    result.columns = ['среднее', 'медиана']
    
    print(result)
    print(f"\nВсего типов транзакций: {len(result)}")
    # Save result
    result.to_csv('outputs/task4_part2.csv')

    # Plot mean and median
    try:
        ax = result.plot(kind='bar', rot=45, figsize=(10, 6), title='Task4 Part2: mean and median by tr_type (with gender)')
        ax.set_ylabel('amount')
        plt.tight_layout()
        plt.savefig('outputs/task4_part2.png')
        plt.close()
    except Exception:
        pass

    return result


def main():
    print("Задание 4 требует данных из Задания 2 и 3")
    print("Загрузите файлы transactions.csv, gender_train.csv, tr_types.csv, tr_mcc_codes.csv")
    print("\nПример использования:")
    print("""
    transactions = pd.read_csv('transactions.csv')
    gender_train = pd.read_csv('gender_train.csv')
    
    # Из Задания 2 получаем top10_regions
    top10_regions = transactions.groupby('region')['amount'].sum().nlargest(10)
    
    result1 = task4_part1(transactions, top10_regions)
    result2 = task4_part2(transactions, gender_train)
    """)


if __name__ == '__main__':
    main()
