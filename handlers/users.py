from aiogram import types
import src.services.user_sql as user_sql
from src.keyboards import reply, inline
from src.services import weather_sql, parse_weather
from src.config import bot, dp


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, """
Привіт, {0.first_name}!
Мене звати Парасолькін ☂️
Я знаю погоду наперед, і не дам тобі несподівано потрапити під дощ)
Також, я можу розповідати тобі детальніше про погоду наперед.
Я маю три режими:
1) Щоденна підписка. Я буду щодня зранку надсилати тобі свіженький прогноз погоди на день.
2) Екстрена. Я буду турбувати тебе тільки у разі якщо сьогодні буде дощ, або ще якась біда.
3) Соціофобний режим. Не буду тобі писати першим, буду тільки відповідати тобі як будеш питатись за погоду.

Зроби свій вибір👇
""".format(message.from_user), reply_markup=reply.sub_choice_mark)
    user_sql.add_new_user(message.from_user.id, "0", "0")


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text in "📅 Щоденна підписка⚠️ Тільки екстрені🤐 Мовчу":
        if message.text == "🤐 Мовчу":
            await bot.send_message(message.from_user.id, "Добре, буду мовчати 🙊")
            user_sql.add_sub_to_user(message.from_user.id, "silence")
        elif message.text == "⚠️ Тільки екстрені":
            await bot.send_message(message.from_user.id, "Добре, буду намагатись не тривожити тебе без причини ❕")
            user_sql.add_sub_to_user(message.from_user.id, "alert")
        elif message.text == "📅 Щоденна підписка":
            await bot.send_message(message.from_user.id, "Чудово, буду писати тобі щодня 🥰")
            user_sql.add_sub_to_user(message.from_user.id, "everyday")
        await bot.send_message(message.from_user.id, "Супер, тепер давай дізнаймося в якому місті ти знаходишся", reply_markup=reply.set_location_mark)

    if message.text == "Повернутись в меню ◀️":
        await bot.send_message(message.from_user.id, "Повертаємось в меню",
                               reply_markup=reply.main_mark)

    if message.text == "Змінити підписку🔄":
        await bot.send_message(message.from_user.id, "Обери підписку яку ти хочеш 👇", reply_markup=reply.sub_choice_mark)

    if message.text == "Подивитись погодку🌤":
        await bot.send_message(message.from_user.id, "На коли дивимось?", reply_markup=reply.weather_tri_mark)

    if message.text in "Погодка на сьогодні ▶️Погодка на завтра ⏩Погодка через день ⏭":
        day, text = "today", "сьогодні"
        if message.text == "Погодка через день ⏭":
            day = "after_tomorrow"
            text = "післязавтра"
        elif message.text == "Погодка на сьогодні ▶️":
            print("TEST")
            day = "today"
            text = "сьогодні"
        elif message.text == "Погодка на завтра ⏩":
            day = "tomorrow"
            text = "завтра"
        weather_data = weather_sql.get_weather_values(user_sql.get_coordinates(message.from_user.id), day=day)
        msg = f"""
Погода на {text}: {weather_data[0]}
Сонечко встає о {weather_data[1]} 🌅
Шанс на опади💧 : {weather_data[4]}% 
Опади {text} будуть {weather_data[2]} годин🕒
Середня температура 🌡: {weather_data[3]} C°
Швидкість вітру💨: {weather_data[5]}
"""
        if day == "today":
            await bot.send_message(message.from_user.id, msg, reply_markup=inline.mark_more_today)
        elif day == "tomorrow":
            await bot.send_message(message.from_user.id, msg, reply_markup=inline.mark_more_tomorrow)
        elif day == "after_tomorrow":
            await bot.send_message(message.from_user.id, msg, reply_markup=inline.mark_more_after_tomorrow)


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    user_sql.add_location_to_user(message.from_user.id, f"{round(message.location.latitude, 2)} {round(message.location.longitude, 2)}")
    weather_sql.update_weather_data(parse_weather.parse_weather(round(message.location.latitude, 2), round(message.location.longitude, 2)))
    await bot.send_message(message.from_user.id, "Молодчинка) Я запам'ятав твоє місто! Якщо захочеш його змінити-просто надішли мені мітку ще раз.", reply_markup=reply.main_mark)


@dp.callback_query_handler()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data in "?more_info_after_tomorrow?more_info_tomorrow?more_info_today":
        day = "today"
        if callback.data == "?more_info_after_tomorrow":
            day = "after_tomorrow"
        elif callback.data == "?more_info_today":
            day = "today"
        elif callback.data == "?more_info_tomorrow":
            day = "tomorrow"
        temp, drop, wind = weather_sql.get_hour_values(user_sql.get_coordinates(callback.from_user.id), day=day)
        print(temp, drop, wind)
        msg = f"""
🕘             🌡             💧          💨
0:00           {temp[0]} °С      {drop[0]}%     {wind[0]} м/c
3:00           {temp[1]} °С      {drop[1]}%     {wind[1]} м/c
6:00           {temp[2]} °С      {drop[2]}%     {wind[2]} м/c
9:00           {temp[3]} °С      {drop[3]}%     {wind[3]} м/c
12:00          {temp[4]} °С      {drop[4]}%     {wind[4]} м/c
15:00          {temp[5]} °С      {drop[5]}%     {wind[5]} м/c
18:00          {temp[6]} °С      {drop[6]}%     {wind[6]} м/c
21:00          {temp[7]} °С      {drop[7]}%     {wind[7]} м/c
"""

        await bot.send_message(callback.from_user.id, msg)
