이번 문서에서는 Django REST Framework(DRF) 기반 애플리케이션에 Celery를 활용하여 비동기 작업을 처리하는 방법을 정리합니다. 특히 주문 생성 시 이메일 전송과 같이 응답 속도에 영향을 줄 수 있는 작업을 백그라운드에서 실행하는 방식에 초점을 맞춥니다.

## 1. Celery란?

Celery는 분산 작업 큐(Distributed Task Queue)로, 대규모 메시지를 처리하고 비동기 또는 주기적 작업을 실행할 수 있게 해주는 파이썬 라이브러리입니다. Django와 함께 사용할 때는 Redis나 RabbitMQ 같은 브로커를 통해 클라이언트와 워커 간 메시지를 교환합니다.

## 2. 기본 구성 요소

- **브로커(Broker)**: 메시지를 중개하는 역할 (Redis 사용)
- **워커(Worker)**: 브로커로부터 전달받은 작업을 실행
- **태스크(Task)**: 실행할 작업 단위 (예: 이메일 전송)

## 3. 프로젝트 설정

### 1단계. 설치

```bash
pip install celery redis
```

### 2단계. 프로젝트 루트에 `celery.py` 생성

```python
# myproject/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

### 3단계. `__init__.py`에 Celery 앱 등록

```python
# myproject/__init__.py
from .celery import app as celery_app
__all__ = ("celery_app",)
```

### 4단계. settings.py 설정

```python
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
```

## 4. Celery 태스크 정의

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

## 5. View에서 비동기 작업 호출

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

## 6. 워커 실행

```bash
celery -A myproject worker --loglevel=info
```

- `-A` 옵션은 Celery 앱 위치 지정
- `--loglevel=info`는 로그 출력 수준 설정

## 7. 결과 확인

1. Django 서버 실행 후, 주문 생성 API 호출
2. Celery 워커 터미널에서 이메일 전송 메시지가 출력됨
3. 콘솔 이메일 백엔드이므로 실제 메일은 전송되지 않고 터미널에 표시됨

## 8. 확장 팁

- 결과 저장이 필요하면 `CELERY_RESULT_BACKEND` 설정을 통해 Redis 등에 저장 가능
- 주기적 작업이 필요하면 Celery Beat 활용 (스케줄링 가능)
- 복잡한 흐름은 체이닝, 그룹화 등의 기능으로 구현 가능

## 마무리

Celery를 활용하면 DRF API에서 긴 시간이 필요한 작업을 백그라운드로 분리해, 응답 속도를 향상시키고 사용자 경험을 개선할 수 있습니다. 이번 예제에서는 이메일 전송을 다뤘지만, 이미지 처리, 외부 API 호출, 통계 집계 등 다양한 분야에 적용 가능합니다.

자세한 내용은 [Celery 공식 문서](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)를 참고하세요.

