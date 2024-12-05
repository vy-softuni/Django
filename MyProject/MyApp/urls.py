from django.urls import path
from . import views

urlpatterns = [
    path('MyApp/', views.MyApp, name='MyApp'),
]