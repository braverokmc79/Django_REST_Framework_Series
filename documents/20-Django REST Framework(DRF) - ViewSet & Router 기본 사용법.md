## Django REST Framework(DRF) - ViewSet & Router 기본 사용법

### 1. 개요

이번 강의에서는 Django REST Framework(DRF)의 **ViewSet**과 **Router**의 개념 및 사용법을 학습합니다. 반복되는 API 뷰 코드를 간소화하고 RESTful한 URL 구조를 자동으로 생성하기 위해 이 기능들을 적극 활용할 수 있습니다.

---

### 2. ViewSet이란?

- 관련된 여러 API 뷰 로직을 하나의 클래스(ViewSet)로 통합할 수 있는 구조
- 기존 `APIView` 또는 `GenericAPIView`처럼 HTTP 메서드(GET, POST 등)를 직접 다루는 대신, ``**, **``**, **``**, **``**, **`` 등의 액션 메서드를 사용

```python
from rest_framework import viewsets

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # 일단 인증 없이 열어둠 (다음 강의에서 수정)
```

- `ModelViewSet`을 상속하면 CRUD를 자동 지원
- 기존의 ListAPIView, CreateAPIView 등을 통합하는 형태

---

### 3. Router란?

- ViewSet은 URL 설정이 별도로 필요
- DRF의 **Router**는 ViewSet과 연결된 URL들을 자동으로 생성해주는 기능 제공

```python
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register('orders', OrderViewSet)

urlpatterns = [
    ...
    path('', include(router.urls)),
]
```

자동으로 생성되는 URL 예시:

```
/orders/            # GET: 전체 목록, POST: 생성
/orders/<pk>/       # GET: 상세, PUT: 전체 수정, PATCH: 부분 수정, DELETE: 삭제
```

---

### 4. 장점 요약

- **코드량 감소**: 중복 없이 하나의 ViewSet으로 CRUD 지원
- **자동 URL 등록**: router.register만으로 RESTful 경로 자동 생성
- **유지보수 용이**: 비즈니스 로직 변경 시 한 곳에서 수정 가능

---

### 5. 필드 자동 생성 제어

- 예: `order_id`는 UUIDField로 자동 생성되므로, 수동 입력 막기 위해 read\_only 지정

```python
class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    ...
```

---

### 6. Form 기반 HTML API 테스트

- DRF 브라우저 UI에서 POST 요청 시 `order_id`를 수동으로 입력하라는 필드가 사라짐
- ViewSet은 브라우저 기반 폼과도 잘 통합되어 시각적인 테스트가 가능함

---

### 7. URL 접근 예시 및 테스트

- `/orders/` → 주문 전체 목록 조회 및 생성
- `/orders/<uuid>/` → 단일 주문 조회, 수정, 삭제
- 폼에서 PUT 요청 보내면 자동으로 상태가 변경됨 (`status = 'Confirmed'` 등)

---

### 8. 페이지네이션 해제 (뷰셋 별도 설정)

```python
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = None  # 이 ViewSet에 한해 페이지네이션 제거
```

---

### 9. 정리

- `ViewSet`은 DRF에서 CRUD API 구현 시 매우 효율적인 구조를 제공
- `ModelViewSet`과 `DefaultRouter`를 함께 사용하면 몇 줄의 코드로 전체 API 생성 가능
- 다음 강의에서는 ViewSet에 사용자 정의 액션 추가 및 권한/필터링 적용을 다룹니다

