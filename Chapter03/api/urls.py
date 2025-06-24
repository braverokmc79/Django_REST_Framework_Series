from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: redirect('product_list')),
    path('products/', views.product_list, name="product_list"),
    path('products/<int:pk>/', views.product_detail),
    path('orders/', views.order_list),
]
