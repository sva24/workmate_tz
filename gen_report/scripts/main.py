import sys
from gen_report.parser import create_parser
from gen_report.files_loader import FileLoader
from gen_report.report import generate_report


def main():
    """
    Основная функция для запуска генерации отчетов.
    """
    try:
        file_paths, report_type = create_parser()

        loaded_files = FileLoader.load_files(file_paths)

        generate_report(report_type, loaded_files)

    except ValueError as e:
        print(f"Ошибка ввода: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
