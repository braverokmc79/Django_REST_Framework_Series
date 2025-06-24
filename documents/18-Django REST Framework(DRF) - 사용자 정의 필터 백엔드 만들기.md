## Django REST Framework(DRF) - 사용자 정의 필터 백엔드 만들기

### 1. 개요

이번 영상에서는 Django REST Framework에서 **사용자 정의(Custom) 필터 백엔드**를 만드는 방법을 알아봅니다. 기존의 `django-filter`, `SearchFilter`, `OrderingFilter` 외에도, 자신만의 필터링 로직을 추가하고 싶은 경우에 유용합니다.

---

### 2. 기본 개념

DRF에서는 `BaseFilterBackend` 클래스를 상속하고, `filter_queryset(self, request, queryset, view)` 메서드를 오버라이딩하여 사용자 정의 필터를 만들 수 있습니다.

예시: `IsOwnerFilterBackend`

```python
class IsOwnerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
```

이 필터는 로그인한 사용자 본인이 소유한 데이터만 응답하도록 제한합니다.

---

### 3. 실습: 재고가 있는 상품만 응답하는 필터 만들기

#### 1) `filters.py` 파일에 다음 클래스 추가:

```python
from rest_framework.filters import BaseFilterBackend

class InStockFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)  # 재고가 0보다 큰 상품만 필터링
```

> 이 필터는 재고가 하나라도 있는 상품만 필터링하여 클라이언트에게 보여줍니다.

---

### 4. 뷰(View)에 사용자 정의 필터 백엔드 추가하기

기존 View에서 filter\_backends에 추가:

```python
from .filters import ProductFilter, InStockFilterBackend

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, InStockFilterBackend]
    filterset_class = ProductFilter
```

- `InStockFilterBackend`는 마지막에 추가
- 자동으로 재고가 0인 상품을 제외한 결과만 응답합니다

---

### 5. 테스트 방법

- API 요청: `GET /products/`
- 응답에는 재고가 있는 상품만 포함됨

#### 확인 방법:

- 필터 주석 처리 전: `stock = 0`인 상품은 제외됨
- 필터 주석 처리 후: 모든 상품 응답됨 (재고 0 포함)

> 필요에 따라 `.filter()` → `.exclude()`로 바꾸면 반대 조건도 구현 가능

---

### 6. 정리

- DRF에서는 `BaseFilterBackend`를 상속해 간단히 사용자 정의 필터를 구현할 수 있음
- `filter_queryset` 메서드를 오버라이딩하여 로직 정의
- 다양한 API View에 재사용 가능
- 기존 필터들과 함께 조합 사용 가능

> 다음 강의에서는 DRF의 페이지네이션(Pagination) 기능을 활용해 데이터 응답을 나누는 방법을 알아봅니다.

