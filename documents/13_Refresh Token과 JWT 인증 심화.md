
## 13-Refresh Token과 JWT 인증 심화
[![13 - Refresh Token과 JWT 인증 심화](https://img.youtube.com/vi/H3OY36wa7Cs/0.jpg)](https://youtu.be/H3OY36wa7Cs?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



---


### 1. 개요
이번 강의는 이전에 구성한 JWT(Json Web Token) 인증의 **Refresh Token** 사용법과 **JWT 인증 설정 커스터마이징**에 대해 다루는 짧은 심화편입니다.

---

### 2. JWT 인증 흐름 복습
- `/api/token/` 경로에 POST 요청 → access token + refresh token 응답
- access token은 만료 시간이 있음 → 만료 후 재사용 불가
- refresh token은 비교적 긴 유효기간을 가짐 → 새로운 access token 발급에 사용됨

---

### 3. Refresh Token을 이용한 access token 갱신

`/api/token/refresh/` 경로로 POST 요청 시, 새로운 access token이 발급됩니다.

#### 요청 예시 (api.http 파일에서):
```http
POST http://localhost:8000/api/token/refresh/ HTTP/1.1
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

- 이 요청은 access token이 만료된 경우에도 유효한 refresh token만 있다면 새로운 access token을 발급합니다.
- 새로 발급된 access token은 다시 Authorization 헤더에 넣어 API 요청에 사용 가능

---

### 4. simplejwt 기본 설정 및 변경 옵션
`djangorestframework-simplejwt` 패키지는 다양한 설정을 제공합니다.

#### 주요 설정 항목:
```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),   # 액세스 토큰 유효 시간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),      # 리프레시 토큰 유효 시간
    'ALGORITHM': 'HS256',                             # 토큰 서명 알고리즘
    'SIGNING_KEY': SECRET_KEY,             #서명에 사용할 키 (보통 Django SECRET_KEY)
    'AUTH_HEADER_TYPES': ('Bearer',)  #인증헤더타입 (예:Authorization: Bearer<token>)
}

```

- 기본적으로 access token은 5분, refresh token은 1일 유효
- 설정을 통해 유효시간을 늘리거나 줄일 수 있음
- 서명 키, 인코딩 알고리즘, 인증 헤더 형식 등도 변경 가능

---

### 5. 커스터마이징 포인트
- 설정 파일에서 Token View에 사용할 serializer 교체 가능
- 토큰 payload 구조를 커스터마이징하려면 custom serializer 작성 가능
- 추가적인 클레임(claim)을 넣고 싶다면 `TokenObtainPairSerializer`를 상속 받아 오버라이딩

✅ 1) drf_course/auth_serializers.py
```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        print("✅ CustomTokenObtainPairSerializer.validate()  :", data)

        # 추가 정보도 넣을 수 있음
        return data
```


✅ 2) drf_course/custom_token_view.py
```python
from rest_framework_simplejwt.views import TokenObtainPairView
from .auth_serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

✅  3) drf_course/urls.py
```python
from django.urls import path
from .custom_token_view import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

```

### 정리

- 커스텀 시리얼라이저와 뷰를 새로 만든 뒤
    
- `urls.py`에서 해당 뷰를 등록하면 끝!
    

이 방법이 가장 깔끔하고 유지보수에도 좋아요.


---

### 6. 정리
- JWT 인증에서 access token은 짧은 수명을 갖고, refresh token은 재발급을 위한 용도로 사용됨
- `/api/token/refresh/`를 이용해 access token 재발급 가능
- `simplejwt`는 다양한 설정을 통해 인증 시스템을 유연하게 조정 가능
- 

> 다음 강의에서는 Update 및 Delete API 구현을 실습하며 권한 설정이 실제로 어떻게 작동하는지 확인합니다.

