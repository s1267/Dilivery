from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_keyboard = InlineKeyboardButton("Отменить", callback_data='cancel_form')
cancel_mark_up = InlineKeyboardMarkup().add(cancel_keyboard)