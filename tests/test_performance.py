import pytest
from gen_report.reports.performance import prepare_perf_report, print_report


def test_prepare_perf_report_sorting():
    employees = [
        {"position": "QA", "performance": "5"},
        {"position": "Dev", "performance": "10"},
        {"position": "Manager", "performance": "7"},
    ]

    report = prepare_perf_report(employees)

    assert report[0]["position"] == "Dev"
    assert report[1]["position"] == "Manager"
    assert report[2]["position"] == "QA"
    assert report[0]["performance"] == 10.0
    assert report[2]["performance"] == 5.0


def test_prepare_perf_report_float_conversion():
    employees = [
        {"position": "Dev", "performance": "12.5"},
        {"position": "QA", "performance": "8"},
    ]

    report = prepare_perf_report(employees)
    assert report[0]["performance"] == 12.5
    assert report[1]["performance"] == 8.0


def test_prepare_perf_report_empty():
    employees = []
    report = prepare_perf_report(employees)
    assert report == []


def test_prepare_perf_report_invalid_performance():
    employees = [
        {"position": "Dev", "performance": "abc"},
    ]

    with pytest.raises(ValueError):
        prepare_perf_report(employees)


def test_print_report_output(monkeypatch):

    output = []

    monkeypatch.setattr("builtins.print", lambda x: output.append(x))

    employees = [
        {"position": "Dev", "performance": 10.0},
        {"position": "QA", "performance": 8.0},
    ]

    print_report(employees)

    assert len(output) > 0
    assert "position" in output[0]
    assert "performance" in output[0]

