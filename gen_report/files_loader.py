import os
from typing import List
import csv


class FileLoader:
    @staticmethod
    def validate_files(file_paths: List[str]) -> None:
        """
        Проверяет корректность переданных файлов
        Raises:
            ValueError: если файлы некорректны
        """
        errors = []

        if not file_paths:
            errors.append("Не указаны файлы для обработки")

        for file_path in file_paths:
            if not os.path.exists(file_path):
                errors.append(f"Файл не найден: {file_path}")
            elif not os.path.isfile(file_path):
                errors.append(f"Указанный путь не является файлом: {file_path}")

        if errors:
            raise ValueError("\n".join(errors))

    @staticmethod
    def load_files(file_paths: List[str]) -> List[dict]:
        """
        Загружает и парсит файлы
        Returns:
            List[dict]: список данных из файлов
        """
        loaded_data = {}

        for file_path in file_paths:
            try:
                if file_path.endswith('.csv'):
                    data = FileLoader._load_csv(file_path)
                else:
                    raise ValueError(f"Неподдерживаемый формат файла: {file_path}")

                loaded_data.update(data)

            except Exception as e:
                raise ValueError(f"Ошибка загрузки файла {file_path}: {str(e)}")

        return loaded_data

    @staticmethod
    def load_files(file_paths: List[str]) -> list:
        """
        Загружает файлы и возвращает список сотрудников
        """
        employees_list = []

        for file_path in file_paths:
            if file_path.endswith('.csv'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    employees_list.extend(list(reader))

        return employees_list
