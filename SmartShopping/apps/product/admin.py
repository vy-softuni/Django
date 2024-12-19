from django.contrib import admin
from django.db.models import ImageField

from image_uploader_widget.widgets import ImageUploaderWidget

from apps.product.models import Product, Category, ProductCollection


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", 'created')
    list_filter = ('created',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'price',
        'discount',
        'total_price',
        'category',
        'active',
        'created'
    )
    fields = (
        ('name', 'category'),
        ('price', 'discount'),
        'description',
        'image',
        ('sku', 'active')
    )
    list_display_links = ('name', 'sku')
    list_editable = ('price', 'discount', 'active')
    list_filter = ('category', 'active', 'created')
    search_fields = ('name', 'sku', 'description', 'category__name')
    formfield_overrides = {ImageField: {'widget': ImageUploaderWidget}}


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    list_display = ("name", 'active', 'show_on_homepage', 'order', 'created')
    list_filter = ('active', 'created')
    list_editable = ('active', 'show_on_homepage', 'order')
    search_fields = ('name',)
    filter_horizontal = ('products',)
    fields = (
        'name',
        'description',
        'products',
        ('order', 'active', 'show_on_homepage'),
    )
