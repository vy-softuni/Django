from django.contrib import admin
from django.db import models
from django import forms

from apps.order.models import Order, OrderItem, PromoCode, OrderAddress


@admin.register(PromoCode)
class PromoCodeModelAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "active", "created")
    fields = (("code", "discount"), "active")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    min_num = 1
    exclude = ('name',)
    readonly_fields = ('price', 'sale_price', 'item_price')


class OrderAddressStacked(admin.StackedInline):
    model = OrderAddress
    extra = 0
    min_num = 1
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 1})},
    }
    fields = ("phone", ("city", "postcode"), "address")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline, OrderAddressStacked)
    list_display = (
        'id',
        'customer',
        'status',
        'payment_method',
        'payment_status',
        "discount",
        "total_price",
        "created",
    )
    list_display_links = ('id', 'customer', 'status')
    list_filter = ('status', 'payment_method', 'payment_status', 'created')
    search_fields = (
        'customer__email',
        'customer__first_name',
        'customer__last_name',
    )
    fields = (
        ('customer', 'status'),
        ('payment_method', 'payment_status'),
        'promo_code',
    )

    def customer(self, obj):
        return obj.customer.get_full_name()

    def discount(self, obj):
        return obj.coupon_discount
