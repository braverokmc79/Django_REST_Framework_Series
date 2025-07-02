# Django DRF + SimpleJWT + Redis를 활용한 사용자별 JWT 인증 캐시 처리 방법

**목표:** 사용자별로 JWT 토큰 기반 Redis 캐시를 구성하고, 실시간 인증 캐시 처리 및 토큰 갱신 시 기존 캐시를 무효화하는 시스템을 구축합니다.

---

## ✅ 전체 흐름 요약

1. **JWT로 로그인 또는 인증** → Redis에 사용자 정보 캐싱
2. **요청 시 캐시 확인** → 있으면 캐시 응답, 없으면 DB 조회 후 캐싱
3. **JWT 갱신(refresh)** → 기존 토큰으로 된 캐시 제거 + 새 토큰으로 다시 캐싱

---

## ⚠️ 왜 기본 JWT 발급 방식으로는 캐시 무효화가 어려운가?

Django REST Framework + SimpleJWT에서는 기본적으로 다음과 같은 뷰를 제공합니다:

- `/api/token/` → `TokenObtainPairView`
- `/api/token/refresh/` → `TokenRefreshView`

이 기본 뷰들은 JWT 발급 및 재발급만 처리하며, **Redis 캐시 삭제나 사용자별 캐시 정리 등의 처리를 하지 않습니다.**

따라서 다음 두 가지 방식 중 하나로 처리해야 합니다:

### ✅ 방법 1: 기본 뷰를 직접 대체 (오버라이딩)

- `LoginView`, `RefreshTokenView`를 직접 만들고, 기존 URL을 우리가 만든 것으로 대체합니다.

```python
# urls.py
urlpatterns = [
    path("api/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", RefreshTokenView.as_view(), name="token_refresh"),
]
```

### ✅ 방법 2: 기본 뷰를 상속하고 일부만 오버라이딩

- `TokenObtainPairView` 또는 `TokenObtainPairSerializer`를 상속하여 Redis 캐시 처리를 추가하는 방식입니다.
- 아래처럼 `validate()`를 커스텀할 수 있습니다:

```python
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        access = data['access']
        cache_user_data(user.id, access, {'username': user.username})
        return data
```

---

## ⚙️ 주요 설정

### settings.py

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

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

## 🔧 Redis 캐시 유틸 함수 정의

### utils/jwt_cache.py

```python
from django.core.cache import cache

JWT_INDEX_KEY = "user_jwt_index:{user_id}"
JWT_CACHE_KEY = "order_list:user:{user_id}:{jwt}"

def get_jwt_cache_key(user_id, jwt):
    return JWT_CACHE_KEY.format(user_id=user_id, jwt=jwt)

def get_jwt_index_key(user_id):
    return JWT_INDEX_KEY.format(user_id=user_id)

def cache_user_data(user_id, jwt, data):
    cache_key = get_jwt_cache_key(user_id, jwt)
    index_key = get_jwt_index_key(user_id)
    
    cache.set(cache_key, data, timeout=60 * 15)
    cache.sadd(index_key, jwt)

def invalidate_user_cache(user_id):
    index_key = get_jwt_index_key(user_id)
    jwt_list = cache.smembers(index_key)
    for jwt in jwt_list:
        cache.delete(get_jwt_cache_key(user_id, jwt))
    cache.delete(index_key)
```

---

## 👤 로그인/토큰 갱신 View에서 Redis 캐시 제어

### views.py

```python
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils.jwt_cache import cache_user_data, invalidate_user_cache
from django.contrib.auth import authenticate

# ✅ 로그인 시 토큰 발급 + Redis 캐시 등록
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        user_data = {'username': user.username, 'email': user.email}
        cache_user_data(user.id, access_token, user_data)

        return Response({
            'access': access_token,
            'refresh': str(refresh),
        })

# ✅ 토큰 갱신 시 기존 캐시 무효화 + 새 토큰 캐시 등록
class RefreshTokenView(APIView):
    def post(self, request):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        user = token.user

        invalidate_user_cache(user.id)  # 기존 JWT 기반 캐시 삭제

        new_access = str(token.access_token)
        user_data = {'username': user.username, 'email': user.email}
        cache_user_data(user.id, new_access, user_data)

        return Response({
            'access': new_access
        })

# ✅ 사용자 인증 후 요청 처리 시 캐시 활용
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        jwt = request.auth  # 현재 요청의 JWT access token 문자열

        from .utils.jwt_cache import get_jwt_cache_key
        key = get_jwt_cache_key(user.id, jwt)
        cached_data = cache.get(key)
        if cached_data:
            return Response({"cached": True, "data": cached_data})

        order_data = get_orders_from_db(user)
        cache_user_data(user.id, jwt, order_data)

        return Response({"cached": False, "data": order_data})
```

---

## 📦 보조 함수 예시

```python
def get_orders_from_db(user):
    return [
        {"id": 1, "product": "노트북", "user": user.username},
        {"id": 2, "product": "마우스", "user": user.username},
    ]
```

---

## ✅ 정리

| 단계 | 처리 내용 |
|------|------------|
| 로그인 | access, refresh 토큰 발급 + 사용자 데이터 Redis 저장 |
| 요청 시 | access token으로 Redis 키 구성 → 캐시 확인 후 응답 |
| 토큰 갱신 | 기존 사용자 토큰 캐시 삭제 → 새 토큰 기준으로 재저장 |

이 구조를 통해, 토큰 기반 인증 캐시 무효화를 사용자 기준으로 안전하게 제어할 수 있으며, JWT가 자주 바뀌는 상황에서도 **캐시 충돌 없이 정확한 사용자 데이터 제공**이 가능합니다.

SimpleJWT를 사용할 때는 꼭 **기본 뷰를 오버라이드하거나, Serializer를 커스텀**해서 Redis 캐시 로직을 명시적으로 넣는 것이 핵심입니다.
