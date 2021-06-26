from typing import List

from djangoproject.usersmanage.models import User, Purchase, Bascet, Item, Category, SubCategory, Admins
from asgiref.sync import sync_to_async


@sync_to_async()
def select_user(user_id: int) -> User:
    user = User.objects.filter(user_id=user_id).first()
    print(user)
    return user


@sync_to_async()
def add_user(user_id, name, username, email=None, phone_number=None):
    try:
        return User(user_id=int(user_id), username=username, name=name, email=email, phone_number=phone_number).save()
    except Exception:
        return select_user()


@sync_to_async()
def select_all_users() -> List[User]:
    users = User.objects.all()
    return users


@sync_to_async()
def count_users():
    return User.objects.all().count()


@sync_to_async()
def get_item(item_id) -> Item:
    return Item.objects.filter(id=int(item_id)).first()


@sync_to_async()
def get_items(category_id, subcategory_id=None) -> List[Item]:
    return Item.objects.filter(category_id=int(category_id), subcategory_id=subcategory_id).all()


@sync_to_async()
def count_items(category_id, subcategory_id=None):
    if subcategory_id:
        return Item.objects.filter(category_id=category_id, subcategory_id=subcategory_id).all().count()
    else:
        return Item.objects.filter(category_id=category_id).all().count()


@sync_to_async()
def get_category() -> List[Category]:
    return Category.objects.all()


@sync_to_async()
def get_subcategory(category_id) -> List[SubCategory]:
    return SubCategory.objects.filter(category_id=int(category_id)).all()


@sync_to_async()
def add_bascet(user_id, item_id, quantity):
    return Bascet(user_id_id=user_id, item_id_id=item_id, quantity=quantity).save()


@sync_to_async()
def select_purchase(payload) -> Purchase:
    return Purchase.objects.filter(payload=payload).first()


@sync_to_async()
def add_purchase(user_id, successful, amount=None, phone=None, shipping_address=None, payload=None, items=None):
    return Purchase(buyer_id=user_id, amount=amount, shipping_address=shipping_address, phone_number=phone,
                    payload=payload, items=items, successful=successful).save()


@sync_to_async()
def get_bascet(user_id):
    return Bascet.objects.filter(user_id=user_id).all()


@sync_to_async()
def delete_bascet(user_id):
    return Bascet.objects.filter(user_id=user_id).delete()


@sync_to_async()
def get_admins() -> List[Admins]:
    return Admins.objects.all()
