#!/usr/bin/env python3
"""
КОМПЛЕКСНОЕ РУКОВОДСТВО ПО ВЫПОЛНЕНИЮ ЗАДАНИЙ 4-8
Анализ транзакций: статистика, разницы по полам, ночные транзакции
"""

# ============================================================
# СТРУКТУРА ФАЙЛОВ И ФУНКЦИЙ
# ============================================================

FILE_STRUCTURE = """
Структура проекта для заданий 4-8:

/Zhasus/
├── task4.py                    # Среднее и медиана по amount
├── task5.py                    # Разница в тратах/поступлениях по полам
├── task6.py                    # Макс доход по типам для разных полов
├── task7.py                    # Анализ разницы в тратах по MCC
├── task8.py                    # Ночные транзакции (00:00-06:00)
├── master_analysis.py          # Комплексный скрипт (все задания)
├── examples_4_8.py             # Примеры использования
├── TASKS_4_8_README.md         # Подробное описание
└── REQUIREMENTS.txt            # Зависимости (pandas, numpy, matplotlib)

Требуемые данные (CSV файлы):
├── transactions.csv            # Основная таблица транзакций
├── gender_train.csv            # Информация о поле клиентов
├── tr_mcc_codes.csv            # Коды и описания MCC категорий
└── tr_types.csv                # Типы транзакций
"""

# ============================================================
# ПОДГОТОВКА ДАННЫХ
# ============================================================

PREPARATION_STEPS = """
ШАГ 1: Загрузка данных

    import pandas as pd
    
    transactions = pd.read_csv('transactions.csv')
    gender_train = pd.read_csv('gender_train.csv')
    tr_mcc_codes = pd.read_csv('tr_mcc_codes.csv')
    tr_types = pd.read_csv('tr_types.csv')

ШАГ 2: Объединение таблиц (важно! следуйте порядку)

    # LEFT JOIN с gender_train
    transactions = pd.merge(transactions, gender_train, how='left')
    
    # INNER JOIN с tr_mcc_codes
    transactions = pd.merge(transactions, tr_mcc_codes, how='inner')
    
    # INNER JOIN с tr_types
    transactions = pd.merge(transactions, tr_types, how='inner')
    
    # Проверка результата
    print(transactions.shape)  # Должно быть (999584, N)

ШАГ 3: Проверка данных

    print(transactions.columns)     # Все ли колонки?
    print(transactions.head())      # Первые строки
    print(transactions.info())      # Типы данных
    print(transactions.dtypes)      # Типы каждой колонки
"""

# ============================================================
# ОПРЕДЕЛЕНИЯ ОСНОВНЫХ ПОНЯТИЙ
# ============================================================

DEFINITIONS = """
ОСНОВНЫЕ ОПРЕДЕЛЕНИЯ:

1. ТРАНЗАКЦИИ:
   - Положительный amount (amount > 0): ПОСТУПЛЕНИЯ (доход на карту)
   - Отрицательный amount (amount < 0): ТРАТЫ (расход со счета)
   - amount = 0: нейтральные операции

2. ПОЛ (gender column):
   - Обычно: 0 = женщины, 1 = мужчины
   - ИЛИ: 'F' = женщины, 'M' = мужчины
   - ВНИМАНИЕ: При вычислении модуля не нужно знать точное обозначение

3. ВРЕМЯ (tr_datetime):
   - Формат: "2021-01-15 14:30:45" или "2021-01-15T14:30:45"
   - Выделение часа: tr_datetime.dt.hour или первые 2 символа до ":"

4. НОЧНОЕ ВРЕМЯ:
   - Диапазон: 00:00 - 06:00 (часы 0-5)
   - INNER JOIN: Оставляет только совпадающие записи
   - LEFT JOIN: Сохраняет все записи из левой таблицы
"""

# ============================================================
# ОПИСАНИЕ КАЖДОГО ЗАДАНИЯ
# ============================================================

TASK4 = """
═══ ЗАДАНИЕ 4: Среднее и медиана по amount ═══

ЧАСТЬ 1: Статистика для топ-10 регионов
─────────────────────────────────────────
Задача: Найти среднее и медиану по столбцу amount для типов транзакций,
        которые встречаются в топ-10 регионов (по сумме amount).

Алгоритм:
  1. Найти топ-10 регионов по сумме amount
  2. Отфильтровать транзакции этих регионов
  3. Сгруппировать по tr_type (тип транзакции)
  4. Вычислить mean() и median() по amount

Пример:
  top10_regions = transactions.groupby('region')['amount'].sum().nlargest(10)
  top10_list = top10_regions.index.tolist()
  subset = transactions[transactions['region'].isin(top10_list)]
  result = subset.groupby('tr_type')['amount'].agg(['mean', 'median'])

ЧАСТЬ 2: Статистика по полам
─────────────────────────────
Задача: Найти среднее и медиану по amount для типов транзакций
        каждого пола.

Алгоритм:
  1. Сгруппировать по gender и tr_type
  2. Вычислить mean() и median() по amount

Пример:
  result = transactions.groupby(['gender', 'tr_type'])['amount'].agg(['mean', 'median'])
"""

TASK5 = """
═══ ЗАДАНИЕ 5: Разница в тратах и поступлениях по полам ═══

ЧАСТЬ 1: Разница в тратах (средних отрицательных значений)
──────────────────────────────────────────────────────────
Задача: Найти модуль разницы между средними тратами женщин и мужчин.

Алгоритм:
  1. Отфильтровать только траты: amount < 0
  2. Сгруппировать по gender
  3. Вычислить среднее (mean) по amount
  4. Вычислить модуль разницы между полами

Пример:
  spendings = transactions[transactions['amount'] < 0]
  avg_spending = spendings.groupby('gender')['amount'].mean()
  # avg_spending[0] = -100, avg_spending[1] = -80
  diff = abs(avg_spending.iloc[0] - avg_spending.iloc[1])  # abs(-100 - (-80)) = 20

ЧАСТЬ 2: Разница в поступлениях
────────────────────────────────
Задача: Найти модуль разницы между средними поступлениями
        (положительными значениями).

Алгоритм:
  1. Отфильтровать только поступления: amount > 0
  2. Сгруппировать по gender
  3. Вычислить среднее (mean) по amount
  4. Вычислить модуль разницы между полами

Пример:
  incomes = transactions[transactions['amount'] > 0]
  avg_income = incomes.groupby('gender')['amount'].mean()
  diff = abs(avg_income.iloc[0] - avg_income.iloc[1])

ВАЖНО: Модуль разницы работает независимо от того, какой пол какое значение имеет!
"""

TASK6 = """
═══ ЗАДАНИЕ 6: Макс доход по типам для разных полов ═══

ЧАСТЬ 1: Топ-10 типов с наименьшим макс доходом
───────────────────────────────────────────────
Задача: Для каждого пола найти 10 типов транзакций с наименьшим
        максимальным значением дохода (положительные amount).

Алгоритм:
  1. Отфильтровать только доходы: amount > 0
  2. Сгруппировать по gender и tr_type
  3. Найти максимум (max) по amount для каждой комбинации
  4. Для каждого пола отсортировать и взять 10 наименьших (nsmallest)

Пример:
  incomes = transactions[transactions['amount'] > 0]
  max_inc = incomes.groupby(['gender', 'tr_type'])['amount'].max().reset_index()
  max_inc.columns = ['gender', 'tr_type', 'max_income']
  for gender in max_inc['gender'].unique():
      subset = max_inc[max_inc['gender'] == gender]
      top10 = subset.nsmallest(10, 'max_income')

ЧАСТЬ 2: Общие типы для обоих полов
───────────────────────────────────
Задача: Из 10 типов для каждого пола найти пересечение
        (типы, встречающиеся у обоих полов).

Алгоритм:
  1. Получить список 10 типов для пола 1
  2. Получить список 10 типов для пола 2
  3. Найти пересечение (intersection)

Пример:
  types_gender1 = set(result['gender1']['tr_type'])
  types_gender2 = set(result['gender2']['tr_type'])
  common = types_gender1.intersection(types_gender2)
"""

TASK7 = """
═══ ЗАДАНИЕ 7: Разница в тратах по MCC категориям ═══

ЧАСТЬ 1: Суммы затрат по MCC для каждого пола
─────────────────────────────────────────────
Задача: Просуммировать траты (amount < 0) по MCC категориям
        для каждого пола отдельно.

Алгоритм:
  1. Отфильтровать только траты: amount < 0
  2. Сгруппировать по gender, mcc_code, mcc_description
  3. Вычислить сумму (sum) по amount

Пример:
  spendings = transactions[transactions['amount'] < 0]
  mcc_sum = spendings.groupby(['gender', 'mcc_code', 'mcc_description'])['amount'].sum()

ЧАСТЬ 2: Топ-10 категорий с наибольшей разницей
───────────────────────────────────────────────
Задача: Найти 10 MCC категорий, где разница между тратами
        мужчин и женщин максимальна.

Алгоритм:
  1. Создать pivot таблицу: строки=MCC, столбцы=gender, значения=sum(amount)
  2. Вычислить модуль разницы между полами
  3. Отсортировать и взять топ-10 (nlargest)

Пример:
  pivot = mcc_sum.unstack(fill_value=0)
  pivot['diff'] = abs(pivot['gender1'] - pivot['gender2'])
  top10 = pivot.nlargest(10, 'diff')

ВЫВОД: Должны содержать MCC код и его описание!
"""

TASK8 = """
═══ ЗАДАНИЕ 8: Ночные транзакции (00:00-06:00) ═══

ЧАСТЬ 1: Выделение часа из datetime
──────────────────────────────────
Задача: Из поля tr_datetime извлечь час транзакции.

Алгоритм:
  1. Убедиться, что tr_datetime это datetime тип
  2. Использовать .dt.hour для извлечения часа
  3. Или вручную: int(datetime_string.split(' ')[1].split(':')[0])

Пример:
  transactions['tr_datetime'] = pd.to_datetime(transactions['tr_datetime'])
  transactions['tr_hour'] = transactions['tr_datetime'].dt.hour
  # tr_hour будет содержать значения 0-23

ЧАСТЬ 2: Подсчет ночных транзакций со тратами
──────────────────────────────────────────────
Задача: Посчитать количество ночных транзакций со тратами для каждого пола.

Алгоритм:
  1. Выбрать только ночные часы: tr_hour в [0, 1, 2, 3, 4, 5]
  2. Отфильтровать только траты: amount < 0
  3. Сгруппировать по gender
  4. Подсчитать количество (size)

Пример:
  night = transactions[
      (transactions['tr_hour'].isin(range(0, 6))) & 
      (transactions['amount'] < 0)
  ]
  result = night.groupby('gender').size()

НОЧНОЕ ВРЕМЯ: 00:00 - 06:00 = часы 0, 1, 2, 3, 4, 5
"""

# ============================================================
# ПОЛЕЗНЫЕ PANDAS ОПЕРАЦИИ
# ============================================================

USEFUL_OPERATIONS = """
ПОЛЕЗНЫЕ PANDAS ОПЕРАЦИИ ДЛЯ ЗАДАНИЙ:

Фильтрация:
  df[df['column'] > 0]              # Строки где column > 0
  df[df['column'].isin([1, 2, 3])]  # Строки где column = 1, 2 или 3
  df[(df['a'] > 0) & (df['b'] < 10)]  # Несколько условий

Группировка и агрегация:
  df.groupby('column')['value'].sum()    # Сумма по группам
  df.groupby('column')['value'].mean()   # Среднее по группам
  df.groupby('column')['value'].median() # Медиана по группам
  df.groupby('column')['value'].max()    # Максимум по группам
  df.groupby('column')['value'].agg(['mean', 'median', 'count'])  # Несколько агрегаций

Сортировка:
  df.sort_values('column')          # Сортировка по возрастанию
  df.sort_values('column', ascending=False)  # По убыванию
  df.nlargest(10, 'column')         # Топ-10 наибольших
  df.nsmallest(10, 'column')        # 10 наименьших

Работа с Pivot таблицами:
  pd.pivot_table(df, index='row_col', columns='col_col', values='val_col', aggfunc='sum')
  pivot.unstack()                   # Преобразовать MultiIndex в столбцы
  pivot[column1].intersection(pivot[column2])  # Пересечение

Работа с datetime:
  pd.to_datetime(df['column'])      # Преобразование в datetime
  df['datetime_col'].dt.hour        # Извлечение часа
  df['datetime_col'].dt.day         # Извлечение дня
  df['datetime_col'].dt.month       # Извлечение месяца

Вычисления:
  abs(value)                        # Модуль (абсолютное значение)
  df['new_col'] = df['col1'] - df['col2']  # Создание новой колонки
  df['new_col'] = abs(df['col1'] - df['col2'])  # С модулем
"""

# ============================================================
# ЧАСТЫЕ ОШИБКИ И РЕШЕНИЯ
# ============================================================

COMMON_ERRORS = """
ЧАСТЫЕ ОШИБКИ И КАК ИХ ИЗБЕЖАТЬ:

1. KeyError: '[column_name]' - Колонки нет после merge
   ├─ Причина: Неправильный порядок merge
   ├─ Решение: Проверить имена колонок перед merge и их типы
   └─ Проверка: print(transactions.columns)

2. TypeError: '<' not supported между 'str' и 'int'
   ├─ Причина: Неправильный тип данных
   ├─ Решение: Преобразовать: df['col'] = df['col'].astype(int)
   └─ Проверка: print(df.dtypes)

3. Cannot unstack - MultiIndex не совпадает
   ├─ Причина: Неправильная структура данных после groupby
   ├─ Решение: Использовать .reset_index(), затем pivot_table
   └─ Пример: 
       result.reset_index(inplace=True)
       pivot = pd.pivot_table(result, ...)

4. NaN значения в результатах
   ├─ Причина: Пропущенные данные при merge
   ├─ Решение: Использовать .fillna(0) или проверить join type
   └─ Пример: pivot.fillna(0)

5. Неправильное количество строк после merge (не 999584)
   ├─ Причина: Ошибка в порядке merge или типе join
   ├─ Решение: Проверить порядок: left -> inner -> inner
   └─ Проверка: 
       transactions = pd.merge(transactions, gender_train, how='left')
       transactions = pd.merge(transactions, tr_mcc_codes, how='inner')
       transactions = pd.merge(transactions, tr_types, how='inner')

6. Часы вне диапазона 0-23
   ├─ Причина: Неправильное выделение часа из datetime
   ├─ Решение: Убедиться что используется .dt.hour
   └─ Проверка: 
       print(transactions['tr_hour'].min(), transactions['tr_hour'].max())

7. Модуль разницы неправильный
   ├─ Причина: Забыли abs()
   ├─ Решение: Всегда использовать abs(value1 - value2)
   └─ Пример: diff = abs(avg1 - avg2)

8. Неправильное количество элементов в пересечении
   ├─ Причина: Использовался не thintersection
   ├─ Решение: set1.intersection(set2)
   └─ Пример:
       types1 = set(list1)
       types2 = set(list2)
       common = types1.intersection(types2)
"""

# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == '__main__':
    print("=" * 80)
    print("КОМПЛЕКСНОЕ РУКОВОДСТВО ПО ЗАДАНИЯМ 4-8")
    print("=" * 80)
    
    print("\n" + FILE_STRUCTURE)
    print("\n" + PREPARATION_STEPS)
    print("\n" + DEFINITIONS)
    print("\n" + TASK4)
    print("\n" + TASK5)
    print("\n" + TASK6)
    print("\n" + TASK7)
    print("\n" + TASK8)
    print("\n" + USEFUL_OPERATIONS)
    print("\n" + COMMON_ERRORS)
    
    print("\n" + "=" * 80)
    print("НАЧНИТЕ С ВЫПОЛНЕНИЯ:")
    print("=" * 80)
    print("""
1. Скопируйте файлы данных в рабочую директорию:
   - transactions.csv
   - gender_train.csv
   - tr_mcc_codes.csv
   - tr_types.csv

2. Запустите комплексный скрипт:
   python3 master_analysis.py

3. ИЛИ запустите отдельные задания:
   python3 task4.py
   python3 task5.py
   python3 task6.py
   python3 task7.py
   python3 task8.py

4. ИЛИ смотрите примеры:
   python3 examples_4_8.py
    """)
