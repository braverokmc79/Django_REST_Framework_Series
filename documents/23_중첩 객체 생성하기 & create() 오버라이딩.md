## 23-중첩 객체 생성하기 & create() 오버라이딩



[23 - 중첩 객체 생성하기 & create() 오버라이딩](https://youtu.be/CAq7AKAT7Q0?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)


---


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

    # 🔹 내부에 중첩 직렬화 클래스 정의: 주문 항목 (OrderItem)을 처리
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product','quantity') #product:ForeignKey,quantity: IntegerField

    # 🔹 주문 고유 ID (UUID) 필드: 읽기 전용 (자동 생성됨)
    order_id = serializers.UUIDField(read_only=True)

    # 🔹 주문 항목 목록을 중첩으로 받음 (OrderItemCreateSerializer를 다수로 처리)
    items = OrderItemCreateSerializer(many=True)

    # ✅ 주문 생성 로직 재정의 (직접 create 오버라이드)
    def create(self, validated_data):
        # 1️⃣ OrderItem 데이터 분리
        orderitem_data = validated_data.pop('items')

        # 2️⃣ Order 생성 (user, status 등)
        order = Order.objects.create(**validated_data)

        # 3️⃣ OrderItem 하나씩 생성 및 Order에 연결
        for item in orderitem_data:
            OrderItem.objects.create(order=order, **item)

        return order  # 생성된 order 반환

    class Meta:
        model = Order
        fields = (
            'order_id',   # 읽기 전용 UUID
            'user',       # 요청 시 자동 할당 (read_only)
            'status',     # 주문 상태 (ex. 'pending')
            'items',      # 주문 항목 리스트
        )
        extra_kwargs = {
            'user': {'read_only': True}  # 요청자가 자동으로 지정되므로 수동 입력 금지
        }

```

> `items` 리스트 안에 있는 중첩 데이터를 별도로 pop하여 각 `OrderItem` 생성

✅ validated_data 요약

`validated_data`는 **Serializer에서 유효성 검사를 통과한 데이터(Django에서 clean된 데이터)를 담고 있는 딕셔너리 입니다

`validated_data`는:

- 사용자가 보낸 JSON 데이터를
    
- `OrderCreateSerializer`가 `is_valid()`를 통해 검증하고
    
- 최종적으로 검증된 필드만 포함된 안전한 딕셔너리입니다
-

|항목|설명|
|---|---|
|`validated_data`|직렬화기(`Serializer`)가 `.is_valid()` 후 만들어주는 **검증된 데이터 딕셔너리**|
|형식|파이썬 `dict` (예: `{ 'status': 'pending', 'items': [...], ... }`)|
|사용 이유|DB 저장 시 안전하고, 검증된 데이터만 사용하기 위함|
|`.pop('items')`|중첩 필드를 따로 분리해 수동으로 처리하기 위함|



✅ 실제 예상 사용 예 (POST 요청 시)

```json
POST /orders/

{
  "status": "pending",
  "items": [
    { "product": 1, "quantity": 2 },
    { "product": 3, "quantity": 1 }
  ]
}

```

→ `user`는 자동으로 `request.user`에서 주입됨  
→ 내부적으로 `Order`를 먼저 생성한 후, `OrderItem`들을 반복 생성하여 해당 `Order`에 연결합니다.


✅ 장점 요약

|항목|설명|
|---|---|
|중첩 생성|`Order`와 하위 `OrderItem`들을 한 번에 생성 가능|
|사용자 자동 설정|`user` 필드를 read_only로 하여 서버에서 자동 할당|
|커스터마이즈 가능성 ↑|`create()`를 직접 오버라이드했기 때문에 유효성 검사, 포인트 차감 등 추가 로직 삽입 가능|







---

### 4. ViewSet에 동적 serializer 적용

 이 ViewSet은  주문 생성과 조회를 분리된 직렬화기와 권한으로 처리 하며,  일반 유저는 자신의 주문만, **관리자는 전체 주문을 조회**할 수 있게 합니다.

```python
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # can also check if POST: if self.request.method == 'POST'
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs
```

- POST 요청 시에만 `OrderCreateSerializer`를 사용하여 중첩된 객체 생성
- `perform_create()`에서 user를 자동 할당

#### 📌 코드별 상세 설명

```python
class OrderViewSet(viewsets.ModelViewSet):
```

DRF의 `ModelViewSet`을 사용하여 `list`, `create`, `retrieve`, `update`, `destroy` 등 REST API 기본 제공.


##### 🔹 `queryset`
```python
queryset = Order.objects.prefetch_related('items__product')
```

- DB에서 주문을 불러올 때, `items__product` 관계를 **미리 로딩(pre-fetch)** 하여 **N+1 쿼리 방지**.
    
- 주문 상세 보기나 목록에서 성능 개선 효과 있음.


##### 🔹 `serializer_class`
```python
serializer_class = OrderSerializer
```

기본으로는 `OrderSerializer`를 사용함. (`list`, `retrieve` 등에서 사용)


##### 🔹 `permission_classes`
```python
permission_classes = [IsAuthenticated]
```

로그인된 사용자만 접근 가능하게 설정함.


##### 🔹 `pagination_class`
```python
pagination_class = None
```

페이지네이션 비활성화됨. 전체 주문을 한 번에 내려줌.  
(`LimitOffsetPagination` 등으로 변경 가능)


##### 🔹 `filterset_class` + `filter_backends`
```python
filterset_class = OrderFilter
filter_backends = [DjangoFilterBackend]
```

URL에서 `/orders/?status=pending&created_at__gte=2025-06-01` 등 필터 적용 가능.

##### ✅ `perform_create`

```python
def perform_create(self, serializer):
    serializer.save(user=self.request.user)

```

- `POST /orders/`로 주문 생성할 때, `request.user`를 직접 주입함.
    
- 클라이언트가 user를 넣지 않아도, **현재 로그인된 사용자로 자동 지정**됨.
    
- `OrderCreateSerializer`에서 `user`는 `read_only=True` 처리되어 있어야 함 (→ 안전성 ↑).


##### ✅ `get_serializer_class`

```python
def get_serializer_class(self):
    if self.action == 'create':
        return OrderCreateSerializer
    return super().get_serializer_class()
```

- `create` 요청일 경우에만 `OrderCreateSerializer`를 사용하도록 분기.
    
- 그 외에는 기본 `OrderSerializer`를 사용.
    
- 이렇게 하면 생성(create)과 조회(read)의 직렬화 구성을 명확히 분리할 수 있어 실무에서 매우 유용합니다.


##### ✅ `get_queryset`
```python
def get_queryset(self):
    qs = super().get_queryset()
    if not self.request.user.is_staff:
        qs = qs.filter(user=self.request.user)
    return qs
```

- 관리자면 전체 주문을 조회 가능
    
- 일반 사용자는 자신의 주문만 조회 가능
    
- `GET /orders/`, `GET /orders/1/` 등에서 이 제한이 항상 적용됨


##### ✅ 요약 표

|메서드|역할|핵심 설명|
|---|---|---|
|`get_queryset()`|조회 권한 분리|일반 유저는 자신의 주문만|
|`get_serializer_class()`|직렬화기 분기|생성 시에만 `OrderCreateSerializer` 사용|
|`perform_create()`|생성 시 유저 자동 지정|POST 요청 시 `user` 필드 자동 주입|
|`queryset + prefetch_related`|성능 최적화|N+1 문제 방지|


##### ✅ 실제 사용 흐름 예

1. **POST /orders/**
    
    - 요청 바디에 `items`, `status`만 전달
    - `OrderCreateSerializer` 사용        
    - `perform_create()`로 현재 유저 자동 저장
        

2. **GET /orders/**
    
    - 일반 유저는 자신의 주문만        
    - 관리자면 전체 주문 조회 가능
    - 필터셋으로 검색도 가능 (`?status=pending`)






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
	"order_id": "f6bb0c03-85d4-4315-b4a3-ea5ff7cf309a",
	"user": 2,
	"status": "Pending",
	"items": [
		{
			"product": 1,
			"quantity": 2
		},
		{
			"product": 3,
			"quantity": 1
		}
	]
}
```

---

### 7. 요약

- 중첩 객체를 함께 생성하려면 `create()` 메서드를 오버라이딩해야 함
- POST 요청 시 전용 serializer 사용
- 관련 필드는 `pop()` 후 루프 돌며 관련 모델 인스턴스 생성
- `perform_create()`로 인증된 사용자 자동 설정


### 8. 유사 프로젝트 및 개발 방법

`OrderCreateSerializer`처럼 **중첩 객체 생성 + 커스텀 로직이 들어간 Serializer**는 보기엔 간단하지만,  
실제로 **처음부터 빈 손으로 만들라고 하면 막막해지는** 아주 대표적인 예입니다.

🔍 왜 만들기 어려울까?

1. **`nested serializer` + `create()` 오버라이드** 조합이 생소함  
    → DRF 기본 CRUD만 쓰다 보면 중첩 객체 직접 만드는 경험이 드묾.
    
2. **`validated_data.pop('items')` 같은 구조**를 떠올리기 어렵다  
    → 중첩 필드를 따로 꺼내 처리해야 한다는 감각은 실습 없이는 잘 안 잡힘.
    
3. **중첩된 객체를 DB에 직접 연결하는 구조**를 코드로 옮기기 쉽지 않음  
    → `OrderItem.objects.create(order=order, **item)` 이런 코드 구조가 익숙하지 않으면 어렵게 느껴짐.
    
4. **직렬화 구조는 보기 쉽지만, 반대로 구성은 난이도↑**  
    → 특히 중첩 쓰고, `user`는 read_only로 처리하고, UUID까지 다루는 건 고급 패턴.


#### ✅ 어떻게 익숙해질 수 있을까?

> "중첩 Serializer 만들기"는 **2~3번만 실습**해보면 그때부터 **머리에 구조가 확실히 박힙니다.**

예를 들어, 이런 프로젝트에서 다시 써볼 수 있어요:

- 게시글 + 이미지 여러 개 업로드 (`PostSerializer` + `ImageSerializer`)
    
- 설문지 + 질문 항목들 (`SurveySerializer` + `QuestionSerializer`)
    
- 주문 + 주문 상세 (`OrderCreateSerializer`처럼)



```python
class ParentCreateSerializer(serializers.ModelSerializer):
    class ChildCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Child
            fields = [...]

    children = ChildCreateSerializer(many=True)

    def create(self, validated_data):
        children_data = validated_data.pop('children')
        parent = Parent.objects.create(**validated_data)
        for child in children_data:
            Child.objects.create(parent=parent, **child)
        return parent

```

이 구조만 기억해두면, 대부분의 중첩 생성 API는 다시 만들 수 있습니다.




> 다음 강의에서는 ViewSet 내부에서 `update()` 메서드를 활용한 중첩 객체 수정 전략을 다룹니다.

