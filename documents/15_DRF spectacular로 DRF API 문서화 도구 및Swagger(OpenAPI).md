##  15-DRF-spectacular로 DRF API 문서화 도구 및Swagger(OpenAPI) 



[15 - drf-spectacular로 DRF API 문서화 도구](https://youtu.be/E3LUvsPWLwM?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



---


### 1. 개요

Django REST Framework나 Django Ninja 등 다양한 API 프레임워크로 API를 개발할 때, **API 구조를 문서화**하여 다른 팀원(프론트엔드, 모바일 개 발자 등)과 공유하는 것은 매우 중요합니다. 이를 쉽게 처리할 수 있도록 돕는 도구가 바로 `DRF-spectacular`입니다.

---

### 2. drf-spectacular 소개

`DRF-spectacular`은 **OpenAPI 3.0** 스키마를 생성해주는 Django REST Framework 전용 패키지로, 다음과 같은 특징을 갖습니다:

- 유연하고 확장 가능
- 다양한 클라이언트 코드 생성 도구와 호환 가능
- Swagger UI, Redoc UI 지원

---

### 3. 설치 및 설정

#### 1) 설치

```bash
pip install drf-spectacular
```

#### 2) `INSTALLED_APPS` 등록 (`settings.py`)

```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
]
```

#### 3) REST\_FRAMEWORK 설정에 스키마 클래스 추가

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    ...
}
```


```python
# Application definition

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
       'rest_framework.renderers.JSONRenderer',
       'rest_framework.renderers.BrowsableAPIRenderer',  # <- 이게 있어야 UI 보임
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```
#### 🔹 `DEFAULT_RENDERER_CLASSES`

- **`JSONRenderer`**: API 응답을 JSON 형식으로 반환합니다. (기본적인 데이터 전송용)
    
- **`BrowsableAPIRenderer`**: 웹 브라우저에서 DRF UI를 제공합니다.  
    👉 이게 있어야 `/api/` 주소 접속 시 예쁘고 테스트 가능한 웹 UI가 나옵니다.


```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    'rest_framework.authentication.SessionAuthentication',
],

```

#### 🔹 `DEFAULT_AUTHENTICATION_CLASSES`

- **`JWTAuthentication`**: 토큰 기반 인증 (로그인 시 토큰을 발급받아 사용)
- **`SessionAuthentication`**: Django의 기본 세션 인증 (관리자 페이지나 브라우저 기반 로그인에 사용)
    
⚠️ 둘 다 같이 쓰면, 브라우저에선 세션으로, API 호출에선 JWT로 인증 가능해 유용합니다.


```python
'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
```


#### 🔹 `DEFAULT_SCHEMA_CLASS`

- **drf-spectacular** 라이브러리를 사용해서 OpenAPI(Swagger) 문서 자동 생성을 가능하게 합니다.    
- `AutoSchema`가 스키마 생성을 자동화해 줍니다.

### ✅ 결론

위 설정은 다음 목적에 적합합니다:

- 브라우저에서 UI로 테스트 가능하게 하고 (`BrowsableAPIRenderer`)    
- JWT 토큰 인증과 세션 인증을 함께 지원하고 (`JWT + Session`)
- 자동으로 Swagger 문서를 만들게 하고 (`drf-spectacular`)
    



#### 4) 추가 설정 - 문서 제목, 설명 등

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'E-Commerce API',
    'DESCRIPTION': 'Django REST Framework 기반 프로젝트 API 문서입니다.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

---

### 4. API 스키마 파일 생성 (선택 사항)

```bash
python manage.py spectacular --file schema.yaml
```

- `schema.yaml` 파일이 생성됨
- 다른 시스템이나 문서화 플랫폼과 공유 가능


**[drf-spectacular] schema.yaml Postman / Insomnia Import Guide**

---


#### 1. Postman에서 schema.yaml 불러오기

1. **Postman 실행**
    
2. ▶️ **"Import"** 버튼 클릭
    
3. **"File" 항목 선택**
    
4. `schema.yaml` 파일 선택 후 Import
    
5. Postman이 OpenAPI 스키마를 분석하여 요청 목록을 자동 생성함
    
6. 각 API 요청에 대한 카드가 자동 생성되어 작업 공간에 추가됨
    

---

#### 2. Insomnia에서 schema.yaml 불러오기

1. **Insomnia 실행**
    
2. ▶️ 상단 메뉴에서 **"Create" > "Request Collection" > "Import From File"** 선택
    
3. `schema.yaml` 선택 후 Import
    
4. Insomnia가 OpenAPI 정의를 불러오고, 각 요청을 자동으로 구성함
    

1️⃣ `schema.yaml` 파일 임포트
![파일임포트](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEic4-qUQK_6XMsnBa5VGYAhY-4OFj9UJoNvuIdsQXirtOGwKMCmJbAZ_2S2DayKDsvTO4HZoS34KjWH_I5E3NEFMe21M1IbAXF9l9ae0d1K7pqbgTusZthK9tdWw-prlL8AkYmrb7LY4cwKb6wDZ_fKL0cIGB9oQrGzREhvXE6yEVUcKbeg2WcDAvXLzNtq/s2117/2025-06-27%2018%2058%2053.png)


2️⃣ Generate Collection 선택
![Generate Collection 선택](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhnCyi6LeS8RsgQrycI5-1scaqAXtZYpFRn8Ns23GktlgWcNGcKpsCWzMBqEkWwZTZapEc43-FzjegVY9b6rvBID75BBsjNScPETL-vObMne6k1GLCj_-6j33slXLJiiiVWtAvWANeq5l5Zvj_oYSNedo_U3gN4W_KPNqOyF_DR0Doca2eP4OySr4X5sPBD/s2131/22.png)


3️⃣Base Environment 선택
![Base Environment 선택](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj3uldR4KLahuR7ZQMfLk_s4boKJFTjM7RItZY6OduSaocka6TNNBBohOBznCHkniQlbbSExKdyjyjghGYaEe5qs4blh1dYGGcvis6g13UeCUp1JrV3G8YBKJTo_xTaIDu9sX9gjquBmmcb6Y2iofIL1MJxILgsSCprW5IPwwA4Ehc7owjl7H_r-EVgLkf2/s2124/2025-06-27%2019%2001%2006.png)


4️⃣ base_url 환경변수 입력 : http://localhost:8000
![base_url 입력](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhCDLhHsIhFPaXizUkKsER-hBbkQ3nyaMXgW_YwOjPWc_6gsPCZDlqkQkO51YvxhgPEZsAdHydjS8YboA8yqqVVp3Gue0mbr2HpSbDn4pn8K3RR0Dp1gj9qhguCQTpC8oGCFrjr1C5U3TKOVw3GcyDEmTstsx5W7JrO99hIuGnc4D85oI22xBmqtDLnivEM/s2031/2025-06-27%2019%2001%2056.png)




---

#### 3. JWT Bearer Token 연동 (Postman 기준)

- Insomnia에서는 Headers를 수동으로 입력해야 할 수도 있음.


1. 해당 요청 클릭
    
2. ▶️ "Authorization" 패널 선택
    
3. **"Bearer Token"** 선택
    
4. JWT Access Token 입력 (예: `eyJ0eXAiOiJKV1QiLCJhb...`)
    

---

#### 요약

- OpenAPI 3.0 스키마(`schema.yaml`) 생성
    
- Postman / Insomnia에서 스키마를 가져와 API 테스트 자동화 가능
    
- JWT 토큰을 Bearer 형식으로 설정하여 인증이 필요한 API 호출 가능
    
---

Swagger UI 기반의 문서 화면에서는 "Authorize" 버튼을 통해 JWT 토큰을 입력하고 인증된 상태로 테스트하는 것도 가능합니다.


---


### 5. 문서 URL 연결 (`urls.py`)

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

- `/api/schema/` → OpenAPI 스키마를 YAML 형태로 반환
- `/api/schema/swagger-ui/` → Swagger 기반의 웹 UI
- `/api/schema/redoc/` → Redoc 기반의 문서 UI


#### ✅ swagger 한글 설정 방법

Swagger UI에 한국어(`ko`)를 적용하려면,   setting.py 에  "lang": "ko" 추가
 
```python

SPECTACULAR_SETTINGS = {
    'TITLE': 'E-Commerce API',
    'DESCRIPTION': 'Django REST Framework 기반 프로젝트 API 문서입니다.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    "SWAGGER_UI_SETTINGS": {
        "lang": "ko"  # ✅ 언어 설정 여기서
    },
}
```


#### ✅ Swagger UI 다국어 지원 현황

|설정|지원 여부|비고|
|---|---|---|
|`swagger_ui_settings={"lang": "ko"}`|✅ 지원|`drf-spectacular` 0.26.2 이상 필요|
|Redoc|❌ 한글 미지원|직접 번역 필요|

#### 📦 설치 버전 확인 (중요)

```bash
pip show drf-spectacular
```

버전이 **0.26.2 이상**이어야 `swagger_ui_settings`가 정상 적용됩니다.  
필요 시 업그레이드:

```
pip install --upgrade drf-spectacular
```

#### ✅ 참고 사항
- Swagger UI가 자동으로 언어를 감지하는 경우도 있지만, 서버에서 `lang` 명시적으로 넘겨주는 것이 더 확실합니다.
    
- OpenAPI 스펙 자체는 번역하지 않으므로, `description`, `title`, 필드 주석 등을 **직접 한글로 작성**해야 Swagger 화면도 자연스럽게 한글로 나옵니다.

###### ✍ 예: 한글 스펙 작성 예시

```python
class NoticeSerializer(serializers.Serializer):
    title = serializers.CharField(help_text='공지 제목')
    content = serializers.CharField(help_text='공지 내용')

class NoticeView(APIView):
    @extend_schema(
        summary="공지 등록",
        description="신문 공고를 등록합니다.",
        request=NoticeSerializer,
        responses={200: OpenApiResponse(description="성공")},
    )
    def post(self, request):
        ...

```


---

### 6. 문서 UI 확인

- Swagger UI에서 전체 API 엔드포인트 목록, 요청/응답 데이터 구조, 파라미터 등을 시각적으로 확인 가능
- 예시:
  - `GET /products/` → 응답 JSON 구조 확인
  - `POST /products/` → 요청 바디 예시 및 필드 요구사항 확인
  - `DELETE /products/{id}/` → 응답 없음 (204 코드)

모든 정보는 **Serializer** 정의 기반으로 자동 추출됩니다.

---

### 7. 응답 예시 & 필드 스키마 자동 생성

- 각 API에 대해 요청 및 응답 스키마가 자동으로 문서화됨
- 필드 설명, 필수 여부, 타입 정보 등도 함께 제공됨
- 모든 정보는 DRF Serializer에 정의된 필드 기반으로 추론됨

---

### 8. 정리

- `DRF-spectacular`는 Django REST Framework 기반 프로젝트에서 OpenAPI 3 문서를 쉽고 강력하게 생성할 수 있게 해줍니다.
- Swagger/Redoc UI를 통해 개발자와 사용자 간 원활한 API 공유 가능
- 설정만으로 완전한 문서 자동화가 가능하여 개발 생산성 향상

> 다음 강의에서는 필터링, 검색, 정렬 기능을 DRF에 적용하는 방법을 배웁니다.

