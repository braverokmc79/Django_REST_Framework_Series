from django.contrib import admin
from api.models import Order, OrderItem, Product


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