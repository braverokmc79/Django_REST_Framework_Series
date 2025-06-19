
## Django REST Framework(DRF) - 동적 필터링 & get_queryset() 메서드 오버라이딩

### 1. 개요

이전 영상에서는 Django REST Framework의 제너릭 API View인 `ListAPIView`와 `RetrieveAPIView`를 사용해 데이터를 조회하는 방법을 알아봤습니다. 이번에는 **인증된 사용자에 따라 쿼리셋을 동적으로 필터링**하는 방법, 즉 `get_queryset()` 메서드를 오버라이딩하는 방법을 소개합니다.

---

### 2. 목표 예시: 로그인한 사용자에게 자신의 주문만 보여주기

기존의 주문 API(`/orders`)는 전체 주문을 반환합니다. 하지만 보안상 각 사용자는 **자신의 주문만** 볼 수 있어야 하므로, 인증된 사용자에 따라 주문 목록을 필터링하는 API가 필요합니다.

이 작업을 위해 `get_queryset()` 메서드를 오버라이딩하고, 해당 메서드 내에서 `self.request.user`를 사용해 쿼리셋을 필터링합니다.

---

### 3. admin 등록과 샘플 데이터 생성

먼저 관리자 페이지에서 주문을 손쉽게 추가할 수 있도록 `Order` 모델과 `OrderItem` 모델을 admin에 등록합니다. 이를 위해 TabularInline 클래스를 사용해 주문 작성 시 바로 주문 항목도 추가 가능하도록 구성합니다.

```python
class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
```

그 다음 `createsuperuser` 명령어로 슈퍼유저를 만들고, 로그인한 후 관리자 페이지에서 테스트 주문을 생성합니다.

---

### 4. get_queryset() 메서드 오버라이딩

`views.py`에서 기존 `OrderListAPIView`를 복사해 새로운 클래스를 정의합니다:

```python
class UserOrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
```

- `self.request.user`를 통해 현재 로그인된 사용자에 접근 가능
    
- 해당 사용자에 속한 주문만 필터링해서 반환
    

---

### 5. URL 연결

`urls.py`에 다음을 추가합니다:

```python
path('user-orders/', UserOrderListAPIView.as_view()),
```

이제 `/user-orders/` 엔드포인트로 요청을 보내면 로그인된 사용자 본인의 주문만 반환됩니다.

---

### 6. 동작 확인

1. 사용자 John Do로 로그인한 상태에서 `/user-orders/` 요청 → John의 주문만 반환됨
    
2. admin 사용자로 로그인한 후 요청 → admin의 주문만 반환됨
    
3. 로그아웃 상태에서 요청 → 오류 발생 (익명 사용자 접근 불가)
    

이처럼 `get_queryset()`을 활용하면 인증된 사용자에 따라 데이터를 동적으로 필터링할 수 있습니다.

---

### 7. 보안 문제 및 다음 주제 예고

현재 `/user-orders/`는 누구나 접근할 수 있는 공개된 API입니다. 이 상태에서는 익명 사용자도 요청을 보낼 수 있으므로, `request.user`가 `AnonymousUser`일 경우 오류가 발생할 수 있습니다.

이를 방지하기 위해, 다음 영상에서는 **DRF의 권한(Permissions)** 기능을 활용해 인증된 사용자만 접근할 수 있도록 설정하는 방법을 다룰 예정입니다.

---

> 다음 강의: 인증(permissions)을 활용해 로그인된 사용자만 자신의 주문 목록을 조회할 수 있도록 제한하기