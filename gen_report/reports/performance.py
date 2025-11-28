from typing import List
from tabulate import tabulate


def make_perf_report(employees: list) -> None:
    """
      Обрабатывает переданные данные и создает отчет о производительности.

      Args:
          employees (dict): Данные для обработки.

      Returns:
          List[dict]: Данные для вывода пользователю.
      """
    report = []
    for emp in employees:
        report.append({
            'position': emp['position'],
            'performance': float(emp['performance']),
        })

    print_perf_report(sorted(report, key=lambda x: x['performance'], reverse=True))


def print_perf_report(employees: List[dict]) -> None:
    """Печатает отчет о производительности в виде таблицы"""
    table_data = []
    for idx, item in enumerate(employees, 1):
        table_data.append([
            idx,
            item['position'],
            item['performance']
        ])

    headers = ["position", "performance"]
    print(tabulate(table_data, headers=headers))
