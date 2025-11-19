"""Задание 8: Анализ ночных транзакций со тратами по полам"""
import os
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Ensure outputs directory exists
os.makedirs('outputs', exist_ok=True)


def task8_part1(transactions):
    """
    Из поля tr_datetime выделите час tr_hour, в который произошла транзакция,
    как первые 2 цифры до ":".
    """
    print("\n=== ЗАДАНИЕ 8, ЧАСТЬ 1 ===")
    print("Выделение часа из datetime поля")
    
    # Преобразуем tr_datetime в datetime если это необходимо
    if transactions['tr_datetime'].dtype == 'object':
        transactions['tr_datetime'] = pd.to_datetime(transactions['tr_datetime'])
    
    # Выделяем час (первые 2 цифры до ":")
    transactions['tr_hour'] = transactions['tr_datetime'].dt.strftime('%H').astype(int)
    
    print("\nВыборка данных с выделенным часом:")
    print(transactions[['tr_datetime', 'tr_hour']].head(10))
    # Save a sample with tr_hour
    try:
        transactions[['tr_datetime', 'tr_hour']].head(100).to_csv('outputs/task8_part1_sample_with_hour.csv', index=False)
    except Exception:
        pass

    return transactions


def task8_part2(transactions):
    """
    Посчитайте количество транзакций со значением в столбце amount строго меньше 0 
    в ночное время для мужчин и женщин. 
    Ночное время – это промежуток с 00:00 по 06:00 часов.
    """
    print("\n=== ЗАДАНИЕ 8, ЧАСТЬ 2 ===")
    print("Количество ночных транзакций со тратами (amount < 0) по полам")
    
    # Проверяем наличие tr_hour, если нет - создаем
    if 'tr_hour' not in transactions.columns:
        if transactions['tr_datetime'].dtype == 'object':
            transactions['tr_datetime'] = pd.to_datetime(transactions['tr_datetime'])
        transactions['tr_hour'] = transactions['tr_datetime'].dt.strftime('%H').astype(int)
    
    # Выбираем ночные часы (0-5, то есть 00:00 по 05:59)
    night_hours = range(0, 6)
    night_transactions = transactions[
        (transactions['tr_hour'].isin(night_hours)) & 
        (transactions['amount'] < 0)
    ]
    
    # Группируем по полу
    result = night_transactions.groupby('gender').size()
    
    print("\nКоличество ночных транзакций со тратами по полам:")
    print(result)
    
    # Дополнительная статистика
    print("\nДополнительная информация:")
    total_night = len(night_transactions)
    print(f"Всего ночных транзакций со тратами: {total_night}")
    
    # Процент от всех транзакций со тратами
    all_spendings = transactions[transactions['amount'] < 0]
    percentage = (total_night / len(all_spendings) * 100) if len(all_spendings) > 0 else 0
    print(f"Процент от всех транзакций со тратами: {percentage:.2f}%")
    
    # По часам в ночное время
    night_by_hour = night_transactions.groupby('tr_hour').size()
    print("\nРаспределение ночных транзакций по часам:")
    print(night_by_hour)
    # Save counts by gender and by hour
    try:
        result.to_csv('outputs/task8_part2_counts_by_gender.csv')
    except Exception:
        # if result is a Series without name
        try:
            pd.DataFrame(result).to_csv('outputs/task8_part2_counts_by_gender.csv')
        except Exception:
            pass

    try:
        night_by_hour.to_csv('outputs/task8_part2_night_by_hour.csv')
    except Exception:
        pass

    # Plot gender counts
    try:
        ax = result.plot(kind='bar', title='Task8 Part2: night spendings count by gender')
        ax.set_ylabel('count')
        plt.tight_layout()
        plt.savefig('outputs/task8_part2_counts_by_gender.png')
        plt.close()
    except Exception:
        pass

    # Plot hourly distribution
    try:
        ax = night_by_hour.plot(kind='bar', title='Task8 Part2: night transactions by hour')
        ax.set_xlabel('hour')
        ax.set_ylabel('count')
        plt.tight_layout()
        plt.savefig('outputs/task8_part2_night_by_hour.png')
        plt.close()
    except Exception:
        pass

    return result


def main():
    print("Задание 8 требует объединенной таблицы с полом и datetime полем")
    print("\nПример использования:")
    print("""
    # Объединяем таблицы согласно инструкции
    transactions = pd.merge(transactions, gender_train, how='left')
    transactions = pd.merge(transactions, tr_mcc_codes, how='inner')
    transactions = pd.merge(transactions, tr_types, how='inner')
    
    transactions = task8_part1(transactions)
    result = task8_part2(transactions)
    """)


if __name__ == '__main__':
    main()
