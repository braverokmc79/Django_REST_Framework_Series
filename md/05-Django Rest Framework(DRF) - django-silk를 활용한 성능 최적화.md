
## Django REST Framework(DRF) - django-silk를 활용한 성능 최적화

### 1. 도입

Django REST Framework나 다른 백엔드 프레임워크를 사용할 때, 데이터베이스 쿼리를 최대한 최적화하는 것이 중요합니다. 이는 API의 전반적인 성능을 향상시키고 응답 속도를 빠르게 만듭니다.

이번 영상에서는 `django-silk`라는 툴을 사용하여 SQL 쿼리와 HTTP 요청을 분석하고 최적화하는 방법을 설명합니다. 이 도구는 개발 환경에서 성능 병목지점을 파악하는 데 매우 유용합니다.

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
INSTALLED_APPS += ["silk"]

MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]
```

> 주의: `GZipMiddleware`보다 뒤에 위치하면 인코딩 에러 발생 가능

`urls.py` 설정:

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

---

### 4. API 성능 분석 예시

#### ✅ products 엔드포인트

- `/products` 요청 시 1개의 SQL 쿼리만 실행됨
- 응답 시간: 약 138ms
- 매우 효율적인 상태로 추가 최적화 필요 없음
    
#### ⚠️ orders 엔드포인트

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
    

결과:

- 쿼리 수: 19 → 3으로 감소
    
- 응답 시간: 92ms → 57ms로 단축
    

---

### 6. 추가 팁

- `prefetch_related()` 뒤에 `.all()`은 생략해도 됨
    
- 쿼리 결과가 동일하고 성능도 유지됨
    
- 실서비스에서 많은 수의 주문/상품 데이터를 다룰 때 효과적
    

---

### 7. 마무리

- `django-silk`는 API 개발 중 성능 병목을 쉽게 찾아내는 강력한 도구입니다.
    
- ORM 쿼리를 분석하여 `select_related` 또는 `prefetch_related`로 성능을 높일 수 있습니다.
    
- 실시간 인터페이스를 통해 요청 및 쿼리의 성능 데이터를 확인할 수 있어 매우 실용적입니다.
    

다음 영상에서는 함수형 뷰에서 클래스 기반 뷰(Generic Views)로 넘어가는 내용을 다룰 예정입니다.