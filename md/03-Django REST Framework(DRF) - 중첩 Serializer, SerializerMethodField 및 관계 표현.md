## Django REST Framework(DRF) - 중첩 Serializer, SerializerMethodField 및 관계 표현

### 1. 개요

이번 영상에서는 Django REST Framework(DRF)를 활용해 **중첩 Serializer**와 **SerializerMethodField**를 사용하여 관계형 데이터를 직렬화하는 방법을 배웁니다. 특히 외래 키(ForeignKey)와 다대다 관계에서 데이터를 어떻게 표현하고, 데이터를 중첩해서 JSON 응답으로 반환할 수 있는지 다룹니다.

---

### 2. 중첩 Serializer 구현하기

`Order` 모델과 `OrderItem` 모델 간의 관계를 중첩해서 표현하려면, `OrderSerializer` 안에 `OrderItemSerializer`를 필드로 선언합니다.

```python
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'created_at', 'status', 'items')
```

> `many=True`: 리스트 형태의 데이터임을 의미함 `read_only=True`: 생성 시 이 필드는 입력받지 않음

모델에 `related_name='items'`를 설정해야 `order.items.all()`로 접근이 가능합니다:

```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
```

---

### 3. SerializerMethodField 사용하기

`SerializerMethodField`는 모델에 없는 값을 동적으로 계산하여 응답에 포함할 수 있습니다. 예: 총 주문 금액 계산

```python
class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'created_at', 'status', 'items', 'total_price')

    def get_total_price(self, obj):
        return sum(item.item_subtotal for item in obj.items.all())
```

`item_subtotal`은 `OrderItem` 모델의 `@property`입니다:

```python
@property
def item_subtotal(self):
    return self.product.price * self.quantity
```

---

### 4. ForeignKey 데이터를 표현하는 다양한 방식

기본적으로 외래 키는 ID(PK) 값으로 표현됩니다. 하지만 DRF에서는 다양한 방법으로 외래 키 데이터를 표현할 수 있습니다:

#### 방법 1: 기본 PK 표현 (기본값)

```json
"user": 1
```

#### 방법 2: 중첩 Serializer로 표현

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
```

#### 방법 3: 문자열 표현 (StringRelatedField)

```python
user = serializers.StringRelatedField(read_only=True)
```

> 모델에 `__str__` 정의 필요

#### 방법 4: HyperlinkedRelatedField

```python
user = serializers.HyperlinkedRelatedField(
    view_name='user-detail',
    read_only=True
)
```

#### 방법 5: SlugRelatedField

```python
user = serializers.SlugRelatedField(
    slug_field='username',
    read_only=True
)
```

---

### 5. 중첩 구조 대신 평면 구조로 표현하기

중첩을 피하고 특정 필드만 평면적으로 노출하고 싶을 경우:

```python
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='product.price')

    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')
```

---

### 6. 모델 프로퍼티를 직렬화에 포함하기

모델에 정의된 `@property`도 `fields`에 명시하면 응답에 포함시킬 수 있습니다:

```python
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')
```

---

### 7. 마무리

이번 영상에서는 다음을 다뤘습니다:

- 중첩 Serializer를 사용하여 관계형 모델을 JSON으로 표현
- `SerializerMethodField`로 동적 필드 생성
- 외래 키 데이터 표현 방법 다양화
- JSON 구조를 평면화(flatten)하여 응답 가독성 개선

> 다음 영상에서는 모델에 종속되지 않은 일반 Serializer를 사용하여 집계 데이터를 처리하는 방법을 배웁니다.

