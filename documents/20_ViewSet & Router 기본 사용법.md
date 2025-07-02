
## 20-ViewSet & Router 기본 사용법


[20 - ViewSet & Router 기본 사용법](https://youtu.be/4MrB4IvW6Ow?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



---

### 1. 개요

이번 강의에서는 Django REST Framework(DRF)의 **ViewSet**과 **Router**의 개념 및 사용법을 학습합니다. 반복되는 API 뷰 코드를 간소화하고 RESTful한 URL 구조를 자동으로 생성하기 위해 이 기능들을 적극 활용할 수 있습니다.

---

### 2. ViewSet이란?

- **ViewSet은** 관련된 여러 HTTP 요청 처리 로직(`list`, `create`, `retrieve`, `update`, `destroy`)을 **하나의 클래스에 통합**한 구조입니다.
- 
- DRF의 `APIView`나 `GenericAPIView`처럼 `get()`, `post()` 메서드를 직접 다루는 대신, ViewSet은 **"행위 중심(Action-based)" 메서드**를 사용합니다.
- 
- 기존 `APIView` 또는 `GenericAPIView`처럼 HTTP 메서드(GET, POST 등)를 직접 다루는 대신, 

```python
def list(self, request): ...
def create(self, request): ...
def retrieve(self, request, pk=None): ...
def update(self, request, pk=None): ...
def destroy(self, request, pk=None): ...
```
- 등의 액션 메서드를 사용

```python
from rest_framework import viewsets

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # 일단 인증 없이 열어둠 (다음 강의에서 수정)
```

- `ModelViewSet`을 상속하면 CRUD를 자동 지원
- 기존의 ListAPIView, CreateAPIView 등을 통합하는 형태


✅ `ModelViewSet`이 자동 지원하는 CRUD 액션 메서드

| 메서드 이름             | 기능    | HTTP 메서드 | 엔드포인트 예시     |
| ------------------ | ----- | -------- | ------------ |
| `list()`           | 목록 조회 | GET      | `/orders/`   |
| `retrieve()`       | 단건 조회 | GET      | `/orders/1/` |
| `create()`         | 생성    | POST     | `/orders/`   |
| `update()`         | 전체 수정 | PUT      | `/orders/1/` |
| `partial_update()` | 부분 수정 | PATCH    | `/orders/1/` |
| `destroy()`        | 삭제    | DELETE   | `/orders/1/` |
✨ 즉, `ModelViewSet`은 `ListAPIView`, `CreateAPIView`, `RetrieveAPIView`, `UpdateAPIView`, `DestroyAPIView` 등을 **통합한 올인원 클래스**입니다.


---

### 3. Router란?

- ViewSet은 URL 설정이 별도로 필요
- DRF의 **Router**는 ViewSet과 연결된 URL들을 자동으로 생성해주는 기능 제공

```python
from django.urls import path
from django.shortcuts import redirect
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
		...
# path('orders/', views.OrderListAPIView.as_view()),
# path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls

```


views.py
```python
from rest_framework import generics ,filters , viewsets

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

  
# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer

  
# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         qs =super().get_queryset()
#         return qs.filter(user=self.request.user)
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

