from gen_report.reports.performance import make_perf_report
from typing import List


def generate_report(report: str, data: List[dict]):
    """
    Формирует отчёт

    Args:
        report (str): Выбранный вид отчета
        data (List[dict]): Сформированный отчет.

    Returns:
        str: Итоговое представление различий в заданном формате.
    """
    if report == 'performance':
        make_perf_report(data)
