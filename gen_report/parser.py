import argparse


def create_parser(argv=None):
    """
    Создает парсер аргументов командной строки
    Args:
        argv (list): Список аргументов командной строки. По умолчанию None.

    Returns:
        tuple: Кортеж из двух элементов:
            - list: Пути к файлам.
            - str: Выбранный отчёт
    """
    parser = argparse.ArgumentParser(
        description='Создание отчётов')
    parser.add_argument('--files', type=str, nargs='+',
                        required=True, help='Передайте файлы в качестве аргумента')
    parser.add_argument('--report', required=True, help='Нужный вид отчёта')

    args = parser.parse_args(argv)
    return args.files, args.report
