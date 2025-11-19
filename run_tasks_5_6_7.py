"""Runner to execute tasks 5, 6, and 7 and save their outputs to outputs/."""
import os
from master_analysis import load_data, prepare_merged_data

from task5 import task5_part1, task5_part2
from task6 import task6_part1, task6_part2
from task7 import task7_part1, task7_part2


def main():
    cwd = os.getcwd()
    print(f"Running runner in: {cwd}")

    # Load and prepare data
    transactions, gender_train, tr_mcc_codes, tr_types = load_data()
    transactions = prepare_merged_data(transactions, gender_train, tr_mcc_codes, tr_types)

    # Run task5
    print('\nRunning Task 5...')
    res5_1 = task5_part1(transactions)
    res5_2 = task5_part2(transactions)

    # Run task6
    print('\nRunning Task 6...')
    res6_1 = task6_part1(transactions)
    res6_2 = task6_part2(transactions, res6_1)

    # Run task7
    print('\nRunning Task 7...')
    res7_1 = task7_part1(transactions)
    res7_2 = task7_part2(transactions)

    print('\nAll tasks 5,6,7 executed. Look in outputs/ for CSV and PNG files.')


if __name__ == '__main__':
    main()
