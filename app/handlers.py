from app.reports import AVAILABLE_REPORTS

def register_report(report_name: str) -> callable:
    """
    Декоратор для регистрации класса отчёта в глобальном словаре REPORTS.

    Args:
        report_name (str): Ключ, под которым класс отчёта будет зарегистрирован в словаре REPORTS.

    Returns:
        callable: Декоратор, который регистрирует класс в словаре REPORTS.
    """
    def decorator(report_class: type) -> type:
        """
        Регистрирует класс отчёта в словаре REPORTS.

        Args:
            report_class (type): Класс отчёта, который нужно зарегистрировать.

        Returns:
            type: Исходный класс отчёта без изменений.
        """
        AVAILABLE_REPORTS[report_name] = report_class
        return report_class

    return decorator
