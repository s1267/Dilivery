from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardRemove

from handlers.users.item_to_basket import send_user_basket
from handlers.users.menu import get_menu
from keyboards.default import start_keyboard
from utils.db_api.db_commands import add_user
from keyboards.inline import caregory_keyboard

from loader import dp
import logging


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await add_user(user_id=message.from_user.id, username=message.from_user.username,
                          name=message.from_user.full_name)
    await message.answer(
        f"Здравствуйте,{message.from_user.full_name}\n Напишите мне в телеграмм: <b>@Cherbuxa</b>\n Вас приветствует служба доставки быстрой еды <b>Null</b>.\n Прежде чем приступить к покупкам, заполните контактную форму по кнопке на вашей панели",
        reply_markup=start_keyboard.start_markup)


@dp.message_handler(commands=['myid'])
async def get_user_id(message: types.Message):
    await message.answer(f"Ваш ID :{message.from_user.id}")


@dp.message_handler(text="Меню")
async def answer_menu(message: types.Message):
    await get_menu(message)


@dp.message_handler(text="Корзина")
async def go_backet(message: types.Message):
    await send_user_basket(message)

