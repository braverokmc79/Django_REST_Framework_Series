## Django REST Framework(DRF) - SearchFilter와 OrderingFilter 사용하기

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
        'rest_framework.filters.SearchFilter',
    ],
}
```

#### View에 적용:

```python
from rest_framework import generics, filters
from .models import Product
from .serializers import ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']  # 검색 대상 필드 지정
```

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
from rest_framework import generics, filters

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'name']  # 정렬 허용 필드
    ordering = ['price']  # 기본 정렬 순서
```

#### 정렬 사용 예시:

```
GET /products/?ordering=price      # 가격 오름차순
GET /products/?ordering=-price     # 가격 내림차순
GET /products/?ordering=name       # 이름 오름차순
```

---

### 5. SearchFilter와 OrderingFilter 함께 사용하기

```python
filter_backends = [filters.SearchFilter, filters.OrderingFilter]
search_fields = ['name', 'description']
ordering_fields = ['price', 'name']
```

#### 동시 사용 예시:

```
GET /products/?search=TV&ordering=-price
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

