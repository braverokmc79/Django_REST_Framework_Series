## Django REST Framework(DRF) - ViewSet 권한 설정 & 관리자 vs 일반 사용자

### 1. 개요

이번 강의에서는 Django REST Framework의 ViewSet에서 **관리자(admin)** 와 **일반 사용자(user)** 간의 접근 권한을 어떻게 나누고 제어하는지를 배웁니다. 인증된 사용자라 하더라도 본인이 아닌 다른 사용자의 데이터를 조회하거나 수정하는 것을 방지하기 위한 필터링 및 권한 설정을 실습합니다.

---

### 2. 현재 ViewSet 기본 설정 복습

```python
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
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
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            # 일반 사용자일 경우: 본인의 주문만 필터링
            queryset = queryset.filter(user=self.request.user)

        return queryset
```

- `is_staff`가 False인 일반 사용자에겐 본인의 주문만 응답
- 관리자는 모든 주문 데이터 접근 가능

---

### 5. 효과 확인

- 브라우저 기반 API 혹은 VSCode REST Client를 통해 테스트
- 일반 사용자로 요청 시 자신의 주문만 반환됨
- 다른 사람의 주문 ID로 상세 요청 시 404 Not Found 응답

```http
GET /orders/   # 일반 사용자: 본인 주문만 응답
GET /orders/<other_user_order_id>/   # 일반 사용자: 404 응답
```

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

