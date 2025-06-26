## 09-APIView 클래스 활용법
[![09 - APIView 클래스 활용법](https://img.youtube.com/vi/TVFCU0w65Ak/0.jpg)](https://youtu.be/TVFCU0w65Ak?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)


---


### 1. 개요

이번에는 Django REST Framework에서 제공하는 `APIView` 클래스를 어떻게 사용하는지에 대해 설명합니다. 이 클래스는 Django의 일반적인 뷰 클래스와 유사하지만, REST API에 특화된 기능을 제공하여 더욱 유연하고 강력한 API 뷰를 만들 수 있습니다.

---

### 2. APIView 클래스의 특징
`APIView`는 `django.views.View`를 상속하며 다음과 같은 차별점이 있습니다:
- 핸들러 메서드(`get`, `post` 등)는 Django의 `HttpRequest`가 아닌 DRF의 `Request` 객체를 받습니다.
- 응답은 DRF의 `Response` 객체를 반환합니다.
- 컨텐츠 협상(Content Negotiation)을 자동으로 처리하여 브라우저에서는 HTML, 클라이언트 요청 시에는 JSON 등의 형식으로 반환됩니다.
- 예외가 발생하면 DRF가 이를 적절한 HTTP 응답으로 변환합니다.
- 요청이 처리되기 전에 인증, 권한, 요청 제한(throttling) 등이 먼저 적용됩니다.

---

### 3. 예제 코드: 기존 함수형 뷰 → APIView 클래스 기반 뷰로 변환

#### 함수형 뷰:
```python
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
##### ✔ 특징

- `@api_view(['GET'])`를 사용해 HTTP 메서드를 지정
    
- 일반 `def` 함수로 작성
    
- 간단하고 빠르게 작성 가능
    
- 소규모 API에 적합


#### APIView 클래스로 변환:
```python
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': products.count(),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)
```

####  ✔ 특징

- `APIView`를 상속하여 클래스 기반으로 작성    
- 
- `get()`, `post()`, `put()` 등 메서드로 명확하게 분리
- 
- 뷰 로직을 재사용하거나 확장하기에 유리
- 
- URL 등록 시 `.as_view()`로 처리




`urls.py`에서 함수형 뷰 대신 클래스를 등록:
```python
path('products/info/', ProductInfoAPIView.as_view()),
```


#### 🔄 함수형 → 클래스형 변환 요약

|항목|함수형 뷰 (`@api_view`)|클래스형 뷰 (`APIView`)|
|---|---|---|
|선언 방식|`@api_view(['GET'])` + `def`|`class ... (APIView)`|
|메서드 구분|데코레이터로 제한|`def get()`, `def post()` 등 명시적|
|재사용성/확장성|낮음|높음|
|대규모 API 설계|불리함|유리함|



---

### 4. 작동 방식 확인
- `get()` 메서드는 GET 요청에 반응하며, 내부 로직은 기존 함수형 뷰의 내용과 동일하게 작동합니다.
- 브라우저에서 `/products/info/`로 접속 시 상품 리스트와 `count`, `max_price` 필드가 함께 반환됩니다.
- `.as_view()` 메서드를 통해 클래스형 뷰를 Django가 처리할 수 있도록 변환합니다.

---

### 5. 포맷 협상 기능 테스트
- 기본적으로 브라우저에서는 HTML 형식으로 응답이 반환됩니다.
- URL에 `?format=json` 또는 `.json`을 붙이면 JSON 형식으로 순수 데이터가 반환됩니다.
- 이는 `APIView`가 내부적으로 컨텐츠 협상을 처리하기 때문에 가능한 기능입니다.

---

### 6. 마무리 및 활용 포인트
- `APIView`는 제너릭 뷰(`ListAPIView`, `CreateAPIView` 등)보다 유연하게 커스텀 로직을 작성할 수 있게 해줍니다.
- 모델이나 쿼리셋에 얽매이지 않고, 다양한 외부 데이터나 로직을 조합해 응답을 만들 때 유용합니다.
- GET 외에도 `post`, `put`, `delete` 등의 메서드를 추가하여 다양한 HTTP 메서드에 대한 처리를 구현할 수 있습니다.

---

> 다음 강의에서는 Create, Update, Delete 작업을 처리하는 제너릭 뷰와 JWT 인증 방식에 대해 다룰 예정입니다.

