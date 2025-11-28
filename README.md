# workmate_tz

Утилита для генерации отчетов по данным сотрудников из CSV файлов.

## Установка

```bash
# Клонируйте репозиторий
git clone git@github.com:sva24/workmate_tz.git

# Установка зависимостей
poetry install

# Запуск с примером данных
poetry run python -m gen_report.scripts.main --files example_data.csv --report performance
Или
poetry run report --files employees1.csv employees2.csv --report performance
```
Добавление новых отчетов:
Создайте функцию в gen_report/report.py:
```bash
python
def generate_custom_report(data):
    # ваша логика
    return formatted_data
 ```
Добавьте обработку в generate_report():
```bash
python
def generate_report(report_type, data):
    if report_type == 'custom':
        return generate_custom_report(data)
 ```
Теперь можно использовать:

```bash
poetry run python -m gen_report.scripts.main --files data.csv --report custom
 ```

## Пример запуска скрипта
[![workmate tz](https://radika1.link/2025/11/28/workmate_tz07e4feddf99aa223.jpg)](https://radikal.cloud/i/workmate-tz.q08weD)