# Zhasus — Комплексный анализ транзакций (Задания 4-8)

## Описание проекта

Этот проект содержит полный набор Python-скриптов для анализа данных транзакций с использованием pandas, matplotlib и seaborn. Проект включает решения для заданий 1–8, с особым акцентом на задания 4–8, которые включают:

- **Задание 4**: Среднее и медиана по amount для типов транзакций
- **Задание 5**: Разница в тратах и поступлениях по полам
- **Задание 6**: Максимальный доход по типам транзакций для разных полов
- **Задание 7**: Топ-10 категорий с наибольшей разницей в тратах по полам
- **Задание 8**: Анализ ночных транзакций со тратами по полам

Все скрипты автоматически сохраняют результаты в виде CSV-файлов и PNG-диаграмм в папку `outputs/`.

---

## Структура проекта

```
Zhasus/
├── task1_time_series.py              # Анализ временных рядов
├── task2_top_regions.py              # Топ-10 регионов по сумме транзакций
├── task3_age_gender_heatmap.py       # Тепловая карта возраста и пола
├── task4.py                          # Среднее и медиана по типам транзакций
├── task5.py                          # Разница в тратах/поступлениях по полам
├── task6.py                          # Макс доход по типам и полам
├── task7.py                          # Разница в тратах по MCC категориям
├── task8.py                          # Ночные транзакции
├── run_task8.py                      # Runner для задачи 8
├── run_tasks_5_6_7.py                # Runner для задач 5, 6, 7
├── master_analysis.py                # Главный скрипт (выполняет все задачи)
├── generate_sample_data.py           # Генератор демо-данных
├── examples_4_8.py                   # Примеры использования задач 4-8
├── GUIDE_TASKS_4_8.py                # Подробное руководство
├── requirements.txt                  # Зависимости проекта
├── README.md                         # Основной README
├── TASKS_4_8_README.md               # README для задач 4-8
├── SUMMARY_TASKS_4_8.md              # Итоговая сводка
├── INDEX_TASKS_4_8.txt               # Индекс задач
├── .gitignore                        # Git-исключения (outputs/ исключён)
├── data/                             # Папка для исходных данных (если требуется)
└── outputs/                          # Папка с сохранёнными результатами
    ├── task4_part1.csv / .png
    ├── task5_part1_avg_by_gender.csv / .png
    ├── task5_part1_diff.txt
    ├── task6_part1_top10_*.csv / .png
    ├── task7_part1_spending_by_mcc.csv / .png
    ├── task8_part1_sample_with_hour.csv
    └── task8_part2_*.csv / .png
```

---

## Установка и подготовка

### 1. Клонирование репозитория

```bash
git clone https://github.com/Zhasik1/Zhasus.git
cd Zhasus
```

### 2. Установка зависимостей

#### Вариант A: Через pip (рекомендуется)

```bash
python3 -m pip install --user -r requirements.txt
```

#### Вариант B: Через conda (для окружения Anaconda)

```bash
conda activate base    # или имя вашего окружения
conda install -y pandas matplotlib seaborn
```

### 3. Проверка установки

```bash
python3 - <<'PY'
import pandas as pd
import matplotlib
import seaborn as sns
print(f'✓ pandas {pd.__version__}')
print(f'✓ matplotlib {matplotlib.__version__}')
print(f'✓ seaborn {sns.__version__}')
PY
```

---

## Подготовка данных

### Вариант A: Использование реальных данных

Поместите ваши CSV-файлы в корень проекта:
- `transactions.csv` — данные транзакций
- `gender_train.csv` — данные о поле клиентов
- `tr_mcc_codes.csv` — справочник MCC-кодов
- `tr_types.csv` — справочник типов транзакций

### Вариант B: Генерация демо-данных

Если у вас нет реальных данных, сгенерируйте демо-данные:

```bash
cd Zhasus
python3 generate_sample_data.py
```

Этот скрипт создаст 10,000 синтетических транзакций для тестирования.

---

## Запуск задач

### Быстрый запуск (рекомендуется)

#### Запустить задачи 5, 6, 7 (с автосохранением результатов)

```bash
cd Zhasus
python3 run_tasks_5_6_7.py
```

Результаты появятся в папке `outputs/`:
- CSV-файлы с данными
- PNG-диаграммы

#### Запустить задачу 8 (ночные транзакции)

```bash
cd Zhasus
python3 run_task8.py
```

#### Запустить все задачи (4-8) сразу

```bash
cd Zhasus
python3 master_analysis.py
```

### Использование в Python-скрипте или Jupyter

```python
import pandas as pd
from task5 import task5_part1, task5_part2
from task6 import task6_part1, task6_part2
from task7 import task7_part1, task7_part2

# Загрузить данные
transactions = pd.read_csv('transactions.csv')
gender_train = pd.read_csv('gender_train.csv')
tr_mcc_codes = pd.read_csv('tr_mcc_codes.csv')
tr_types = pd.read_csv('tr_types.csv')

# Объединить таблицы
transactions = pd.merge(transactions, gender_train, how='left')
transactions = pd.merge(transactions, tr_mcc_codes, how='inner')
transactions = pd.merge(transactions, tr_types, how='inner')

# Выполнить задания
res5_1 = task5_part1(transactions)  # Разница в тратах
res5_2 = task5_part2(transactions)  # Разница в поступлениях

res6_1 = task6_part1(transactions)  # Макс доход по типам
res6_2 = task6_part2(transactions, res6_1)  # Общие типы

res7_1 = task7_part1(transactions)  # Суммы по MCC
res7_2 = task7_part2(transactions)  # Топ-10 по разнице
```

---

## Описание задач 4-8

### Задание 4: Среднее и медиана по amount

**Файл**: `task4.py`

**Вывод**:
- Среднее и медиану по типам транзакций в топ-10 регионах
- Среднее и медиану по типам транзакций для каждого пола

**Сохранённые файлы**:
- `outputs/task4_part1.csv` — результаты часть 1
- `outputs/task4_part1.png` — диаграмма часть 1
- `outputs/task4_part2.csv` — результаты часть 2
- `outputs/task4_part2.png` — диаграмма часть 2

---

### Задание 5: Разница в тратах и поступлениях по полам

**Файл**: `task5.py`

**Вывод**:
- Модуль разницы между средними тратами женщин и мужчин
- Модуль разницы между средними поступлениями мужчин и женщин

**Сохранённые файлы**:
- `outputs/task5_part1_avg_by_gender.csv` — средние траты
- `outputs/task5_part1_diff.txt` — разница в тратах
- `outputs/task5_part1.png` — диаграмма
- `outputs/task5_part2_avg_by_gender.csv` — средние поступления
- `outputs/task5_part2_diff.txt` — разница в поступлениях
- `outputs/task5_part2.png` — диаграмма

---

### Задание 6: Максимальный доход по типам транзакций

**Файл**: `task6.py`

**Вывод**:
- Топ-10 типов транзакций с наименьшим максимальным доходом для каждого пола
- Типы транзакций, встречающиеся у обоих полов

**Сохранённые файлы**:
- `outputs/task6_part1_top10_0.csv` / `.png` — результаты для пола 0
- `outputs/task6_part1_top10_1.csv` / `.png` — результаты для пола 1
- `outputs/task6_part2_common_types.txt` — общие типы

---

### Задание 7: Топ-10 категорий с наибольшей разницей в тратах

**Файл**: `task7.py`

**Вывод**:
- Суммы затрат по каждой MCC-категории для мужчин и женщин
- Топ-10 категорий с наибольшей разницей в тратах между полами

**Сохранённые файлы**:
- `outputs/task7_part1_spending_by_mcc.csv` — суммы по категориям
- `outputs/task7_part1_top20.csv` — топ-20 примеров
- `outputs/task7_part2_top10.csv` — топ-10 по разнице
- `outputs/task7_part2_top10.png` — диаграмма

---

### Задание 8: Анализ ночных транзакций

**Файл**: `task8.py`

**Вывод**:
- Выделение часа из поля `tr_datetime`
- Количество ночных транзакций со тратами (00:00-06:00) по полам
- Распределение по часам

**Сохранённые файлы**:
- `outputs/task8_part1_sample_with_hour.csv` — примеры с часом
- `outputs/task8_part2_counts_by_gender.csv` — количество по полам
- `outputs/task8_part2_counts_by_gender.png` — диаграмма по полам
- `outputs/task8_part2_night_by_hour.csv` — распределение по часам
- `outputs/task8_part2_night_by_hour.png` — диаграмма по часам

---

## Просмотр результатов

После запуска скриптов результаты сохранятся в папке `outputs/`.

### На macOS

```bash
# Список всех файлов
ls -la outputs/

# Просмотр CSV в терминале
head -n 20 outputs/task5_part1_avg_by_gender.csv

# Открыть PNG в приложении по умолчанию
open outputs/task5_part1.png
```

### На Linux

```bash
# Просмотр CSV
cat outputs/task5_part1_avg_by_gender.csv

# Открыть PNG (требуется графическое окружение)
xdg-open outputs/task5_part1.png
```

### На Windows

```bash
# Просмотр CSV
type outputs\task5_part1_avg_by_gender.csv

# Открыть PNG
start outputs\task5_part1.png
```

---

## Требования

- **Python**: 3.7 или выше
- **pandas**: >= 1.3.0
- **matplotlib**: >= 3.4.0
- **seaborn**: >= 0.11.0 (опционально)
- **numpy**: входит в зависимости pandas

Полный список в файле `requirements.txt`.

---

## Структура данных

### Ожидаемые колонки в `transactions.csv`

```
- transaction_id: уникальный идентификатор транзакции
- customer_id: идентификатор клиента
- tr_datetime: дата и время транзакции (формат: YYYY-MM-DD HH:MM:SS)
- amount: сумма транзакции (положительное = поступление, отрицательное = трата)
- region: регион транзакции
- tr_type: тип транзакции (например: 'type_a', 'type_b', и т.д.)
- mcc_code: MCC-код категории (например: '5411')
```

### Ожидаемые колонки в `gender_train.csv`

```
- customer_id: идентификатор клиента
- gender: пол (0 = женщина, 1 = мужчина)
```

### Ожидаемые колонки в `tr_mcc_codes.csv`

```
- mcc_code: MCC-код (соответствует transaction.mcc_code)
- mcc_description: описание категории
```

### Ожидаемые колонки в `tr_types.csv`

```
- tr_type: тип транзакции (соответствует transaction.tr_type)
- tr_type_name: название типа
```

---

## Известные проблемы и решения

### Проблема: `ModuleNotFoundError: No module named 'pandas'`

**Решение**: Установите зависимости:
```bash
python3 -m pip install --user -r requirements.txt
```

### Проблема: `FileNotFoundError: 'transactions.csv' not found`

**Решение**: Убедитесь, что CSV-файлы находятся в корне проекта (где находится скрипт). Или сгенерируйте демо-данные:
```bash
python3 generate_sample_data.py
```

### Проблема: Диаграммы не сохраняются

**Решение**: Убедитесь, что папка `outputs/` существует и доступна для записи:
```bash
mkdir -p outputs
chmod 755 outputs
```

---

## Git и GitHub

### Текущее состояние репозитория

```
71ebed6 (HEAD -> main, origin/main) Add complete project: tasks 1-8, runners, data, and docs; exclude generated outputs/
9e0eee6 Add runner run_tasks_5_6_7.py to generate task5-7 outputs
c93b7cc Save outputs and add plots for tasks 4-8; add run_task8.py
7e63d61 Add all project files: data, scripts, and outputs
457769a Initial commit: Add README
```

### Работа с репозиторием

Клонирование:
```bash
git clone https://github.com/Zhasik1/Zhasus.git
cd Zhasus
```

Обновление:
```bash
git pull origin main
```

Проверка статуса:
```bash
git status
```

**Примечание**: Папка `outputs/` добавлена в `.gitignore`, поэтому генерируемые результаты не будут закоммичены. Это нормально — результаты создаются локально при запуске скриптов.

---

## Дополнительные файлы

- **`examples_4_8.py`** — примеры использования функций из task4–task8
- **`GUIDE_TASKS_4_8.py`** — подробное руководство с объяснениями
- **`SUMMARY_TASKS_4_8.md`** — итоговая сводка по каждому заданию
- **`INDEX_TASKS_4_8.txt`** — индекс и описание всех задач

---

## Лицензия

Этот проект создан в образовательных целях.

---

## Контакты и вопросы

Если у вас есть вопросы или предложения, откройте Issue на GitHub: https://github.com/Zhasik1/Zhasus/issues

---

**Последнее обновление**: 21 ноября 2025 г.
**Версия**: 1.0
