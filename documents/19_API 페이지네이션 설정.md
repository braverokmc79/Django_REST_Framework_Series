## 19-API 페이지네이션 설정
[![19 - API 페이지네이션 설정](https://img.youtube.com/vi/sTyMe2R9mzk/0.jpg)](https://youtu.be/sTyMe2R9mzk?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)




---

### 1. 개요
이번 강의에서는 Django REST Framework(DRF)에서 **페이지네이션(Pagination)** 기능을 적용하여 많은 양의 데이터를 적절히 나누어 응답하는 방법을 학습합니다. 데이터를 무조건 전부 응답하는 방식은 프론트엔드에 부담을 줄 수 있으므로 페이지 단위로 나누는 것이 효율적입니다.

---

### 2. DRF의 페이지네이션 클래스
DRF는 세 가지 기본 페이지네이션 클래스를 제공합니다:

1. **PageNumberPagination** (페이지 번호 기반)
2. **LimitOffsetPagination** (제한 개수 + 시작 지점 기반)
3. **CursorPagination** (고급, 시간 기반 정렬 등 사용 시)

이번 강의에서는 주로 1번과 2번을 다룹니다.

---

### 3. PageNumberPagination 설정

#### 1) 전역 설정 (`settings.py`):
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
}
```
- 한 페이지에 2개 항목만 응답


#### 2) 실제 응답 구조:
```json
{
  "count": 20,
  "next": "http://localhost:8000/products/?page=2",
  "previous": null,
  "results": [
    ...상품 데이터...
  ]
}
```

- `count`: 전체 데이터 수
- `next`, `previous`: 다음/이전 페이지 URL
- `results`: 현재 페이지의 데이터 리스트

#### 3) 페이지네이션 + 정렬 동시 사용 예시:
```
GET /products/?page=2&ordering=name
```

---

### 4. View 별 개별 설정
```python
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_num'  # 쿼리 파라미터 이름 변경
    page_size_query_param = 'size'  # 클라이언트가 size 조절 가능
    max_page_size = 6  # 최대 size 제한
```

```python
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]

    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    ordering = ['price']  # 기본 정렬 순서
    pagination_class = LimitOffsetPagination

    #✅ 개별설정시 다음과 같이 추가 설정하면된다.
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = 'pagenum'
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.max_page_size = 6  # 최대 size 제한
```

---


### 5. 클라이언트 조절 예시
```
GET /products/?size=3
```
- `size`를 통해 페이지 크기 조절 가능
- `max_page_size`보다 크면 무시됨 (예: size=1000 → 최대값인 6으로 제한됨)

---

### 6. LimitOffsetPagination 사용법
```python
from rest_framework.pagination import LimitOffsetPagination

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
```

#### 쿼리 파라미터 예시:
```
GET /products/?limit=4&offset=6
```
- `limit`: 몇 개 가져올지
- `offset`: 몇 번째부터 시작할지

- 응답 구조는 `results`, `count`, `next`, `previous` 포함

---

### 7. 주의사항

```
 queryset = Product.objects.order_by('pk')
```
- 정렬(`.order_by()`) 없이 페이지네이션 시 경고 발생할 수 있음 → 기본 정렬 지정 필요
- 사용자 지정 페이지 크기 허용 시 `max_page_size` 반드시 설정


---

### 8.커스텀 페이지네이터 클래스 정의


#### 1) drf_course/custom_pagination.py 
(혹은 views.py 상단에 함께 작성 가능)

```python
# custom_pagination.py (혹은 views.py 상단에 함께 작성 가능)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomLimitOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        current_page = (self.offset // self.limit) + 1 if self.limit else 1

        return Response({
            'total_count': self.count,                   # 전체 아이템 수
            'limit': self.limit,                   # 페이지당 개수
            'offset': self.offset,                 # 시작 오프셋
            'current_page': current_page,          # 현재 페이지 번호
            'next': self.get_next_link(),          # 다음 페이지 URL
            'previous': self.get_previous_link(),  # 이전 페이지 URL
            'results': data                        # 실제 데이터
        })

```


#### 2) `ProductListCreateAPIView`에 적용하기

```python
# views.py # ← 경로에 맞게 수정
from drf_course.custom_pagination import CustomLimitOffsetPagination 

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]
    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    ordering = ['price']

    pagination_class = CustomLimitOffsetPagination  # ✅ 커스텀 페이지네이터 적용

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

```


🖨️ 출력 예
```json
{
    "total_count": 7,
    "limit": 2,
    "offset": 0,
    "current_page": 1,
    "next": "[http://127.0.0.1:8000/products/?limit=2&offset=2](http://127.0.0.1:8000/products/?limit=2&offset=2)",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "A Scanner Darkly",
            "description": "Veritatis d",
            "price": "12.99",
            "stock": 4
        },
        {
            "id": 3,
            "name": "Velvet Underground & Nico",
            "description": "E",
            "price": "15.99",
            "stock": 11
        }
    ]
}
```



---

### 9. 정리
- DRF에서 간단한 설정만으로 강력한 페이지네이션 기능 제공
- 전역/개별 View 설정 가능
- `PageNumberPagination`과 `LimitOffsetPagination`으로 대부분의 케이스 커버 가능
- 클라이언트 커스터마이징도 유연하게 지원

> 다음 강의에서는 DRF의 ViewSet 개념과 활용법을 다룹니다.

