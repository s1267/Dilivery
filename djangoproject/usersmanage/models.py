from jsonfield import JSONField
from django.db import models
import os


class TimeBasedModels(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModels):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID пользователя Телеграмм")
    name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    username = models.CharField(max_length=100, verbose_name="Username пользователя")
    email = models.CharField(max_length=100, verbose_name="Почта", null=True)
    phone_number = models.CharField(max_length=50, verbose_name="Номер телефона", null=True)

    def __str__(self):
        return f"#{self.id} ({self.user_id} - {self.name})"


class Admins(TimeBasedModels):
    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID пользователя Телеграмм")


class Category(TimeBasedModels):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Наименование категории", max_length=50)

    def __str__(self):
        return f"#{self.id}-{self.name}"


class SubCategory(TimeBasedModels):
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Наименование подкатегории", max_length=50)
    category_id = models.ForeignKey(Category, verbose_name="Id категории", on_delete=models.CASCADE)

    def __str__(self):
        return f"#{self.id}-{self.name}"


class Item(TimeBasedModels):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название Товара", max_length=50)
    photo = models.CharField(verbose_name="URL картинки", max_length=255)
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=8)
    desc = models.TextField(verbose_name="Описание", max_length=3000, blank=True, null=True)

    category_id = models.ForeignKey(Category, verbose_name="ID категории", on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(SubCategory, verbose_name="ID подкатегории", on_delete=models.CASCADE,
                                       blank=True, null=True)

    def __str__(self):
        return f"{self.id}-{self.name}"


class Purchase(TimeBasedModels):
    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"

    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, verbose_name="Покупатель", on_delete=models.SET(0))
    amount = models.DecimalField(verbose_name="Стоимость", decimal_places=2, max_digits=8, null=True)
    items = models.JSONField(verbose_name="Товары", null=True)
    payload = models.IntegerField(verbose_name="ID заказа", null=True)
    purchase_time = models.DateTimeField(verbose_name="Время покупки", auto_now_add=True)
    shipping_address = JSONField(verbose_name="Адрес доствки", null=True)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=50, null=True)
    successful = models.BooleanField(verbose_name="Состояние оплаты", default=False)

    def __str__(self):
        return f"#{self.id}-{self.buyer}-{self.amount}"


class Bascet(TimeBasedModels):
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзинки"

    user_id = models.ForeignKey(User, verbose_name="Id Пользователя", on_delete=models.SET(0))
    item_id = models.ForeignKey(Item, verbose_name="Id Товара", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество")
