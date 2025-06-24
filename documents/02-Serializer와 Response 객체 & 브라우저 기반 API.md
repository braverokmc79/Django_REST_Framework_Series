## 02-Serializer와 Response 객체 & 브라우저 기반 API
[![02 - Serializer와 Response 객체 & 브라우저 기반 API](https://img.youtube.com/vi/BMym71Dwox0/0.jpg)](https://youtu.be/BMym71Dwox0?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---


🔗 소스 1. https://github.com/bugbytes-io/drf-course-api
🔗  소스 2. https://github.com/braverokmc79/Django_REST_Framework_Series



#### ✅1) 프로젝트 실행 방법 : 
	이전강의 디렉토리 복사 후 실행

#### ✅2) 더미 데이터 삽입 방법 (populate\_database 커맨드)

1강 확인  

```bash

python manage.py populate_db

```



---


### 1. 개요

이 영상에서는 Django REST Framework(DRF)의 가장 핵심적인 개념 중 하나인 **Serializer**를 소개하고, `Response` 객체 및 브라우저 기반 API가 어떻게 동작하는지 실습을 통해 살펴봅니다.

---

### 2. DRF 설치 및 설정

DRF는 pip 또는 uv 등의 도구로 설치할 수 있으며, 시작 코드에 이미 `requirements.txt`에 포함되어 있습니다. 설치가 완료되었으면 `settings.py`의 `INSTALLED_APPS`에 다음을 추가합니다:

```python
'rest_framework',
```

---

### 3. serializers.py 생성 및 기본 구조

`api/serializers.py` 파일을 생성하고 아래와 같이 작성합니다:

```python
from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
```

Serializer는 복잡한 모델 인스턴스 또는 쿼리셋을 JSON, XML 등으로 변환할 수 있고, 역으로 JSON 데이터를 모델로 역직렬화할 수 있도록 돕습니다.

---

### 4. Serializer 클래스의 역할

- **직렬화(Serialization)**: Django 모델/쿼리셋 → JSON 변환
- **역직렬화(Deserialization)**: JSON → 모델 인스턴스 변환
- `ModelSerializer`는 Django의 `ModelForm`처럼 모델과 필드를 자동 매핑해줍니다.
- 필드 수준 유효성 검증도 가능 (ex: `validate_price`)

---

### 5. 뷰에서 Serializer 사용

`views.py`에 다음과 같은 함수형 뷰를 작성합니다:

```python
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

```

- `@api_view(['GET'])`는 이 뷰가 GET 요청만 받도록 제한합니다.
- `Response()`는 DRF의 Response 객체로, 자동으로 콘텐츠 협상을 처리합니다.

---

### 6. URL 등록 및 테스트

`urls.py`에 다음을 추가합니다:

```python
from django.urls import path
from . import views

urlpatterns = [
     path('products/', views.product_list),
]
```

- 브라우저에서 `localhost:8000/products/`로 접속하면 JSON 응답 확인 가능
- DRF의 브라우저 기반 API가 활성화되어 인터페이스가 제공됩니다
- `?format=json`을 URL 뒤에 붙이면 JSON 응답의 원시 데이터를 볼 수 있습니다

---

### 7. 단일 객체 조회 구현

`urls.py`에 다음 경로 추가:

```python
path('products/<int:pk>/', views.product_detail),
```

`views.py`에 단일 상품 조회 함수 추가:

```python
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
```

- `get_object_or_404()`는 존재하지 않는 ID에 대해 404 에러를 반환
- 하나의 객체는 `many=True` 없이 직렬화

---

### 8. 브라우저 기반 API와 렌더러(Renderers)

- DRF는 다양한 출력 포맷을 지원하는 **렌더러** 시스템을 내장
- 대표 렌더러:
  - JSONRenderer (기본 JSON 응답)
  - BrowsableAPIRenderer (개발 편의를 위한 HTML 기반 API UI)

렌더러는 요청자의 `Accept` 헤더 또는 URL의 `?format=` 파라미터를 기반으로 자동 선택됩니다.

---

### 9. 마무리

이번 영상에서는 다음 내용을 다뤘습니다:

- `ModelSerializer`를 사용해 Django 모델을 JSON으로 직렬화
- `validate_필드명()`을 통해 필드별 유효성 검증
- 함수형 뷰에서 직렬화 데이터를 `Response`로 반환
- DRF의 브라우저 기반 API와 렌더링 방식

> 다음 학습 : 중첩 Serializer(Nested Serializer)\*\*를 통해 관계형 모델을 JSON으로 표현하는 방법을 알아봅니다.

