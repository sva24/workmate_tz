import pytest
import sys
from pathlib import Path


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_main_success_flow(monkeypatch):
    from gen_report.scripts import main

    mock_loaded_files = {'employee1': {'data': 'test'}}

    def mock_create_parser():
        return ['file1.csv', 'file2.csv'], 'performance'

    class MockFileLoader:
        def load_files(self, file_paths):
            assert file_paths == ['file1.csv', 'file2.csv']
            return mock_loaded_files

    def mock_generate_report(report_type, data):
        assert report_type == 'performance'
        assert data == mock_loaded_files

    # Применяем monkeypatch
    monkeypatch.setattr(main, 'create_parser', mock_create_parser)
    monkeypatch.setattr(main, 'FileLoader', MockFileLoader)
    monkeypatch.setattr(main, 'generate_report', mock_generate_report)

    main.main()


def test_main_with_different_report_types(monkeypatch):
    from gen_report.scripts import main

    report_types = ['performance', 'summary', 'detailed']

    for report_type in report_types:
        def mock_create_parser():
            return (['file1.csv'], report_type)

        class MockFileLoader:
            def load_files(self, file_paths):
                return {}

        call_args = []

        def mock_generate_report(report_type_arg, data):
            call_args.append((report_type_arg, data))

        # Применяем monkeypatch
        monkeypatch.setattr(main, 'create_parser', mock_create_parser)
        monkeypatch.setattr(main, 'FileLoader', MockFileLoader)
        monkeypatch.setattr(main, 'generate_report', mock_generate_report)

        main.main()

        assert call_args[0][0] == report_type
        call_args.clear()


def test_main_with_multiple_files(monkeypatch):
    """Тест main с несколькими файлами"""
    from gen_report.scripts import main

    test_files = ['file1.csv', 'file2.json', 'file3.yaml']

    def mock_create_parser():
        return (test_files, 'performance')

    received_files = []

    class MockFileLoader:
        def load_files(self, file_paths):
            received_files.extend(file_paths)
            return {'loaded': 'data'}

    def mock_generate_report(report_type, data):
        assert data == {'loaded': 'data'}

    monkeypatch.setattr(main, 'create_parser', mock_create_parser)
    monkeypatch.setattr(main, 'FileLoader', MockFileLoader)
    monkeypatch.setattr(main, 'generate_report', mock_generate_report)

    main.main()

    assert received_files == test_files


def test_main_file_loader_initialization(monkeypatch):
    from gen_report.scripts import main

    loader_instances = []

    class MockFileLoader:
        def __init__(self):
            loader_instances.append(self)

        def load_files(self, file_paths):
            return {}

    def mock_create_parser():
        return ['file1.csv'], 'performance'

    def mock_generate_report(report_type, data):
        pass

    monkeypatch.setattr(main, 'create_parser', mock_create_parser)
    monkeypatch.setattr(main, 'FileLoader', MockFileLoader)
    monkeypatch.setattr(main, 'generate_report', mock_generate_report)

    main.main()

    assert len(loader_instances) == 1
    assert isinstance(loader_instances[0], MockFileLoader)


def test_main_direct_execution(monkeypatch):
    from gen_report.scripts import main

    main_called = []

    def mock_main():
        main_called.append(True)

    monkeypatch.setattr(main, 'main', mock_main)

    main.__name__ = "__main__"

    if main.__name__ == "__main__":
        main.main()

    assert main_called == [True]


def test_main_with_parser_error(monkeypatch):
    from gen_report.scripts import main

    def mock_create_parser():
        raise SystemExit("Ошибка парсера")

    monkeypatch.setattr(main, 'create_parser', mock_create_parser)

    with pytest.raises(SystemExit):
        main.main()


def test_main_with_file_loader_error(monkeypatch):
    from gen_report.scripts import main

    def mock_create_parser():
        return (['file1.csv'], 'performance')

    class MockFileLoader:
        def load_files(self, file_paths):
            raise ValueError("Файл не найден")

    monkeypatch.setattr(main, 'create_parser', mock_create_parser)
    monkeypatch.setattr(main, 'FileLoader', MockFileLoader)

    with pytest.raises(ValueError, match="Файл не найден"):
        main.main()


def test_main_with_empty_files_list(monkeypatch):
    from gen_report.scripts import main

    def mock_create_parser():
        return [], 'performance'

    class MockFileLoader:
        def load_files(self, file_paths):
            assert file_paths == []
            return {}

    def mock_generate_report(report_type, data):
        assert report_type == 'performance'
        assert data == {}

    monkeypatch.setattr(main, 'create_parser', mock_create_parser)
    monkeypatch.setattr(main, 'FileLoader', MockFileLoader)
    monkeypatch.setattr(main, 'generate_report', mock_generate_report)

    main.main()


def test_main_with_single_file(monkeypatch):
    from gen_report.scripts import main

    test_file = 'single_file.csv'

    def mock_create_parser():
        return [test_file], 'summary'

    received_files = []

    class MockFileLoader:
        def load_files(self, file_paths):
            received_files.extend(file_paths)
            return {'single': 'file_data'}

    def mock_generate_report(report_type, data):
        assert report_type == 'summary'
        assert data == {'single': 'file_data'}

    monkeypatch.setattr(main, 'create_parser', mock_create_parser)
    monkeypatch.setattr(main, 'FileLoader', MockFileLoader)
    monkeypatch.setattr(main, 'generate_report', mock_generate_report)

    main.main()

    assert received_files == [test_file]