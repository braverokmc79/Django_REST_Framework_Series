## Django REST Framework(DRF) - 설정과 모델 구성

### 1. 개요

이번 시리즈에서는 Django에서 가장 인기 있는 API 구축 도구인 \*\*Django REST Framework(DRF)\*\*를 처음부터 끝까지 단계별로 다루게 됩니다. 이 영상에서는 DRF의 전반적인 개요와 함께, API에 필요한 기본 모델(Product, Order, OrderItem, User)을 정의합니다.

---

### 2. REST API 구성 계획

이번 시리즈에서 만들 API는 다음 기능들을 포함합니다:

- 상품 조회 및 상세 보기
- 상품 생성, 수정, 삭제
- 주문 생성 및 조회
- 사용자 인증 및 권한 설정

시리즈 전반에서는 다음과 같은 DRF의 핵심 개념들을 다룰 예정입니다:

- Request, Response 객체
- 함수형/제너릭/클래스 기반 뷰
- ViewSet
- Serializer
- 인증(Authentication), 권한(Permission)
- 캐싱, 페이징, 필터링
- 테스트 코드 작성 등

---

### 3. 모델 구성 개요

이 API는 총 4개의 주요 모델을 기반으로 구성됩니다:

- `Product`: 상품
- `Order`: 주문
- `OrderItem`: 상품과 주문 사이의 연결 테이블
- `User`: 사용자 모델(커스텀 User 모델 사용)

아래는 `django-extensions`의 `graph_models` 명령어로 생성한 ERD(Entity Relationship Diagram)입니다. 이 구조를 바탕으로 모델을 생성합니다.

---

### 4. 모델 생성 과정

#### 1) User 모델

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```

기본 `AbstractUser`를 상속받아 향후 확장을 고려한 사용자 모델을 정의합니다.

`settings.py`에 다음을 추가해야 합니다:

```python
AUTH_USER_MODEL = 'api.User'
```

#### 2) Product 모델

```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name
```

#### 3) Order 모델

```python
import uuid

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
```

#### 4) OrderItem 모델

```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
```

---

### 5. 마이그레이션 적용 및 DB 생성

```bash
python manage.py makemigrations
python manage.py migrate
```

SQLite 데이터베이스에 테이블이 생성되며, `Django SQLite Explorer`로 확인 가능합니다.

---

### 6. 더미 데이터 삽입 (populate\_database 커맨드)

`manage.py`에 있는 커스텀 커맨드인 `populate_database`를 실행하면 다음과 같은 데이터가 자동 삽입됩니다:

- 테스트 사용자 1명
- 무작위 상품 여러 개
- 무작위 주문 3개
- 각 주문마다 2개의 상품을 포함한 `OrderItem`

```bash
python manage.py populate_database
```

데이터베이스를 확인하면 각 테이블이 잘 채워져 있고, 상품-주문 간 다대다 관계도 연결되어 있음을 확인할 수 있습니다.

---

### 7. ERD 시각화 도구

`django-extensions`의 `graph_models` 명령어를 이용해 ERD를 생성할 수 있습니다:

```bash
python manage.py graph_models api > models.dot
```

생성된 `.dot` 파일을 [Graphviz Online](https://edotor.net) 등에 붙여넣으면 ER 다이어그램을 시각화할 수 있습니다.

---

### 8. 마무리 및 다음 영상 예고

이제 모델 구성이 완료되었으며, 다음 영상에서는 DRF의 핵심 기능인 **Serializer**를 학습합니다. Serializer는 Django 모델/쿼리셋을 JSON으로 직렬화하거나, JSON 데이터를 유효성 검사 후 모델 인스턴스로 변환하는 데 사용됩니다.

---

> 다음 영상: DRF에서 Serializer의 개념과 역할 알아보기

