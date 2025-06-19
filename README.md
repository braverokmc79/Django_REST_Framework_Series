# Django REST Framework series  - DRF 기반

Django REST framework(DRF)를 활용한 간단한 Todo API 예제입니다. 이 프로젝트는 API 설계, 직렬화, 뷰셋, 라우팅 등 Django DRF의 기본을 학습하는 데 초점을 맞춥니다.

---

## 학습 추천: [코담](https://codam.kr/)

### 파이썬·장고 웹개발 | 코담 - 코드에 세상을 담다

[![코담 소개 이미지](https://codam.kr/assets/images/og-image.jpg)](https://codam.kr/)

---

## 🎓 강의 내용

1. Django REST Framework(DRF) - 설정과 모델 구성
2. Django REST Framework(DRF) - Serializer와 Response 객체 | 브라우저 기반 API
3. Django REST Framework(DRF) - 중첩 Serializer, SerializerMethodField 및 관계 표현
4. Django REST Framework(DRF) - Serializer 하위 클래스와 집계형 API 데이터 처리
5. Django REST Framework(DRF) - django-silk를 활용한 성능 최적화
6. Django REST Framework(DRF) - Generic View 소개 | ListAPIView & RetrieveAPIView
7. Django REST Framework(DRF) - 동적 필터링 | get_queryset() 메서드 오버라이딩
8. Django REST Framework(DRF) - 권한 시스템 및 테스트
9. Django REST Framework(DRF) - APIView 클래스 활용법
10. Django REST Framework(DRF) - 데이터 생성하기 | ListCreateAPIView와 Generic View 내부 구조
11. Django REST Framework(DRF) - Generic View에서 권한 설정 커스터마이징 | VSCode REST Client 확장 기능 사용
12. Django REST Framework(DRF) - djangorestframework-simplejwt를 이용한 JWT 인증
13. Django REST Framework(DRF) - Refresh Token과 JWT 인증 심화
14. Django REST Framework(DRF) - 데이터 수정 및 삭제 처리
15. Django REST Framework(DRF) - drf-spectacular로 DRF API 문서화 도구
16. Django REST Framework(DRF) - django-filter 기와 DRF를 이용한 API 필터링
17. Django REST Framework(DRF) - SearchFilter와 OrderingFilter 사용하기
18. Django REST Framework(DRF) - 사용자 정의 필터 백엔드 만들기
19. Django REST Framework(DRF) - API 페이지네이션 설정
20. Django REST Framework(DRF) - ViewSet & Router 기본 사용법
21. Django REST Framework(DRF) - Viewset에서의 액션, 필터링, 권한 처리
22. Django REST Framework(DRF) - Viewset 권한 설정 | 관리자 vs 일반 사용자
23. Django REST Framework(DRF) - 중첩 객체 생성하기 | Serializer의 create() 메서드 오버라이딩
24. Django REST Framework(DRF) - 중첩 객체 수정하기 | ModelSerializer의 update() 메서드 사용
25. Django REST Framework(DRF) - ModelSerializer 필드 구성 - Redis와 함께 캐싱 처리하기
26. Django REST Framework(DRF) - Django & Redis - Vary Header를 통한 캐싱 동작 제어
27. Django REST Framework(DRF) - Vary 헤더로 캐시 제어
28. Django REST Framework(DRF) - API 호출 제한 (Throttling)
29. Django REST Framework(DRF) -  API 테스트하기
30. Django REST Framework(DRF) - Celery 비동기 작업 처리하기
31. Django REST Framework(DRF) - Djoser를 활용한 인증 시스템 구축 | JWT 및 토큰 인증 베스트 프랙티스

---

## ⚙️ 개발 환경

* Python 3.12.3
* Django 5.2.1
* Django REST Framework
* 가상환경: `venv` 사용

---

## ▶️ 실행 방법

1. 가상환경 활성화

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

2. 패키지 설치

```bash
pip install -r requirements.txt

#파워셸 :  
$env:PYTHONUTF8=1; pip install -r requirements.txt
```

3. 서버 실행

```bash
python manage.py runserver
```

---

## 📆 DB 마이그레이션

```bash
# 1. 모델 변경 사항 탐지
python manage.py makemigrations

# 2. 실제 DB에 반영
python manage.py migrate

# 3. 반영 확인
python manage.py showmigrations

```

```bash
 manage.py startapp api
```

---

## 마이그레이션 초기화시 (초기화 방식으로)
```bash
rm -f db.sqlite3
rm -r snippets/migrations
python manage.py makemigrations snippets
python manage.py migrate
python manage.py createsuperuser  # 테스트 사용자 생성

```




### 📌 이 명령어의 역할
django-extensions 패키지의 graph_models 명령어는 지정한 앱(api)의 모델 간 관계를 .dot 파일로 출력합니다.
이 .dot 파일은 Graphviz를 이용해 시각화할 수 있습니다


```bash
# 4. 모델 확인 
python manage.py graph_models api > models.dot

```


## ✅ Django 모델 시각화: 설치 및 사용 가이드

### 1. 패키지 설치

```bash
pip install django-extensions pydot
```

---

### 2. `settings.py`에 앱 추가

```python
INSTALLED_APPS = [
    # ...
    'django_extensions',
]
```

---

### 3. 모델 관계 `.dot` 파일로 추출

```bash
python manage.py graph_models api > models.dot
```

> `api`는 앱 이름입니다. 시각화할 앱의 이름으로 변경하세요.

---

### 4. Graphviz 설치 (이미지로 변환하기 위해 필수)

* 공식 홈페이지: [https://graphviz.org/download/](https://graphviz.org/download/)
* 설치 후 `dot` 명령어가 터미널에서 실행 가능해야 합니다.

---

### 5. `.dot` 파일을 이미지(PNG)로 변환

```bash
dot -Tpng models.dot -o models.png
```

> `models.png` 파일이 생성되며, Django 모델 간의 관계를 시각적으로 확인할 수 있습니다.

---


### 2. 온라인 .dot 파일 시각화 사이트
아래 웹사이트에 .dot 파일 내용 붙여넣거나 업로드해서 그래프를 바로 볼 수 있습니다.
<a href="https://edotor.net/" target="_blank">
Graphviz Visual Editor (edotor.net)
</a>
<a href="https://dreampuf.github.io/GraphvizOnline/?engin" target="_blank">
Viz.js Online
</a>






## 📦 Commit 메시지 컨벤션 (Conventional Commits)

복잡한 개발 과정을 관리하기 위해 [Conventional Commits](https://www.conventionalcommits.org/) 형식을 적용합니다.

### ✍️ 컨벤션 타입 예시

| 타입         | 설명                  |
| ---------- | ------------------- |
| `feat`     | 새로운 기능 추가           |
| `fix`      | 버그 수정               |
| `docs`     | 문서 변경 (README 등)    |
| `style`    | 코드 포맷팅 등 (기능 변화 없음) |
| `refactor` | 리팩토링 (기능 변화 없음)     |
| `test`     | 테스트 코드 추가/수정        |
| `chore`    | 기타 변경사항 (빌드 설정 등)   |

### 💡 예시

```bash
git commit -m "feat: Todo 목록 조회 API 구현"
git commit -m "fix: 날짜 형식 오류 수정"
git commit -m "docs: README 업데이트"
git commit -m "style: 불필요한 공백 제거"
git commit -m "refactor: view 함수 분리"
git commit -m "test: Todo 생성 테스트 추가"
git commit -m "chore: requirements.txt 정리"
```

---

## 🔑 슈퍼 유저 생성

```bash
python manage.py createsuperuser
```

---

## 👨‍💼 Author

* **코담(Codam)**: \[[https://codam.kr](https://codam.kr)]
