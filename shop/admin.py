from django.contrib import admin
from shop.models.categories import Category
from shop.models.products import Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "name",
        "image",
        "description",
        "price",
        "available",
        "created",
        "updated",
    ]
    list_filter = ["category", "available", "created", "updated"]
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}
