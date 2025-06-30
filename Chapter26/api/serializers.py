from attr import fields
from rest_framework import serializers
from .models import Product, Order, OrderItem, User
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'user_permissions', 'is_authenticated', 'get_full_name', 'orders')        
        # exclude = ('password', 'user_permissions')
        # fields = '__all__'    





# ✅ 개별 상품 정보 직렬화
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock')
        extra_kwargs = {
            'name': {'label': '상품명'},
            'description': {'label': '상품 설명'},
            'price': {'label': '가격'},
            'stock': {'label': '재고 수량'},
        }

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("가격은 0보다 커야 합니다.")
        return value


# ✅ 주문 항목 직렬화
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', label='상품명')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price',
        label='상품 가격'
    )

    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')
        extra_kwargs = {
            'quantity': {'label': '수량'},
            'item_subtotal': {'label': '소계'},
        }


# ✅ 주문 직렬화
class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True, label='주문 항목')
    total_price = serializers.SerializerMethodField(method_name='total', label='총 가격')

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = ('order_id', 'created_at', 'user', 'status', 'items', 'total_price')
        extra_kwargs = {
            'order_id': {'label': '주문 ID'},
            'created_at': {'label': '주문일'},
            'user': {'label': '사용자'},
            'status': {'label': '주문 상태'},
        }



# ✅ 새로운 중첩 생성용 Serializer 정의
class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items', None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if orderitem_data is not None:
                # Clear existing items (optional, depends on requirements)
                instance.items.all().delete()

                # Recreate items with the updated data
                for item in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)
        return instance


    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)

        return order


    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'status',
            'items',
        )
        extra_kwargs = {
            'user': {'read_only': True}
        }








# ✅ 전체 상품 목록 + 통계 직렬화
class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True, label='상품 목록')
    count = serializers.IntegerField(label='상품 개수')
    max_price = serializers.FloatField(label='최고가')
