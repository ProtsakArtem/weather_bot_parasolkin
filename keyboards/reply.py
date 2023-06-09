from aiogram import types

#Вибір типу підписки
btn_first_mode = types.KeyboardButton("📅 Щоденна підписка")
btn_second_mode = types.KeyboardButton("⚠️ Тільки екстрені")
btn_third_mode = types.KeyboardButton("🤐 Мовчу")
sub_choice_mark = types.ReplyKeyboardMarkup(resize_keyboard=True).add(btn_first_mode, btn_second_mode, btn_third_mode)


#Кнопка запросу геолокації
btn_send_location = types.KeyboardButton("Надіслати локацію 📍", request_location=True)
set_location_mark = types.ReplyKeyboardMarkup(resize_keyboard=True).add(btn_send_location)


#Головне меню
btn_check_weather = types.KeyboardButton("Подивитись погодку🌤")
btn_change_sub = types.KeyboardButton("Змінити підписку🔄")
main_mark = types.ReplyKeyboardMarkup(resize_keyboard=True).add(btn_check_weather, btn_change_sub)


#Меню погоди
btn_weather_today = types.KeyboardButton("Погодка на сьогодні ▶️")
btn_weather_tomorrow = types.KeyboardButton("Погодка на завтра ⏩")
btn_weather_after_tomorrow = types.KeyboardButton("Погодка через день ⏭")
btn_go_menu = types.KeyboardButton("Повернутись в меню ◀️")
weather_tri_mark = types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=3).add(btn_weather_today, btn_weather_tomorrow, btn_weather_after_tomorrow, btn_go_menu)