"""
Демо деректер генераторы - Задания 4-8 үшін
Sample data generator for testing Tasks 4-8
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data():
    """Тапсырмалар үшін демо деректер құрау"""
    
    print("Демо деректер генерирленуде...")
    
    # 1. TRANSACTIONS таблицасы
    np.random.seed(42)
    n_transactions = 10000
    
    transactions = pd.DataFrame({
        'transaction_id': range(1, n_transactions + 1),
        'customer_id': np.random.randint(1000, 2000, n_transactions),
        'tr_datetime': [datetime(2021, 1, 1) + timedelta(minutes=x) for x in range(n_transactions)],
        'amount': np.random.normal(0, 5000, n_transactions),
        'region': np.random.choice(['North', 'South', 'East', 'West', 'Center'], n_transactions),
        'tr_type': np.random.choice(['type_a', 'type_b', 'type_c', 'type_d', 'type_e'], n_transactions),
        'mcc_code': np.random.choice(['5411', '5412', '5413', '5414', '5415'], n_transactions),
    })
    
    # 2. GENDER_TRAIN таблицасы
    customers = transactions['customer_id'].unique()
    gender_train = pd.DataFrame({
        'customer_id': customers,
        'gender': np.random.choice([0, 1], len(customers))  # 0 = female, 1 = male
    })
    
    # 3. TR_MCC_CODES таблицасы
    tr_mcc_codes = pd.DataFrame({
        'mcc_code': ['5411', '5412', '5413', '5414', '5415'],
        'mcc_description': [
            'Grocery stores and supermarkets',
            'Convenience stores',
            'Bakeries',
            'Butcher shops',
            'Fish and seafood shops'
        ]
    })
    
    # 4. TR_TYPES таблицасы
    tr_types = pd.DataFrame({
        'tr_type': ['type_a', 'type_b', 'type_c', 'type_d', 'type_e'],
        'tr_type_name': [
            'Cash withdrawal',
            'Card payment',
            'Transfer',
            'Deposit',
            'Fee'
        ]
    })
    
    # Файлдарды сақтау
    transactions.to_csv('transactions.csv', index=False)
    print(f"✓ transactions.csv сохранен ({len(transactions)} строк)")
    
    gender_train.to_csv('gender_train.csv', index=False)
    print(f"✓ gender_train.csv сохранен ({len(gender_train)} строк)")
    
    tr_mcc_codes.to_csv('tr_mcc_codes.csv', index=False)
    print(f"✓ tr_mcc_codes.csv сохранен ({len(tr_mcc_codes)} строк)")
    
    tr_types.to_csv('tr_types.csv', index=False)
    print(f"✓ tr_types.csv сохранен ({len(tr_types)} строк)")
    
    print("\n✅ Демо деректер сәтті құрылды!")
    print("\nТеперь можно запустить:")
    print("  python3 master_analysis.py")
    
    return transactions, gender_train, tr_mcc_codes, tr_types


if __name__ == '__main__':
    generate_sample_data()
