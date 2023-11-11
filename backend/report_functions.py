import json
from datetime import date, datetime, timedelta

db_name = "reports_data.json"


def read_db():
    """
    Функция для чтения базы данных из файла
    :return: В случае успеха возвращает базу данных, иначе пустой словарь
    """
    global db_name
    try:
        with open(db_name, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {}


def write_db(db):
    """
    Запись новых данны в базу данных
    :param db: Словарь с базой данных
    :return: True - если запись прошла успешно, иначе False
    """
    global db_name
    try:
        with open(db_name, 'w') as fp:
            json.dump(db, fp)
        return True
    except Exception as e:
        return False


def get_last_date_of_month(year, month):
    if month == 12:
        last_date = datetime(year, month, 31)
    else:
        last_date = datetime(year, month + 1, 1) + timedelta(days=-1)

    return last_date


def get_first_date_of_current_month(year, month):
    first_date = datetime(year, month, 1)
    return first_date
