from typing import Union

from aiogram import types

from handlers.users.payment import invoice_for_payment
from keyboards.inline.bascket_keyboard import markup
from loader import dp, bot
from utils.db_api.db_commands import select_user, get_bascet, get_item, delete_bascet


async def get_user_basket(message: Union[types.Message, types.CallbackQuery]):
    global user
    dict = {}
    if isinstance(message, types.Message):
        user = await select_user(message.from_user.id)
    elif isinstance(message, types.CallbackQuery):
        user = await select_user(message.message.chat.id)
    user_basket = await get_bascet(user_id=user.id)
    if user_basket:
        for c, items in enumerate(user_basket):
            item = await get_item(item_id=items.item_id_id)
            dict.update({c: {'item': item, 'basket': items}})
        return dict
    else:
        return None


async def send_user_basket(message: types.Message):
    dict = await get_user_basket(message=message)
    if not dict:
        await message.answer(text="Ваша корзина пуста")
    else:
        await invoice_for_payment(message)


@dp.callback_query_handler(text='clear')
async def delete_items(callback_query: types.CallbackQuery):
    user = await select_user(callback_query.from_user.id)
    clear = await delete_bascet(user_id=user.id)
    await bot.answer_callback_query(callback_query.id, cache_time=None, text='Все предметы были удалены',
                                    show_alert=True)
