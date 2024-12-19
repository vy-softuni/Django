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


@method_decorator(login_required, name='dispatch')
class ProductAddToCartView(View):
    http_method_names = ['post']

    def get_order(self):
        order, _ = Order.objects.get_or_create(
            customer=self.request.user, status=Order.OrderStatus.SHOPPING
        )
        return order

    def add_item(self, order, product, quantity):
        if not OrderItem.objects.filter(order=order, product=product).exists():
            OrderItem.objects.create(
                order=order,
                product=product,
                name=product.name,
                quantity=quantity,
                price=product.price,
                sale_price=(product.price - product.discount)
            )

    def post(self, request, *args, **kwargs):
        if product_id := self.request.POST.get('product'):
            product = get_object_or_404(Product, pk=product_id)
            order = self.get_order()
            quantity = int(self.request.POST.get('quantity', 1))
            self.add_item(order, product, quantity)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class ProductRemoveFromCartView(View):
    http_method_names = ['post']

    def remove_item(self, order, item_id):
        get_object_or_404(OrderItem, pk=item_id, order=order).delete()

    def post(self, request, *args, **kwargs):
        if item_id := self.request.POST.get('item'):
            self.remove_item(request.user.cart(), item_id)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class OrderItemQuantityUpdateView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        quantity = int(self.request.POST.get('quantity'))
        item_id = self.request.POST.get('item_id')
        if item_id and quantity:
            order_item = get_object_or_404(
                OrderItem, pk=item_id, order=request.user.cart()
            )
            if quantity > 10:
                quantity = 10
            elif quantity < 1:
                quantity = 1
            order_item.quantity = quantity
            order_item.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class AddPromoCodeView(TemplateView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        referer_url = request.META.get('HTTP_REFERER').split('?')[0]
        error = ""
        order = request.user.cart()
        code = request.POST.get('promo_code')
        if 'clear' in request.POST:
            order.promo_code = None
        else:
            if promo_code := PromoCode.objects.filter(code__exact=code).first():
                order.promo_code = promo_code
            else:
                error = f"?error=promo_code&promo_code={code}"
        order.save()
        return HttpResponseRedirect(referer_url+error)


class BillingAddressView(TemplateView, FormView):
    template_name = 'order/billing_address.html'
    extra_context = {'title': "Billing Address"}
    form_class = OrderBillingAddress
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['order'] = self.request.user.cart()
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        order = self.request.user.cart()
        billing_address = form.save(commit=False)
        billing_address.order = order
        billing_address.save()
        order.status = Order.OrderStatus.ORDER_PLACED
        order.save()
        return super().form_valid(form)


class OrderListView(TemplateView):
    template_name = 'order/list.html'
    extra_context = {'title': "Order List"}

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['orders'] = Order.objects.filter(
            customer=self.request.user,
        ).exclude(status=Order.OrderStatus.SHOPPING)
        return kwargs


class OrderDetailView(DetailView):
    template_name = 'order/detail.html'
    extra_context = {'title': "Order Detail"}
    queryset = Order.objects.exclude(status=Order.OrderStatus.SHOPPING)
