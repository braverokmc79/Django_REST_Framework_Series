## 21-Viewset에서의 액션, 필터링, 권한 처리



[21 - Viewset에서의 액션, 필터링, 권한 처리](https://youtu.be/rekvVrjUMjg?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)


---

### 1. 개요

이번 강의에서는 Django REST Framework의 ViewSet을 확장하여 **액션 추가**, **필터링 적용**, **권한 제어** 기능을 다루게 됩니다. ViewSet의 기본 CRUD 외에 사용자 맞춤형 기능을 추가하고, 필터 조건 및 인증 기반 제어를 통해 더욱 안전하고 유연한 API를 구성하는 방법을 배웁니다.

---

### 2. 필터링 기능 확장
#### 1) 주문(Order)에 대한 필터 클래스 생성
`ProductFilter`와 유사하게 `OrderFilter`를 생성하여 `status`, `created_at` 필드 기준으로 필터 가능하게 구성합니다.

```python
import django_filters
from api.models import Product, Order

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


http://127.0.0.1:8000/orders/user-orders/?created_exact=2025-06-25

적용이 안된다.

🔖 DateFilter
`Order.created_at` 필드는  `DateTimeField`일 텐데, 여기에 `exact='2025-06-25'`을 걸면:

- **DB에서는 '2025-06-25 00:00:00'** 으로 해석됨
    
- 그러나 실제 저장된 `created_at` 값은 **2025-06-25 14:35:22** 등의 시간이 포함된 값이기 때문에
    
- `exact` 조건과 **정확히 일치하지 않음** → 결과 없음

✅ 해결 방법: `DateFromToRangeFilter` 사용 (추천)

```python
from django_filters import DateFromToRangeFilter
import django_filters

class OrderFilter(django_filters.FilterSet):
    created_at = DateFromToRangeFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact'],  # 그대로 두어도 됨
        }
```

다음과 같이 요청시 하루 검색 가능

```bash
/orders/user-orders/?created_at_after=2025-06-25&created_at_before=2025-06-25

```

또는 시간 범위 지정도 가능
```bash
/orders/user-orders/?created_at_after=2025-06-25T00:00&created_at_before=2025-06-25T23:59

```




#### 2) ViewSet에 필터 클래스 적용
```python
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderFilter

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    ...
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
```

이제 다음과 같은 쿼리 예시로 필터링 가능합니다:
```
/orders/?status=Confirmed
/orders/?created_at__gt=2024-09-30
/orders/?created_at_after=2025-06-24&created_at_before=2025-06-24
```

---


### 3. 사용자 정의 액션 추가
#### 사용자 주문 목록 조회 액션 (`@action`)
```python
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    ...
	 
	 permission_classes = [IsAuthenticated]
	 filterset_class = OrderFilter
	...
	

    @action(
        detail=False,    # 여러 개를 다루는 list 형식 (단일 객체 X)
        methods=['get'],   # GET 요청만 허용
        url_path='user-orders',     # URL: `/orders/user-orders/` 로 접근   
    )
    def user_orders(self, request):
	    #orders = self.get_queryset().filter(user=request.user)
        filtered_qs = self.filter_queryset(self.get_queryset())
        orders = filtered_qs.filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
```

ur : http://127.0.0.1:8000/orders/user-orders/


http://127.0.0.1:8000/orders/user-orders/?created_at__lt=2025-07-20

- `@action`: 커스텀 경로 정의용 데코레이터
- `detail=False`: 단일 객체가 아닌 리스트 응답
- `permission_classes`: 해당 액션에만 인증 필요 적용
- URL 예: `/orders/user-orders/`
- orders = self.get_queryset().filter(user=request.user)  # 현재 로그인한 사용자의 주문만 조회
- serializer = self.get_serializer(orders, many=True)     # 여러 개니까 many=True
-  return Response(serializer.data)                        # 직렬화된 JSON 응답 반환
- filtered_qs = self.filter_queryset(self.get_queryset())  # 필터셋, 검색, 정렬 적용됨
- orders = filtered_qs.filter(user=request.user)  # 여기에 사용자 필터 추가




#### 인증되지 않은 경우 처리
- 로그인하지 않은 사용자가 해당 URL 접근 시 401 Unauthorized 응답 발생
- 예외 대신 명확한 인증 에러 반환 가능함

---

### 4. ViewSet 전체 권한 적용
```python
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    
```

- 위 설정으로 ViewSet의 모든 기본/커스텀 액션에 인증이 요구됨
- 개별 액션의 권한 설정은 불필요해짐



🌟 OrderViewSet 최종 코드

```python
from rest_framework.decorators import action
from rest_framework.permissions import  IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import  OrderFilter


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
  

    @action(
        detail=False,
        methods=['get'],
        url_path='user-orders',
    )
    def user_orders(self, request):
        #orders = self.get_queryset().filter(user=request.user)
        filtered_qs = self.filter_queryset(self.get_queryset())
        orders = filtered_qs.filter(user=request.user
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
```



---



### 5. 정리
- ViewSet에서 필터링, 사용자 정의 액션, 권한을 효율적으로 적용할 수 있음
- 커스텀 액션은 `@action` 데코레이터로 추가하고, 사용자 조건에 맞게 로직 구현 가능
- `IsAuthenticated` 권한 클래스로 보안 강화 가능

> 다음 강의에서는 인증된 사용자에 따라 조회/수정/삭제 범위를 제한하고, 관리자에게만 전체 접근 권한을 부여하는 고급 권한 제어 방법을 배웁니다.





