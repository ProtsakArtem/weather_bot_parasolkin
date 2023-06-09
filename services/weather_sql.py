import sqlite3
from statistics import mean


def check_weather_data_table():
    """
    Перевіряє чи існує таблиця weather_data, якщо ні - створює її.
    :return:
    """
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS weather_data
                (coordinates TEXT PRIMARY KEY,
                daily_avg_today TEXT,
                daily_avg_tomorrow TEXT,
                daily_avg_after_tomorrow TEXT,
                daily_sunrise_today TEXT,
                daily_sunrise_tomorrow TEXT,
                daily_sunrise_after_tomorrow TEXT,
                daily_drops_today TEXT,
                daily_drops_tomorrow TEXT,
                daily_drops_after_tomorrow TEXT,
                daily_temp_today REAL,
                daily_temp_tomorrow REAL,
                daily_temp_after_tomorrow REAL,
                after_tomorrow_hour_temp TEXT,
                tomorrow_hour_temp TEXT,
                today_hour_temp TEXT,
                today_drop_chance TEXT,
                tomorrow_drop_chance TEXT,
                after_tomorrow_drop_chance TEXT,
                today_windspeed TEXT,
                tomorrow_windspeed TEXT,
                after_tomorrow_windspeed TEXT)''')


def update_weather_data(data):
    """
    Перевіряє наявніть локації в базі даних, якщо вона є - заміняє показники на актуальні, якщо ні - додає запис в таблицю weather_data з актуальними показниками
    :param data: tuple (кортеж, який повертає функція parse_weather)
    :return:
    """
    coordinates, daily_avg_today, daily_avg_tomorrow, daily_avg_after_tomorrow, daily_sunrise_today, daily_sunrise_tomorrow, daily_sunrise_after_tomorrow, daily_drops_today, daily_drops_tomorrow, daily_drops_after_tomorrow, daily_temp_today, daily_temp_tomorrow, daily_temp_after_tomorrow, after_tomorrow_hour_temp, tomorrow_hour_temp, today_hour_temp, today_drop_chance, tomorrow_drop_chance, after_tomorrow_drop_chance, today_windspeed, tomorrow_windspeed, after_tomorrow_windspeed = data
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()

    # Перевірка наявності запису в базі даних
    c.execute('''SELECT * FROM weather_data WHERE coordinates=?''', (coordinates,))
    row = c.fetchone()

    if row:
        # Якщо запис існує
        existing_coordinates = row[0]
        if existing_coordinates == coordinates:
            # Оновлюємо дані на актуальні
            c.execute('''UPDATE weather_data SET
                         daily_avg_today=?, daily_avg_tomorrow=?, daily_avg_after_tomorrow=?,
                         daily_sunrise_today=?, daily_sunrise_tomorrow=?, daily_sunrise_after_tomorrow=?,
                         daily_drops_today=?, daily_drops_tomorrow=?, daily_drops_after_tomorrow=?,
                         daily_temp_today=?, daily_temp_tomorrow=?, daily_temp_after_tomorrow=?,
                         after_tomorrow_hour_temp=?, tomorrow_hour_temp=?, today_hour_temp=?,
                         today_drop_chance=?, tomorrow_drop_chance=?, after_tomorrow_drop_chance=?,
                         today_windspeed=?, tomorrow_windspeed=?, after_tomorrow_windspeed=?
                         WHERE coordinates=?''',
                      (daily_avg_today, daily_avg_tomorrow, daily_avg_after_tomorrow,
                       daily_sunrise_today, daily_sunrise_tomorrow, daily_sunrise_after_tomorrow,
                       ", ".join(str(x) for x in daily_drops_today),
                       ", ".join(str(x) for x in daily_drops_tomorrow),
                       ", ".join(str(x) for x in daily_drops_after_tomorrow),
                       daily_temp_today, daily_temp_tomorrow, daily_temp_after_tomorrow,
                       ", ".join(str(x) for x in after_tomorrow_hour_temp),
                       ", ".join(str(x) for x in tomorrow_hour_temp),
                       ", ".join(str(x) for x in today_hour_temp),
                       ", ".join(str(x) for x in today_drop_chance),
                       ", ".join(str(x) for x in tomorrow_drop_chance),
                       ", ".join(str(x) for x in after_tomorrow_drop_chance),
                       ", ".join(str(x) for x in today_windspeed),
                       ", ".join(str(x) for x in tomorrow_windspeed),
                       ", ".join(str(x) for x in after_tomorrow_windspeed),
                       coordinates))
    else:
        # Якщо запису нема - додаємо
        c.execute('''INSERT INTO weather_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (coordinates, daily_avg_today, daily_avg_tomorrow, daily_avg_after_tomorrow,
                   daily_sunrise_today, daily_sunrise_tomorrow, daily_sunrise_after_tomorrow,
                   ", ".join(str(x) for x in daily_drops_today),
                   ", ".join(str(x) for x in daily_drops_tomorrow),
                   ", ".join(str(x) for x in daily_drops_after_tomorrow),
                   daily_temp_today, daily_temp_tomorrow, daily_temp_after_tomorrow,
                   ", ".join(str(x) for x in after_tomorrow_hour_temp),
                   ", ".join(str(x) for x in tomorrow_hour_temp),
                   ", ".join(str(x) for x in today_hour_temp),
                   ", ".join(str(x) for x in today_drop_chance),
                   ", ".join(str(x) for x in tomorrow_drop_chance),
                   ", ".join(str(x) for x in after_tomorrow_drop_chance),
                   ", ".join(str(x) for x in today_windspeed),
                   ", ".join(str(x) for x in tomorrow_windspeed),
                   ", ".join(str(x) for x in after_tomorrow_windspeed)))

    conn.commit()
    conn.close()


def get_weather_values(cords, day = "today"):
    """
    Дістає з таблиці weather_data дані для щоденного прогнозу
    :param cords: string (формат - "хх.хх хх.хх")
    :param day: string (today, tomorrow, after_tomorrow)
    :return: tuple Повертає кортеж зі значеннями
    """
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()

    # Дістаємо значення з таблиці по заданим координатам
    c.execute(f'''SELECT daily_avg_{day}, daily_sunrise_{day}, daily_drops_{day}, daily_temp_{day},
                         {day}_drop_chance, {day}_windspeed
                 FROM weather_data WHERE coordinates=?''', (cords,))
    row = c.fetchone()
    if row:
        daily_avg = row[0]
        daily_sunrise = row[1]
        daily_drops = row[2]
        daily_temp = row[3]
        print(row[4].split(", "))
        print(row[5].split(", "))
        drop_chance = round(mean([float(x) for x in row[4].split(", ")]), 1)
        windspeed = round(mean([float(x) for x in row[5].split(", ")]), 1)
    else:
        daily_avg = None
        daily_sunrise = None
        daily_drops = None
        daily_temp = None
        drop_chance = None
        windspeed = None
    conn.close()
    return (daily_avg, daily_sunrise, daily_drops, daily_temp, drop_chance, windspeed)


def get_hour_values(cords, day = "today"):
    """
    Дістає з таблиці weather_data дані для погодинного прогнозу
    :param cords: string (формат - "хх.хх хх.хх")
    :param day: string (today, tomorrow, after_tomorrow)
    :return: tuple Повертає кортеж зі значеннями
    """
    print(f"coordinates = {cords}")
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute(f'''SELECT {day}_hour_temp, {day}_drop_chance, {day}_windspeed
                    FROM weather_data WHERE coordinates=?''', (cords,))
    row = c.fetchone()
    print(f"row: {row}")
    if row:
        hour_temp = row[0].split(', ')
        drop_chance = row[1].split(', ')
        windspeed = row[2].split(', ')
    else:
        hour_temp = None
        drop_chance = None
        windspeed = None

    conn.close()

    return (hour_temp, drop_chance, windspeed)