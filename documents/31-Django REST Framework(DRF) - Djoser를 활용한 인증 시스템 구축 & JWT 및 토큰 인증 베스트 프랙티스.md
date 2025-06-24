이번 문서에서는 Django REST Framework(DRF) 기반의 API 애플리케이션에 인증 시스템을 구축하는 방법을 [Djoser](https://djoser.readthedocs.io/en/latest/)를 활용하여 정리해보겠습니다. 토큰 기반 인증(Token Authentication)과 JSON Web Token(JWT)을 활용한 인증 방식 모두를 살펴보며, 공식 문서와 실전 적용 사례를 바탕으로 구성합니다.

## 1. Djoser란?

Djoser는 Django의 기본 인증 시스템을 RESTful 방식으로 제공하는 라이브러리입니다. React, Vue.js, React Native 등 SPA(Single Page Application) 프론트엔드와 Django 백엔드 간 인증 처리를 쉽게 해주는 패키지입니다. 

### 제공 기능
- 회원가입 / 로그인 / 로그아웃
- 비밀번호 초기화 / 변경
- 이메일 인증
- 토큰 기반 인증 및 JWT 인증
- 소셜 로그인 지원

## 2. 설치 및 기본 설정

### 1단계. 필수 패키지 설치
```bash
pip install djoser djangorestframework djangorestframework-simplejwt django-cors-headers
```

### 2단계. settings.py 설정
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# CORS 허용 설정 (React 개발 서버 기준)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

# 인증 클래스 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # 또는 'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
}

# 이메일 콘솔 출력
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 3단계. URL 설정
```python
from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),  # 토큰 인증
    path('auth/', include('djoser.urls.jwt')),       # JWT 인증
]
```

## 3. 인증 방식 비교 및 사용

### ✅ 토큰 인증 (Token Authentication)
- `/auth/token/login/`: 로그인, 토큰 반환
- `/auth/token/logout/`: 로그아웃 (DB에서 토큰 삭제)
- `/auth/users/me/`: 로그인한 사용자 정보 조회

#### 장점
- 설정 간단, 사용 편리
- 서버 측에서 토큰을 저장하므로 토큰 취소가 용이

#### 단점
- DB 쿼리가 매 요청마다 필요 (토큰 유효성 확인 시)

### ✅ JWT 인증 (Simple JWT)
- `/auth/jwt/create/`: 로그인, access/refresh 토큰 반환
- `/auth/jwt/refresh/`: refresh 토큰으로 access 토큰 갱신
- `/auth/jwt/verify/`: 토큰 유효성 검증

#### 장점
- 무상태 인증 방식 (stateless): 매 요청마다 DB 조회 불필요
- 성능 향상, 확장성 우수

#### 단점
- 토큰 만료 전까지 수동 로그아웃 어려움 (Blacklist 필요 시 DB 설정 필요)

### ✅ 인증 요청 예시 (JWT)
```http
POST /auth/jwt/create/
Content-Type: application/json

{
  "username": "admin",
  "password": "test"
}
```
응답:
```json
{
  "access": "...",
  "refresh": "..."
}
```
요청 헤더에 아래처럼 사용:
```
Authorization: JWT {access_token}
```

## 4. 커스터마이징

Djoser는 기본 제공되는 시리얼라이저를 오버라이드하여 사용자 정의 로직을 추가할 수 있습니다.
```python
DJOSER = {
    'SERIALIZERS': {
        'user': 'myapp.serializers.CustomUserSerializer',
    }
}
```
- 예: 사용자 등록 시 추가 필드 요구, 응답 형식 변경 등

## 5. 실전 적용 팁

- 클라이언트(React 등)는 로그인 후 받은 토큰을 localStorage/sessionStorage에 저장하고, 요청 시 Authorization 헤더에 첨부
- Access token 만료 시 Refresh token으로 재발급 → 401 처리 대응 로직 필요
- 로그아웃 시 토큰 제거 (Token 방식: 서버에서 삭제, JWT: 클라이언트에서 무효화 or Blacklist)

## 마무리

Djoser는 Django REST Framework에서 인증 기능을 빠르고 안전하게 구현할 수 있는 강력한 도구입니다. SPA와 백엔드 간 인증 연동을 단순화하며, 기본적인 인증 시나리오부터 JWT 기반 고급 인증까지 폭넓게 지원합니다.

더욱 자세한 내용은 [Djoser 공식 문서](https://djoser.readthedocs.io/en/latest/)를 참고하세요. 다음 문서에서는 React 프론트엔드와의 연동 예제를 다룰 예정입니다.

