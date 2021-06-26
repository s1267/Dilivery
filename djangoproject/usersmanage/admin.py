from django.contrib import admin

from .models import Item, Purchase, User, Bascet, Category, SubCategory, Admins


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "name", "username", "phone_number", "created_at")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category_id", "subcategory_id")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", 'amount', "created_at", "successful")


@admin.register(Admins)
class AdminsAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id")


@admin.register(Bascet)
class BascetAdmin(admin.ModelAdmin):
    list_display = ("user_id", "item_id", "quantity")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category_id")

# Register your models here.
