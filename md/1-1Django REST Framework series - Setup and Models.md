
## 🎥 본 강의 유튜브 링크

🔗 [https://youtu.be/6AEvlNgRPNc?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t](https://youtu.be/6AEvlNgRPNc?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

## ✨ Django REST Framework Series - 모델 구축 및 초기 데이터베이스 세팅

[![Watch on YouTube](https://img.youtube.com/vi/6AEvlNgRPNc/0.jpg)](https://youtu.be/6AEvlNgRPNc?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---




### 포함 목차

1. Django REST Framework 소개
    
2. 시작 코드 다운로드 및 환경 설정
    
3. 모델 구축
    
4. 커스텀 유저 모델 설정
    
5. ERD 단어구드 생성
    
6. 관리 명령어로 데이터베이스 채워기
    

---

### 강의 내용

현대 웹 개발에서 API를 만드는 일은 매우 일반적입니다. 이 시리즈에서는 가장 대중적인 Django용 API 프레임워크인 **Django REST Framework**를 사용하여 처음부터 끝까지 프로젝트를 진행합니다. 기존에 DRF를 개별적으로 소개한 영상들은 있었지만, 이번에는 전체 흐름을 따라가는 구조로 구성되었습니다.

우리가 만들 API는 **상품(products)**과 **주문(orders)**을 중심으로 하며, 이들을 통해 CRUD(Create, Read, Update, Delete) 작업을 REST API로 구현할 예정입니다.

---

### 시리즈 전체에서 다르는 개념

- `Request`와 `Response` 객체
    
- 다양한 DRF 제공 뷰(View), GenericView, ViewSet 등
    
- 핵심 개념인 `Serializer`
    
- `Validator`, 인증(Authentication), 권한(Permissions)
    
- 캐싱(Caching), 트래픽 제한(Throttling)
    
- 페이지네이션(Pagination), 필터링(Filtering)
    
- 테스트 코드
    

---

### 이 강의의 조명

이번 1강에서는 이 프로젝트에서 사용할 모델을 정의합니다.

- 핵심 모델: `Product`, `Order`, `OrderItem`
    
- ERD(Entity Relationship Diagram)를 사용해 관계를 시각화
    
- `Django Extensions`의 `graph_models` 명령어로 ERD 생성
    
- `populate_db`라는 커스텀 관리 명령어로 테스트용 더미 데이터 생성
    
- 가상 환경 설정, 필요한 패키지 설치까지 안내
    

---

### 가장 중요한 비고 사항

- 이번 영상에서는 프론트엔드는 전혀 사용하지 않습니다. React나 Vue 같은 클라이언트 앱을 만들지 않고, **오직 API 자체에만 집중**합니다.
    
- API 테스트는 VSCode 확장인 REST Client 등을 활용합니다.
    
- 깃허브에 제공된 [시작 코드](https://github.com/bugbytes-io/drf-course-api)를 클로드하여 개발을 시작합니다.
    

---

### 생성 할 모델 조건

- 커스텀 유저 모델: Django의 `AbstractUser`
    
- Product 모델: 이름, 설명, 가격, 재고, 이미지
    
- Order 모델: UUID 기본키, 유저 외래키, 생성일시, 주문 상태
    
- OrderItem: 주문-상품 중간 테이블, 수량 필드 포함
    
- 상태 필드는 Django의 `TextChoices`를 활용하여 열거형으로 구성
    

---

### 데이터베이스 채워보기

- `python manage.py populate_db`
    
- 더미 유저, 상품 4개, 주문 3개, 각각 주문에 2개의 상품 연결
    
- SQLite 데이터베이스에 실제 데이터 저장 여부 확인
    

---

### 공유한 ERD 생성방법

- Django Extensions의 `graph_models` 명령어를 실행:
    
    ```bash
    python manage.py graph_models api > models.dot
    ```
    
- 생성된 `.dot` 파일 내용을 [Graphviz Online](https://edotor.net/)에 붙여 넣어 ERD 확인 가능
    

---

### 다음 단계: Serializer

다음 강의에서는 **Serializer**에 대해 학습합니다. 모델 객체를 JSON으로 직렬화하거나, JSON을 받아 모델 인스턴스로 변환하는 과정에서 반드시 필요한 구성 요소입니다.




### 1. Django REST Framework 소개

- Django에서 API를 개발할 때 가장 놔노르 사용되는 패키지: `Django REST Framework`
    
- 본 시리즈에서는 **상품(Product)**, **주문(Order)**, **주문 상세(OrderItem)** 모델을 구축하고 이를 활용한 API CRUD를 개발함
    
- `Request`, `Response`, `ViewSet`, `Serializer`, `Authentication`, `Permissions`, `Pagination`, `Filtering`, `Throttling`, `Testing` 등 다양한 기능들을 시리즈 전체에서 다룰
    


---

### 2. 시작 코드 다운로드 및 환경 설정

- [Github 시작 코드](https://github.com/bugbytes-io/drf-course-api)
    
- 주요 패키지:
    
    ```bash
    Django
    djangorestframework
    django-extensions
    pillow
    ```
    
- 가상 환경 설정 및 필수 패키지 설치:
    
    ```bash
    python -m venv venv-drf
    source venv-drf/bin/activate
    pip install -r requirements.txt
    ```
    

---

### 3. 모델 구축: `models.py`

#### 커스텀 유저 모델

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```

#### Product 모델

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

#### Order 모델

```python
import uuid

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING'
        CONFIRMED = 'CONFIRMED'
        CANCELLED = 'CANCELLED'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    products = models.ManyToManyField('Product', through='OrderItem', related_name='orders')

    def __str__(self):
        return f"Order {self.id} by {self.user}"
```

#### OrderItem 모델

```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.order.id}"
```

---

### 4. 커스텀 유저 모델 설정

```python
# settings.py 내의 마지막에 추가
AUTH_USER_MODEL = 'api.User'
```

---

### 5. ERD 단어구드 생성

```bash
python manage.py graph_models api > models.dot
```

- [Graphviz Online](https://edotor.net/) 에 붙여\uub123으면 ERD 생성 가능
    

---

### 6. 관리 명령어로 데이터베이스 채워기

```bash
python manage.py populate_db
```

- 가상 유저, 상품, 주문, 주문개별 데이터 및 관계 형식으로 자동 생성
    

---




### 🔶 1. **User 모델 (`api_models_User`)**

- `AbstractUser`를 상속하여 확장된 사용자 모델입니다.
    
- 기본적으로 Django에서 제공하는 인증 필드를 포함합니다.

🔸 주요 필드

| 필드명                                     | 필드 타입         | 설명                     |
| --------------------------------------- | ------------- | ---------------------- |
| `id`                                    | BigAutoField  | 기본 키 (자동 생성)           |
| `username`                              | CharField     | 사용자명                   |
| `email`                                 | EmailField    | 이메일 주소                 |
| `password`                              | CharField     | 비밀번호 (해시 처리됨)          |
| `first_name` / `last_name`              | CharField     | 이름 / 성                 |
| `is_active`, `is_staff`, `is_superuser` | BooleanField  | 활성화 여부, 직원 여부, 슈퍼유저 여부 |
| `last_login`                            | DateTimeField | 마지막 로그인 시간             |
| `date_joined`                           | DateTimeField | 가입일자                   |


### 🔶 2. **Product 모델 (`api_models_Product`)**

- 판매되는 **상품** 정보를 담고 있는 모델입니다.
    
#### 🔸 주요 필드

| 필드명           | 필드 타입                | 설명     |
| ------------- | -------------------- | ------ |
| `id`          | BigAutoField         | 기본 키   |
| `name`        | CharField            | 상품명    |
| `description` | TextField            | 상품 설명  |
| `image`       | ImageField           | 상품 이미지 |
| `price`       | DecimalField         | 상품 가격  |
| `stock`       | PositiveIntegerField | 재고 수량  |


### 🔶 3. **Order 모델 (`api_models_Order`)**

- 사용자의 **주문** 정보를 저장합니다.
    
#### 🔸 주요 필드
| 필드명          | 필드 타입             | 설명                     |
| ------------ | ----------------- | ---------------------- |
| `order_id`   | UUIDField         | 주문 식별자 (고유 UUID)       |
| `user`       | ForeignKey → User | 주문자                    |
| `created_at` | DateTimeField     | 주문 생성 시간               |
| `status`     | CharField         | 주문 상태 (예: 결제완료, 배송중 등) |

### 🔶 4. **OrderItem 모델 (`api_models_OrderItem`)**

- 주문에 포함된 **상품 항목**들입니다.

🔸 주요 필드

|필드명|필드 타입|설명|
|---|---|---|
|`id`|BigAutoField|기본 키|
|`order`|ForeignKey → Order|어떤 주문에 속한 항목인지|
|`product`|ForeignKey → Product|어떤 상품인지|
|`quantity`|PositiveIntegerField|수량|

### 🔁 관계 요약

- `User` ↔ `Order`: **1:N 관계** (사용자는 여러 주문 가능)
    
- `Order` ↔ `OrderItem`: **1:N 관계** (주문에는 여러 상품 항목이 있음)
    
- `OrderItem` ↔ `Product`: **N:1 관계** (여러 주문 항목이 하나의 상품 참조)






### 다음 단계

- 다음 강의에서는 `Serializer`를 통해 모델 데이터를 JSON으로 지렬화하는 방법을 합니다.
    
- `serializers.py` 파일을 구성하고, 응답에 드림을 수집하는 방법을 합니다.







