from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_category, get_items, count_items, get_subcategory

buy_button = InlineKeyboardButton("Оплатить", pay=True)
clear_basket = InlineKeyboardButton('Очистить корзину', callback_data='clear')
markup = InlineKeyboardMarkup().add(buy_button, clear_basket)
