"""Задание 7: Топ-10 категорий с наибольшей разницей в тратах по полам"""
import os
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Ensure outputs directory exists
os.makedirs('outputs', exist_ok=True)


def task7_part1(transactions):
    """
    Найдите суммы затрат по каждой категории (mcc) для мужчин и для женщин.
    """
    print("\n=== ЗАДАНИЕ 7, ЧАСТЬ 1 ===")
    print("Суммы затрат по категориям (MCC) для каждого пола")
    
    # Выбираем только траты (amount < 0)
    spendings = transactions[transactions['amount'] < 0].copy()
    
    # Группируем по полу и категории MCC
    spending_by_mcc = spendings.groupby(['gender', 'mcc_code', 'mcc_description'])['amount'].sum().reset_index()
    spending_by_mcc.columns = ['gender', 'mcc_code', 'mcc_description', 'total_spending']
    
    # Переводим в абсолютные значения для удобства
    spending_by_mcc['total_spending'] = abs(spending_by_mcc['total_spending'])
    
    print(spending_by_mcc.head(20))
    # Save full table and a sample
    try:
        spending_by_mcc.to_csv('outputs/task7_part1_spending_by_mcc.csv', index=False)
        spending_by_mcc.head(20).to_csv('outputs/task7_part1_top20.csv', index=False)
    except Exception:
        pass

    return spending_by_mcc


def task7_part2(transactions):
    """
    Найдите топ-10 категорий с самыми большими относительными модулями разности 
    в тратах для разных полов.
    """
    print("\n=== ЗАДАНИЕ 7, ЧАСТЬ 2 ===")
    print("Топ-10 категорий с наибольшей разницей в тратах между полами")
    
    # Выбираем только траты (amount < 0)
    spendings = transactions[transactions['amount'] < 0].copy()
    
    # Группируем по полу и MCC, считаем сумму
    spending_by_mcc_gender = spendings.groupby(['gender', 'mcc_code', 'mcc_description'])['amount'].sum().reset_index()
    
    # Переводим в абсолютные значения
    spending_by_mcc_gender['abs_spending'] = abs(spending_by_mcc_gender['amount'])
    
    # Пивотируем таблицу
    pivot = spending_by_mcc_gender.pivot_table(
        index=['mcc_code', 'mcc_description'],
        columns='gender',
        values='abs_spending',
        fill_value=0
    )
    
    # Считаем разницу между полами
    genders = list(pivot.columns)
    if len(genders) >= 2:
        pivot['diff'] = abs(pivot[genders[0]] - pivot[genders[1]])
    else:
        pivot['diff'] = pivot.iloc[:, 0]
    
    # Берем топ-10 по разнице
    top_10 = pivot.nlargest(10, 'diff')
    
    print(top_10)
    print("\nОписания MCC-кодов для топ-10 категорий:")
    for idx, row in top_10.iterrows():
        mcc_code, mcc_desc = idx
        print(f"{mcc_code}: {mcc_desc} - разница: {row['diff']:.2f}")
    # Save top10 and plot
    try:
        top_10.to_csv('outputs/task7_part2_top10.csv')
        ax = top_10['diff'].plot(kind='bar', title='Task7 Part2: top10 mcc diff by gender', figsize=(10,6))
        ax.set_ylabel('difference')
        plt.tight_layout()
        plt.savefig('outputs/task7_part2_top10.png')
        plt.close()
    except Exception:
        pass

    return top_10


def main():
    print("Задание 7 требует объединенной таблицы с MCC-кодами и описаниями")
    print("\nПример использования:")
    print("""
    # Объединяем таблицы согласно инструкции
    transactions = pd.merge(transactions, gender_train, how='left')
    transactions = pd.merge(transactions, tr_mcc_codes, how='inner')
    transactions = pd.merge(transactions, tr_types, how='inner')
    
    result1 = task7_part1(transactions)
    result2 = task7_part2(transactions)
    """)


if __name__ == '__main__':
    main()
