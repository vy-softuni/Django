from django.urls import path, include

from apps.views import HomeView
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('', include('apps.product.urls')),
    path('account/', include('apps.accounts.urls')),
    path('', include('apps.order.urls')),
]
