from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.start_keyboard import start_markup
from keyboards.inline.caregory_keyboard import categories_keyboard, subcategories_keyboard, items_keybord, \
    item_keyboard, menu_cd, add_to_basket
from loader import dp, bot
from utils.db_api.db_commands import get_item, select_user, add_bascet


async def get_menu(message: types.Message):
    await list_categories(message)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    mark_up = await categories_keyboard()
    if isinstance(message, types.Message):
        await message.answer("Наши категории", reply_markup=mark_up)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await bot.answer_callback_query(call.id, cache_time=None)
        await call.message.edit_text("Наши категории", reply_markup=mark_up)


async def list_subcategories(callback: types.CallbackQuery, category_id, **kwargs):
    mark_up = await subcategories_keyboard(category_id=category_id)
    await bot.answer_callback_query(callback.id, cache_time=None)
    await callback.message.edit_text("Наши подкатегории", reply_markup=mark_up)


async def list_items(callback: types.CallbackQuery, category_id, subcategory_id, **kwargs):
    mark_up = await items_keybord(category_id=category_id, subcategory_id=subcategory_id)
    await bot.answer_callback_query(callback.id, cache_time=None)
    await callback.message.edit_text("Наши товары", reply_markup=mark_up)


async def show_item(callback: types.CallbackQuery, category_id, subcategory_id, item_id, **kwargs):
    mark_up = item_keyboard(category_id=category_id, subcategory_id=subcategory_id, item_id=item_id)
    item = await get_item(item_id)
    caption = f'Купи {item.name}\nОписание:{item.desc}\nЦена:{item.price}₽\nФото:<a href="{item.photo}">-</a>'
    print(caption)
    await bot.answer_callback_query(callback.id, cache_time=None)
    await callback.message.edit_text(caption, reply_markup=mark_up)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    item_id = callback_data.get('item_id')
    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items,
        "3": show_item
    }
    current_level_func = levels[current_level]
    print(current_level_func)

    await current_level_func(
        call,
        category_id=category,
        subcategory_id=subcategory,
        item_id=item_id
    )


@dp.callback_query_handler(add_to_basket.filter())
async def add_to_basket(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    print("я словил")
    item_id = callback_data.get('item_id')
    user = await select_user(call.from_user.id)
    item = await get_item(item_id=item_id)
    print(user.id, item.id)
    basket = {'user_id': user.id, 'item_id': item.id, 'quantity': 0}
    await state.update_data(basket=basket, item=item)
    await bot.answer_callback_query(call.id, cache_time=None)
    await call.message.answer("Введите кол-во товара", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("enter_quantity")


@dp.message_handler(state='enter_quantity')
async def enter_quantity(message: types.Message, state: FSMContext):
    quantity = message.text
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer("Введите заново")
    if quantity < 100:

        async with state.proxy() as data:
            data['basket']['quantity'] = quantity
        basket = data.get('basket')
        add = await add_bascet(user_id=basket['user_id'], item_id=basket['item_id'], quantity=basket['quantity'])
        await message.answer("Товар добавлен в корзину", reply_markup=start_markup)
        await state.finish()
    else:
        await message.answer("Количество превышает допустимое значение. Введите значение меньше")
