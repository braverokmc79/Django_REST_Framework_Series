

## 30-Celery 비동기 작업 처리하기



[30 - Celery 비동기 작업 처리하기](https://youtu.be/E6HPMk0bKPY?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)



🔗 [소스 1: bugbytes-io/drf-course-api](https://github.com/bugbytes-io/drf-course-api)

🔗 [소스 2: braverokmc79/Django_REST_Framework_Series](https://github.com/braverokmc79/Django_REST_Framework_Series)


---

### 1. 개요

이번 강의에서는 Django REST Framework(DRF) 기반 애플리케이션에 Celery를 활용하여 비동기 작업을 처리하는 방법을 정리합니다. 특히 주문 생성 시 이메일 전송과 같이 응답 속도에 영향을 줄 수 있는 작업을 백그라운드에서 실행하는 방식에 초점을 맞춥니다.

---

### 1. Celery란?

Celery는 분산 작업 큐(Distributed Task Queue)로, 대규모 메시지를 처리하고 비동기 또는 주기적 작업을 실행할 수 있게 해주는 파이썬 라이브러리입니다. Django와 함께 사용할 때는 Redis나 RabbitMQ 같은 브로커를 통해 클라이언트와 워커 간 메시지를 교환합니다.


---

### 2. 기본 구성 요소

- **브로커(Broker)**: 메시지를 중개하는 역할 (Redis 사용)
- **워커(Worker)**: 브로커로부터 전달받은 작업을 실행
- **태스크(Task)**: 실행할 작업 단위 (예: 이메일 전송)


---

### 3. 프로젝트 설정

#### 1단계. 설치

```bash
pip install celery redis
```

#### 2단계. 프로젝트 루트에 `celery.py` 생성

```python
# myproject/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

#### 3단계. `__init__.py`에 Celery 앱 등록

```python
# myproject/__init__.py
from .celery import app as celery_app
__all__ = ("celery_app",)
```

#### 4단계. settings.py 설정

```python
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
```




---

### 4. Celery 태스크 정의

`api/tasks.py`:

```python
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_confirmation_email(order_id, user_email):
    subject = "주문 확인"
    message = f"주문 번호 {order_id}가 접수되었습니다."
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email]
    )
```




---

### 5. View에서 비동기 작업 호출

`perform_create` 메서드에서 태스크 호출:

```python
from api.tasks import send_order_confirmation_email

class OrderViewSet(...):
    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        send_order_confirmation_email.delay(order.id, self.request.user.email)
```

- `.delay()`를 호출하면 Redis 브로커를 통해 작업이 워커로 전송됨
- ORM 객체 대신 단순한 타입만 인자로 넘길 것




---


### 6. 워커 실행

```bash
celery -A myproject worker --loglevel=info
```

- `-A` 옵션은 Celery 앱 위치 지정
- `--loglevel=info`는 로그 출력 수준 설정



---

### 7. 결과 확인

1. Django 서버 실행 후, 주문 생성 API 호출
2. Celery 워커 터미널에서 이메일 전송 메시지가 출력됨
3. 콘솔 이메일 백엔드이므로 실제 메일은 전송되지 않고 터미널에 표시됨


---

### 8. 확장 팁

- 결과 저장이 필요하면 `CELERY_RESULT_BACKEND` 설정을 통해 Redis 등에 저장 가능
- 주기적 작업이 필요하면 Celery Beat 활용 (스케줄링 가능)
- 복잡한 흐름은 체이닝, 그룹화 등의 기능으로 구현 가능


---

### 마무리

Celery를 활용하면 DRF API에서 긴 시간이 필요한 작업을 백그라운드로 분리해, 응답 속도를 향상시키고 사용자 경험을 개선할 수 있습니다. 이번 예제에서는 이메일 전송을 다뤘지만, 이미지 처리, 외부 API 호출, 통계 집계 등 다양한 분야에 적용 가능합니다.

자세한 내용은 [Celery 공식 문서](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)를 참고하세요.




---


# Spring Boot Kafka vs Django Celery 비교 

**백엔드에서 비동기 작업 처리**는 필수적인 기능입니다. Python 진영에서는 `Django + Celery`, Java 진영에서는 `Spring Boot + Kafka` 또는 `@Async` 기반 비동기 처리 방식이 많이 사용됩니다. 이 글에서는 이 두 가지 조합을 비교해보겠습니다.

---

## ✅ 개요

| 항목         | Django + Celery        | Spring Boot + Kafka              |
| ---------- | ---------------------- | -------------------------------- |
| 언어/프레임워크   | Python / Django        | Java / Spring Boot               |
| 주요 목적      | 비동기 작업 처리, 주기적 작업      | 비동기 메시지 처리, 이벤트 기반 시스템           |
| 메시지 브로커    | Redis, RabbitMQ        | Kafka, RabbitMQ (또는 Redis)       |
| 주기적 작업 지원  | `celery-beat`로 cron 지원 | `@Scheduled`, Quartz Scheduler 등 |
| 실시간 비동기 작업 | ✅ 가능                   | ✅ 가능                             |
| 확장성        | 수평 확장 쉬움 (Worker 방식)   | 고성능 스트리밍 처리 가능 (Kafka 기반)        |
| 메시지 순서 보장  | 브로커 설정 및 Celery 설정 필요  | Kafka 파티션 기준 순서 보장               |

---

## ✅ 구조적 차이점

### 🔹 Django + Celery 구조

```
사용자 요청
     ↓
  Django App
     ↓ (비동기 호출)
   Celery Task Queue
     ↓
   Redis / RabbitMQ (브로커)
     ↓
  Celery Worker → 결과 처리
```

### 🔹 Spring Boot + Kafka 구조

```
사용자 요청
     ↓
Spring Boot App
     ↓ (KafkaTemplate 등으로 전송)
   Kafka Broker (토픽에 저장)
     ↓
Kafka Consumer(@KafkaListener)
     ↓
    처리 및 응답 (필요시 DB 등)
```

---

## ✅ 개발자 경험 (DX) 비교

|항목|Django + Celery|Spring Boot + Kafka|
|---|---|---|
|설정 편의성|상대적으로 간단 (pip 설치)|설정이 복잡하고 JVM 생태계 요구|
|디버깅|Celery 로그로 가능하나 초기엔 다소 헷갈림|Kafka는 구조 파악이 필요, 복잡도 높음|
|문서/자료|많음 (Django/Celery 공식문서, 블로그)|많음 (Spring 공식 문서, Kafka 문서)|
|실습 난이도|로컬에서도 쉽게 가능|Kafka는 도커/클러스터 등 환경 구성 필요|

---

## ✅ 실무 적합성

|시나리오|추천 기술|
|---|---|
|이메일/알림 발송, 예약작업 등|Django + Celery|
|주문 이벤트 처리, 실시간 로그 수집|Spring Boot + Kafka|
|고성능 스트리밍 처리|Kafka (Spring or Python)|
|단순 백그라운드 작업|Celery or @Async (Spring)|

---

## ✅ 결론

- Python 개발자라면 Django + Celery로 빠르게 비동기/스케줄 작업 환경을 구축할 수 있습니다.
    
- Java 기반 서비스나 마이크로서비스 환경이라면 Spring Boot + Kafka가 강력한 선택지입니다.
    
- **Kafka는 프레임워크가 아니라 메시지 시스템**이므로, Django에서도 Kafka를 사용할 수 있습니다.
    

결국 선택은 다음에 달려 있습니다:

- 언어 선호도
    
- 시스템 복잡도
    
- 처리할 트래픽 규모
    
- 운영 환경 구성 능력
    
