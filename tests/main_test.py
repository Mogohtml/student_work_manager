import pytest
import csv
from typing import List, Dict, Any

@pytest.fixture
def csv_files(tmp_path) -> List[str]:
    """
    Фикстура для создания тестовых CSV-файлов с данными студентов.

    Args:
        tmp_path: Временная директория для создания файлов.

    Returns:
        List[str]: Список путей к созданным CSV-файлам.
    """
    # Данные для первого файла
    example1_data = [
        ["student_name", "subject", "teacher_name", "date", "grade"],
        ["Алексеев Алексей", "Математика", "Смирнов Дмитрий", "2023-09-01", "4"],
        ["Кузнецова Анна", "История", "Васильев Андрей", "2023-09-02", "5"],
    ]

    # Данные для второго файла
    example2_data = [
        ["student_name", "subject", "teacher_name", "date", "grade"],
        ["Новикова Ольга", "Английский язык", "Попова Елена", "2023-10-10", "5"],
    ]

    # Создаем CSV-файлы
    example1_file = tmp_path / "example1.csv"
    example2_file = tmp_path / "example2.csv"

    with open(example1_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(example1_data)

    with open(example2_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(example2_data)

    return [str(example1_file), str(example2_file)]

@pytest.fixture
def sample_rows() -> List[Dict[str, Any]]:
    """
    Фикстура с тестовыми данными студентов для проверки генерации отчётов.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными студентов.
    """
    return [
        {
            "student_name": "Алексеев Алексей      ",
            "subject": "Математика",
            "teacher_name": "Смирнов",
            "date": "2023-09-01",
            "grade": "4",
        },
        {
            "student_name": "Алексеев Алексей   ",
            "subject": "Физика",
            "teacher_name": "Иванов",
            "date": "2023-09-02",
            "grade": "5",
        },
        {
            "student_name": "Алексеев Алексей",
            "subject": "Физика",
            "teacher_name": "Иванов",
            "date": "2023-09-02",
            "grade": "?",
        },
        {
            "student_name": "Кузнецова Анна",
            "subject": "История",
            "teacher_name": "Васильева",
            "date": "2023-09-01",
            "grade": "3",
        },
        {
            "student_name": "Кузнецова Анна",
            "subject": "Литература",
            "teacher_name": "Петрова",
            "date": "2023-09-02",
            "grade": "4",
        },
        {
            "student_name": "Новикова Ольга",
            "subject": "Английский",
            "teacher_name": "Попова",
            "date": "2023-09-01",
            "grade": "5",
        },
        {
            "student_name": "Пустое Имя",
            "subject": "Музыка",
            "teacher_name": "Сергеев",
            "date": "2023-09-01",
            "grade": "",
        },
        {
            "student_name": "",
            "subject": "Химия",
            "teacher_name": "Фёдорова",
            "date": "2023-09-01",
            "grade": "5",
        },
        {
            "student_name": "Ошибка Данных",
            "subject": "Биология",
            "teacher_name": "Сергеев",
            "date": "2023-09-01",
            "grade": "abc",
        },
        {
            "student_name": "   ",
            "subject": "Биология",
            "teacher_name": "Сергеев",
            "date": "2023-09-01",
            "grade": "3",
        },
    ]
