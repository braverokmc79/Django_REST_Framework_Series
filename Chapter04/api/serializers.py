from os import read
from turtle import mode
from rest_framework import serializers
from .models import Product, Order, OrderItem


#개별 상품 정보 직렬화
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


    

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price')
    
    class Meta:
        model = OrderItem
        fields = ('product_name','product_price','quantity','item_subtotal')



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')
    
    def total(self, obj):
      order_items = obj.items.all()
      return sum(order_item.item_subtotal for order_item in order_items)
    
    
    class Meta:
        model = Order
        fields = ('order_id', 'created_at',  'user', 'status', 'items' , 'total_price')

        

#전체 상품 목록과 함께, 총 개수(count), 최대 가격(max\_price) 정보 포함
class ProductInfoSerializer(serializers.Serializer):
     products =ProductSerializer(many=True)
     count =serializers.IntegerField()
     max_price =serializers.FloatField()
