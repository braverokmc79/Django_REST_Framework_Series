## Django REST Framework(DRF) - drf-spectacular로 DRF API 문서화 도구 적용하기

### 1. 개요

Django REST Framework나 Django Ninja 등 다양한 API 프레임워크로 API를 개발할 때, **API 구조를 문서화**하여 다른 팀원(프론트엔드, 모바일 개발자 등)과 공유하는 것은 매우 중요합니다. 이를 쉽게 처리할 수 있도록 돕는 도구가 바로 `drf-spectacular`입니다.

---

### 2. drf-spectacular 소개

`drf-spectacular`은 **OpenAPI 3.0** 스키마를 생성해주는 Django REST Framework 전용 패키지로, 다음과 같은 특징을 갖습니다:

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

#### 4) 추가 설정 - 문서 제목, 설명 등

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'My API 문서',
    'DESCRIPTION': 'Django REST Framework 기반 프로젝트 API 문서입니다.',
    'VERSION': '1.0.0',
}
```

---

### 4. API 스키마 파일 생성 (선택 사항)

```bash
python manage.py spectacular --file schema.yaml
```

- `schema.yaml` 파일이 생성됨
- 다른 시스템이나 문서화 플랫폼과 공유 가능

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

- `drf-spectacular`는 Django REST Framework 기반 프로젝트에서 OpenAPI 3 문서를 쉽고 강력하게 생성할 수 있게 해줍니다.
- Swagger/Redoc UI를 통해 개발자와 사용자 간 원활한 API 공유 가능
- 설정만으로 완전한 문서 자동화가 가능하여 개발 생산성 향상

> 다음 영상에서는 필터링, 검색, 정렬 기능을 DRF에 적용하는 방법을 배웁니다.

