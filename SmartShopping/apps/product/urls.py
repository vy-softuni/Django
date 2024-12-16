from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='list'),
    path(
        'product/<int:pk>/',
        views.ProductDetailView.as_view(),
        name='detail'
    ),
    path(
        'product/collection/<int:pk>/',
        views.ProductCollectionDetailView.as_view(),
        name='collection'
    ),
]

