from rest_framework import serializers
from .models import Product, Order, OrderItem

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
    
    class OrderItemCreateSerializer(serializers.ModelSerializer): # 🔹 내부에 중첩 직렬화 클래스 정의: 주문 항목 (OrderItem)을 처리
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')  # product: ForeignKey, quantity: IntegerField
  
    order_id = serializers.UUIDField(read_only=True)   # 🔹 주문 고유 ID (UUID) 필드: 읽기 전용 (자동 생성됨)
    items = OrderItemCreateSerializer(many=True) # 🔹 주문 항목 목록을 중첩으로 받음 (OrderItemCreateSerializer를 다수로 처리)
    
    def create(self, validated_data):  # ✅ 주문 생성 로직 재정의 (직접 create 오버라이드)
        orderitem_data = validated_data.pop('items')         # 1️⃣ OrderItem 데이터 분리
        order = Order.objects.create(**validated_data)         # 2️⃣ Order 생성 (user, status 등)

        for item in orderitem_data:                             # 3️⃣ OrderItem 하나씩 생성 및 Order에 연결
            OrderItem.objects.create(order=order, **item)
        return order                                 # 생성된 order 반환

    class Meta:
        model = Order
        fields = (
            'order_id',   # 읽기 전용 UUID
            'user',       # 요청 시 자동 할당 (read_only)
            'status',     # 주문 상태 (ex. 'pending')
            'items',      # 주문 항목 리스트
        )
        extra_kwargs = {
            'user': {'read_only': True}  # 요청자가 자동으로 지정되므로 수동 입력 금지
        }



# ✅ 전체 상품 목록 + 통계 직렬화
class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True, label='상품 목록')
    count = serializers.IntegerField(label='상품 개수')
    max_price = serializers.FloatField(label='최고가')
