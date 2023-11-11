import json

db_name = "database.json"


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


if __name__ == "__main__":
    # Пример работы

    # Сохраняем имя БД в переменную
    file_name = "test.json"
    # Считываем содержимое базы данных
    data = read_db(file_name)
    # Меняем/Присваиваем новое значение по ключу "key"
    data['key'] = 12312
    # Записываем БД в файл
    write_db(file_name, data)
