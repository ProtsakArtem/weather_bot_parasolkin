from statistics import mean
import requests

table_weater = {
    0: "Чисте небо🌥",
    1: "Переважно ясно🌤",
    2: "Мінлива хмарність☁️",
    3: "Похмуро☁️",
    45: "Туман🌫",
    48: "Туман(Можливо іней)🌫",
    51: "Мряка слабка😬",
    53: "Помірна мряка😬",
    55: "Густа мряка😬",
    56: "Крижаний дощ🌧",
    57: "Крижаний дощ🌧",
    61: "Слабкий дощ🌧",
    63: "Середній дощ🌧",
    65: "Сильний дощ🌧",
    66: "Крижаний дощ🌧",
    67: "Сильний крижаний дощ🌧",
    71: "Слабкий снігопад🌨",
    73: "Середній снігопад❄️",
    75: "Сильний снігопад❄️",
    77: "Крупний сніг❄️",
    80: "Дощ легкий🌦",
    81: "Помірний дощ🌧",
    82: "Сильний дощ🌧",
    85: "Невеликий снігопад❄️",
    86: "Сильний снігопад❄️",
    95: "Гроза помірна⛈",
    96: "Гроза з невеликим градом⛈",
    99: "Гроза з сильним градом⛈",
}


def parse_weather(latitude, longitude):
    """
    Надсилає запит на API та отримує всі дані про погоду за заданими координатами
    :param latitude: float/string
    :param longitude: float/string
    :return: tuple
    Повертає кортеж зі значеннями усіх показників
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation_probability,windspeed_10m&daily=weathercode,sunrise,sunset,precipitation_hours&windspeed_unit=ms&forecast_days=3&timezone=auto"
    ans = requests.get(url=url).json()

    daily_avg_today, daily_avg_tomorrow, daily_avg_after_tomorrow = [table_weater[x] for x in ans["daily"]["weathercode"]]
    daily_sunrise_today, daily_sunrise_tomorrow, daily_sunrise_after_tomorrow = [x[-5:] for x in ans["daily"]["sunrise"]]
    daily_drops_today, daily_drops_tomorrow, daily_drops_after_tomorrow = ans["daily"]["precipitation_hours"]
    daily_temp_today = round(mean(ans["hourly"]["temperature_2m"][0:24]), 1)
    daily_temp_tomorrow = round(mean(ans["hourly"]["temperature_2m"][24:48]), 1)
    daily_temp_after_tomorrow = round(mean(ans["hourly"]["temperature_2m"][48:72]), 1)

    today_hour_temp = ans["hourly"]["temperature_2m"][0:24][0::3]
    tomorrow_hour_temp = ans["hourly"]["temperature_2m"][24:48][0::3]
    after_tomorrow_hour_temp = ans["hourly"]["temperature_2m"][48:72][0::3]

    today_drop_chance = ans["hourly"]["precipitation_probability"][0:24][0::3]
    tomorrow_drop_chance = ans["hourly"]["precipitation_probability"][24:48][0::3]
    after_tomorrow_drop_chance = ans["hourly"]["precipitation_probability"][48:72][0::3]

    today_windspeed = ans["hourly"]["windspeed_10m"][0:24][0::3]
    tomorrow_windspeed = ans["hourly"]["windspeed_10m"][24:48][0::3]
    after_tomorrow_windspeed = ans["hourly"]["windspeed_10m"][48:72][0::3]
    coordinates = f"{latitude} {longitude}"
    daily_drops_today = [daily_drops_today]
    daily_drops_tomorrow = [daily_drops_tomorrow]
    daily_drops_after_tomorrow = [daily_drops_after_tomorrow]

    return(coordinates, daily_avg_today, daily_avg_tomorrow, daily_avg_after_tomorrow,
                        daily_sunrise_today, daily_sunrise_tomorrow, daily_sunrise_after_tomorrow,
                        daily_drops_today, daily_drops_tomorrow, daily_drops_after_tomorrow,
                        daily_temp_today, daily_temp_tomorrow, daily_temp_after_tomorrow,
                        after_tomorrow_hour_temp, tomorrow_hour_temp, today_hour_temp,
                        today_drop_chance, tomorrow_drop_chance, after_tomorrow_drop_chance,
                        today_windspeed, tomorrow_windspeed, after_tomorrow_windspeed)
