import pytest
from app.utils import RowsInfo, StudentPerformanceReport

def test_rows_info_successful_read_and_combine(csv_files):
    """Тест: Проверка корректного объединения данных из нескольких CSV-файлов."""
    rows_info = RowsInfo(csv_files)

    # Проверяем, что все записи из файлов загружены
    assert len(rows_info.rows) == 3

    # Проверяем уникальные имена студентов
    student_names = {row["student_name"] for row in rows_info.rows}
    expected_names = {"Иванов Иван", "Петрова Мария", "Семенова Елена"}
    assert student_names == expected_names

def test_rows_info_handle_missing_file(capfd):
    """Тест: Проверка обработки отсутствующего файла."""
    rows_info = RowsInfo(["no_such_file.csv"])

    # Проверяем, что данные не загружены
    assert rows_info.rows == []

    # Проверяем вывод предупреждения
    out, _ = capfd.readouterr()
    expected_warning = (
        "Внимание: данные из файла 'no_such_file.csv' не были получены или файл отсутствует."
    )
    assert expected_warning in out

def test_student_performance_report_generation(sample_rows):
    """Тест: Проверка генерации отчёта об успеваемости студентов."""
    report = StudentPerformanceReport(sample_rows)
    report_data = report.report_data

    # Проверяем наличие студентов в отчёте
    student_names = [row[0] for row in report_data]
    assert "Иванов Иван" in student_names
    assert "Петрова Мария" in student_names
    assert "Семенова Елена" in student_names

    # Проверяем отсутствие некорректных записей
    assert "Пробелы" not in student_names
    assert "" not in student_names
    assert "Ошибки" not in student_names
    assert "   " not in student_names

    # Проверяем корректность средних баллов
    expected_data = [
        ["Семенова Елена", 5.0],  # Средний балл: 5
        ["Иванов Иван", 4.5],     # Средний балл: (4 + 5) / 2
        ["Петрова Мария", 3.5],   # Средний балл: (3 + 4) / 2
    ]
    assert report_data == expected_data

    # Проверяем сортировку: сначала по среднему баллу (по убыванию), затем по имени (по возрастанию)
    sorted_by_name = sorted(report_data, key=lambda student: student[0])
    sorted_by_grade = sorted(sorted_by_name, key=lambda student: student[1], reverse=True)
    assert sorted_by_grade == report_data
