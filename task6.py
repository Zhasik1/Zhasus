"""Задание 6: Максимальный доход по типам транзакций для разных полов"""
import os
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Ensure outputs directory exists
os.makedirs('outputs', exist_ok=True)


def task6_part1(transactions):
    """
    Для каждого типа транзакций рассчитайте максимальную сумму прихода на карту 
    (из строго положительных сумм по столбцу amount) отдельно для мужчин и женщин.
    Оставьте по 10 типов транзакций для мужчин и для женщин, наименьших среди всех 
    типов транзакций по полученным значениям max_income.
    """
    print("\n=== ЗАДАНИЕ 6, ЧАСТЬ 1 ===")
    print("Топ-10 типов транзакций с наименьшим макс доходом для каждого пола")
    
    # Выбираем только положительные значения (доход)
    income_transactions = transactions[transactions['amount'] > 0].copy()
    
    # Группируем по полу и типу транзакции, берем максимум
    max_income_by_type = income_transactions.groupby(['gender', 'tr_type'])['amount'].max().reset_index()
    max_income_by_type.columns = ['gender', 'tr_type', 'max_income']
    
    # Для каждого пола берем 10 типов с наименьшим max_income
    result = {}
    for gender in max_income_by_type['gender'].unique():
        gender_data = max_income_by_type[max_income_by_type['gender'] == gender]
        top_10 = gender_data.nsmallest(10, 'max_income')
        result[gender] = top_10
        print(f"\nПол: {gender}")
        print(top_10)
        # Save each gender's top10
        try:
            top_10.to_csv(f'outputs/task6_part1_top10_{gender}.csv', index=False)
            ax = top_10.set_index('tr_type')['max_income'].plot(kind='bar', title=f'Task6 Part1: min 10 max_income for {gender}', figsize=(8,5))
            ax.set_ylabel('max_income')
            plt.tight_layout()
            plt.savefig(f'outputs/task6_part1_top10_{gender}.png')
            plt.close()
        except Exception:
            pass
    
    return result


def task6_part2(transactions, task6_part1_result):
    """
    Среди типов транзакций, найденных в пункте 1, выделите те, которые встречаются 
    одновременно и у мужчин, и у женщин.
    """
    print("\n=== ЗАДАНИЕ 6, ЧАСТЬ 2 ===")
    print("Типы транзакций, встречающиеся у обоих полов")
    
    # Получаем типы для каждого пола
    genders = list(task6_part1_result.keys())
    
    if len(genders) >= 2:
        types_gender1 = set(task6_part1_result[genders[0]]['tr_type'])
        types_gender2 = set(task6_part1_result[genders[1]]['tr_type'])
        
        # Пересечение
        common_types = types_gender1.intersection(types_gender2)
        
        print(f"\nОбщие типы транзакций: {common_types}")
        print(f"Количество общих типов: {len(common_types)}")
        # Save common types
        try:
            with open('outputs/task6_part2_common_types.txt', 'w') as f:
                for t in sorted(common_types):
                    f.write(str(t) + "\n")
        except Exception:
            pass

        return common_types
    else:
        print("Недостаточно данных для сравнения полов")
        return set()


def main():
    print("Задание 6 требует объединенной таблицы с полом")
    print("\nПример использования:")
    print("""
    # Объединяем таблицы согласно инструкции
    transactions = pd.merge(transactions, gender_train, how='left')
    transactions = pd.merge(transactions, tr_mcc_codes, how='inner')
    transactions = pd.merge(transactions, tr_types, how='inner')
    
    result1 = task6_part1(transactions)
    result2 = task6_part2(transactions, result1)
    """)


if __name__ == '__main__':
    main()
