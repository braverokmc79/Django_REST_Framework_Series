from django.contrib import admin
from api.models import Order, OrderItem, Product
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    list_per_page = 20  # 한 페이지에 20개씩 표시
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]    
    list_per_page = 20  # 한 페이지에 20개씩 표시
    
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']
    list_per_page = 20  # 한 페이지에 20개씩 표시
    
    
    
admin.site.register(Product, ProductAdmin)        
admin.site.register(Order, OrderAdmin)    
admin.site.register(User, UserAdmin)  # ✅ User 모델 등록