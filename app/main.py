import argparse
import sys
from app.utils import RowsInfo, RawDataReport
from app.reports import AVAILABLE_REPORTS

class StudentPerformanceArgumentParser(argparse.ArgumentParser):
    """Кастомный парсер аргументов для обработки ошибок с понятными сообщениями."""

    def error(self, message):
        """Выводит пользовательские сообщения об ошибках вместо стандартных."""
        if "required: --report" in message:
            sys.stderr.write(
                "Ошибка: Не указан обязательный параметр --report. "
                "Укажите название отчёта из доступных вариантов.\n"
            )
        elif "required: --files" in message or "argument --files" in message:
            sys.stderr.write(
                "Ошибка: Не указан обязательный параметр --files. "
                "Передайте путь к одному или нескольким CSV-файлам через пробел.\n"
            )
        elif "argument --report" in message:
            sys.stderr.write(
                f"Ошибка: Некорректное значение для --report. "
                f"Доступные отчёты: {list(AVAILABLE_REPORTS.keys())}.\n"
            )
        else:
            sys.stderr.write(f"Ошибка: {message}\n")
        sys.exit(2)

def main():
    parser = StudentPerformanceArgumentParser(
        description="Инструмент для анализа академической успеваемости студентов."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Путь к одному или нескольким CSV-файлам с данными студентов."
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=list(AVAILABLE_REPORTS.keys()),
        help="Название отчёта для генерации."
    )
    args = parser.parse_args()

    student_data = RowsInfo(args.files)
    if student_data.rows:
        report_generator = AVAILABLE_REPORTS[args.report](student_data.rows)
        print(report_generator.generate_report())
    else:
        print("Ошибка: Данные для отчёта отсутствуют или файлы не были прочитаны.")


if __name__ == "__main__":
    main()
