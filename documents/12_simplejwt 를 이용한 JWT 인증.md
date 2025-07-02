
## 12-simplejwt 를 이용한 JWT 인증


[12 - simplejwt를 이용한 JWT 인증](https://youtu.be/Xp0-Yy5ow5k?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)




---

### 1. 개요

이번 강의에서는 Django REST Framework(DRF)에 **JWT(Json Web Token)** 인증을 추가하는 방법을 배웁니다. 클라이언트는 JWT를 Authorization 헤더에 담아 전송하고, DRF는 해당 토큰을 검증해 요청을 허용하거나 거부합니다.

---

### 2. 인증이란?

- 인증(Authentication)은 요청을 보낸 사용자가 누구인지 확인하는 절차입니다.
- DRF는 다양한 인증 방식을 지원하며, 사용자 정의 방식도 구현할 수 있습니다.
- 인증은 **모든 뷰의 가장 앞단에서 실행되며**, 이후 권한(Permission), 속도 제한(Throttling) 등의 로직이 이어집니다.

DRF 요청 객체에서는 다음 속성을 통해 인증 정보를 확인할 수 있습니다:

- `request.user`: 로그인된 사용자 객체 (User 인스턴스)
- `request.auth`: 인증 토큰 등의 추가 정보

---

### 3. 기본 인증 방식 설정

`settings.py`에 다음을 추가하여 기본 인증 방식을 설정합니다:

```python
  
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

- JWT 인증을 최우선으로 사용하고, 실패 시 세션 인증으로 대체
- Django Admin 사이트를 위해 `SessionAuthentication`은 유지


---

### 4. simplejwt 설치 및 설정

1. 패키지 설치:

```bash
pip install djangorestframework-simplejwt
```

2. JWT 관련 URL 패턴 추가 (`urls.py`):

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

### 5. JWT 토큰 발급 및 사용

##### 1)django 관리자 비번 변경

```bash
python manage.py changepassword admin
```

###### 단순 비번 변경방법 `settings.py`에서 아래 설정을 찾으세요:
```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_PASSWORD_VALIDATORS = []
```

AUTH_PASSWORD_VALIDATORS = [][] 빈리스트로 변경 하면 검증이 꺼집니다.


#### ✅ 2. 관리자 페이지에서 직접 변경

1. 로그인: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
    
2. 사용자(User) → 원하는 사용자 클릭
    
3. 비밀번호 변경 링크 클릭 → 새 비밀번호 입력 후 저장



---

###  🔖 **Insomnia 실행 후 임포트**

1. Insomnia 실행
    
2. 좌측 상단 메뉴 클릭 (예: **`+ Create`** 옆 아이콘 또는 앱 로고)
    
3. **Import / Export → Import Data → From File** 클릭
    
4. 저장한 `django_rest_collection.json` 선택
    

🖼️ 임포트 된 Insomnia

![임포트된 insomnia](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgTDlaGJd7QXeWxr-dR5ev_PwqS9mDlx2ihBrYjwT3tcgwP9Q06YHl-KLlNguN9-UK4UFXUYsRDiP7nRfldGdS_arJyjFsHiyRzF5TNof7VpaIbTPsyf5w63qj_QoKCfPQgANDi4anEQAgf2xIECHvAMDKU3g7JRGTZsovr79U6hHXKvratEqZIDEk0E9Us/w424-h640/2025-06-27%2014%2008%2038.png)



---

###### ✅ **1. Import 후 확인**

- 워크스페이스 이름이 **`Django_REST_Framework_Series`** 인 것이 보이면 성공입니다.
    
- `JWT - Get Token`, `GET - Product List` 등 여러 요청들이 함께 들어있습니다.

###### Tip: 자동 토큰 저장 스크립트 사용 방법

`JWT - Get Token` 요청의 **Test 탭 (After Response)** 에 아래 코드 넣으시면,  
로그인 후 `access`, `refresh` 토큰이 환경변수에 자동 저장됩니다.

```js
insomnia.test("Status code is 200", function () {
    insomnia.response.to.have.status(200);  // ✅ 올바른 상태 코드 확인
    const body = insomnia.response.json();  // 응답 JSON 파싱
	
    // ✅ 환경 변수 저장
    insomnia.environment.set("access", body.access);
    insomnia.environment.set("refresh", body.refresh);
	 const access=insomnia.environment.get("access");
});

```


다운로드 Django REST Framework(DRF).yaml 

[📥 Django REST Framework (DRF) YAML 파일 다운로드](https://codam.kr/assets/file/DjangoRESTFramework(DRF).yaml)


---


#### JWT 발급

`POST /api/token/`

```json
{
  "username": "admin",
  "password": "test"
}
```

- 응답: `access`, `refresh` 토큰

#### JWT 검증 및 사용

- 모든 보호된 API 요청에는 `Authorization: Bearer <access_token>` 헤더 필요

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOi...
```

- 토큰이 유효하지 않거나 만료되면 `401 Unauthorized` 응답
- refresh 토큰으로 access 토큰 갱신 가능 (`/api/token/refresh/`)

---

### 6. JWT 디코딩 확인

JWT는 3개의 파트로 구성됨:

- Header (알고리즘 정보 등)
- Payload (유저 정보, 만료시간 등)
- Signature (검증용 서명)

사이트 [https://jwt.io](https://jwt.io)에서 JWT를 디코딩하면 다음과 같은 payload 확인 가능:

```json
{
  "token_type": "access",
  "exp": 1718993471,
  "user_id": 1
}
```

- `user_id`를 통해 토큰 사용자 식별 가능 → DB 조회 없이 인증 가능

---

### 7. JWT를 이용한 권한 검사

예: 상품 생성 API는 관리자만 가능하도록 설정함:

```python
from rest_framework.permissions import (IsAuthenticated,IsAdminUser,AllowAny)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    ...
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]
```

#### 테스트 시나리오:

- 일반 사용자 로그인 후 JWT로 상품 생성 요청 → `403 Forbidden`
- 관리자 로그인 후 JWT 포함 → `201 Created`

---

### 8. 기타 테스트 및 주의사항

- JWT 인증 설정 후 테스트 코드에서 401이 발생할 수 있음 → 기대 상태 코드 403에서 401로 변경 필요
- 응답 코드 정리:
  - 인증 실패: `401 Unauthorized`
  - 권한 없음: `403 Forbidden`

---

### 9. 요약

- `djangorestframework-simplejwt` 패키지를 이용해 JWT 기반 인증을 구성
- Access/Refresh 토큰 발급 및 갱신 가능
- JWT 디코딩을 통해 사용자 인증 가능
- 관리자 권한 검사와 함께 보호된 API 작성 가능

> 다음 영상에서는 Update와 Delete API 구현에 대해 알아봅니다.

