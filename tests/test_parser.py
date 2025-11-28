import pytest
from gen_report.parser import create_parser


def test_create_parser_success_single_file():
    argv = ["--files", "file1.csv", "--report", "performance"]
    files, report_type = create_parser(argv)

    assert files == ["file1.csv"]
    assert report_type == "performance"


def test_create_parser_success_multiple_files():
    argv = ["--files", "file1.csv", "file2.csv", "--report", "performance"]
    files, report_type = create_parser(argv)

    assert files == ["file1.csv", "file2.csv"]
    assert report_type == "performance"


def test_create_parser_missing_files():
    argv = ["--report", "performance"]
    with pytest.raises(SystemExit):
        create_parser(argv)


def test_create_parser_missing_report():
    argv = ["--files", "file1.csv"]
    with pytest.raises(SystemExit):
        create_parser(argv)


def test_create_parser_no_arguments():
    argv = []
    with pytest.raises(SystemExit):
        create_parser(argv)
