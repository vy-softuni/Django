from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.conf import settings

from currencies import Currency

from apps.models import TimestampedModel


class CustomerAddress(TimestampedModel):
    customer = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE
    )
    address = models.TextField()
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)


class PromoCode(TimestampedModel):
    code = models.CharField(max_length=100, unique=True)
    discount = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Promo code"
        verbose_name_plural = "Promo codes"


class Order(TimestampedModel):
    class OrderStatus(models.IntegerChoices):
        SHOPPING = 1, "Shopping"
        ORDER_PLACED = 2, "Order Placed"
        PROCESSED = 3, "Processed"
        SHIPPED = 4, "Shipped"
        DELIVERED = 5, "Delivered"
        CANCELLED = 6, "Cancelled"

    class PaymentMethod(models.IntegerChoices):
        CASH = 1, "Cash"
        CARD = 2, "Card"

    class PaymentStatus(models.IntegerChoices):
        PAID = 1, "Paid"
        UNPAID = 2, "Unpaid"

    status = models.IntegerField(
        choices=OrderStatus, default=OrderStatus.SHOPPING
    )
    payment_method = models.IntegerField(
        choices=PaymentMethod, default=PaymentMethod.CASH
    )
    payment_status = models.IntegerField(
        choices=PaymentStatus, default=PaymentStatus.UNPAID
    )
    customer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )
    promo_code = models.ForeignKey(
        "order.PromoCode", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_price(self):
        total = 0
        for item in self.orderitem_set.all():
            total += item.item_price
        return total

    @property
    def total_price(self):
        return Currency(settings.DEFAULT_CURRENCY).get_money_format(
            self.get_total_price_after_discount()
        )

    def get_total_price_after_discount(self):
        total_price = self.get_total_price()
        if self.promo_code:
            total_price -= self.promo_code.discount
        return total_price

    @property
    def get_subtotal(self):
        return Currency(settings.DEFAULT_CURRENCY).get_money_format(
            self.get_total_price()
        )

    @property
    def coupon_discount(self):
        price = 0
        if self.promo_code:
            price = self.promo_code.discount
        return Currency(settings.DEFAULT_CURRENCY).get_money_format(price)


class OrderItem(TimestampedModel):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        "product.Product", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    price = models.IntegerField()
    sale_price = models.IntegerField()

    @property
    def item_price(self):
        price = self.product.price - self.product.discount
        return self.quantity * price


class OrderAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
