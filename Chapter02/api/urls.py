from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = ""  

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)