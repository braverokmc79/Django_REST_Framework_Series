이번 문서에서는 Django REST Framework(DRF)의 API 테스트 도구 사용법을 공식 문서와 실무 예제를 바탕으로 정리해보겠습니다. 테스트는 API의 신뢰성과 보안을 보장하는 핵심 요소이며, DRF는 이를 위해 다양한 유틸리티를 제공합니다.

## 1. DRF 테스트 유틸리티 개요

Django REST Framework는 Django의 기존 테스트 프레임워크를 확장하여 RESTful API에 최적화된 테스트 클래스를 제공합니다.

### 주요 클래스
- **APIRequestFactory**: Django의 `RequestFactory`를 확장한 것으로, view 함수/클래스를 직접 호출할 때 사용합니다.
- **APIClient**: Django의 `Client`를 확장한 것으로, 실제 API 요청처럼 처리되며 인증, 권한 테스트에 유용합니다.
- **APITestCase**: `django.test.TestCase`를 상속하며, 내부적으로 `self.client`가 `APIClient` 인스턴스를 참조합니다.

## 2. 설정 예시

### 기본 테스트 구조
```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@example.com", "pass")
        self.user = User.objects.create_user("user", "user@example.com", "pass")
        self.product = Product.objects.create(name="테스트 상품", price=10000)
        self.url = reverse("product-detail", kwargs={"product_id": self.product.pk})
```

## 3. 테스트 메서드 예시

### 인증 없이 GET 요청 (허용됨)
```python
def test_get_product(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["name"], self.product.name)
```

### 인증 없이 PUT 요청 (허용 안 됨)
```python
def test_unauthorized_update_product(self):
    data = {"name": "변경된 이름"}
    response = self.client.put(self.url, data)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

### 인증 없이 DELETE 요청 (허용 안 됨)
```python
def test_unauthorized_delete_product(self):
    response = self.client.delete(self.url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

### 일반 사용자 DELETE 요청 (허용 안 됨)
```python
def test_only_admins_can_delete_product(self):
    self.client.login(username="user", password="pass")
    response = self.client.delete(self.url)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
```

### 관리자 DELETE 요청 (허용됨)
```python
    self.client.login(username="admin", password="pass")
    response = self.client.delete(self.url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
```

## 4. 응답 데이터 확인 팁
- `response.data`: DRF의 Response 객체는 JSON 파싱 없이 딕셔너리 형태로 바로 접근 가능
```python
self.assertEqual(response.data, {"id": 1, "name": "테스트 상품"})
```

## 5. 상태 코드 사용
숫자 대신 DRF의 `rest_framework.status` 모듈 상수 사용을 권장합니다.
```python
from rest_framework import status
status.HTTP_200_OK
status.HTTP_401_UNAUTHORIZED
status.HTTP_403_FORBIDDEN
status.HTTP_204_NO_CONTENT
```

## 6. 마무리

Django REST Framework는 API 테스트를 간편하고 직관적으로 할 수 있도록 강력한 도구를 제공합니다. 인증, 권한, 응답 구조를 자동화된 테스트로 검증하면 API의 신뢰성과 유지보수성이 크게 향상됩니다.

추가로 `PUT`, `PATCH` 요청 테스트는 `DELETE` 테스트와 유사하게 구현 가능합니다. 더 자세한 내용은 DRF 공식 문서의 [Testing](https://www.django-rest-framework.org/api-guide/testing/) 페이지를 참고하세요.

