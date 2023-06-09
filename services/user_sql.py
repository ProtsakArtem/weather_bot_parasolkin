import sqlite3

DB_FILE = "weather.db"


def check_create_database(database_name = DB_FILE):
    """
    Перевірка чи існує база даних, і створення якщо не існує
    :param database_name:
    :return:
    """
    conn = None
    try:
        # Пробуємо підключитись
        conn = sqlite3.connect(database_name)
        print(f"База даних '{database_name}' існує.")

    except sqlite3.Error as e:
        # Якщо база даних не існує створюємо її
        print(f"База даних '{database_name}' не існує. Створюю нову базу даних...")
        conn = sqlite3.connect(database_name)
        print(f"База даних '{database_name}' успішно створена.")

    finally:
        if conn:
            conn.close()


def check_user_table():
    """
    Перевірка наявності таблиці users в базі даних, і її створення в разі відсутності
    :return:
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id INTEGER PRIMARY KEY,
                     coordinates TEXT,
                     sub TEXT)''')


def add_new_user(user_id, coordinates, sub):
    """
    Запис до таблиці users нового користувача
    :param user_id: int(message.from_user.id / callback.from_user.id)
    :param coordinates: string (формат- "хх.хх хх.хх")
    :param sub: string (everyday / alarm)
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Перевірка наявності запису в таблиці
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_record = c.fetchone()

    if existing_record:
        # Запис існує, оновлюємо його
        c.execute("UPDATE users SET coordinates = ?, sub = ? WHERE user_id = ?",
                  (coordinates, sub, user_id))
    else:
        # Запис не істує, створюємо
        c.execute("INSERT INTO users (user_id, coordinates, sub) VALUES (?, ?, ?)",
                  (user_id, coordinates, sub))

    conn.commit()
    conn.close()


def add_sub_to_user(user_id, sub):
    """
    Змінення значення sub для користувача з відповідним user_id
    :param user_id: int(message.from_user.id / callback.from_user.id)
    :param sub: string (everyday / alarm)
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET sub = ? WHERE user_id = ?", (sub, user_id))
    conn.commit()
    conn.close()


def add_location_to_user(user_id, coords):
    """
    Змінення локації (coordinates) для користувача з відповідним user_id
    :param user_id: int(message.from_user.id / callback.from_user.id)
    :param coords: string (формат - "хх.хх хх.хх")
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET coordinates = ? WHERE user_id = ?", (coords, user_id))
    conn.commit()
    conn.close()


def get_nonzero_coordinates():
    """
    Отримання усіх юзерів, у яких зазначені координати
    :return: list
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # отримання усіх записів де є координати
    c.execute("SELECT coordinates FROM users WHERE coordinates != '0' AND coordinates != 0")
    result = c.fetchall()

    # Преобразуємо в список
    coordinates = [row[0] for row in result]

    conn.close()
    return coordinates


def get_coordinates(user_id):
    """
    Отримання координатів за user_id
    :param user_id: int(message.from_user.id / callback.from_user.id)
    :return: string (формат - "хх.хх хх.хх")
    """
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''SELECT coordinates FROM users WHERE user_id=?''', (user_id,))
    row = c.fetchone()
    coordinates = row[0] if row else None
    conn.close()
    return coordinates


def get_sub(user_id):
    """
    Отримання типу підписки за user_id користувача
    :param user_id: int(message.from_user.id / callback.from_user.id)
    :return: string (everyday / alarm / 0)
    """
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''SELECT sub FROM users WHERE user_id=?''', (user_id,))
    row = c.fetchone()

    sub = row[0] if row else None
    conn.close()
    return sub


def get_users_with_sub(sub_value):
    """
    Отримання списку людей з вказаним типом підписки
    :param sub_value: string (everyday / alarm / 0)
    :return: list
    """
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()

    c.execute("SELECT user_id, coordinates FROM users WHERE sub = ?", (sub_value,))
    rows = c.fetchall()

    conn.close()

    return rows
