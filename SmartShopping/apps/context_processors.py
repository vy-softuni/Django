from core import PROJECT_NAME
from apps.product.models import ProductCollection, Category


def context(request):
    context = {
        "collections": ProductCollection.objects.filter(active=True),
        "categories": Category.objects.all(),
        "item_ids": [],
        "project_name": PROJECT_NAME,
    }
    if request.user.is_authenticated:
        order = request.user.cart()
        if hasattr(order, 'orderitem_set'):
            context["item_ids"] = list(
                order.orderitem_set.values_list("product_id", flat=True)
            )
    return context
