from venv import create
import django_filters
from api.models import Product, Order
from rest_framework import filters
from django_filters import DateFromToRangeFilter


class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)  # 재고가 0보다 큰 상품만 필터링


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'], 
            'price': ['exact', 'lt', 'gt', 'range']
        }
        
        
class OrderFilter(django_filters.FilterSet):
    #created_at = django_filters.DateFilter(field_name='created_at__date')
    created_at = DateFromToRangeFilter(field_name='created_at__date')
        
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact']
        } 