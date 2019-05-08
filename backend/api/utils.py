import datetime


def get_quarter(date: datetime.date) -> int:
    return (date.month - 1) // 3
