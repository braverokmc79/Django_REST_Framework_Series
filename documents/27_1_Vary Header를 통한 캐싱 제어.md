
## 27-Vary Header를 통한 캐싱 제어


[27 - Vary 헤더로 캐시 제어](https://youtu.be/iUn8go-XZNw?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



---

### 1. 개요

이번 강의에서는 Django 및 Django REST Framework(DRF) 환경에서 **Redis를 캐시 백엔드로 활용하는 방법**과 함께, **Vary Header를 이용해 인증 사용자별로 다른 응답 캐싱을 구현하는 방식**을 학습합니다. 캐싱된 데이터가 인증된 사용자마다 다르게 유지되어야 하는 경우, 이를 해결하는 핵심 방법을 다룹니다.

---

### 2. Redis 캐시 서버 구성

- Redis는 **인메모리 기반 Key-Value 저장소**이며, 빠른 응답을 요구하는 API 캐싱에 적합합니다.
- Docker 명령어로 Redis 컨테이너 실행:

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

### 3. 사용자별 캐싱 문제점

- 동일한 URL(`/orders/`)로 요청해도 사용자에 따라 반환되는 주문 목록이 달라야 함
- 단순히 `@cache_page`만 사용하면 최초 요청자의 응답이 캐시되어, 다른 사용자가 같은 URL에 접근해도 동일한 결과를 받게 되는 문제가 발생함

---

### 4. Vary Header로 해결하기

- Django의 `patch_vary_headers()` 또는 `@vary_on_headers()` 데코레이터를 사용하면 캐시 키에 요청 헤더 값을 포함시킬 수 있음

```python
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 15), name='list')
@method_decorator(vary_on_headers(['Authorization']), name='list')
class OrderViewSet(viewsets.ModelViewSet):
    ...
```

- `Authorization` 헤더를 기준으로 캐시를 분리하여 사용자마다 다른 캐시가 유지됨

---

### 5. Redis 캐시 무효화 (개별 사용자 캐시 삭제가 어려운 이유)

- JWT 토큰은 주기적으로 변경되므로 매번 다른 캐시 키 생성
- Django Signals에서 요청 객체를 참조할 수 없기 때문에, `Authorization` 기반 캐시 키를 직접 삭제하는 것이 어렵습니다

#### 해결 방안 (선택적)

- 사용자 ID를 포함한 prefix 기반 캐시 키 구성 → 특정 사용자의 캐시만 삭제 가능
- 예:

```python
cache.delete_pattern(f"*order_list:{user.pk}*")
```

> 단, 이를 위해선 캐시 키 생성 시에 사용자 ID를 포함시켜야 합니다

---

### 6. Redis CLI로 캐시 확인 및 삭제

```bash
docker exec -it django-redis redis-cli
select 1
keys *
flushdb   # 전체 삭제 시
```

---

### 7. 요약

- 사용자 인증 정보에 따라 캐시를 분리하지 않으면 잘못된 데이터가 반환될 수 있음
- `@vary_on_headers(['Authorization'])`를 사용하면 사용자별 응답을 각각 캐시 가능
- Redis 키 전략과 무효화 방법은 JWT 구조, 만료 시간, 프로젝트 특성에 맞게 설계 필요

> 다음 강의에서는 조건부 요청(If-Modified-Since, ETag 등)을 이용한 고급 캐싱 전략을 다룹니다.

