## Django REST Framework(DRF) - 데이터 생성하기 & ListCreateAPIView와 Generic View 내부 구조

### 1. 개요

이번 영상에서는 Django REST Framework를 이용해 **데이터를 생성(Post)** 하는 방법과 함께, `ListCreateAPIView` 클래스 및 DRF의 **제너릭 뷰 내부 구조**를 깊이 있게 살펴봅니다.

---

### 2. 리스트 조회와 단일 조회 복습

지금까지 우리는 `ListAPIView`로 여러 객체를 JSON으로 반환하고, `RetrieveAPIView`로 단일 객체를 조회하는 작업을 수행해왔습니다. 이들은 모두 GET 요청을 처리하며, **서버의 데이터를 변경하지 않는** 비파괴적인(read-only) 요청입니다.

---

### 3. POST 요청을 이용한 데이터 생성: CreateAPIView

이번에는 `CreateAPIView`를 사용해 POST 요청으로 새로운 데이터를 생성하는 방법을 알아봅니다.

- `ListAPIView`는 GET 요청만 받고,
- `CreateAPIView`는 POST 요청만 받습니다.

```python
from rest_framework import generics

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

- 모델에 연결된 필드들 중 필수 값들은 POST 요청으로 함께 전송해야 합니다.
- 예: `name`, `description`, `price`, `stock` 등
- `id` 필드는 자동 생성되므로 요청에 포함하면 안 됩니다.

---

### 4. ProductSerializer 수정

`ProductSerializer`에는 생성 시 필요한 모든 필드가 포함되어야 합니다. `description` 필드가 빠져 있다면 추가해야 합니다.

---

### 5. CreateAPIView 뷰 테스트

`urls.py`에 다음 라인을 등록합니다:

```python
path('products/create/', ProductCreateAPIView.as_view()),
```

브라우저에서 `/products/create/`로 이동하면 HTML 폼이 나타나고, POST 요청을 보내면 `201 Created` 응답과 함께 생성된 객체의 데이터가 반환됩니다.

---

### 6. GET과 POST 통합: ListCreateAPIView

REST 설계에서는 **같은 URL 엔드포인트에서 GET과 POST를 모두 지원**하는 것이 일반적입니다.

이를 위해 DRF는 `ListCreateAPIView`라는 클래스를 제공합니다:

```python
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

- GET 요청 시 전체 목록을 반환
- POST 요청 시 새 객체를 생성

`urls.py`에서는 기존의 `/products/` 경로를 이 뷰로 연결하면 됩니다:

```python
path('products/', ProductListCreateAPIView.as_view()),
```

이제 같은 URL에서 GET/POST 모두 처리됩니다.

---

### 7. 내부 구조 및 동작 방식 이해

`ListCreateAPIView`는 DRF의 `GenericAPIView`를 기반으로 하며, 다음 두 믹스인을 상속받습니다:

- `ListModelMixin` → `list()` 메서드 제공
- `CreateModelMixin` → `create()` 메서드 제공

이들 메서드는 내부적으로 다음 흐름을 따릅니다:

#### list()

- `get_queryset()` → 쿼리셋 가져오기
- `filter_queryset()` → 필터링 적용
- `get_serializer()` → 직렬화 처리
- `Response(serializer.data)` 반환

#### create()

- `request.data` 가져오기
- `serializer = get_serializer(data=request.data)`
- `serializer.is_valid()` → 검증
- `serializer.save()` → DB 저장
- `Response(serializer.data, status=201)` 반환

이러한 내부 흐름은 필요한 경우 각 메서드를 오버라이드(재정의)해서 커스터마이징할 수 있습니다.

예시:

```python
def create(self, request, *args, **kwargs):
    print(request.data)
    return super().create(request, *args, **kwargs)
```

---

### 8. 정리

- `CreateAPIView`는 POST 전용, `ListAPIView`는 GET 전용
- `ListCreateAPIView`는 GET과 POST를 동시에 처리 가능
- DRF의 믹스인 구조를 이해하면 내부 로직을 커스터마이징하기 쉬워짐
- REST API의 일관된 URL 설계를 위해 `ListCreateAPIView`를 적극 활용하는 것이 좋음

---

> 다음 영상에서는 Update와 Delete 요청을 처리하는 뷰, 그리고 ViewSet을 사용하는 구조에 대해 소개할 예정입니다.

