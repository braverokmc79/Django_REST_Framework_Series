
## 11-Generic View에서 권한 설정 커스터마이징 & REST Client 사용


[11 - Generic View에서 권한 설정 커스터마이징 & REST Client 사용](https://youtu.be/mlQZ1i8rUKQ?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)


---


### 1. 개요

이번 강의에서는 Django REST Framework의 `GenericAPIView`에서 **요청 메서드에 따라 권한을 다르게 설정하는 방법**과 함께, VSCode에서 **REST Client 확장 기능**을 활용해 API 테스트를 간편하게 수행하는 방법을 소개합니다.


---

### 2. 문제 상황: GET은 허용, POST는 제한하고 싶을 때

`ProductListCreateAPIView`는 GET 요청으로 전체 상품 목록을 응답하고, POST 요청으로 상품을 새로 생성합니다. 그런데 다음과 같은 요구가 있습니다:

- **GET**: 누구나 접근 가능 (`AllowAny`)
- **POST**: 관리자만 가능 (`IsAdminUser`)

이처럼 요청 방식(GET vs POST)에 따라 서로 다른 권한을 설정하려면 `get_permissions()` 메서드를 **오버라이딩**해야 합니다.

---

### 3. get\_permissions() 메서드 오버라이딩

🔐 `get_permissions()` 메서드: 요청 방식에 따라 권한을 다르게 설정

```python
from rest_framework.permissions import (IsAuthenticated,IsAdminUser,AllowAny)

#🔖 mixin_generics 형태
## POST 요청을 이용한 데이터 생성 : CreateAPIVIew

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        self.permission_classes = [AllowAny]  # 기본적으로 모두 허용 (GET)
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]  # POST 요청만 관리자만 허용
        return super().get_permissions()
```

📌 핵심 요점:

|요청 방식|권한 클래스|설명|
|---|---|---|
|`GET`|`AllowAny`|누구나 접근 가능 (비회원 포함)|
|`POST`|`IsAdminUser`|**관리자(superuser 또는 is_staff=True인 유저)**만 가능|



이제:

- 누구나 GET 요청 가능
- 관리자가 아니면 POST 요청 시 `403 Forbidden` 오류 발생

---

### 4. VSCode REST Client 확장 기능 사용

#### 📦 설치 방법

- VSCode 마켓플레이스에서 `REST Client` 설치
- `.http` 확장자의 파일을 만들면 여러 API 요청을 작성하고 전송할 수 있음

#### 📁 예시:  `/Chapter11/api.http`

```http
### GET 전체 상품 목록
GET http://localhost:8000/products/ HTTP/1.1

### POST 상품 생성 (관리자만 가능)
POST http://localhost:8000/products/ HTTP/1.1
Content-Type: application/json

{
  "name": "샘플 상품",
  "description": "설명입니다",
  "price": "12000.00",
  "stock": 5
}
```

- `###` 구분자를 사용해 여러 요청 작성 가능
- VSCode 내에서 각 요청 오른쪽 상단 `Send Request` 버튼으로 테스트 가능
- POST 요청 시 권한 오류가 나면 403 메시지와 함께 "인증 정보가 제공되지 않았습니다"라는 응답 확인 가능


![api.http](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgo_GHrG9Du0rIylCW63mPdeqw097n7gLaRCFQAOxr4BIHlnuJaGR5XZOvFjo75FrJj5h_ShrGeYpGrLEWMiONJYuE_UL1Jbs5iijxGITEgbcGF1ePR9x9eK9D-D2O08r6OjNz0XdBZvqEVCRR-g-u1YrDbBL3nLQKQagznsiLecq7YcmN2PeYQr-M2yYJw/s2069/2025-06-26%2017%2032%2034.png)



---

### 5. 권한 적용 결과 확인

- GET 요청 → 응답 정상, 전체 상품 JSON 반환
- POST 요청 (비인증 사용자) → 403 오류 발생
- POST 요청 (관리자 로그인 후) → `201 Created` 응답 반환, 새 상품 생성됨

---

### 6. 요약

- `get_permissions()` 메서드를 오버라이딩하면 요청 방식(GET/POST)에 따라 동적으로 권한을 설정할 수 있음
- DRF 내장 권한 클래스 'IsAuthenticated',   `IsAdminUser`, `AllowAny` 활용
- VSCode REST Client 확장 기능으로 Postman 없이 빠르게 API 요청 테스트 가능


> 다음 강의에서는 JWT 인증과 Authorization 헤더를 사용하여 관리자 인증을 구현하는 방법을 다룹니다.

