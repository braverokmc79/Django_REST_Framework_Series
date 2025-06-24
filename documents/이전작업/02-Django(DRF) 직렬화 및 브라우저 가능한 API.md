
# 🎥 2강: Django REST Framework 직렬화와 브라우저 가능한 API


🔗 [https://youtu.be/BMym71Dwox0](https://youtu.be/BMym71Dwox0)

[![Watch on YouTube](https://img.youtube.com/vi/BMym71Dwox0/0.jpg)](https://youtu.be/BMym71Dwox0)



---

## 목차

1. Django REST Framework 설치 및 설정
    
2. 직렬화(Serializers)란 무엇인가?
    
3. ModelSerializer 구현 및 필드 지정
    
4. 필드 수준 유효성 검사
    
5. 함수형 뷰(Function-Based View) 구현
    
6. DRF Response와 Browsable API
    
7. 단일 객체 직렬화 처리
    

---

## 1. Django REST Framework 설치 및 설정

- Django REST Framework는 pip 또는 uv로 설치 가능
    
- `requirements.txt`에 이미 등록되어 있으면 설치는 자동 처리됨
    
- `settings.py`의 `INSTALLED_APPS`에 `'rest_framework'` 추가
    

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

---

## 2. 직렬화(Serializers)란?

- QuerySet이나 모델 인스턴스를 JSON, XML 등으로 변환 (serialization)
    
- 반대로 JSON 요청 데이터를 모델 인스턴스로 변환 (deserialization)
    
- Django의 Form, ModelForm과 유사한 개념
    

공식 정의:

> "Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types."

---

## 3. `ModelSerializer` 구현

`serializers.py` 파일을 `api` 앱 내에 생성한 후 아래와 같이 `ProductSerializer` 정의

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
        )
```

- `ModelSerializer`는 자동으로 각 필드 타입을 감지하여 적절한 DRF 필드를 사용
    

### ✅ 설명:

- `name`, `description`: 문자열
    
- `price`: Decimal 필드
    
- `stock`: 정수 (PositiveInteger)
    
- `id`: 기본적으로 Django가 생성한 기본 키
    

---

## 4. 필드 수준 유효성 검사

가격(`price`)이 0보다 커야 한다는 검증 추가:

```python
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
```

- 메서드 명은 `validate_<fieldname>` 형식
    
- Django의 `clean_<fieldname>`과 유사한 개념
    

---

## 5. 함수형 뷰(Function-Based View) 구현

`views.py` 파일에서 제품 목록 및 단일 제품 조회 뷰 생성

```python
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
```

### ✅ 설명:

- `@api_view(['GET'])`: HTTP GET 요청만 허용
    
- `many=True`: 여러 개의 인스턴스 직렬화 시 필요
    

---

## 6. DRF Response와 Browsable API

- `JsonResponse` 대신 DRF의 `Response` 객체를 사용하면 콘텐츠 협상이 가능
    
- 브라우저에서 `/products`에 접속 시, HTML 형식의 browsable API 제공
    

브라우저 주소에 `?format=json`을 추가하면 JSON 직접 확인 가능:

```
http://localhost:8000/products?format=json
```

---

## 7. 단일 객체 직렬화 처리

- `GET /products/<pk>/` 요청 처리:
    

`urls.py` 예시:

```python
from django.urls import path
from .views import product_list, product_detail

urlpatterns = [
    path('products/', product_list),
    path('products/<int:pk>/', product_detail),
]
```

브라우저로 `http://localhost:8000/products/1/` 접속 시 ID 1번 제품 정보를 확인할 수 있음

---




## 8.  Django REST Framework: 포맷 접미사(.json, .api 등) 허용 설정



### ✅ 1. views.py - 함수형 뷰(Function-Based View) 예시
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def user_detail(request, pk, format=None):  # format 인자를 추가해야 함
    user = {"id": pk, "name": "홍길동"}
    return Response(user)

```


### ✅ 2. urls.py 설정

```python
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import user_detail

urlpatterns = [
    path('users/<int:pk>/', user_detail),
]
```

#### format_suffix_patterns 적용

```python
urlpatterns = format_suffix_patterns(urlpatterns)
```


### ✅ 3. settings.py (선택 사항 - 렌더러 설정)
#### 포맷에 따른 응답 지원: .json, .api, .xml 등

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        # 'rest_framework.renderers.XMLRenderer',  # 필요 시 주석 해제 및 설치 필요
    ]
}

```

### ✅ 4. 요청 예시
```python
# 기본 JSON:        GET /users/1/
# JSON 접미사:       GET /users/1.json
# Browsable API 접미사: GET /users/1.api
# XML 응답:         GET /users/1.xml (XMLRenderer 사용 시)

```


## ✅ 마무리

이 강의에서는 DRF의 기본적인 직렬화 처리와 함수형 뷰를 통한 API 응답 구현을 살펴보았습니다. 다음 강의에서는 관계형 모델을 다룰 수 있는 **Nested Serializer**를 학습할 예정입니다.

---

## 🔖 태그

`#Django` `#DRF` `#Serializer` `#APIView` `#직렬화` `#RESTAPI` `#BrowsabeAPI`













































