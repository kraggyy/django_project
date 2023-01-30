from django.contrib import admin

from products.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sku', 'created_at')
    list_filter = ('price',)
    readonly_fields = ('id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
