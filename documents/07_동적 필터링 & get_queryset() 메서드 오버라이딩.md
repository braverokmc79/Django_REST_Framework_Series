
## 07-동적 필터링 & get_queryset() 메서드 오버라이딩


[07 - 동적 필터링 & get_queryset() 메서드 오버라이딩](https://youtu.be/3Gi-w4Swge8?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)


---


### 1. 개요

이전 강의에서는 Django REST Framework의 제너릭 API View인 `ListAPIView`와 `RetrieveAPIView`를 사용해 데이터를 조회하는 방법을 알아봤습니다. 이번에는 **인증된 사용자에 따라 쿼리셋을 동적으로 필터링**하는 방법, 즉 `get_queryset()` 메서드를 오버라이딩하는 방법을 소개합니다.

---

### 2. 목표 예시: 로그인한 사용자에게 자신의 주문만 보여주기

기존의 주문 API(`/orders`)는 전체 주문을 반환합니다. 하지만 보안상 각 사용자는 **자신의 주문만** 볼 수 있어야 하므로, 인증된 사용자에 따라 주문 목록을 필터링하는 API가 필요합니다.

이 작업을 위해 `get_queryset()` 메서드를 오버라이딩하고, 해당 메서드 내에서 `self.request.user`를 사용해 쿼리셋을 필터링합니다.

---
#### ✅ 1. 관리자 계정 비밀번호 재설정 (manage.py 사용)

만약 계정은 기억나고 **비밀번호만 잊어버렸다면**, 다음 명령으로 변경할 수 있습니다

```bash
python manage.py changepassword <username>

```

예

```python
python manage.py changepassword admin

```


---

### 3. admin 등록과 샘플 데이터 생성

먼저 관리자 페이지에서 주문을 손쉽게 추가할 수 있도록 `Order` 모델과 `OrderItem` 모델을 admin에 등록합니다. 이를 위해 TabularInline 클래스를 사용해 주문 작성 시 바로 주문 항목도 추가 가능하도록 구성합니다.

api/admin.py
```python
class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
```

그 다음 `createsuperuser` 명령어로 슈퍼유저를 만들고, 로그인한 후 관리자 페이지에서 테스트 주문을 생성합니다.

#### 🔖 ModelAdmin / `TabularInline` / `StackedInline
##### ✅ `ModelAdmin`

- 하나의 모델(예: `Order`)을 **관리자 화면에서 전반적으로 관리**하는 설정.
    
- 어떤 필드를 보여줄지, 필터나 검색 기능 등을 어떻게 구성할지 등을 정의함.

```python
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')  # 관리자 목록에 표시할 필드
    search_fields = ('customer__name',)
    list_filter = ('status',)
```


##### ✅ `TabularInline` / `StackedInline`

- **연관된 다른 모델**(예: `OrderItem`)을, 부모 모델의 편집 화면에 **inline(인라인) 형식으로 같이 표시**할 때 사용.
    
- `TabularInline`은 테이블 형태로, `StackedInline`은 블록 형태로 보여줌.

```python
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # 빈 폼 1개 추가로 표시

```


##### ✅ 함께 사용하는 이유

예를 들어 `Order`에는 여러 개의 `OrderItem`이 연결되어 있으니, 관리자가 주문 하나를 편집할 때 관련 항목도 **같은 화면에서 추가/수정/삭제**할 수 있도록 하기 위함입니다

```python
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
```

이렇게 하면 Order 수정 페이지 안에서 OrderItem을 직접 추가하거나 수정할 수 있게 됩니다.

##### 🔁 간단히 예를 들면

| 기능                               | 설명                       | 사용 클래스                             |
| -------------------------------- | ------------------------ | ---------------------------------- |
| 주문 전체 목록 보기                      | 어떤 주문이 있는지 리스트로 확인       | `ModelAdmin`                       |
| 주문 상세 페이지에서 해당 주문의 아이템도 함께 보기/수정 | 주문 내 항목들을 inline으로 함께 수정 | `TabularInline` 또는 `StackedInline` |





---

### 4. get_queryset() 메서드 오버라이딩

`views.py`에서 기존 `OrderListAPIView`를 복사해 새로운 클래스를 정의합니다:

```python
class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
```

- `self.request.user`를 통해 현재 로그인된 사용자에 접근 가능
    
- 해당 사용자에 속한 주문만 필터링해서 반환

#### 🔍 구성요소 설명

##### 1. `generics.ListAPIView`

- Django REST Framework에서 **목록 조회 전용 API 뷰 클래스**입니다.
    
- `GET` 요청 시 `queryset`의 데이터를 리스트로 반환합니다.
    

---

##### 2. `queryset = Order.objects.prefetch_related('items__product')`

- `Order` 모델을 기본적으로 조회합니다.
    
- `prefetch_related('items__product')`:  
    → 쿼리 최적화를 위해 `Order`와 연결된 `OrderItem`, 그리고 그 `OrderItem`에 연결된 `Product`를 미리 불러옵니다.  
    → **N+1 문제를 방지**함.
    

---

##### 3. `serializer_class = OrderSerializer`

- 응답 결과를 JSON으로 바꿔줄 때 사용할 **시리얼라이저**를 지정합니다.
    

---

##### 4. `def get_queryset(self)`

- `queryset`을 커스터마이징합니다.
    
- `super().get_queryset()`은 위에서 정의한 `queryset`을 가져옵니다.
    
- `.filter(user=self.request.user)`는 로그인한 사용자(`request.user`)의 주문만 필터링합니다.
    

---

## 🧠 요약하자면:

> **"로그인한 사용자의 주문 목록만 가져오는 API이며, 관련된 상품 정보도 미리 불러오는 최적화된 방식이다."**


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