

## Django REST Framework(DRF) - 권한 시스템 및 테스트

### 1. 개요

이번 영상에서는 Django REST Framework에서 **권한(Permissions)** 시스템을 소개하고, 이를 실제 뷰 클래스에 적용하여 인증된 사용자만 특정 API에 접근할 수 있도록 제한하는 방법을 설명합니다. 또한, 해당 기능을 테스트하는 방법도 함께 다룹니다.

---

### 2. 문제 상황: 인증되지 않은 사용자 접근 오류

지난 영상에서 `/user-orders/` 엔드포인트는 로그인된 사용자만 자신의 주문을 확인할 수 있도록 `get_queryset()`을 오버라이딩했습니다. 하지만 인증되지 않은 사용자가 접근하면, `self.request.user`가 `AnonymousUser`가 되어 오류가 발생합니다.

이를 방지하려면 DRF에 이 뷰는 인증된 사용자만 접근 가능하다고 명시해야 합니다.

---

### 3. DRF 권한 시스템 개요

* **Permissions**는 인증(Authentication) 및 요청 제한(Throttling)과 함께 작동하여 API 접근을 제어합니다.
* 뷰가 실행되기 전에 먼저 권한 검사가 수행됩니다.
* `request.user`와 `request.auth` 정보를 바탕으로 요청이 허용될지 여부를 판단합니다.

대표적인 권한 클래스:

* `IsAuthenticated`: 인증된 사용자만 접근 허용
* `IsAuthenticatedOrReadOnly`: 인증되면 전체 권한, 비인증 사용자는 읽기 전용

---

### 4. 권한 클래스 적용 방법

`views.py`에서 `UserOrderListAPIView`에 권한 클래스를 추가합니다:

```python
from rest_framework.permissions import IsAuthenticated

class UserOrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
```

이제 인증되지 않은 사용자가 요청하면 **403 Forbidden** 응답을 받습니다.

---

### 5. 테스트 코드 작성

권한 기능이 정상 작동하는지 테스트를 통해 검증합니다.

```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from api.models import User, Order

class UserOrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        Order.objects.create(user=self.user1)
        Order.objects.create(user=self.user1)
        Order.objects.create(user=self.user2)
        Order.objects.create(user=self.user2)

    def test_user_orders_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('user-orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        orders = response.json()
        self.assertTrue(all(order['user'] == self.user1.id for order in orders))

    def test_user_orders_unauthenticated(self):
        url = reverse('user-orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

* 첫 번째 테스트는 인증된 사용자가 자신의 주문만 받는지 확인
* 두 번째 테스트는 비인증 사용자가 접근 시 403 오류가 반환되는지 확인
* `status.HTTP_403_FORBIDDEN`와 같은 상수를 사용하면 코드 가독성이 높아집니다.

---

### 6. 브라우저에서 확인

1. 로그인하지 않은 상태에서 `/user-orders/` 접속 → "인증 정보가 제공되지 않았습니다" 메시지 표시
2. 로그인 후 `/user-orders/` 요청 → 해당 사용자 주문만 반환

---

### 7. 정리

* DRF의 `IsAuthenticated` 권한 클래스를 사용하면 인증된 사용자만 API에 접근할 수 있도록 설정할 수 있습니다.
* 권한 로직이 제대로 작동하는지 테스트 코드를 작성해 자동 검증하는 것이 중요합니다.
* 응답 코드에 매직 넘버 대신 `rest_framework.status`의 상수를 사용하는 것이 좋습니다.

---

> 다음 강의에서는 `APIView` 클래스를 사용해 모델에 의존하지 않는 커스텀 API 뷰를 만드는 방법을 소개합니다.


