## Django REST Framework(DRF) - API 페이지네이션 설정

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
    'PAGE_SIZE': 5,
}
```
- 한 페이지에 5개 항목만 응답

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
    queryset = Product.objects.order_by('id')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
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
- 정렬(`.order_by()`) 없이 페이지네이션 시 경고 발생할 수 있음 → 기본 정렬 지정 필요
- 사용자 지정 페이지 크기 허용 시 `max_page_size` 반드시 설정

---

### 8. 정리
- DRF에서 간단한 설정만으로 강력한 페이지네이션 기능 제공
- 전역/개별 View 설정 가능
- `PageNumberPagination`과 `LimitOffsetPagination`으로 대부분의 케이스 커버 가능
- 클라이언트 커스터마이징도 유연하게 지원

> 다음 강의에서는 DRF의 ViewSet 개념과 활용법을 다룹니다.

