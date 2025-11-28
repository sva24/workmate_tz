import csv
from pathlib import Path
from typing import Dict, List


class FileLoader:
    """
    Универсальный загрузчик файлов сотрудников.
    """

    def __init__(self):
        self.formats = {
            ".csv": self._load_csv,
        }

    @staticmethod
    def validate_files(file_paths: List[str]) -> List[Path]:
        """
        Проверяет корректность переданных файлов.

        Args:
           List[str]: file_paths: список путей

        Returns:
            Список объектов Path

        Raises:
            ValueError: если пути некорректны
        """
        errors = []
        paths: List[Path] = []

        if not file_paths:
            raise ValueError("Не указаны файлы для обработки")

        for raw_path in file_paths:
            p = Path(raw_path)

            if not p.exists():
                errors.append(f"Файл не найден: {p}")
            elif not p.is_file():
                errors.append(f"Указанный путь не является файлом: {p}")
            else:
                paths.append(p)

        if errors:
            raise ValueError("\n".join(errors))

        return paths

    def load_files(self, file_paths: List[str]) -> List[Dict]:
        """
        Загружает файлы любого поддерживаемого формата.

        Args:
            file_paths(List[str]: список путей к файлам

        Returns:
            Список словарей сотрудников

        Raises:
            ValueError: если формат не поддерживается
        """
        paths = self.validate_files(file_paths)

        all_employees = []

        for p in paths:
            ext = p.suffix.lower()

            if ext not in self.formats:
                raise ValueError(f"Формат файла '{ext}'"
                                 f" пока не поддерживается: {p}")

            loader = self.formats[ext]
            employees = loader([p])
            all_employees.extend(employees)

        return all_employees

    def _load_csv(self, files: List[Path]) -> List[Dict]:
        """
        Обработчик CSV-файлов.

        Args:
           files(List[Path]: files: список Path к файлам .csv


        Returns:
            Список сотрудников из всех файлов

        Raises:
            ValueError: если CSV повреждён или кодировка неверна
        """
        employees = []

        for p in files:
            try:
                with p.open("r", newline="") as f:
                    reader = csv.DictReader(f)
                    employees.extend(reader)
            except UnicodeDecodeError:
                raise ValueError(f"Ошибка кодировки в файле {p}")
            except csv.Error as e:
                raise ValueError(f"Ошибка парсинга CSV в файле {p}: {e}")

        return employees
