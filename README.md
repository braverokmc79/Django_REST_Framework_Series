# Django REST Framework series  - DRF 기반

Django REST framework(DRF)를 활용한 간단한 Todo API 예제입니다. 이 프로젝트는 API 설계, 직렬화, 뷰셋, 라우팅 등 Django DRF의 기본을 학습하는 데 초점을 맞춥니다.

---

## 학습 추천: [코담](https://codam.kr/)

### 파이썬·장고 웹개발 | 코담 - 코드에 세상을 담다

[![코담 소개 이미지](https://codam.kr/assets/images/og-image.jpg)](https://codam.kr/)

---

## 🎓 강의 내용

1. Django(DRF) 설정과 모델 구성
2. Django(DRF) 직렬화 및 브라우저 가능한 API
3. Django(DRF) 중첩 직렬화기 및 관계 처리
4. Django(DRF) 서브클래스 직렬화기 & 집계 데이터
5. Django(DRF) django-silk를 활용한 성능 최적화
6. Django(DRF) 제네릭 뷰 (ListAPIView, RetrieveAPIView)
7. Django(DRF) 동적 필터링 - `get_queryset()` 오버라이드
8. Django(DRF) 권한 시스템 및 테스트
9. Django(DRF) APIView 클래스 활용
10. Django(DRF) 데이터 생성 - ListCreateAPIView
11. Django(DRF) 권한 커스터마이징 & VSCode REST Client
12. Django(DRF) JWT 인증 설정 (simplejwt)
13. Django(DRF) 리프레시 토큰 활용
14. Django(DRF) 데이터 수정 및 삭제 처리
15. Django(DRF) drf-spectacular로 API 문서화
16. Django(DRF) django-filter 기반 API 필터링
17. Django(DRF) SearchFilter & OrderingFilter
18. Django(DRF) 사용자 정의 필터 백엔드 작성
19. Django(DRF) PI 페이지네이션 설정
20. Django(DRF) ViewSet & Router 기본 사용법
21. Django(DRF) ViewSet의 필터링과 권한 설정
22. Django(DRF) 관리자 vs 일반 사용자 권한 설정
23. Django(DRF) 중첩 객체 생성 - `create()` 오버라이드
24. Django(DRF) 중첩 객체 수정 - `update()` 활용
25. Django(DRF) ModelSerializer 필드 베스트 프랙티스
26. Django(DRF) Redis 캐싱 적용
27. Django(DRF) Vary 헤더로 캐시 제어
28. Django(DRF) API 쓰로틀링 적용
29. Django(DRF) API 테스트 전략
30. Django(DRF) Celery 비동기 작업 연동
31. Django(DRF) Djoser를 활용한 인증 시스템 구축

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
