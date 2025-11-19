"""Runner for Task 8: loads data, prepares table and runs task8 functions.

Usage: run from repository root (Zhasus/) with python3 run_task8.py
This script will read transactions.csv and gender_train.csv, merge them,
call task8_part1 and task8_part2 and report saved output files in outputs/.
"""
import os
import pandas as pd

from task8 import task8_part1, task8_part2


def main():
    cwd = os.getcwd()
    print(f"Running Task 8 runner in: {cwd}")

    # Files expected in current directory
    tx_path = 'transactions.csv'
    gender_path = 'gender_train.csv'

    if not os.path.exists(tx_path):
        print(f"Missing {tx_path} in {cwd}")
        return
    if not os.path.exists(gender_path):
        print(f"Missing {gender_path} in {cwd}")
        return

    print('Loading transactions...')
    transactions = pd.read_csv(tx_path)
    print('Loading gender data...')
    gender = pd.read_csv(gender_path)

    # Merge gender into transactions on customer_id if present
    if 'customer_id' in transactions.columns and 'customer_id' in gender.columns:
        transactions = pd.merge(transactions, gender[['customer_id', 'gender']], on='customer_id', how='left')
        print('Merged gender into transactions.')
    else:
        print('customer_id key missing; proceeding without gender merge.')

    # Run task8 parts
    transactions = task8_part1(transactions)
    res = task8_part2(transactions)

    print('\nTask 8 completed. Saved outputs are in the outputs/ folder.')


if __name__ == '__main__':
    main()
