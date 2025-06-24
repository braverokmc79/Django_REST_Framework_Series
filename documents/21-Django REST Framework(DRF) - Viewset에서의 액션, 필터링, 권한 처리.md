## Django REST Framework(DRF) - ViewSet에서의 액션, 필터링, 권한 처리

### 1. 개요
이번 강의에서는 Django REST Framework의 ViewSet을 확장하여 **액션 추가**, **필터링 적용**, **권한 제어** 기능을 다루게 됩니다. ViewSet의 기본 CRUD 외에 사용자 맞춤형 기능을 추가하고, 필터 조건 및 인증 기반 제어를 통해 더욱 안전하고 유연한 API를 구성하는 방법을 배웁니다.

---

### 2. 필터링 기능 확장
#### 1) 주문(Order)에 대한 필터 클래스 생성
`ProductFilter`와 유사하게 `OrderFilter`를 생성하여 `status`, `created_at` 필드 기준으로 필터 가능하게 구성합니다.

```python
import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')

    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact'],
        }
```

- `status`: 정확히 일치하는 값 필터링
- `created_at`: 날짜 비교 (미만/초과/일치)
- `__date`를 활용해 `DateTimeField`에서 날짜만 추출하여 비교

#### 2) ViewSet에 필터 클래스 적용
```python
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderFilter

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
```

이제 다음과 같은 쿼리 예시로 필터링 가능합니다:
```
/orders/?status=Confirmed
/orders/?created_at__gt=2024-09-30
/orders/?created_at__exact=2024-12-06
```

---

### 3. 사용자 정의 액션 추가
#### 사용자 주문 목록 조회 액션 (`@action`)
```python
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    ...

    @action(detail=False, methods=['get'], url_path='user-orders', permission_classes=[IsAuthenticated])
    def user_orders(self, request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
```

- `@action`: 커스텀 경로 정의용 데코레이터
- `detail=False`: 단일 객체가 아닌 리스트 응답
- `permission_classes`: 해당 액션에만 인증 필요 적용
- URL 예: `/orders/user-orders/`

#### 인증되지 않은 경우 처리
- 로그인하지 않은 사용자가 해당 URL 접근 시 401 Unauthorized 응답 발생
- 예외 대신 명확한 인증 에러 반환 가능함

---

### 4. ViewSet 전체 권한 적용
```python
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
```

- 위 설정으로 ViewSet의 모든 기본/커스텀 액션에 인증이 요구됨
- 개별 액션의 권한 설정은 불필요해짐

---

### 5. 정리
- ViewSet에서 필터링, 사용자 정의 액션, 권한을 효율적으로 적용할 수 있음
- 커스텀 액션은 `@action` 데코레이터로 추가하고, 사용자 조건에 맞게 로직 구현 가능
- `IsAuthenticated` 권한 클래스로 보안 강화 가능

> 다음 강의에서는 인증된 사용자에 따라 조회/수정/삭제 범위를 제한하고, 관리자에게만 전체 접근 권한을 부여하는 고급 권한 제어 방법을 배웁니다.

