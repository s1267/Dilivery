from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_markup = ReplyKeyboardMarkup(resize_keyboard=True)
start_markup.add(KeyboardButton("Меню")).add(KeyboardButton("Корзина")).add(KeyboardButton("Форма доставки"))
