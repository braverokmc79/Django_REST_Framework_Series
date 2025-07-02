## 28-API 호출 제한 (Throttling)



[28 - API 호출 제한 (Throttling)](https://youtu.be/95ndK3P9YLI?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)


---


### 1. 개요
이번 강의에서는 Django REST Framework(DRF)에서 **API 호출 제한(Throttling)** 기능을 활용하여 사용자별, 요청 유형별로 **요청 빈도를 제한하는 방법**을 학습합니다. 이는 API 남용을 방지하고, 서비스 자원을 효율적으로 관리하기 위한 중요한 기법입니다.

---

### 2. Throttling이란?
- 일정 시간 동안 특정 사용자 또는 IP가 보낼 수 있는 요청 수를 제한하는 것
- 예: 익명 사용자는 하루 100회, 인증 사용자는 분당 3회 요청 가능
- 초과 시 HTTP 429 Too Many Requests 응답 반환

---

### 3. 기본 Throttle 클래스
DRF에서는 아래와 같은 기본 Throttle 클래스를 제공합니다:

- `AnonRateThrottle`: 익명 사용자 전용
- `UserRateThrottle`: 인증 사용자 전용
- `ScopedRateThrottle`: 특정 뷰(View)에 개별 제한 설정 가능

`settings.py` 예시:
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',            
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '2/minute',
        'products': '2/minute',
        'orders': '4/minute'
    }
}
```
- 익명 사용자는 분당 2회, 인증 사용자는 분당 3회 요청 허용

---

### 4. 실습: 익명 사용자 제한 테스트

1. `/products/` API에 접근 (비로그인 상태)
2. 첫 두 요청은 정상 응답
3. 세 번째 요청부터 429 응답 발생:
```json
{
  "detail": "요청이 너무 많습니다. 33초 후에 다시 시도하세요."
}
```
- 응답 헤더에 `Retry-After` 포함됨

---

### 5. 인증 사용자 제한 테스트

- 로그인 후 `/products/` API 접근 시 최대 3회까지 응답 가능
- 4회째 요청 시 429 오류 발생

---

### 6. 커스텀 Throttle 클래스 구성

`throttles.py`:

```python
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

`settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'myapp.throttles.BurstRateThrottle',
        'myapp.throttles.SustainedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '10/minute',
        'sustained': '15/hour',
    }
}
```

- **burst**: 단기간 빠른 요청 허용 (10회/분)
- **sustained**: 장기 요청 수 제한 (15회/시)

---

### 7. ScopedRateThrottle 사용

`views.py`:
```python
from rest_framework.throttling import ScopedRateThrottle


class ProductListCreateAPIView(generics.ListCreateAPIView):
    throttle_scope = 'products'
    throttle_classes = [ScopedRateThrottle]


	...




class OrderViewSet(viewsets.ModelViewSet):
    throttle_scope = 'orders'
    queryset = Order.objects.prefetch_related('items__product')

	...




```


- `throttle_scope`: 속도 제한의 **이름표(tag)** 역할을 함.
    
- `ScopedRateThrottle`: 해당 이름표에 설정된 제한 값을 적용하는 클래스.

##### 🔹 ProductListCreateAPIView

```python
from rest_framework.throttling import ScopedRateThrottle

class ProductListCreateAPIView(generics.ListCreateAPIView):
    throttle_scope = 'products'
    throttle_classes = [ScopedRateThrottle]
    ...
```

→ `'products'`라는 이름으로 속도 제한 적용됨.  
예: 하루 100번만 요청 가능 (`products: 100/day`)

##### 🔹 OrderViewSet

```python
class OrderViewSet(viewsets.ModelViewSet):
    throttle_scope = 'orders'
    queryset = Order.objects.prefetch_related('items__product')
    ...
```

→ `'orders'`라는 이름으로 속도 제한 적용됨.  
예: 한 시간에 10번만 요청 가능 (`orders: 10/hour`)


---


`settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',            
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '2/minute',
        'products': '2/minute',
        'orders': '4/minute'
    }
}
```

- `/products/` API는 분당 2회, `/orders/` API는 분당 4회 요청 허용

---

### 8. 추가 참고 사항
- DRF Throttle은 Django 캐시 백엔드를 이용해 호출 기록을 저장
- Redis 캐시 사용 시 더 정교하고 빠른 제한 적용 가능
- Throttling은 보안 목적이 아닌 서비스 남용 방지를 위한 정책임
  - **DoS 공격 대응은 불가**
  - 방화벽(WAF), AWS Shield, Cloudflare 등 외부 보안 도구와 병행 필요

---

### 9. 요약
- DRF의 Throttling 기능은 인증/비인증 사용자 또는 개별 API 엔드포인트 단위로 요청 제한을 걸 수 있는 중요한 도구
- `AnonRateThrottle`, `UserRateThrottle`, `ScopedRateThrottle`을 활용하여 다양한 정책 구현 가능
- Redis 등 외부 캐시 연동 및 커스텀 클래스 확장으로 더욱 정밀한 제어 가능

> 다음 강의에서는 Django REST Framework의 **테스트 도구**를 활용한 API 테스트 자동화 방법을 배웁니다.




