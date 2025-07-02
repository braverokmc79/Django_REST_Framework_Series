## 17-SearchFilter와 OrderingFilter 사용하기



[17 - SearchFilter와 OrderingFilter 사용하기](https://youtu.be/LCYqDsl1WYI?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



---


### 1. 개요

이번 강의에서는 Django REST Framework에서 API 응답 데이터를 **검색(SearchFilter)** 하고 **정렬(OrderingFilter)** 하는 방법을 알아봅니다. 클라이언트가 원하는 조건에 맞는 데이터를 효율적으로 조회할 수 있도록 구현하면, 응답 속도 개선과 함께 사용자 경험도 좋아집니다.

---

### 2. 기본 개념 정리

- 기본적으로 DRF의 제네릭 ListView는 전체 QuerySet을 응답합니다.
- 하지만 많은 데이터 중 일부만 필요한 경우, **검색 및 정렬 기능**이 있으면 클라이언트 입장에서 불필요한 데이터를 제거할 수 있어 효율적입니다.

---

### 3. SearchFilter 사용하기

`SearchFilter`는 지정한 필드에 대해 **부분 검색**을 할 수 있도록 도와줍니다.

#### 설정 방법 (`settings.py`):

```python
REST_FRAMEWORK = {
  'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',  # 필터셋 기반 필터
        'rest_framework.filters.SearchFilter',                # ?search= 검색
        'rest_framework.filters.OrderingFilter',          # ?ordering= 정렬
    ],
}
```

### 🔍 추가 설명

- `DjangoFilterBackend`는 `filterset_class` 또는 `filterset_fields`를 기반으로 작동합니다.
    
- `SearchFilter`는 뷰에서 `search_fields = ['name', 'title', ...]`처럼 설정하면 `?search=키워드` 방식으로 검색이 됩니다.
    
- 두 필터는 **함께 등록해도 충돌하지 않으며**, 각각의 역할을 합니다.

- `OrderingFilter`는 `?ordering=필드명` 형식으로 API 응답을 **정렬**해줍니다.
    
- 정렬 대상 필드는 `ordering_fields` 속성에 명시합니다.


✅ `OrderingFilter`와 `SearchFilter`는 **추가 설치가 필요 없습니다.**

|기능|필터 클래스|설치 필요 여부|
|---|---|---|
|일반 검색|`rest_framework.filters.SearchFilter`|❌ DRF 기본 내장|
|정렬 기능|`rest_framework.filters.OrderingFilter`|❌ DRF 기본 내장|
|필드 기반 필터링|`django_filters.rest_framework.DjangoFilterBackend`|✅ `django-filter` 설치 필요|



#### View에 적용:

```python
from rest_framework import generics, filters
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    # filter_backends = [
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    #     filters.OrderingFilter,
    # ]

```

📌  View에 `filter_backends`를 지정하면?

⚠️ 결과: `settings.py`의 설정은 무시되고, **이 View에서는 `SearchFilter`만 적용됨**.

✅ 결론

> `filter_backends`를 **View에 명시하지 않으면** → `settings.py`의 `DEFAULT_FILTER_BACKENDS`가 **자동 적용됩니다.**
> 
> 반대로, View에 `filter_backends`를 직접 쓰면 settings의 기본값은 **무시됩니다.**

🎯 추천 팁

- 대부분의 API에 공통 필터를 적용하려면 **settings.py**에서 전역 설정만 해두면 충분합니다.
    
- 특별한 View만 다르게 하고 싶을 때만 `filter_backends`를 직접 지정하세요.

\\
#### 검색 사용 예시:

```
GET /products/?search=카메라
```

- `name` 또는 `description`에 "카메라"가 포함된 상품 반환

> 참고: `icontains` 방식으로 동작하며 대소문자 구분 없이 부분 문자열로 매칭됨

---

### 4. OrderingFilter 사용하기

`OrderingFilter`는 쿼리파라미터로 지정된 필드를 기준으로 정렬된 결과를 반환합니다.

#### View에 적용:

```python
from api.filters import ProductFilter
from rest_framework import generics ,filters
from django_filters.rest_framework import DjangoFilterBackend


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ['=name', 'description']
    
    ordering_fields = ['name', 'price', 'stock'] # 정렬 허용 필드
    ordering = ['price']  # 기본 정렬 순서
```

##### ✅ `search_fields`에서 `=`의 의미는?

- `=name` → **이 필드는 "정확히 일치하는 값만" 검색하라**는 의미입니다.  
    (SQL로 치면 `WHERE name = '검색어'` 느낌)
    
- `description` → `icontains`로 동작 (기본값):  
    → SQL로 치면 `WHERE description ILIKE '%검색어%'`

#####  🔍 예시

```python
search_fields = ['=name', 'description']
```

- `?search=apple` 로 검색할 경우:
    - `name == 'apple'` → 정확히 일치하는 name만 검색됨
    - `description ILIKE '%apple%'` → description에 "apple"이 포함된 결과도 함께 검색됨


###### ✅ 지원되는 prefix 목록 (`SearchFilter`에서)

| 접두사(prefix) | 의미                              | 예시                                          |
| ----------- | ------------------------------- | ------------------------------------------- |
| `^`         | startswith (시작일치)               | `^name` → `'apple'` → name이 "apple"로 시작하는 값 |
| `=`         | exact (정확히 일치)                  | `=name` → `'apple'` → name이 정확히 "apple"인 값  |
| `@`         | full-text search (PostgreSQL 등) | `@title`                                    |
| 없음          | icontains (부분일치, 대소문자 무시)       | `description` → `%검색어%`                     |


필요하면 더 복잡한 커스텀 검색도 가능합니다. 
예: `search_fields = ['^title', '=author__username']` 등.



#### 정렬 사용 예시:

```
GET /products/?ordering=price      # 가격 오름차순
GET /products/?ordering=-price     # 가격 내림차순
GET /products/?ordering=name       # 이름 오름차순
```

---

### 5. SearchFilter와 OrderingFilter 함께 사용하기

```python
 filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    ordering = ['price']  # 기본 정렬 순서
```



#### 동시 사용 예시:

```
GET /products/?search=TV&ordering=-price

GET  http://127.0.0.1:8000/products/?search=Television
```



- 이름 또는 설명에 'TV'가 포함된 상품 중, 가격이 높은 순으로 정렬

---

### 6. 브라우저 기반 API에서 검색 및 정렬 필드 노출

- DRF의 Browsable API 또는 Swagger UI에서
  - 검색: 검색창이 노출됨
  - 정렬: 드롭다운으로 정렬 기준 선택 가능

---

### 7. 정리

- `SearchFilter`는 부분 검색, `OrderingFilter`는 정렬을 간단하게 구현할 수 있는 DRF 내장 필터 백엔드
- `search_fields`, `ordering_fields` 설정으로 원하는 필드에 기능 적용 가능
- 두 필터는 함께 사용할 수 있으며, 실시간 검색, 정렬 UI에도 쉽게 연동 가능

> 다음 강의에서는 페이지네이션(Pagination)을 이용한 응답 데이터 분할 방식에 대해 다룹니다.





