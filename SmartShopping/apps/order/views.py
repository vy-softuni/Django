from django.views.generic import TemplateView, FormView, View, DetailView
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from apps.order.models import Order, OrderItem, PromoCode
from apps.product.models import Product
from apps.order.forms import OrderBillingAddress


@method_decorator(login_required, name='dispatch')
class CartView(TemplateView):
    template_name = 'order/cart.html'
    extra_context = {'title': "Shopping Cart"}

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['cart_order'] = Order.objects.filter(
            customer=self.request.user,
            status=Order.OrderStatus.SHOPPING
        ).first()
        return kwargs


