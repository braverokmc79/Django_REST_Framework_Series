
# 1. DRF개발 방식

## Django REST Framework(DRF)에서 **가장 많이 쓰이고 공식적으로도 추천되는 방식**은 다음과 같습니다


### ✅ **1위: 제네릭 뷰(GenericAPIView + Mixin / 단축 클래스)**

---
```python
  #GenericAPIView
  path("generics/list/", TodoGenericsListAPI.as_view()),
  path("generics/create/", TodoGenericsCreateAPI.as_view()),
  path("generics/retrieve/<int:pk>/", TodoGenericsRetrieveAPI.as_view()),
  path("generics/update/<int:pk>/", TodoGenericsUpdateAPI.as_view()),  
  path("generics/delete/<int:pk>/", TodoGenericsDeleteAPI.as_view()),



  # GenericAPIView + Mixin
  path("mixin_generics/", TodoGenericsListCreateAPI.as_view()),
  path("mixin_generics/<int:pk>/", TodoGenericsRetrieveUpdateDeleteAPI.as_view()),
```

  🔖 GenericAPIView 호출예 
```python
 #
  # http://127.0.0.1:8000/todo/generics/list/
  # http://127.0.0.1:8000/todo/generics/create/
  # http://127.0.0.1:8000/todo/generics/retrieve/1/
  # http://127.0.0.1:8000/todo/generics/update/1/
  # http://127.0.0.1:8000/todo/generics/delete/1
  
```

  🔖 GenericAPIView + Mixin 호출예
```python
# List + Create 
#generics.ListCreateAPIView
# http://127.0.0.1:8000/todo/mixin_generics/   GET, CREATE



# Retrieve + Update + Delete (RUD)
# generics.RetrieveUpdateDestroyAPIView
# http://127.0.0.1:8000/todo/mixin_generics/1/ GET, PUT, DELETE 모두 처리
```


#### ✅ **[방식 1] 단축 클래스(Generic Class-based Views)**

```python
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Todo
from .serializers import TodoSerializer

class TodoListCreateAPI(ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodoDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
```

##### ✅ RetrieveUpdateDestroyAPIView는 다음 HTTP 메서드 3개를 처리합니다:

|메서드|설명|예시 URL|
|---|---|---|
|GET|상세 조회|/todo/1/|
|PUT|전체 수정|/todo/1/ + JSON 바디|
|DELETE|삭제|/todo/1/|

##### ✅ 장점:

- `RetrieveAPIView + UpdateAPIView + DestroyAPIView`를 **하나로 합친 클래스**
    
- 중복 없이 **하나의 API endpoint에서 상세조회, 수정, 삭제 처리** 가능
    

##### ✅ 구성 요약:

```python
class TodoGenericsRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()         # 어디서 데이터를 가져올지
    serializer_class = TodoSerializer     # 데이터를 어떻게 직렬화할지
```

---

#### ✅ **[방식 2] GenericAPIView + Mixin 조합**

```python
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .models import Todo
from .serializers import TodoSerializer

class TodoListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TodoDetailAPI(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

##### ✅ 장점:

- **조합의 유연성**: 필요한 Mixin만 골라 쓸 수 있어 **정밀 제어 가능**
    
- **공식 문서 예제에서도 종종 등장하는 패턴**
    
- **복잡한 조건 처리나 커스터마이징이 쉬움**
    

---

#### 🔖 제너릭 뷰(Generic View) 방식 비교 요약

| 항목           | 단축 클래스(Generic Views)             | GenericAPIView + Mixin 조합 |
| ------------ | --------------------------------- | ------------------------- |
| **코드 간결성**   | 매우 높음 (GET/POST/PUT/DELETE 자동 지원) | 중간 (직접 메서드 구현 필요)         |
| **사용 난이도**   | 쉬움                                | 약간 높음 (직접 Mixin 조합 필요)    |
| **커스터마이징**   | 낮음 (기본 동작 위주)                     | 높음 (로직 세분화 및 복잡한 처리 가능)   |
| **유지보수**     | 쉬움 (반복 코드 없음)                     | 구조 명확, 복잡한 프로젝트에 적합       |
| **공식 권장 여부** | ✅ 가장 먼저 소개되는 방식                   | ✅ 다양한 상황에 대응 가능           |

---

####  ✅ **정리**: 대부분의 경우엔 **단축 클래스(Generic View)로 충분하며, 특별한 커스터마이징이 필요할 때는 GenericAPIView + Mixin** 조합을 고려하는 것이 좋습니다.



___



### ✅ 2위: ViewSet + Router 방식

🔹 예시:
```python
from rest_framework.viewsets import ModelViewSet
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

```

URL은 `router`를 통해 자동 생성됨

```python
# urls.py
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = router.urls

```


####  🔖 장점:

| 항목                | 설명                                              |
| ----------------- | ----------------------------------------------- |
| **URL 자동 생성**     | list, retrieve, create, update, destroy 등 자동 처리 |
| **Admin 스타일의 구성** | Django Admin처럼 직관적                              |
| **대규모 프로젝트에 유리**  | URL, View, Action 간 결합이 명확함                     |


---


### ✅ 3위: APIView (직접 메서드 구현)


```python
from rest_framework.views import APIView
class TodoAPIView(APIView):
    def get(self, request):
        ...
    def post(self, request):
        ...
```

#### ⚠️ 단점:

- 반복 코드 많음
    
- `queryset`, `serializer` 자동 지원 없음
    
- CRUD 모두 직접 처리해야 함
    
- 일반적으로 **복잡하거나 비표준 API**에만 사용



### 🎯 결론: **DRF에서 가장 많이 쓰이고 추천되는 방식**

| 순위    | 방식                                                                              | 추천 상황                       |
| ----- | ------------------------------------------------------------------------------- | --------------------------- |
| ✅ 1위  | `GenericAPIView` + 단축 클래스 (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`) | **일반적인 CRUD API**           |
| ✅ 2위  | `ModelViewSet` + `Router`                                                       | **관리형 API 전체 자동화 원할 때**     |
| ⚠️ 3위 | `APIView`                                                                       | **복잡한 로직, 커스텀 처리 많을 때만** 사용 |




---




# 2-강의 목록

### Django REST Framework(DRF) 강의

> 아래는 Django REST Framework를 체계적으로 학습할 수 있는 BugBytes 의 YouTube 강의 시리즈입니다.  



---

### 01 - 설정과 모델 구성
[![01 - 설정과 모델 구성](https://img.youtube.com/vi/6AEvlNgRPNc/0.jpg)](https://youtu.be/6AEvlNgRPNc?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 02 - Serializer와 Response 객체 & 브라우저 기반 API
[![02 - Serializer와 Response 객체 & 브라우저 기반 API](https://img.youtube.com/vi/BMym71Dwox0/0.jpg)](https://youtu.be/BMym71Dwox0?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 03 - 중첩 Serializer, SerializerMethodField 및 관계 표현
[![03 - 중첩 Serializer, SerializerMethodField 및 관계 표현](https://img.youtube.com/vi/KfSYadIFHgY/0.jpg)](https://youtu.be/KfSYadIFHgY?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 04 - Serializer 하위 클래스와 집계형 API 데이터 처리
[![04 - Serializer 하위 클래스와 집계형 API 데이터 처리](https://img.youtube.com/vi/_xbI0-mjtw4/0.jpg)](https://youtu.be/_xbI0-mjtw4?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 05 - django-silk를 활용한 성능 최적화
[![05 - django-silk를 활용한 성능 최적화](https://img.youtube.com/vi/OG8alXR4bEs/0.jpg)](https://youtu.be/OG8alXR4bEs?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 06 - Generic View 소개 & ListAPIView & RetrieveAPIView
[![06 - Generic View 소개 & ListAPIView & RetrieveAPIView](https://img.youtube.com/vi/vExjSChWPWg/0.jpg)](https://youtu.be/vExjSChWPWg?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 07 - 동적 필터링 & get_queryset() 메서드 오버라이딩
[![07 - 동적 필터링 & get_queryset() 메서드 오버라이딩](https://img.youtube.com/vi/3Gi-w4Swge8/0.jpg)](https://youtu.be/3Gi-w4Swge8?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 08 - 권한 시스템 및 테스트
[![08 - 권한 시스템 및 테스트](https://img.youtube.com/vi/rx5IV_4Iuog/0.jpg)](https://youtu.be/rx5IV_4Iuog?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 09 - APIView 클래스 활용법
[![09 - APIView 클래스 활용법](https://img.youtube.com/vi/TVFCU0w65Ak/0.jpg)](https://youtu.be/TVFCU0w65Ak?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

###  10-GET과 POST를 동시에 처리하는 ListCreateAPIView
[![10 - 데이터 생성하기 & ListCreateAPIView와 Generic View 내부 구조](https://img.youtube.com/vi/Jh85U1nhMh8/0.jpg)](https://youtu.be/Jh85U1nhMh8?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 11 - Generic View에서 권한 설정 커스터마이징 & REST Client 사용
[![11 - Generic View에서 권한 설정 커스터마이징 & REST Client 사용](https://img.youtube.com/vi/mlQZ1i8rUKQ/0.jpg)](https://youtu.be/mlQZ1i8rUKQ?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 12 - simplejwt를 이용한 JWT 인증
[![12 - simplejwt를 이용한 JWT 인증](https://img.youtube.com/vi/Xp0-Yy5ow5k/0.jpg)](https://youtu.be/Xp0-Yy5ow5k?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 13 - Refresh Token과 JWT 인증 심화
[![13 - Refresh Token과 JWT 인증 심화](https://img.youtube.com/vi/H3OY36wa7Cs/0.jpg)](https://youtu.be/H3OY36wa7Cs?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 14 - 데이터 수정 및 삭제 처리
[![14 - 데이터 수정 및 삭제 처리](https://img.youtube.com/vi/08gHVFPFuBU/0.jpg)](https://youtu.be/08gHVFPFuBU?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 15 - DRF-spectacular로 DRF API 문서화 도구 및 Swagger(OpenAPI) 문서 자동화
[![15 - drf-spectacular로 DRF API 문서화 도구](https://img.youtube.com/vi/E3LUvsPWLwM/0.jpg)](https://youtu.be/E3LUvsPWLwM?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 16 - django-filter와 DRF를 이용한 API 필터링
[![16 - django-filter와 DRF를 이용한 API 필터링](https://img.youtube.com/vi/NDFgTGTI8zg/0.jpg)](https://youtu.be/NDFgTGTI8zg?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 17 - SearchFilter와 OrderingFilter 사용하기
[![17 - SearchFilter와 OrderingFilter 사용하기](https://img.youtube.com/vi/LCYqDsl1WYI/0.jpg)](https://youtu.be/LCYqDsl1WYI?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 18 - 사용자 정의 필터 백엔드 만들기
[![18 - 사용자 정의 필터 백엔드 만들기](https://img.youtube.com/vi/u4S71cO5QhI/0.jpg)](https://youtu.be/u4S71cO5QhI?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 19 - API 페이지네이션 설정
[![19 - API 페이지네이션 설정](https://img.youtube.com/vi/sTyMe2R9mzk/0.jpg)](https://youtu.be/sTyMe2R9mzk?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 20 - ViewSet & Router 기본 사용법
[![20 - ViewSet & Router 기본 사용법](https://img.youtube.com/vi/4MrB4IvW6Ow/0.jpg)](https://youtu.be/4MrB4IvW6Ow?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 21 - Viewset에서의 액션, 필터링, 권한 처리
[![21 - Viewset에서의 액션, 필터링, 권한 처리](https://img.youtube.com/vi/rekvVrjUMjg/0.jpg)](https://youtu.be/rekvVrjUMjg?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 22 - Viewset 권한 설정 & 관리자 vs 일반 사용자
[![22 - Viewset 권한 설정 & 관리자 vs 일반 사용자](https://img.youtube.com/vi/KmYYg1qJKNQ/0.jpg)](https://youtu.be/KmYYg1qJKNQ?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 23 - 중첩 객체 생성하기 & create() 오버라이딩
[![23 - 중첩 객체 생성하기 & create() 오버라이딩](https://img.youtube.com/vi/CAq7AKAT7Q0/0.jpg)](https://youtu.be/CAq7AKAT7Q0?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 24 - 중첩 객체 수정하기 & update() 사용
[![24 - 중첩 객체 수정하기 & update() 사용](https://img.youtube.com/vi/QtkES6O_ed4/0.jpg)](https://youtu.be/QtkES6O_ed4?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 25 - ModelSerializer 필드 구성 & Redis 캐싱 처리
[![25 - ModelSerializer 필드 구성 & Redis 캐싱 처리](https://img.youtube.com/vi/NgUARZNOuTY/0.jpg)](https://youtu.be/NgUARZNOuTY?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 26 - Django & Redis - Vary Header를 통한 캐싱 제어
[![26 - Django & Redis - Vary Header를 통한 캐싱 제어](https://img.youtube.com/vi/5W2Yff00H8s/0.jpg)](https://youtu.be/5W2Yff00H8s?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 27 - Vary 헤더로 캐시 제어
[![27 - Vary 헤더로 캐시 제어](https://img.youtube.com/vi/iUn8go-XZNw/0.jpg)](https://youtu.be/iUn8go-XZNw?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 28 - API 호출 제한 (Throttling)
[![28 - API 호출 제한 (Throttling)](https://img.youtube.com/vi/95ndK3P9YLI/0.jpg)](https://youtu.be/95ndK3P9YLI?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 29 - API 테스트하기
[![29 - API 테스트하기](https://img.youtube.com/vi/sRluxnmZ-H8/0.jpg)](https://youtu.be/sRluxnmZ-H8?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 30 - Celery 비동기 작업 처리하기
[![30 - Celery 비동기 작업 처리하기](https://img.youtube.com/vi/E6HPMk0bKPY/0.jpg)](https://youtu.be/E6HPMk0bKPY?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

### 31 - Djoser를 활용한 인증 시스템 구축 & JWT 베스트 프랙티스
[![31 - Djoser를 활용한 인증 시스템 구축 & JWT 베스트 프랙티스](https://img.youtube.com/vi/QO8UyXWNg-k/0.jpg)](https://youtu.be/QO8UyXWNg-k?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)

---

