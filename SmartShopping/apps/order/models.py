from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.conf import settings


from apps.models import TimestampedModel


class CustomerAddress(TimestampedModel):
    customer = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE
    )
    address = models.TextField()
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)



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
        return 

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
