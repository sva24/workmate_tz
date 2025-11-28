from typing import List

from gen_report.reports.performance import make_perf_report


def generate_report(report: str, data: List[dict]):
    """
    Формирует отчёт

    Args:
        report (str): Выбранный вид отчета
        data (List[dict]): Сформированный отчет.

    Returns:
        Возвращает отчёт, согласно переданному параметру
    """
    if report == "performance":
        make_perf_report(data)
