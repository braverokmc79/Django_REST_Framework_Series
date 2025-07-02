
## 04-Serializer 하위 클래스와 집계형 API 데이터 처리

[04 - Serializer 하위 클래스와 집계형 API 데이터 처리](https://youtu.be/_xbI0-mjtw4?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



---


### 강의 목차

1. 목표: 하나의 API에서 여러 데이터와 집계 결과를 포함해 응답하는 시리얼라이저 구현
2. 직렬화기 클래스: `serializers.Serializer` 사용
3. 설명: 목록 + 집계(count, 최대 가격) 포함 응답 처리

---

### 1. 개요

Django REST Framework에서 `ModelSerializer`는 모델 기반 필드를 자동으로 생성하지만, 여러 집계 결과를 함께 반환하거나 특정 포맷으로 데이터를 제어하고 싶을 땐 `Serializer` 클래스를 사용해야 합니다.

---

### 2. 모델 정의 (예시)

`models.py`

```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
```

`Product` 모델은 이름, 설명, 가격, 재고, 이미지 정보를 포함합니다.

---

### 3. 직렬화기 생성

`serializers.py`

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock')
  
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
```

- `ProductSerializer`: 개별 상품 정보 직렬화
- `ProductInfoSerializer`: 전체 상품 목록과 함께, 총 개수(count), 최대 가격(max\_price) 정보 포함

`serializers.Serializer`는 특정 모델에 바인딩되지 않고, **자유로운 구조의 JSON 응답/입력**을 정의할 수 있는 Serializer입니다.  
즉, 모델이 아닌 순수 Python 구조에 맞게 정의된 "일반 Serializer"라고 보면 됩니다.

---

### 4. 뷰 작성

`views.py`

```python
from django.db.models import Max
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductInfoSerializer

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': products.count(),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
```

- `products.count()` → 전체 상품 수
- `aggregate(Max('price'))['max_price']` → 상품 중 최대 가격
- 응답 시 `products`, `count`, `max_price`가 모두 포함됩니다.

---

### 5. URL 라우팅 등록

`urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('products/info/', views.product_info),
]
```

---

### 6. 응답 예시

```json
{
    "products": [
        {"id": 1, "name": "Product A", "price": 12.00, "stock": 10},
        {"id": 2, "name": "Product B", "price": 22.00, "stock": 5}
    ],
    "count": 2,
    "max_price": 22.0
}
```

---

### 정리 및 참고 사항

- `serializers.Serializer`를 사용하면 모델에 직접 연결되지 않은 자유로운 구조의 데이터를 응답할 수 있습니다.
- 집계 데이터를 포함하는 응답을 만들 때 유용하며, 뷰에서 데이터를 가공한 후 시리얼라이저에 넘기는 방식입니다.
- 다음 강의에서는 SQL 분석 도구인 `django-silk`를 활용해 API 쿼리를 최적화하는 방법을 다룰 예정입니다.

