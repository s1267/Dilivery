from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_category, get_items, count_items, get_subcategory

menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
add_to_basket = CallbackData("add", "item_id")


def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(level=level, category=category, subcategory=subcategory, item_id=item_id)


async def categories_keyboard():
    CURRENT_LEVEL = 0
    mark_up = InlineKeyboardMarkup()
    categories = await get_category()
    for category in categories:
        number_of_items = await count_items(category_id=category.id)
        button_text = f"{category.name}({number_of_items} шт)"
        subcategories = await get_subcategory(category_id=category.id)
        if subcategories:
            callback_data = make_callback_data(CURRENT_LEVEL + 1, category=category.id)
        else:
            callback_data = make_callback_data(CURRENT_LEVEL + 2, category=category.id)
        mark_up.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return mark_up


async def subcategories_keyboard(category_id):
    CURRENT_LEVEL = 1
    mark_up = InlineKeyboardMarkup()
    subcategories = await get_subcategory(category_id=category_id)
    for subcategory in subcategories:
        number_of_items = await count_items(category_id=category_id, subcategory_id=subcategory.id)
        button_text = f"{subcategory.name} ({number_of_items} шт)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category_id, subcategory=subcategory.id)
        mark_up.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    mark_up.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category_id)
        )
    )
    return mark_up


async def items_keybord(category_id, subcategory_id):
    CURRENT_LEVEL = 2
    mark_up = InlineKeyboardMarkup(row_width=1)
    if subcategory_id == "0":
        items = await get_items(category_id=category_id)
        print(items)
    else:
        items = await get_items(category_id=category_id, subcategory_id=subcategory_id)
        print(items)
    for item in items:
        button_text = f"{item.name}-{item.price}₽"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category_id, subcategory=subcategory_id,
                                           item_id=item.id)
        mark_up.insert(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    if subcategory_id =="0":
        mark_up.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=CURRENT_LEVEL - 2, category=category_id, subcategory=subcategory_id)
            )
        )
    else:
        mark_up.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category_id)
            )
        )
    return mark_up


def item_keyboard(category_id, subcategory_id, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Добавить в корзину",
            callback_data=add_to_basket.new(item_id=item_id)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category_id, subcategory=subcategory_id)
        )
    )
    return markup
