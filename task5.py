"""Задание 5: Разница в тратах и поступлениях по полам"""
import os
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Ensure outputs directory exists
os.makedirs('outputs', exist_ok=True)


def task5_part1(transactions):
    """
    Определите модуль разницы между средними тратами женщин и мужчин
    (трата – отрицательное значение в столбце amount).
    """
    print("\n=== ЗАДАНИЕ 5, ЧАСТЬ 1 ===")
    print("Модуль разницы между средними тратами женщин и мужчин")
    
    # Выбираем только траты (amount < 0)
    spendings = transactions[transactions['amount'] < 0].copy()
    
    # Группируем по полу и считаем среднее
    avg_by_gender = spendings.groupby('gender')['amount'].mean()
    
    print("\nСредние траты по полам:")
    print(avg_by_gender)
    
    # Вычисляем модуль разницы
    if len(avg_by_gender) == 2:
        diff = abs(avg_by_gender.iloc[0] - avg_by_gender.iloc[1])
        print(f"\nМодуль разницы между средними тратами: {diff:.2f}")

        # Save averages and difference
        avg_by_gender.to_csv('outputs/task5_part1_avg_by_gender.csv')
        with open('outputs/task5_part1_diff.txt', 'w') as f:
            f.write(str(diff))

        # Plot
        try:
            ax = avg_by_gender.plot(kind='bar', title='Task5 Part1: average spendings by gender', rot=0)
            ax.set_ylabel('average amount')
            plt.tight_layout()
            plt.savefig('outputs/task5_part1.png')
            plt.close()
        except Exception:
            pass

        return diff
    else:
        print("Недостаточно данных по полам")
        return None


def task5_part2(transactions):
    """
    Определите модуль разницы между средними поступлениями у мужчин и женщин.
    """
    print("\n=== ЗАДАНИЕ 5, ЧАСТЬ 2 ===")
    print("Модуль разницы между средними поступлениями у мужчин и женщин")
    
    # Выбираем только поступления (amount > 0)
    incomes = transactions[transactions['amount'] > 0].copy()
    
    # Группируем по полу и считаем среднее
    avg_by_gender = incomes.groupby('gender')['amount'].mean()
    
    print("\nСредние поступления по полам:")
    print(avg_by_gender)
    
    # Вычисляем модуль разницы
    if len(avg_by_gender) == 2:
        diff = abs(avg_by_gender.iloc[0] - avg_by_gender.iloc[1])
        print(f"\nМодуль разницы между средними поступлениями: {diff:.2f}")

        # Save averages and diff
        avg_by_gender.to_csv('outputs/task5_part2_avg_by_gender.csv')
        with open('outputs/task5_part2_diff.txt', 'w') as f:
            f.write(str(diff))

        try:
            ax = avg_by_gender.plot(kind='bar', title='Task5 Part2: average incomes by gender', rot=0)
            ax.set_ylabel('average amount')
            plt.tight_layout()
            plt.savefig('outputs/task5_part2.png')
            plt.close()
        except Exception:
            pass

        return diff
    else:
        print("Недостаточно данных по полам")
        return None


def main():
    print("Задание 5 требует объединенной таблицы с полом")
    print("\nПример использования:")
    print("""
    # Объединяем таблицы согласно инструкции
    transactions = pd.merge(transactions, gender_train, how='left')
    transactions = pd.merge(transactions, tr_mcc_codes, how='inner')
    transactions = pd.merge(transactions, tr_types, how='inner')
    
    result1 = task5_part1(transactions)
    result2 = task5_part2(transactions)
    """)


if __name__ == '__main__':
    main()
