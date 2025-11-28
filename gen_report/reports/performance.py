from typing import Dict, List

from tabulate import tabulate


def prepare_perf_report(employees: List[Dict]) -> List[Dict]:
    """
    Обрабатывает сотрудников и возвращает список словарей
    с должностью и производительностью, отсортированный по performance.
    """
    report = []
    for emp in employees:
        report.append(
            {
                "position": emp["position"],
                "performance": float(emp["performance"]),
            }
        )

    return sorted(report, key=lambda x: x["performance"], reverse=True)


def print_report(employees: List[Dict]) -> None:
    """Печатает отчет о производительности в виде таблицы"""

    table_data = []
    for idx, item in enumerate(employees, 1):
        table_data.append([idx, item["position"], item["performance"]])

    headers = ["position", "performance"]
    print(tabulate(table_data, headers=headers))


def make_perf_report(employees: List[Dict]) -> None:
    """
    Основная функция генерации отчета: обрабатывает данные и печатает таблицу.
    """
    report_sorted = prepare_perf_report(employees)
    print_report(report_sorted)
