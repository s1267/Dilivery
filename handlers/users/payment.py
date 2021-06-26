import random
from aiogram import types
from aiogram.types import LabeledPrice, ContentTypes
import json

from asgiref.sync import sync_to_async

from loader import dp, bot
from utils.db_api.db_commands import select_user, delete_bascet, add_purchase, select_purchase,get_admins
from utils.misc import ItemPayment
from keyboards.inline.bascket_keyboard import markup



async def invoice_for_payment(message: types.Message):
    from handlers.users.item_to_basket import get_user_basket
    user = await select_user(message.from_user.id)
    dict = await get_user_basket(message)
    dict_to_json = json.dumps({dict[elem]['item'].name: dict[elem]['basket'].quantity for elem in dict},
                              sort_keys=False, ensure_ascii=False, separators=(',', ': '))
    print(dict_to_json)
    payload = random.randint(100000, 999999)
    text = [
        f"{elem + 1}){dict[elem]['item'].name}(Количество: {dict[elem]['basket'].quantity})->{dict[elem]['item'].price}"
        for elem in dict]
    print(text)
    item_for_pay = ItemPayment(
        title='Оплата',
        description="Общая стоимость",
        currency="RUB",
        prices=[

            LabeledPrice(
                label=dict[element]['item'].name,
                amount=(int(float(round(dict[element]['item'].price, 2)) * dict[element]['basket'].quantity * 100)))
            for element in dict
        ],
        start_parameter=f"create_invoice_from_basket_{message.from_user.id}",
        reply_markup=markup,
        need_shipping_address=True
    )
    purchase_data_add = await add_purchase(
        user_id=user.id,
        items=dict_to_json,
        payload=payload,
        successful=False
    )
    await bot.send_message(chat_id=message.chat.id, text="Ваша корзина:\n" + '\n'.join(text))
    await bot.send_invoice(chat_id=message.chat.id, **item_for_pay.generate_invoice(),
                           payload=payload)


@dp.pre_checkout_query_handler()
async def pre_checkout_query(query: types.PreCheckoutQuery):
    user = await select_user(query.from_user.id)
    if user.phone_number:
        await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True,
                                            error_message="Что-то пошло не так")
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False)
        await bot.send_message(chat_id=query.from_user.id, text="Вы не оставили свой номер телефона")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    print(message)
    json_shipping = json.dumps(dict(message.successful_payment.order_info.shipping_address), sort_keys=False,
                               ensure_ascii=False, separators=(',', ': '))
    print(json_shipping)
    print(type(json_shipping))
    user = await select_user(message.from_user.id)
    invoice_payload = message.successful_payment.invoice_payload
    purchase = await select_purchase(int(invoice_payload))
    purchase.shipping_address = json_shipping
    purchase.phone_number = user.phone_number
    purchase.successful = True
    await sync_to_async(purchase.save)()
    json_items = json.loads(purchase.items)
    json_address = json.loads(purchase.shipping_address)
    list_admins = await get_admins()
    for admin in list_admins:
        await bot.send_message(chat_id=admin.user_id, text=f"Новый заказ №{purchase.payload}\nТело заказа:\n" + '\n'.join(
            ['<b>[{1}]{0}</b>'.format(k, v) for (k, v) in
             json_items.items()]) + f"\nАдрес: {json_address['street_line1']}" + f"\nИмя покупателя:{user.name}\nТелефон:{purchase.phone_number}")
    clear = await delete_bascet(user_id=user.id)
    await bot.send_message(message.chat.id,
                           'Спасибо за то что воспользовались нашим сервисом\nСписание на сумму` {} {}` прошло успешно'.format(
                               message.successful_payment.total_amount / 100, message.successful_payment.currency),
                           parse_mode='Markdown')
