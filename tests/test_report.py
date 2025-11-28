import pytest
from gen_report import report


def test_generate_report_calls_make_perf_report(monkeypatch):
    called = {"flag": False, "data": None}

    def fake_make_perf_report(data):
        called["flag"] = True
        called["data"] = data

    monkeypatch.setattr(report, "make_perf_report", fake_make_perf_report)

    data = [
        {"position": "Dev", "performance": "10"},
        {"position": "QA", "performance": "8"},
    ]

    report.generate_report("performance", data)

    assert called["flag"] is True
    assert called["data"] == data


def test_generate_report_invalid_type(monkeypatch):
    called = {"flag": False}

    def fake_make_perf_report(data):
        called["flag"] = True

    monkeypatch.setattr("gen_report.reports.performance.make_perf_report", fake_make_perf_report)

    data = [{"position": "Dev", "performance": "10"}]

    report.generate_report("seek_day", data)

    assert called["flag"] is False
