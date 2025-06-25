
## 06-Generic View 소개 & ListAPIView & RetrieveAPIView

[![06 - Generic View 소개 & ListAPIView & RetrieveAPIView](https://img.youtube.com/vi/vExjSChWPWg/0.jpg)](https://youtu.be/vExjSChWPWg?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)


---



### 1. 개요

이번 강의 에서는 지금까지 사용해온 함수형 뷰(function-based view) 대신 클래스 기반 뷰(class-based view)를 사용하는 방법을 소개합니다. DRF의 진정한 강점은 이 클래스 기반 뷰(Generic View)에 있으며, 반복되는 로직을 줄이고 공통된 동작을 추상화하여 더 효율적인 개발이 가능합니다.

---

### 2. Generic View의 개념

Generic View는 공통적인 패턴을 추상화하여, 반복 코드를 줄이고 DRY(Don't Repeat Yourself) 원칙을 지킬 수 있도록 설계되었습니다.

예를 들어 모델 인스턴스를 나열하거나 생성하는 API 뷰를 만들고 싶다면, `ListCreateAPIView`와 같은 클래스를 상속받아 아주 간단히 구현할 수 있습니다.

```python
from rest_framework import generics

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

위 코드만으로 다음 두 가지 기능을 동시에 제공합니다:

- 전체 유저 목록을 조회 (GET)
    
- 새 유저를 생성 (POST)
    

---

### 3. ListAPIView 적용 예시

기존의 `products` 함수형 뷰를 `ListAPIView`로 변경하면 다음과 같습니다:

기존 :
```python
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer =ProductSerializer(products, many=True)
    return Response(serializer.data)
```

 ➡️ 변환
 
```python
from rest_framework import generics

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

- `queryset`은 어떤 데이터를 반환할지 결정합니다.
    
- `serializer_class`는 데이터를 어떻게 JSON으로 직렬화할지를 결정합니다.
    



URL 연결 시에는 `.as_view()`를 사용하여 클래스형 뷰를 등록합니다.

```python
path('products/', ProductListAPIView.as_view())
```

브라우저에서 `/products/`로 요청하면 전체 상품 목록을 반환합니다.

---

### 4. RetrieveAPIView 적용 예시

단일 상품 정보를 조회할 뷰는 `RetrieveAPIView`를 사용합니다:

```python
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'
```

이제 `/products/1/`와 같은 요청으로 상품 ID 1번의 상세 정보를 반환할 수 있습니다.

만약 URL에서 사용되는 키워드 인자를 변경하고 싶다면 `lookup_url_kwarg`를 지정할 수 있습니다:

```python
lookup_url_kwarg = 'product_id'
```

URLConf 예시:

```python
path('products/<int:product_id>/', ProductDetailAPIView.as_view())
```

---

### 5. 쿼리셋 필터링 적용

상품 리스트에서 품절된 상품을 제외하고 싶은 경우 `queryset`에 `.filter()`를 적용할 수 있습니다:

```python
queryset = Product.objects.all()
```

➡️

```python
queryset = Product.objects.filter(stock__gt=0)
```

```python
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.exclude(stock__gt=0)
    serializer_class = ProductSerializer
```



재고가 0 이상인 상품만 반환됩니다. 반대로 `exclude(stock=0)`을 통해 품절 상품만 조회할 수도 있습니다.

---

### 6.  order_list   -> OrderListAPIView  변환

#### ✔ 특징

- **함수형 뷰** 방식
- `@api_view(['GET'])`로 HTTP 메서드 지정
- `직접 쿼리`, `직접 시리얼라이즈`, `직접 Response 리턴`
- 단순하지만, 코드가 장황해지기 쉬움
- 
```python
@api_view(['GET'])
def order_list(request):    
    orders = Order.objects.prefetch_related('items__product')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
```

➡️

```python
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
```
#### ✔ 특징

- **클래스형 뷰** 방식 
- `ListAPIView`는 기본적으로 `GET` 요청을 처리함
- `queryset`과 `serializer_class`만 지정하면 자동으로 처리됨
- **반복 코드 최소화**, **유지보수 용이**



---


### 6. 마무리

- `ListAPIView`, `RetrieveAPIView`는 읽기 전용(Read-Only) API에 최적화된 제너릭 클래스입니다.
    
- 쿼리셋과 직렬화 클래스만 지정하면 대부분의 동작을 자동으로 처리합니다.
    
- 이후 영상에서는 사용자 인증된 사용자에 따라 데이터를 필터링하는 동적 쿼리셋(get_queryset)과 CRUD 동작(Post, Put, Delete)을 다루게 됩니다.
    

---

> 다음 강의에서는 인증된 사용자만 자신의 주문 목록을 볼 수 있도록 동적으로 쿼리셋을 조절하는 방법을 알아봅니다.