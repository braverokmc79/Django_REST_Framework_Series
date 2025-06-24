## Django REST Framework(DRF) - Redis와 Vary Header를 통한 캐싱 동작 제어

### 1. 개요

이번 강의에서는 Django 및 Django REST Framework(DRF) 환경에서 **Redis를 캐시 백엔드로 활용하는 방법**과 함께, **Vary Header를 이용해 URL 단위가 아닌 조건별로 캐싱을 다르게 처리하는 방식**을 학습합니다. 특히 API의 응답이 인증 여부나 쿼리 파라미터에 따라 달라질 경우 효과적으로 대응할 수 있습니다.

---

### 2. Redis 캐시 서버 구성

- Redis는 **인메모리 기반 Key-Value 저장소**이며, 빠른 응답을 요구하는 API 캐싱에 적합합니다.
- Docker 명령어로 Redis 컨테이너를 띄움:

```bash
docker run --name django-redis -d -p 6379:6379 redis
```

- Python 클라이언트 설치:

```bash
pip install redis[hiredis] django-redis
```

- `settings.py`에 Redis 설정 추가:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

---

### 3. API 캐싱 구현 (cache\_page 데코레이터)

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 15, key_prefix="product_list"), name='list')
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

- `cache_page`는 해당 뷰의 응답을 일정 시간 동안 캐시함
- `key_prefix`를 지정하면 Redis 키 앞에 구분자를 붙일 수 있음
- 주의: 쿼리 파라미터(ordering 등)가 다르면 각각 캐시됨 (URL 전체가 키로 사용됨)

---

### 4. 성능 확인 예제

- `get_queryset()`에서 `time.sleep(2)` 삽입 → DB 접근 시간 시뮬레이션
- 첫 요청은 느리지만, 이후 캐싱된 응답은 즉시 반환

```python
import time

def get_queryset(self):
    time.sleep(2)
    return super().get_queryset()
```

---

### 5. 캐시 무효화 (Cache Invalidation)

#### Django Signals 활용

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product

@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, **kwargs):
    cache.delete_pattern("*:product_list:*")
```

- `cache.delete_pattern()`은 `django-redis` 전용 함수
- 제품 생성, 수정, 삭제 시 관련 캐시 자동 삭제됨

#### 앱 등록

```python
# apps.py

def ready(self):
    import yourapp.signals
```

---

### 6. Vary Header 적용

- 동일한 URL이라도 인증 여부나 사용자 정보에 따라 응답을 달리할 수 있음
- 이때 `Vary` 헤더를 설정하면 캐시도 조건별로 따로 유지됨

```python
from django.utils.cache import patch_vary_headers

class ProductListCreateAPIView(ListCreateAPIView):
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        patch_vary_headers(response, ['Authorization'])
        return response
```

- `Authorization` 헤더 기준으로 다른 캐시 생성됨
- 인증된 사용자와 비인증 사용자 캐시가 분리됨

---

### 7. Redis CLI로 캐시 확인

```bash
docker exec -it django-redis redis-cli
select 1
keys *
```

- 캐시된 키들을 직접 확인 가능
- `get <key>`로 캐시된 내용 조회

---

### 8. 요약

- Redis는 빠른 성능과 다양한 기능을 제공하는 캐시 백엔드
- `cache_page` 데코레이터로 API 캐시 적용 가능
- URL 기준 외에 `Vary` 헤더를 통해 조건별로 세분화된 캐싱 구현 가능
- Django Signals를 활용한 캐시 무효화 전략으로 실시간 데이터 반영

> 다음 강의에서는 조건부 요청(If-Modified-Since, ETag 등) 기반 캐싱 전략을 다룹니다.

