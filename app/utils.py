import csv
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from tabulate import tabulate
from app.handlers import register_report

class RowsInfo:
    """Класс для загрузки и обработки данных из CSV-файлов."""

    def __init__(self, files: List[str]) -> None:
        """Инициализирует объект и загружает данные из переданных файлов.

        Args:
            files (List[str]): Список путей к CSV-файлам.
        """
        self.rows: List[Dict[str, str]] = self._load_rows_from_files(files)

    def _load_rows_from_files(self, files: List[str]) -> List[Dict[str, str]]:
        """Объединяет данные из нескольких CSV-файлов в единый список.

        Args:
            files (List[str]): Список путей к CSV-файлам.

        Returns:
            List[Dict[str, str]]: Список словарей с данными из всех файлов.
        """
        combined_data: List[Dict[str, str]] = []
        for file_path in files:
            file_data = self._read_csv_file(file_path)
            if file_data:
                combined_data.extend(file_data)
            else:
                print(f"Предупреждение: Файл '{file_path}' не найден или пуст.")
        return combined_data

    @staticmethod
    def _read_csv_file(file_path: str) -> Optional[List[Dict[str, str]]]:
        """Читает CSV-файл и возвращает список словарей с данными.

        Args:
            file_path (str): Путь к CSV-файлу.

        Returns:
            Optional[List[Dict[str, str]]]: Список словарей с данными или None, если файл не найден.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            return None

class Report(ABC):
    """Абстрактный базовый класс для генерации отчётов."""

    def __init__(self, headers: List[str], data: List[Dict[str, str]]) -> None:
        """Инициализирует объект отчёта.

        Args:
            headers (List[str]): Заголовки для таблицы отчёта.
            data (List[Dict[str, str]]): Данные для отчёта.
        """
        self.headers = headers
        self.data = data
        self.report_data: List[List[Any]] = self._create_report_data()

    @abstractmethod
    def _create_report_data(self) -> List[List[Any]]:
        """Создаёт данные для отчёта.

        Returns:
            List[List[Any]]: Данные для отображения в таблице.
        """
        pass

    def generate_report(self) -> str:
        """Форматирует данные отчёта в виде таблицы.

        Returns:
            str: Отформатированная таблица.
        """
        return tabulate(
            self.report_data,
            headers=self.headers,
            tablefmt="grid",
            floatfmt=".1f",
        )

@register_report("student-performance")
class StudentPerformanceReport(Report):
    """Отчёт о среднем балле студентов."""

    def __init__(self, data: List[Dict[str, str]]) -> None:
        """Инициализирует отчёт о среднем балле студентов.

        Args:
            data (List[Dict[str, str]]): Данные студентов.
        """
        super().__init__(
            headers=["student_name", "average_grade"],
            data=data
        )

    def _create_report_data(self) -> List[List[Any]]:
        """Создаёт данные для отчёта о среднем балле студентов.

        Returns:
            List[List[Any]]: Список списков с именами студентов и их средними баллами.
        """
        student_grades: Dict[str, List[float]] = {}
        for row in self.data:
            student_name = row.get("student_name", "").strip()
            if not student_name:
                continue

            try:
                grade = float(row.get("grade", 0))
            except (ValueError, TypeError):
                continue

            student_grades.setdefault(student_name, []).append(grade)

        report_data = [
            [student_name, self._calculate_average(grades)]
            for student_name, grades in student_grades.items()
        ]
        report_data.sort(key=lambda x: (-x[1], x[0]))
        return report_data

    @staticmethod
    def _calculate_average(grades: List[float]) -> float:
        """Вычисляет средний балл.

        Args:
            grades (List[float]): Список оценок.

        Returns:
            float: Средний балл.
        """
        return round(sum(grades) / len(grades), 1)

from app.handlers import register_report


from typing import List, Dict, Any

@register_report("raw-data")
class RawDataReport(Report):
    """Отчёт для вывода сырых данных из CSV-файлов."""

    def __init__(self, data: List[Dict[str, str]]) -> None:
        super().__init__(
            headers=["student_name", "subject", "grade", "date"],
            data=data  # Используем 'data' вместо 'data_files'
        )

    def _create_report_data(self) -> List[List[Any]]:
        """Создаёт данные для отчёта в формате таблицы."""
        report_data = []
        for row in self.data:
            report_data.append([
                row["student_name"],
                row["subject"],
                row["grade"],
                row["date"]
            ])
        return report_data

