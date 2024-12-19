from django.urls import path

from apps.order import views

app_name = 'order'

urlpatterns = [
    path('shopping-cart/', views.CartView.as_view(), name='cart'),
    path(
        'add-to-cart/',
        views.ProductAddToCartView.as_view(),
        name='add_to_cart'
    ),
    path(
        'remove-from-cart/',
        views.ProductRemoveFromCartView.as_view(),
        name='remove_from_cart'
    ),
    path(
        'update-cart/',
        views.OrderItemQuantityUpdateView.as_view(),
        name='update_cart'
    ),
    path('add-promo/', views.AddPromoCodeView.as_view(), name='add_promo'),
    path('address/', views.BillingAddressView.as_view(), name='address'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='detail'),
]
