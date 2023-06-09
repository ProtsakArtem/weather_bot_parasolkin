from src.config import bot
from src.services.parse_weather import parse_weather
import src.services.user_sql
from src.keyboards import inline
from src.services import weather_sql


async def sub_everyday():
    """
    Розсилає всім користувачам з типом підписки everyday актуальну погоду
    """
    baza = src.services.user_sql.get_users_with_sub("everyday")
    for x in baza:
        weather_data = weather_sql.get_weather_values(x[1], day="today")
        msg = f"""
Погода на сьогодні: {weather_data[0]}
Сонечко встає о {weather_data[1]} 🌅
Шанс на опади💧 : {weather_data[4]}% 
Опади сьогодні будуть {weather_data[2]} годин🕒
Середня температура 🌡: {weather_data[3]} C°
Швидкість вітру💨: {weather_data[5]}
"""
        await bot.send_message(x[0], msg, reply_markup=inline.mark_more_today)


async def sub_alert():
    """
    Розсилає всім користувачам з типом підписки alert актуальну погоду, якщо вона погана
    """
    baza = src.services.user_sql.get_users_with_sub("alert")
    for x in baza:
        weather_data = weather_sql.get_weather_values(x[1], day="today")
        if weather_data[0] in "Мряка слабка😬" \
                              "Помірна мряка😬" \
                              "Густа мряка😬" \
                              "Крижаний дощ🌧" \
                              "Крижаний дощ🌧" \
                              "Слабкий дощ🌧" \
                              "Середній дощ🌧" \
                              "Сильний дощ🌧" \
                              "Крижаний дощ🌧" \
                              "Сильний крижаний дощ🌧" \
                              "Слабкий снігопад🌨" \
                              "Середній снігопад❄" \
                              "️Сильний снігопад❄️" \
                              "Крупний сніг❄️" \
                              "Дощ легкий🌦" \
                              "Помірний дощ🌧" \
                              "Сильний дощ🌧" \
                              "Невеликий снігопад❄️" \
                              "Сильний снігопад❄️" \
                              "Гроза помірна⛈" \
                              "Гроза з невеликим градом⛈" \
                              "Гроза з сильним градом⛈":
            msg = f"""
Погода на сьогодні: {weather_data[0]}
Сонечко встає о {weather_data[1]} 🌅
Шанс на опади💧 : {weather_data[4]}% 
Опади сьогодні будуть {weather_data[2]} годин🕒
Середня температура 🌡: {weather_data[3]} C°
Швидкість вітру💨: {weather_data[5]}
"""
            await bot.send_message(x[0], msg, reply_markup=inline.mark_more_today)


def parse_start():
    """
    Збирає і оновлює дані про погоду для усіх наявних локацій в базі даних
    """
    for x in src.services.user_sql.get_nonzero_coordinates():
        lat, long = x.split(" ")
        data = parse_weather(lat, long)
        weather_sql.update_weather_data(data)
