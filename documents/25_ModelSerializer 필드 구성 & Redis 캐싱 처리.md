
## 25-ModelSerializer 필드 구성 & Redis 캐싱 처리
[![25 - ModelSerializer 필드 구성 & Redis 캐싱 처리](https://img.youtube.com/vi/NgUARZNOuTY/0.jpg)](https://youtu.be/NgUARZNOuTY?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)





---

### 1. 개요

이번 강의에서는 Django REST Framework(DRF)에서 **ModelSerializer의 fields 구성 방식**을 비교하고, **Redis를 활용한 API 캐싱 처리**를 소개합니다. 실무에서 필드 구성 방식을 잘못 사용하면 보안 및 성능에 문제가 생길 수 있으므로 주의가 필요합니다.

---

### 2. ModelSerializer에서 필드 구성 방식

#### 1) 명시적으로 fields 지정 (권장 방식)

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')
```

- 필요한 필드만 선택적으로 반환
- 가장 명확하고 안전한 방식

#### 2) `fields = '__all__'` 사용 (비추천)

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
```

- 모델의 모든 필드를 자동 포함
- 단점:
  - password, permissions 등 민감한 정보까지 포함될 수 있음
  - 모델에 새로운 필드가 추가되면 자동으로 노출됨
  - 프론트엔드에 불필요한 필드까지 포함되어 응답 크기 증가

#### 3) exclude 사용 (비추천)

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'user_permissions')
```

- 제외할 필드를 지정하는 방식
- 단점:
  - 새 필드가 추가되어도 자동 포함됨
  - 속성 또는 커스텀 메서드 필드를 지정할 수 없음


#### 4) 속성 및 커스텀 메서드 활용 (명시적 fields 방식에서만 가능)

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'get_full_name', 'is_authenticated')
```

- `get_full_name`, `is_authenticated` 등 모델 메서드/속성 포함 가능
- `fields = '__all__'` 또는 `exclude` 사용 시 오류 발생함



#### 5) 역참조(Related Name) 포함

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'orders')  # orders는 Order 모델에서의 related_name
```

- 외래키로 연결된 객체도 포함 가능
- 필요 시 nested serializer로 확장 가능


####  6) api/modes.py  추가 related_name='orders'

related_name='orders'  로 관계 설정을 해야  UserSerializer 의  fields 에 orders 사용할 수 있음


```python
class Order(models.Model):
		...
	user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='orders')
	...
```


#### 7) api/views.py  추가

api/views.py

```python

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
    
```


#### 8) api/urls.py 추가

```python
 path('users/', views.UserListView.as_view()),
```





---

### 3. 실무 예외 상황

- 실무에서는 fields='**all**'을 사용한 프로젝트도 존재
- password 해시가 API 응답에 포함되거나, 민감한 사용자 권한 데이터가 노출되는 사례 있음
- 필드는 반드시 명시적으로 선언할 것



---

### 4. 캐싱 처리 소개 (Redis)

> 다음 강의에서는 Redis를 활용해 특정 API 응답을 캐싱하여 성능을 높이는 방법을 다룹니다.

- 불변 데이터 또는 자주 요청되는 데이터를 Redis에 저장
- DRF에서는 `@cache_page` 또는 `django-redis` 모듈과 함께 사용 가능

```python
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

- 위 코드는 5분 동안 응답 결과를 캐싱함


---

### 5. 요약

- ModelSerializer의 필드는 명시적으로 정의하는 것이 보안과 유지보수에 가장 안전
- `__all__` 또는 `exclude` 사용은 예기치 않은 필드 노출 위험
- 커스텀 속성, 메서드, 역참조 필드를 포함하려면 `fields`에 명시 필요
- 다음 강의에서는 Redis 기반의 캐시 적용으로 API 성능 최적화를 구현합니다

