
## 22-Viewset 권한 설정 & 관리자 vs 일반 사용자




[22 - Viewset 권한 설정 & 관리자 vs 일반 사용자](https://youtu.be/KmYYg1qJKNQ?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



---

### 1. 개요

이번 강의에서는 Django REST Framework의 ViewSet에서 **관리자(admin)** 와 **일반 사용자(user)** 간의 접근 권한을 어떻게 나누고 제어 하는지를 배웁니다. 인증된 사용자라 하더라도 본인이 아닌 다른 사용자의 데이터를 조회하거나 수정하는 것을 방지하기 위한 필터링 및 권한 설정을 실습 합니다.

---

### 2. 현재 ViewSet 기본 설정 복습

```python
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
        filtered_qs = self.filter_queryset(self.get_queryset())
        orders = filtered_qs.filter(user=request.user)  
        serializer = self.get_serializer(orders, many=True)  
        return Response(serializer.data)
```

- 현재는 인증된 사용자만 모든 주문을 조회할 수 있음
- 관리자뿐만 아니라 일반 사용자도 모든 주문을 볼 수 있어 보안상 문제가 발생함

---

### 3. 문제 상황 예시

- 일반 사용자 A가 `/orders/` 또는 `/orders/<order_id>/`에 접근하면 다른 사람의 주문까지 조회됨
- 프론트엔드에서는 사용자 개인 페이지에서 본인의 주문만 보여야 하는데, 백엔드에서 필터링이 되지 않음

---

### 4. 해결 전략: get\_queryset() 오버라이딩

`get_queryset()` 메서드를 오버라이딩하여 사용자 타입에 따라 응답 데이터를 제한합니다.


```python
class OrderViewSet(viewsets.ModelViewSet):
    # 기본적으로 Order와 관련된 items.product까지 함께 불러옴 (쿼리 최적화)
    queryset = Order.objects.prefetch_related('items__product')
    
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능
    pagination_class = None  # 페이징 비활성화
    filterset_class = OrderFilter  # 필터셋 클래스 지정
    filter_backends = [DjangoFilterBackend]  # 필터 백엔드 활성화

    def get_queryset(self):
        """
        관리자: 전체 주문 조회 가능
        일반 사용자: 본인 주문만 조회 가능
        """
        qs = super().get_queryset()  # 기본 queryset 가져오기
        if not self.request.user.is_staff:
            # 일반 사용자일 경우 본인 주문만 필터링
            qs = qs.filter(user=self.request.user)
        return qs

```


- `is_staff`가 False인 일반 사용자에겐 본인의 주문만 응답
- 관리자는 모든 주문 데이터 접근 가능



 정렬 및 검색 필터 확인

http://127.0.0.1:8000/orders/?status=Confirmed


http://127.0.0.1:8000/orders/?created_at_after=2025-06-24&created_at_before=2025-06-24



---

### 5. 효과 확인

- 브라우저 기반 API 혹은 VSCode REST Client를 통해 테스트
- 일반 사용자로 요청 시 자신의 주문만 반환됨
- 다른 사람의 주문 ID로 상세 요청 시 404 Not Found 응답

```http
GET /orders/   # 일반 사용자: 본인 주문만 응답
GET /orders/<other_user_order_id>/   # 일반 사용자: 404 응답
```


🎈테스트 하기
1) 장과 관리자 화면에서  테스트 유저 등록 후 주문 처리

![테스트유저등록](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhYgEFbpcYmUopE_-DdBSkVvvyAA1hr6WY-ByBNg4X2j9s9oWye-EWeOOc70muhKJ7_3BQUbh443MZcLIAzGw_Usc632dR_3kzLNsJ-PrGv2t7NuXiQltVknYvldvFq6hOQ64T4A1M78yQR9oFYMsBNSRnTY7iQRjMlm33huCp4LvAMjD7a_wQuaNb9k9NV/s1001/2025-06-29%2014%2025%2049.png)


2) insomnia 로 일반 사용자 테스트
![일반사용자](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiwkKTJ7aP9a57RNQJal8B7kckDK_opov9vvp-UEXpYE0vXQI0eMHPMjHCxUcYSDsn_KPdl3mAu_WckFCRBctqTJbvQdjx90NqfM_65EIsIjObkSEC-GVTzbAYZLJQ_MAtjYH44Ha5sQihUORetdIUEVokgRCBE4zh3FiO3bPyXFHIAN8vxhv1rv8oOY-8e/s2132/2025-06-29%2014%2026%2036.png)




 3) 관리지 
![관리자](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgWmXTDdlYm1vkth4cgX9KHK9J09n8-4dCs3-JrWEJ2jnCGRlEhfFe8x6U50h4xA8HmMnrUimM6jWSIPocLXeDbeiV6a2D5aAs6rAO6PPQZS6GjWLmV5PMKyxj109GDckcc0MJKlVCtze196bqapFAXpO21Ys611Mj0LCoL8OiX9RF8sZNy7kYyDI1rD762/s2126/2025-06-29%2014%2026%2014.png)



---

### 6. 커스텀 액션 제거 가능

기존에 `@action(detail=False)`으로 정의했던 `user-orders` 액션은 불필요

- 이유: 기본 `/orders/` 요청 자체가 사용자에 따라 자동 필터링되기 때문

---

### 7. 전체 구성 요약

- `permission_classes = [IsAuthenticated]`: 인증된 사용자만 API 접근 가능
- `get_queryset()` 오버라이딩으로 일반 사용자에겐 데이터 접근 제한
- 관리자는 모든 주문을 자유롭게 조회, 수정, 삭제 가능
- ViewSet 하나로 사용자 유형별 데이터 접근 권한 제어 완성

---

### 8. 마무리 및 다음 강의 예고

이번 강의를 통해 ViewSet 하나로 **권한 제어**, **필터링**, **보안**까지 통합 관리하는 방법을 익혔습니다.

> 다음 강의에서는 **중첩 Serializer**와 관련 객체를 포함한 POST 요청 처리 및 `create()` 메서드 오버라이딩에 대해 학습합니다.

