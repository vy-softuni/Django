from django.db import models
from django.conf import settings



from apps.models import TimestampedModel


class Category(TimestampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product/")
    discount = models.IntegerField(default=0)
    sku = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        price = self.price - self.discount
        return 

class ProductCollection(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    products = models.ManyToManyField(Product)
    active = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    @property
    def active_products(self):
        return self.products.filter(active=True)[:12]
