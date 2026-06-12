# 12-pjt
### 👥 팀원: 최현규, 김근영
### ✈️ 주제: 관심 종목 영상 검색 서비스 (여행 영상 추천) — "야무짐"

---

# 🛫 야무짐 (YAMUZIM) — 여행 준비 & 맞춤 영상 추천 플래너

**야무짐**은 사용자의 여행 정보(여행지, 도시, 출발 날짜)를 기반으로  
**관련 YouTube 영상을 자동 추천**하고, 마음에 드는 영상을 저장·관리할 수 있는 통합 여행 플래닝 웹 애플리케이션입니다.

---

## 🏗️ 시스템 아키텍처

```
사용자
 ├── Kakao 소셜 로그인
 ├── 추가 프로필 입력 (닉네임, 성별, 생년월일)
 ├── 4단계 취향 진단 설문
 ├── 여행 일정 등록 (국가, 도시, 기간)
 │     └── [영상 추천] 버튼 클릭
 │           ↓
 │     Django: 여행지 + 계절 → 검색어 자동 생성
 │           ↓
 │     Vue.js + YouTube Data API v3: 영상 자동 검색 & 렌더링
 │           ↓
 │     영상 클릭 → 상세 페이지 (iframe 재생)
 │           ↓
 │     동영상 저장 / 채널 저장 (localStorage)
 └── 커뮤니티 게시판 (여행 계획 공유, 팔로우 네트워크)
```

---

## ⚡ 구현 기능 명세

### ✅ 필수 기능 (F12xx)

#### F1201 — 동영상 검색결과 출력
- 여행 일정의 여행지(국가·도시)와 출발 월에서 **계절을 자동 도출**해 검색어를 생성
- 예) 도쿄·오사카 7월 여행 → `"도쿄 여름 여행"`, `"오사카 관광지 볼거리"`, `"일본 여행 추천"` 등 자동 생성
- 상단 칩(chip) 버튼으로 추천 검색어 1-click 전환 가능
- 직접 검색어 입력 박스도 제공 (Enter / 찾기 버튼)
- `https://www.googleapis.com/youtube/v3/search` 엔드포인트 사용
- 결과를 썸네일·제목·채널명 카드 그리드로 출력 (`VideoCard` 컴포넌트)

#### F1202 — 동영상 상세 정보 출력
- 카드 클릭 시 `/travel/videos/detail/<video_id>/` 상세 페이지 이동
- `<iframe>` 임베드로 영상 직접 재생
- `https://www.googleapis.com/youtube/v3/videos` 엔드포인트로 제목·채널명·설명·업로드일 표시

#### F1203 — 나중에 볼 영상 저장/삭제
- 상세 페이지 **"동영상 저장"** 버튼 → `localStorage` 에 ID·제목·썸네일 저장
- 이미 저장된 영상은 **"저장 취소"** 버튼으로 변경
- `/travel/videos/saved/` 페이지에서 저장 목록 확인·삭제
- 저장 영상 없을 경우 **"등록된 비디오 없음"** 안내 표시

#### F1204 — 좋아하는 채널 저장/삭제
- 상세 페이지 **"채널 저장"** 버튼 → `localStorage` 에 채널 ID·이름 저장
- `/travel/videos/channels/` 페이지에서 저장 채널 목록 확인·삭제
- 저장 채널 없을 경우 **"등록된 채널 없음"** 안내 표시
- 네비게이션 바에 "볼 영상" / "채널" 바로가기 링크 추가

#### NF1201 — API Key 보안 관리
- YouTube API Key는 `config/.env` 파일에서 환경변수로 관리
- `.gitignore` 에 `.env`, `config/.env` 추가 → 키 노출 방지

#### NF1203 — 컴포넌트화
- Vue.js 3 Composition API 기반 컴포넌트 구조 설계
- 검색 페이지 / 상세 페이지 / 저장 목록 페이지 분리
- Django 템플릿과 Vue.js의 역할 명확히 분리 (`{% verbatim %}` 블록 활용)

---

### 🔧 기존 기능 (Phase 1~4)

| Phase | 기능 |
|-------|------|
| Phase 1 | Kakao OAuth 2.0 소셜 로그인, 추가 프로필 입력, 4단계 취향 진단 설문 |
| Phase 2 | 30개국·도시 자동완성 여행 플랜 등록, 의존적 필터링, 기간 유효성 검증 |
| Phase 3 | 커뮤니티 게시판, 댓글, 비동기 AJAX 좋아요/스크랩 |
| Phase 4 | 비대칭 팔로우 네트워크, 사용자 프로필 대시보드 |

---

## 🎨 기술 스택

| 구분 | 기술 |
|------|------|
| Back-end | Python 3.11+, Django 5.2, SQLite3 |
| Front-end | Vue.js 3 (CDN, Composition API), Vanilla JS (ES6+) |
| API 통신 | Axios 1.7, YouTube Data API v3 |
| 인증 | Kakao OAuth 2.0 REST API |
| 스타일 | Glassmorphism CSS, FontAwesome 6, Google Fonts |
| 데이터 저장 | Django ORM (여행/계정), localStorage (영상·채널 즐겨찾기) |

---

## ⚙️ 실행 가이드

### 1. 패키지 설치
```bash
pip install django python-dotenv requests
```

### 2. 환경변수 설정
`config/.env` 파일을 생성하고 아래 내용을 채웁니다:
```env
KAKAO_REST_API_KEY=카카오_REST_API_키
KAKAO_LOGIN_CLIENT_SECRET=카카오_클라이언트_시크릿
YOUTUBE_API_KEY=유튜브_DATA_API_v3_키
```

- **Kakao API Key**: [카카오 개발자 콘솔](https://developers.kakao.com) → 앱 키 > REST API 키
- **YouTube API Key**: [Google Cloud Console](https://console.cloud.google.com) → YouTube Data API v3 사용 설정 → 사용자 인증 정보 > API 키

### 3. DB 초기화 및 서버 실행
```bash
python manage.py migrate
python manage.py runserver
```

### 4. 사용 흐름
1. `http://127.0.0.1:8000` 접속
2. 카카오 로그인 → 프로필 입력 → 취향 설문
3. 여행 일정 등록 (국가, 도시, 날짜)
4. 홈 화면 여행 카드의 **"영상 추천"** 버튼 클릭
5. 자동 생성된 검색어로 YouTube 영상 탐색
6. 영상 저장 / 채널 저장 후 상단 네비게이션에서 관리

---

## 📁 디렉터리 구조

```
10-pjt/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── .env               ← API 키 (gitignored)
├── accounts/              ← 로그인, 프로필, 팔로우
├── travel/
│   ├── models.py          ← Country, City, Travel
│   ├── views.py           ← 여행 CRUD + 영상 추천 뷰
│   └── urls.py
├── community/             ← 게시판, 댓글, 좋아요
├── templates/
│   ├── base.html
│   ├── index.html
│   └── travel/
│       ├── travel_videos.html    ← 영상 추천 (Vue.js 3)
│       ├── video_detail.html     ← 상세 재생 (iframe + 저장)
│       ├── saved_videos.html     ← 나중에 볼 영상
│       └── saved_channels.html  ← 저장된 채널
└── mytube/                ← 독립 실행형 Vue SPA (참고용)
```

---

## 📚 학습 내용

### Vue.js 3 Composition API
- `ref`, `computed`, `onMounted` 를 사용한 반응형 상태 관리
- Django 템플릿 문법(`{{ }}`)과 Vue.js 보간법 충돌 해결 → `{% verbatim %}` 블록 활용
- Django에서 Python 데이터를 `json.dumps()` 로 직렬화하여 JavaScript 전역 변수로 주입

### YouTube Data API v3
- `search` 엔드포인트: 키워드 검색, `type=video`, `relevanceLanguage=ko` 파라미터
- `videos` 엔드포인트: 비디오 ID로 상세 정보(snippet) 조회
- API 응답 구조 분석: `items[].id.videoId`, `items[].snippet.*`

### 비동기 처리 (Axios)
- `async/await` 패턴으로 API 호출 및 에러 핸들링
- 로딩 상태(`loading.value`) 관리로 UX 개선

### localStorage 활용
- 브라우저 localStorage에 JSON 직렬화하여 영상·채널 영구 저장
- `computed`로 저장 상태 실시간 반영, 토글 방식 저장/삭제 구현

### 환경변수 보안 관리
- `python-dotenv` 로 `.env` 파일 로드
- `.gitignore` 에 API 키 파일 추가하여 외부 유출 방지

---

## 💭 느낀 점 & 개선점

### 느낀 점
- Django 서버 사이드 렌더링과 Vue.js 클라이언트 사이드 렌더링을 **하나의 프로젝트에서 혼합**하는 방식이 흥미로웠다. 각자의 역할을 분리하는 것이 핵심이었다.
- 여행 날짜에서 계절을 자동 계산하고, 여행지 기반 검색어를 생성하는 로직을 구현하면서 **사용자 데이터를 의미 있게 가공하는** 경험을 할 수 있었다.
- `{% verbatim %}` 태그를 통해 Django 템플릿 엔진과 Vue.js 템플릿 문법 충돌을 해결하는 방법을 배웠다.

### 개선점
- **검색어 품질 향상**: 사용자 취향 데이터(맛집 선호, 액티비티 선호 등)를 검색어에 반영하면 더 개인화된 추천이 가능할 것이다.
- **YouTube API 할당량 관리**: 무료 플랜 하루 할당량(10,000 units)을 고려한 캐싱 또는 요청 최소화 전략이 필요하다.
- **localStorage 동기화**: 여러 탭에서 저장 목록이 즉시 동기화되지 않는 한계가 있다. 서버 사이드 DB 저장으로 개선 여지가 있다.
- **페이지네이션**: 검색 결과가 12개로 고정되어 있어, 더 보기(load more) 기능을 추가하면 탐색 UX가 향상될 것이다.

---

*Powered by YAMUZIM × YouTube Data API v3 × Vue.js 3*
