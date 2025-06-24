from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('products/')),
    
    # http://127.0.0.1:8000/products/
    path('products/', views.product_list),
    # http://127.0.0.1:8000/products/1
    path('products/<int:pk>/', views.product_detail),
    # http://127.0.0.1:8000/orders/
    path('orders/', views.order_list),
    # http://127.0.0.1:8000/products/info
    path('products/info/', views.product_info),
]
