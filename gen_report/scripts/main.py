from gen_report.files_loader import FileLoader
from gen_report.parser import create_parser
from gen_report.report import generate_report


def main():
    """
    Основная функция для запуска генерации отчетов.
    """

    file_loader = FileLoader()
    file_paths, report_type = create_parser()

    loaded_files = file_loader.load_files(file_paths)

    generate_report(report_type, loaded_files)


if __name__ == "__main__":
    main()
