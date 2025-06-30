## 26-Django & Redis - Vary Header를 통한 캐싱 제어
[![26 - Django & Redis - Vary Header를 통한 캐싱 제어](https://img.youtube.com/vi/5W2Yff00H8s/0.jpg)](https://youtu.be/5W2Yff00H8s?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



---

### 1. 개요

이번 강의에서는 Django 및 Django REST Framework(DRF) 환경에서 **Redis를 캐시 백엔드로 활용하는 방법**과 함께, **Vary Header를 이용해 URL 단위가 아닌 조건별로 캐싱을 다르게 처리하는 방식**을 학습합니다. 
특히 API의 응답이 인증 여부나 쿼리 파라미터에 따라 달라질 경우 효과적으로 대응할 수 있습니다.

---

### 2. Redis 캐시 서버 구성

- Redis는 **인메모리 기반 Key-Value 저장소**이며, 빠른 응답을 요구하는 API 캐싱에 적합합니다.
- Docker 명령어로 Redis 컨테이너를 띄움:

```bash
docker run --name django-redis -d -p 6379:6379 redis
```

---

##### ✅ 이제 Redis에 접속해보세요

###### ▶ 방법 1: 컨테이너 내부 Redis CLI 접속

```bash
 docker exec -it django-redis redis-cli
```

들어가면 다음처럼 나올 겁니다:

```makefile
127.0.0.1:6379>
```

그리고 간단한 테스트:

```redis
set hello "world"
get hello
```

정상이라면 결과는:
```nginx
OK
"world"
```


###### ▶ 방법 2: Windows에서 Redis 클라이언트 툴 사용

`RedisInsight`, `Medis`, 또는 `redis-cli`가 로컬에 설치되어 있다면:

- **Host**: `localhost`
    
- **Port**: `6379`
    
으로 접속하면 됩니다.



---


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


1️⃣ 예)

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

2️⃣ 적용)

```python

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]

    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = None
  

    @method_decorator(cache_page(60 * 15, key_prefix='product_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()    

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

```

##### ✅ `cache_page(60 * 15)`
- **15분(900초) 동안 캐시** 유지
- 즉, 같은 요청이 15분 이내에 다시 들어오면 DB 접근 없이 이전 응답을 그대로 리턴
    

##### ✅ `key_prefix='product_list'`
- 캐시 키 앞에 붙는 접두사
- 기본적으로 캐시는 요청 경로(URL), 쿼리스트링, 언어 코드 등을 조합해 키를 만들기 때문에, `key_prefix`는 **해당 API의 캐시 범위를 식별**하는 데 사용
    

##### ✅ `method_decorator` 사용 이유
- `ListCreateAPIView`의 `list()`는 클래스 메서드이므로 일반적인 `@cache_page` 데코레이터로 바로 적용이 안 됨
- 그래서 `method_decorator`로 감싸서 **클래스 기반 뷰의 특정 메서드(list)** 에만 캐시 적용



#### ⚠️ 주의사항

1. **POST 요청에는 캐시 안 됨**  
    `list()`는 GET 요청에만 사용되므로, POST 요청 시엔 캐시 영향 없음.
    
2. **쿼리 파라미터에 따라 캐시가 분리됨**  
    예를 들어:  
    - `/api/products/` → 캐시 A
        
    - `/api/products/?search=mouse` → 캐시 B
        
    - 서로 다른 키로 저장됨
    
3. **캐시 무효화는 수동**
    - 예: 새 상품을 등록해도 기존 GET 결과가 캐시되어 반영되지 않음
        
    - 해결: 상품 등록(POST) 후 `cache.delete_pattern()` 등을 이용해 관련 캐시 삭제 필요


#### 🧠 요약

- 이 코드는 `GET /products/` 요청에 대해 15분 동안 결과를 **캐시**함
  
- **성능 향상**에 유리하지만, 캐시 무효화 처리도 고려해야 함 (특히 POST/PUT 후)
    
- `key_prefix`는 같은 URL이더라도 **캐시 충돌을 피하기 위한 고유 접두사**






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

#### ✅ 캐시 무효화 설정

|항목|설명|
|---|---|
|signals.py 작성|✅ 필요|
|signals.py 임포트 설정|✅ 꼭 필요 (`apps.py` → `ready()`에서 import)|
|settings.py 앱 등록|✅ 반드시 `apps.ProductsConfig`로 등록해야 작동|


#### 1) Django Signals 활용

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Product
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    제품이 생성, 업데이트 또는 삭제될 때 제품 목록 캐시를 무효화합니다.
    """
    print("제품 캐시 지우기")

    # Clear product list caches
    cache.delete_pattern('*product_list*')
```

- `cache.delete_pattern()`은 `django-redis` 전용 함수
- 제품 생성, 수정, 삭제 시 관련 캐시 자동 삭제됨

이 **시그널을 통한 캐시 무효화 방법은 실제로 매우 실용적이며, 자동으로 실행됩니다.**  
즉, 이 함수는 **url 호출이나 직접 트리거하지 않아도** `Product` 모델에서 `save()` 또는 `delete()`가 실행되면 **자동으로 호출**됩니다.



####  2) 앱 등록

```python
# api/apps.py

from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from . import signals  # 👈 꼭 추가해야 작동됨
```




#### 3) settings.py 등록 처리
```python
INSTALLED_APPS = [
  ...
    #'api',
    'api.apps.ApiConfig',  # ✅ 반드시 이렇게 클래스 경로로 지정해야 ready() 호출됨
    ...
]
```

`'api.apps.ApiConfig'`는 단지 `'api'` 앱을 **초기화할 때 사용할 설정 클래스**를 명시한 것뿐

이렇게 설정하면 Django는:

1. `api` 폴더를 앱으로 인식하고,
    
2. `api/apps.py` 내부에 정의된 `ApiConfig` 클래스를 사용하며,
    
3. 해당 앱의 **모델, 뷰, 시리얼라이저, URL 등 모든 요소**를 정상적으로 로드합니다.

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


#### ✅ `Vary` 헤더란?

`Vary` 헤더는 **HTTP 응답에서 캐시를 어떻게 구분해서 저장할지를 브라우저나 프록시에게 알려주는 헤더**입니다.

> 즉, "같은 URL이더라도, 어떤 **요청 헤더 값**에 따라 다른 응답을 줄 수 있다"고 알려주는 용도입니다.


##### 🧠 예시 1: `Accept-Language`

```http
GET /products/
Accept-Language: en

GET /products/
Accept-Language: ko

```

이 두 요청은 URL은 같지만, **언어**가 다릅니다.  
서버는 언어에 따라 다른 응답을 줄 수 있죠.

이때 Django 응답 헤더에 이렇게 지정합니다:


```
Vary: Accept-Language
```

👉 그러면 브라우저나 CDN은 `Accept-Language` 값이 다르면 **다른 캐시로 저장**합니다.


##### 🧠 예시 2: `Authorization` 또는 `Cookie`

```python
GET /products/
Authorization: Bearer xxxxxx
```

같은 URL이라도 로그인 상태/비로그인 상태에 따라 결과가 다를 수 있으니:

```python
Vary: Authorization
```

을 지정해주면 캐시 충돌 방지를 할 수 있어요.


##### ✅ Django에서 `Vary` 헤더 추가하는 방법

```python
from django.utils.cache import patch_vary_headers
from django.http import HttpResponse

def my_view(request):
    response = HttpResponse("hello")
    patch_vary_headers(response, ['Accept-Language'])  # 또는 ['Cookie'], ['Authorization']
    return response

```

또는 DRF/뷰셋에서:

```python
def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    patch_vary_headers(response, ['Accept-Language'])
    return response
```

##### ✅ 왜 중요하냐?

- `Vary`를 잘 안 쓰면, **다른 사용자에게 잘못된 캐시 데이터**가 전달될 수 있습니다.
    
- 특히 **인증, 언어, 기기(User-Agent)** 등에 따라 **응답이 달라질 수 있는 경우** 필수입니다.


##### ✅ 요약

|개념|설명|
|---|---|
|`Vary` 헤더|캐시를 요청 헤더에 따라 분기해서 저장하라고 브라우저/프록시에 지시|
|주요 사용 예시|`Accept-Language`, `Authorization`, `Cookie`, `User-Agent` 등|
|사용 목적|인증, 언어, 기기 상태 등에 따라 **올바른 캐시 분리** 보장|
|Django 적용|`patch_vary_headers(response, ['Header-Name'])`|


---

### 7. Redis CLI로 캐시 확인

```bash
docker exec -it django-redis redis-cli
select 1
keys *
```

```shell
(venv) >  docker exec -it django-redis redis-cli
127.0.0.1:6379> select 1
OK

127.0.0.1:6379[1]> keys *
1) ":1:views.decorators.cache.cache_page.product_list.GET.62e20cf4352907fd17b57aa6133d0293.52498d91dc09f347723aa735b400b2c8.ko-kr.Asia/Seoul"
2) ":1:views.decorators.cache.cache_header.product_list.62e20cf4352907fd17b57aa6133d0293.ko-kr.Asia/Seoul"

127.0.0.1:6379[1]>
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

