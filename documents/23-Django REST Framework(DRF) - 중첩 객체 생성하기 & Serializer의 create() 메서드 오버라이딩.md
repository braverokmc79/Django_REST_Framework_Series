## Django REST Framework(DRF) - 중첩 객체 생성하기 & Serializer의 create() 메서드 오버라이딩

### 1. 개요

이번 강의에서는 Django REST Framework(DRF)에서 **POST 요청 시 중첩된 관련 객체를 함께 생성**하는 방법을 학습합니다. 이 과정에서 `create()` 메서드를 오버라이딩하여 **Writable Nested Serializer**를 구현합니다.

---

### 2. 기본 구조 이해

기존에는 `OrderSerializer` 내의 `items` 필드가 `read_only=True`로 설정되어 있어, 주문 생성 시(Order POST 요청) `OrderItem`을 함께 생성할 수 없었습니다.

#### 기존 문제:

- `POST /orders/` 요청 시 `items` 필드는 무시됨
- 주문 생성 후 별도로 `OrderItem` 생성 필요

---

### 3. 새로운 중첩 생성용 Serializer 정의

#### 1) `OrderCreateSerializer` 생성

```python
class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ['product', 'quantity']

    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'status', 'items']
        extra_kwargs = {
            'user': {'read_only': True},
            'order_id': {'read_only': True},
        }

    def create(self, validated_data):
        order_items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in order_items_data:
            OrderItem.objects.create(order=order, **item)
        return order
```

> `items` 리스트 안에 있는 중첩 데이터를 별도로 pop하여 각 `OrderItem` 생성

---

### 4. ViewSet에 동적 serializer 적용

```python
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

- POST 요청 시에만 `OrderCreateSerializer`를 사용하여 중첩된 객체 생성
- `perform_create()`에서 user를 자동 할당

---

### 5. 테스트 예시 (요청 본문)

```json
{
  "status": "Pending",
  "items": [
    { "product": 1, "quantity": 2 },
    { "product": 3, "quantity": 1 }
  ]
}
```

- user 필드는 서버에서 자동 지정되므로 클라이언트가 직접 입력하지 않음

---

### 6. 응답 예시

```json
{
  "order_id": "c7a56d28-0d90-4c3e-bd63-23b4a34b6eec",
  "user": 1,
  "status": "Pending",
  "items": [
    {"product": 1, "quantity": 2},
    {"product": 3, "quantity": 1}
  ]
}
```

---

### 7. 요약

- 중첩 객체를 함께 생성하려면 `create()` 메서드를 오버라이딩해야 함
- POST 요청 시 전용 serializer 사용
- 관련 필드는 `pop()` 후 루프 돌며 관련 모델 인스턴스 생성
- `perform_create()`로 인증된 사용자 자동 설정

> 다음 강의에서는 ViewSet 내부에서 `update()` 메서드를 활용한 중첩 객체 수정 전략을 다룹니다.

