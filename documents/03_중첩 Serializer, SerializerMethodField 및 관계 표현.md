## 03-중첩 Serializer, SerializerMethodField 및 관계 표현



[03 - 중첩 Serializer, SerializerMethodField 및 관계 표현](https://youtu.be/KfSYadIFHgY?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



---


### 1. 개요

이번 영상에서는 Django REST Framework(DRF)를 활용해 **Nested(중첩) Serializer**와 **SerializerMethodField**를 사용하여 관계형 데이터를 직렬화하는 방법을 배웁니다. 특히 외래 키(ForeignKey)와 다대다 관계에서 데이터를 어떻게 표현하고, 데이터를 Nested(중첩)해서 JSON 응답으로 반환할 수 있는지 다룹니다.


Django REST Framework(DRF)에서 Nested Serializer(중첩 직렬화기)란,  
모델 간의 관계(ForeignKey, OneToMany, ManyToMany 등)를 반영해서 직렬화 시, 다른 Serializer를 내부에 포함시키는 방식**을 말합니다.

#### ✅ 예시로 이해하기

🎯 모델 예제
```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

```


🎯 기본적인 Serializer
```python
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()  # ✅ 중첩(Nested) Serializer

    class Meta:
        model = Book
        fields = ['id', 'title', 'author']

```

📌 이렇게 하면 Book 직렬화 시 `author` 필드는 author의  전체 정보(dict)로 표현됩니다.

🎯 결과 JSON 예시

```json
{
  "id": 1,
  "title": "REST API with Django",
  "author": {
    "id": 1,
    "name": "홍길동"
  }
}

```

✅ 왜 사용하는가?

| 장점               | 설명                                                 |
| ---------------- | -------------------------------------------------- |
| **가독성 향상**       | 연관된 모델 데이터를 한 번에 포함시킬 수 있음                         |
| **쿼리 절감**        | select_related 또는 prefetch_related와 병행 시 쿼리 최적화 가능 |
| **복잡한 구조 표현 가능** | 계층적 데이터(API) 표현에 적합                                |

## ⚠️ 주의점

- `Nested Serializer`는 **읽기 전용 (`read_only=True`)** 으로 쓰는 것이 일반적임  
    → 쓰기까지 지원하려면 `create()`/`update()` 메서드 재정의 필요
    
- 복잡해질수록 성능 이슈 발생 가능




---

### 2. Nested(중첩) Serializer 구현하기

`Order` 모델과 `OrderItem` 모델 간의 관계를 Nested(중첩)해서 표현하려면, `OrderSerializer` 안에 `OrderItemSerializer`를 필드로 선언합니다.

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
   order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
```

 
 related_name='items'는  Order 모델에서 OrderItem에 접근할 때 사용할 이름을 지정한 것
따라서 `order.items.all()`로 하면 OrderItem 으로 주문한 상품들 전체를 가져오도록 접근이 가능하다.

---

### 3. SerializerMethodField 사용하기

`SerializerMethodField`는 모델에 없는 값을 동적으로 계산하여 응답에 포함할 수 있습니다. 예: 총 주문 금액 계산

```python
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total') 

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)


    class Meta:
        model = Order
        fields = ('order_id','created_at','user','status','items','total_price')

```

`method_name='total'`은 아래에 정의한 `def total(self, obj):` 메서드를 **사용하겠다는 지정**입니다.

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

#### 방법 2: Nested(중첩) Serializer로 표현

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

### 5. Nested(중첩) 구조 대신 평면 구조로 표현하기

Nested(중첩)을 피하고 특정 필드만 평면적으로 노출하고 싶을 경우:

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



### 7. /api/views.py  에 order_list  추가하기

```python
from api.serializers import ProductSerializer, OrderSerializer
from api.models import Product, Order, OrderItem

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

```

✅ 주요 요소 설명:

|코드|설명|
|---|---|
|`@api_view(['GET'])`|GET 요청만 허용하는 API 뷰로 지정|
|`Order.objects.all()`|DB에서 모든 주문을 가져옴|
|`OrderSerializer(..., many=True)`|여러 개의 Order 인스턴스를 직렬화|
|`Response(...)`|직렬화된 데이터를 클라이언트에 JSON 응답으로 반환|


📜 응답 예시 (OrderSerializer에 따라 달라짐)

```json
[
  {
    "order_id": "123e4567-e89b-12d3-a456-426614174000",
    "user": 1,
    "created_at": "2025-06-20T10:00:00Z",
    "status": "Pending",
    "items": [
      {
        "product": 5,
        "quantity": 2,
        "item_subtotal": "299.98"
      }
    ],
    "total_price": "299.98"
  },
  ...
]

```


### 8.  api/urls.py 에  orders 추가
```python
from django.shortcuts import redirect
from django.urls import path
from . import views
urlpatterns = [
    path('', lambda request: redirect('products/')),
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
    path('orders/', views.order_list),
]   
```



### 9. 마무리

이번 영상에서는 다음을 다뤘습니다:

- Nested(중첩) Serializer를 사용하여 관계형 모델을 JSON으로 표현
- `SerializerMethodField`로 동적 필드 생성
- 외래 키 데이터 표현 방법 다양화
- JSON 구조를 평면화(flatten)하여 응답 가독성 개선

> 다음 학습 : 모델에 종속되지 않은 일반 Serializer를 사용하여 집계 데이터를 처리하는 방법을 배웁니다.

