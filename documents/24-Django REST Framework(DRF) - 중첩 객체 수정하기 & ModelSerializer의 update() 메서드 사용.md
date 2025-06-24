## Django REST Framework(DRF) - 중첩 객체 수정하기 & ModelSerializer의 update() 메서드 사용

### 1. 개요

이 강의에서는 Django REST Framework(DRF)에서 PUT 요청 시 **중첩된 객체도 함께 수정**하는 방법을 학습합니다. 이를 위해 `update()` 메서드를 오버라이딩하고, 전체 작업을 **트랜잭션 처리**하여 데이터 정합성을 유지하는 방식도 함께 다룹니다.

---

### 2. update() 메서드 구조 이해

기존에는 create()만 오버라이딩 했지만, PUT 요청으로 기존 데이터를 수정하려면 `update()` 메서드도 오버라이딩해야 합니다.

```python
class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, required=False)
    ...

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('items', None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if order_items_data is not None:
                # 기존 항목 제거
                instance.items.all().delete()
                # 새 항목 생성
                for item in order_items_data:
                    OrderItem.objects.create(order=instance, **item)

        return instance
```

- `transaction.atomic()` 으로 전체 작업을 하나의 트랜잭션으로 처리
- 기존 `OrderItem`은 삭제 후 새롭게 재생성
- `items` 필드는 없을 수도 있으므로 `required=False`, `.pop(..., None)` 사용

---

### 3. ViewSet 수정

기존의 get\_serializer\_class()를 확장하여 update 액션에도 동일한 serializer 사용

```python
class OrderViewSet(viewsets.ModelViewSet):
    ...

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OrderCreateSerializer
        return super().get_serializer_class()
```

---

### 4. 요청 예시 (PUT)

```json
{
  "status": "Confirmed",
  "items": [
    { "product": 1, "quantity": 3 },
    { "product": 2, "quantity": 2 }
  ]
}
```

- `items` 변경 가능 (예: 수량 수정)
- 기존 `OrderItem` 삭제 후 새롭게 반영

---

### 5. 예외 처리 및 유연성

- `items`가 없는 요청도 유효하게 처리할 수 있도록 구현
- 존재하지 않는 경우 기존 항목 유지됨

```python
if order_items_data is not None:
    ...  # 삭제 후 재생성
# else: 기존 항목 그대로 유지
```

---

### 6. 트랜잭션 처리 이유

- `Order`만 수정되고 `OrderItem` 생성 중 오류 나면 데이터 불일치 발생
- `transaction.atomic()`을 사용해 하나라도 실패 시 전체 작업 롤백됨

---

### 7. Delete 요청 처리

ViewSet이 `ModelViewSet`을 상속받고 있으므로 `DELETE /orders/<id>/` 요청 시 자동 처리됨

```http
DELETE /orders/c7a56d28-0d90-4c3e-bd63-23b4a34b6eec/
Response: 204 No Content
```

- 삭제 후 동일 ID로 GET 요청 시 404 Not Found 반환됨

---

### 8. 요약

- `update()` 메서드를 오버라이딩해 중첩 객체 수정 처리
- `items`가 요청에 포함되지 않으면 기존 항목 유지
- 트랜잭션으로 데이터 일관성 보장
- `ModelViewSet`으로 DELETE도 기본 제공

> 다음 강의에서는 serializer 필드 설정을 좀 더 세밀하게 다루고, 캐시 및 Redis 설정을 활용한 성능 최적화를 진행합니다.

