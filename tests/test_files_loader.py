import pytest
import csv
import tempfile
from pathlib import Path
from gen_report.files_loader import FileLoader


def test_file_loader_initialization():
    loader = FileLoader()
    assert hasattr(loader, 'formats')
    assert '.csv' in loader.formats
    assert callable(loader.formats['.csv'])


def test_validate_files_valid_paths():
    loader = FileLoader()
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp1:
        tmp1_path = tmp1.name
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp2:
        tmp2_path = tmp2.name

    try:
        file_paths = [tmp1_path, tmp2_path]
        result = loader.validate_files(file_paths)

        assert len(result) == 2
        assert all(isinstance(p, Path) for p in result)
        assert result[0] == Path(tmp1_path)
        assert result[1] == Path(tmp2_path)
    finally:
        # Удаляем временные файлы
        Path(tmp1_path).unlink(missing_ok=True)
        Path(tmp2_path).unlink(missing_ok=True)


def test_validate_files_empty_list():
    loader = FileLoader()

    with pytest.raises(ValueError, match="Не указаны файлы для обработки"):
        loader.validate_files([])


def test_validate_files_nonexistent_file():
    loader = FileLoader()

    with pytest.raises(ValueError, match="Файл не найден"):
        loader.validate_files(['/nonexistent/file.csv'])


def test_validate_files_directory_instead_of_file(tmp_path):
    loader = FileLoader()
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()

    with pytest.raises(ValueError, match="Указанный путь не является файлом"):
        loader.validate_files([str(dir_path)])


def test_load_csv_valid_file():
    loader = FileLoader()

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
        writer = csv.writer(tmp)
        writer.writerow(['name', 'position', 'performance'])
        writer.writerow(['John Doe', 'Developer', '4.5'])
        writer.writerow(['Jane Smith', 'Designer', '4.7'])
        tmp_path = tmp.name

    try:
        result = loader._load_csv([Path(tmp_path)])

        assert len(result) == 2
        assert result[0] == {'name': 'John Doe', 'position': 'Developer', 'performance': '4.5'}
        assert result[1] == {'name': 'Jane Smith', 'position': 'Designer', 'performance': '4.7'}
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_load_csv_multiple_files():
    loader = FileLoader()

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp1:
        writer = csv.writer(tmp1)
        writer.writerow(['name', 'position'])
        writer.writerow(['John', 'Dev'])
        tmp1_path = tmp1.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp2:
        writer = csv.writer(tmp2)
        writer.writerow(['name', 'position'])
        writer.writerow(['Jane', 'Designer'])
        tmp2_path = tmp2.name

    try:
        result = loader._load_csv([Path(tmp1_path), Path(tmp2_path)])

        assert len(result) == 2
        assert result[0] == {'name': 'John', 'position': 'Dev'}
        assert result[1] == {'name': 'Jane', 'position': 'Designer'}
    finally:
        Path(tmp1_path).unlink(missing_ok=True)
        Path(tmp2_path).unlink(missing_ok=True)


def test_load_files_success():
    loader = FileLoader()

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
        writer = csv.writer(tmp)
        writer.writerow(['name', 'performance'])
        writer.writerow(['User', '4.8'])
        tmp_path = tmp.name

    try:
        result = loader.load_files([tmp_path])

        assert len(result) == 1
        assert result[0] == {'name': 'User', 'performance': '4.8'}
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_load_files_unsupported_format():
    loader = FileLoader()

    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError, match="Формат файла '.json' пока не поддерживается"):
            loader.load_files([tmp_path])
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_load_files_mixed_valid_invalid():
    loader = FileLoader()

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
        writer = csv.writer(tmp)
        writer.writerow(['name', 'value'])
        writer.writerow(['Test', '1'])
        valid_path = tmp.name

    invalid_path = '/nonexistent/file.csv'

    try:
        with pytest.raises(ValueError, match="Файл не найден"):
            loader.load_files([valid_path, invalid_path])
    finally:
        Path(valid_path).unlink(missing_ok=True)


def test_load_files_empty_csv():
    loader = FileLoader()

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
        writer = csv.writer(tmp)
        writer.writerow(['name', 'position'])
        tmp_path = tmp.name

    try:
        result = loader.load_files([tmp_path])

        assert result == []
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_formats_registry():
    loader = FileLoader()

    assert '.csv' in loader.formats
    assert callable(loader.formats['.csv'])
    assert loader.formats['.csv'] == loader._load_csv


def test_validate_files_returns_path_objects():
    loader = FileLoader()
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        result = loader.validate_files([tmp_path])

        assert len(result) == 1
        assert isinstance(result[0], Path)
        assert result[0] == Path(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)