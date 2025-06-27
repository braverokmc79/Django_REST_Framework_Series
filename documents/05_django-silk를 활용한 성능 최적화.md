
## 05-django-silk를 활용한 성능 최적화
[![05 - django-silk를 활용한 성능 최적화](https://img.youtube.com/vi/OG8alXR4bEs/0.jpg)](https://youtu.be/OG8alXR4bEs?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 1. 개요

Django REST Framework나 다른 백엔드 프레임워크를 사용할 때, 데이터베이스 쿼리를 최대한 최적화하는 것이 중요합니다. 이는 API의 전반적인 성능을 향상시키고 응답 속도를 빠르게 만듭니다.

 `django-silk`라는 툴을 사용하여 SQL 쿼리와 HTTP 요청을 분석하고 최적화하는 방법을 설명합니다. 이 도구는 개발 환경에서 성능 병목지점을 파악하는 데 매우 유용합니다.

---

### 2. django-silk란?

- GitHub에서 42,000개 이상의 스타를 받은 실시간 프로파일링 및 분석 도구
    
- HTTP 요청 및 DB 쿼리를 가로채고 기록한 뒤 웹 인터페이스를 통해 확인 가능
    

---

### 3. 설치 및 설정

```bash
pip install django-silk
```

`settings.py`에 다음 내용 추가:

```python
INSTALLED_APPS += ['silk']

MIDDLEWARE += ['silk.middleware.SilkyMiddleware']
```

> 주의: `GZipMiddleware`보다 뒤에 위치하면 인코딩 에러 발생 가능

drf_course/urls.py` 설정:

```python
from django.urls import path, include
urlpatterns += [
    path('silk/', include('silk.urls', namespace='silk')),
]
```

마이그레이션 실행:

```bash
python manage.py migrate
```

서버 실행 후 `/silk/` 경로에서 silk 대시보드 접속 가능

```bash
python manage.py runserver
```

http://127.0.0.1:8000/silk/

---

### 4. API 성능 분석 예시


  1) http://127.0.0.1:8000/products/ 요청 후   http://127.0.0.1:8000/silk/  요청

#### ✅ products 엔드포인트

- `/products` 요청 시 1개의 SQL 쿼리만 실행됨
- 응답 시간: 약 138ms
- 매우 효율적인 상태로 추가 최적화 필요 없음
    
#### ⚠️ orders 엔드포인트

1)   http://127.0.0.1:8000/orders/  요청 후   http://127.0.0.1:8000/silk/   요청


- `/orders` 요청 시 무려 19개의 쿼리 발생
    
- 그 이유는 각 주문(`Order`)에 대한 하위 항목(`OrderItem`)과 제품(`Product`)을 반복적으로 개별 조회하기 때문
    
- 일명 **N+1 문제** 발생 사례
    

---

### 5. 쿼리 최적화: `prefetch_related()` 사용

기존 코드:

```python
orders = Order.objects.all()
```

최적화 코드:

```python
orders = Order.objects.prefetch_related('items__product')
```

- `items`: `OrderItem`에 대한 related_name
    
- `product`: `OrderItem`이 참조하는 외래키 필드
    
- 위와 같이 중첩 prefetch로 한 번에 관련 테이블 데이터를 가져올 수 있음


Clear DB 호출 후  :   `/orders`   -- > silk/ 호출

](http://127.0.0.1:8000/silk/cleardb/)


결과:

- 쿼리 수: 19 → 3으로 감소
    
- 응답 시간: 92ms → 57ms로 단축
    

---

### 6. 추가 팁

- `prefetch_related()` 뒤에 `.all()`은 생략해도 됨
    
- 쿼리 결과가 동일하고 성능도 유지됨
    
- 실서비스에서 많은 수의 주문/상품 데이터를 다룰 때 효과적

```python
orders = Order.objects.prefetch_related('items__product')

```

는 **N+1 문제를 해결**하기 위해 **`prefetch_related()`**를 사용하는 방식입니다. 의미를 단계별로 설명드리면 다음과 같습니다.


#### 전체 구조 설명

- `Order`: 주문 모델
    
- `items`: 주문이 가진 **다대일 또는 일대다 관계**의 related name (예: `OrderItem` 모델에서 `ForeignKey`로 연결되어 있는 경우)
    
- `product`: 각 `OrderItem`이 연결한 상품 (예: `Product` 모델)

#### 🚩 이 코드의 의미

`Order` 객체를 가져올 때,

1. **관련된 `items` (예: 주문 상품들)** 도 미리 가져오고
    
2. 그 `items` 안에 있는 **`product` 객체들 (상품 정보)** 도 **미리 캐싱**해서 가져오겠다는 뜻입니다.
    
즉, 아래와 같은 관계가 있을 때:


```python
class Order(models.Model):
    # 주문 관련 필드들

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Product(models.Model):
    # 상품 관련 필드들

```

다음과 같은 접근이 있을 때:

```python
for order in orders:
    for item in order.items.all():
        print(item.product.name)

```

이렇게 중첩된 `.all()`과 `.product` 접근이 발생할 경우, `N+1 쿼리` 문제가 생길 수 있습니다.  
이를 방지하기 위해 `prefetch_related('items__product')`를 사용하여 **미리 다 가져오는 방식**입니다.


#### 🔧 정리

- `select_related`: **ForeignKey 또는 OneToOneField**를 따라 **JOIN으로 한 번에 가져옴** (SQL JOIN)
    
- `prefetch_related`: **ManyToManyField나 reverse ForeignKey** (1:N 등)에서 **여러 쿼리로 미리 캐시**

#### ✅ 결론

```python
orders = Order.objects.prefetch_related('items__product')
```

이 코드는,

> 주문 목록을 불러오면서, 관련된 주문 항목들과 그 주문 항목이 참조하는 상품까지 **미리 쿼리해서 캐싱**해두는 코드입니다.  
> 이를 통해 성능을 높이고 불필요한 DB 접근을 줄입니다.


#### ✅ 문법 구조 설명

```python
'items__product'

```

- `items`: `Order` 모델과 연결된 **related name** (예: `OrderItem`의 `order = ForeignKey(Order, related_name='items')`)
    
- `__`: (언더스코어 두 개) → 관계를 **계속 따라 들어갈 때** 사용
    
- `product`: `OrderItem` 모델에 있는 `ForeignKey` 필드
    
즉,   **Order → OrderItem → Product**  
이렇게 **1:N → N:1** 관계를 타고 들어가는 경로를 `__` (더블 언더스코어)로 이어준 것입니다

🔄 예시 모델 구조

```python
class Order(models.Model):
    ...

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=100)

```

🎯 사용 예시

```python
orders = Order.objects.prefetch_related('items__product')

```

이렇게 하면, 다음 코드에서 **DB 쿼리를 최소화**할 수 있습니다:

```python
for order in orders:
    for item in order.items.all():         # 이미 prefetch됨
        print(item.product.name)           # 여기도 prefetch됨

```

📌 정리

| 표현                                   | 의미                                             |
| ------------------------------------ | ---------------------------------------------- |
| `A__B`                               | A를 통해 B로 접근 (관계 타고 들어감)                        |
| `__` (언더스코어 두 개)                     | 관계를 이어주는 Django ORM 문법                         |
| `prefetch_related('items__product')` | Order → OrderItem → Product로 관계를 타고 들어가서 미리 쿼리 |


#### ✅ select_related  와 prefetch_related  핵심 차이 요약

|항목|`select_related`|`prefetch_related`|
|---|---|---|
|사용 대상|`ForeignKey`, `OneToOneField`|`ManyToManyField`, 역방향 `ForeignKey`|
|쿼리 방식|**JOIN**으로 한 번의 SQL 쿼리|여러 개의 쿼리를 실행하고 **파이썬에서 조합**|
|성능|일반적으로 더 빠르고 효율적|약간 느릴 수 있지만 더 유연|
|관계 방향|**정방향 (모델 내부 필드)**|**역방향 (related_name 등)** 또는 M2M|


##### 🔍 각각 설명
1. `select_related` — SQL JOIN으로 가져옴

```python
orders = OrderItem.objects.select_related('product')

```

- `OrderItem`에서 `product`는 `ForeignKey`이므로 `select_related` 사용 가능
    
- SQL에서 **JOIN**으로 한 번에 가져옴

	→ **쿼리 수가 1개**

🔽 사용 예:

```python
for item in orders:
    print(item.product.name)  # product가 JOIN 되어 이미 로딩됨

```


2. `prefetch_related` — 별도 쿼리 + 파이썬에서 조합

```python
orders = Order.objects.prefetch_related('items__product')

```
- `Order` → `OrderItem` (역방향, 즉 related_name) → `Product` 관계
    
- JOIN이 불가능하므로 **여러 쿼리를 날린 후 파이썬에서 조합**
    
- → **쿼리 수가 N+1 대신 2~3개**

🔽 사용 예:

```python
for order in orders:
    for item in order.items.all():
        print(item.product.name)  # 이미 prefetch된 product 사용

```


📌 언제 어떤 걸 써야 하나?

| 상황                                        | 추천                                       |
| ----------------------------------------- | ---------------------------------------- |
| 정방향 `ForeignKey`나 `OneToOneField`         | `select_related`                         |
| 역방향 관계 (related_name, related_query_name) | `prefetch_related`                       |
| `ManyToManyField` 포함된 경우                  | `prefetch_related`                       |
| 한 단계 관계만 최적화하면 되는 경우                      | `select_related('author')` 등             |
| 여러 단계 또는 중첩 관계                            | `prefetch_related('comments__author')` 등 |

##### 🧠 한 줄 요약

- `select_related`는 **JOIN으로 빠르게 가져옴** (단, **정방향** 전용)
    
- `prefetch_related`는 **여러 쿼리로 가져와서 파이썬에서 조합** (복잡한 관계에 유리)




---

### 7. 마무리

- `django-silk`는 API 개발 중 성능 병목을 쉽게 찾아내는 강력한 도구입니다.
    
- ORM 쿼리를 분석하여 `select_related` 또는 `prefetch_related`로 성능을 높일 수 있습니다.
    
- 실시간 인터페이스를 통해 요청 및 쿼리의 성능 데이터를 확인할 수 있어 매우 실용적입니다.
    

다음 강의는 함수형 뷰에서 클래스 기반 뷰(Generic Views)로 넘어가는 내용을 다룰 예정입니다.