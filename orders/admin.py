from django.contrib import admin

from orders.models import Discount, Order


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('amount', 'discount_type', 'is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'discount')
