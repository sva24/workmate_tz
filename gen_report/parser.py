import argparse


def create_parser(argv=None):
    """
    Создает парсер аргументов командной строки.

    Args:
        argv (list | None): Список аргументов для парсинга.
            Используется в тестах. Если None — берутся системные аргументы.

    Returns:
        tuple:
            list[str] — Пути к файлам
            str — Тип отчёта
    """
    parser = argparse.ArgumentParser(description="Создание отчётов")
    parser.add_argument(
        "--files",
        type=str,
        nargs="+",
        required=True,
        help="Передайте файлы в качестве аргумента",
    )
    parser.add_argument("--report", required=True, help="Нужный вид отчёта")

    args = parser.parse_args(argv)
    return args.files, args.report
