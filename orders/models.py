import decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.model_mixin import PKMixin
from shop.model_choices import DiscountTypes


class Discount(PKMixin):
    amount = models.PositiveSmallIntegerField(
        default=0
    )
    code = models.CharField(
        max_length=32
    )
    is_active = models.BooleanField(
        default=True
    )
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )


class Order(PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    products = models.ManyToManyField(
        "products.Product",
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def get_products_through(self):
        return self.products.through.objects \
            .filter(order=self) \
            .select_related('product') \
            .annotate(full_price=F('product__price') * F('quantity'))

    def get_total_amount(self):
        total_amount = 0
        for product_relation in self.get_products_through().iterator():
            total_amount += product_relation.full_price * product_relation.product.curs  # noqa

        if self.discount:
            total_amount = (
                total_amount - self.discount.amount
                if self.discount.discount_type == DiscountTypes.VALUE else
                total_amount - (
                        self.total_amount / 100 * self.discount.amount
                )
            ).quantize(decimal.Decimal('.01'))
        return total_amount
