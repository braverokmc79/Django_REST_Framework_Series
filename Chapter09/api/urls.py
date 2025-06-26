from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('products/')),
    
    # http://127.0.0.1:8000/products/
    # http://127.0.0.1:8000/products/1        
    # http://127.0.0.1:8000/products/info 
    # http://127.0.0.1:8000/orders/   
    # http://127.0.0.1:8000/user-orders  
        
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),
]


    
