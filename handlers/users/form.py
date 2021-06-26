import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async

from state import Form

from keyboards.default import start_keyboard
from keyboards.inline.cancel_form_keyboard import cancel_mark_up

from loader import dp, bot
from utils.db_api.db_commands import select_user


@dp.message_handler(text="Форма доставки")
async def enter_form(message: types.Message):
    await Form.name.set()
    await message.answer(f"Для заполнения формы, назовите ваше имя:",
                         reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(state='*', text="cancel_form")
async def cancel_handler(callback_data: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await bot.answer_callback_query(callback_data.id, cache_time=None)
    await callback_data.message.answer('Закрыто.', reply_markup=start_keyboard.start_markup)


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    mark_up = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отправить номер телефона', request_contact=True))
    print(message)
    await Form.next()
    await message.answer('Укажите номер телефона:', reply_markup=mark_up)


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Form.number_phone)
async def give_thanks(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.contact['phone_number']
    user = await select_user(message.from_user.id)
    user.name = data['name']
    user.phone_number = data['phone']
    await sync_to_async(user.save)()
    await message.answer('Спасибо за заполнение формы. Приступайте к покупкам :3',
                         reply_markup=start_keyboard.start_markup)
    await state.finish()
