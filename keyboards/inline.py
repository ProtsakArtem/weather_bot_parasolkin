from aiogram import types

#Common buttons
btn_more_info_today = types.InlineKeyboardButton(text="Детальніше", callback_data="?more_info_today")
mark_more_today = types.InlineKeyboardMarkup(row_width=1).add(btn_more_info_today)
btn_more_info_tomorrow = types.InlineKeyboardButton(text="Детальніше", callback_data="?more_info_tomorrow")
mark_more_tomorrow = types.InlineKeyboardMarkup(row_width=1).add(btn_more_info_tomorrow)
btn_more_info_after_tomorrow = types.InlineKeyboardButton(text="Детальніше", callback_data="?more_info_after_tomorrow")
mark_more_after_tomorrow = types.InlineKeyboardMarkup(row_width=1).add(btn_more_info_after_tomorrow)

