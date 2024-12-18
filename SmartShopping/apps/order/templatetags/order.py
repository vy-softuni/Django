from django import template
from django.conf import settings

from currencies import Currency

register = template.Library()

@register.filter
def item_total(product, quantity):
    price = product.price - product.discount
    return Currency(settings.DEFAULT_CURRENCY).get_money_format(
        price * quantity
    )
