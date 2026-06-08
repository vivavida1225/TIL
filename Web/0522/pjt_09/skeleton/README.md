# 스켈레톤 (교육생 작업용)

이 폴더는 **교육생이 직접 구현할 코드**입니다.  
정답 구현은 `server/proxy/`(Django 중간 서버), `server/openai/`(FastAPI 모델 서버)에 있습니다.

## proxy (Django 중간 서버)

- **위치**: `skeleton/proxy/`
- **실행**: `server/skeleton/proxy` 폴더에서 `python manage.py runserver 0.0.0.0:8080`
- **구현할 곳**:
  - `proxies/views.py` — 나머지 뷰에서 serializer 검증 후 services 호출, 응답 반환 (chat_response 는 예시)
  - `proxies/services.py` — 나머지 서비스에서 `MODEL_SERVER_URL` 로 HTTP POST 후 응답 파싱 반환 (get_chat_response 는 예시)

`.env` 에 `MODEL_SERVER_URL="http://localhost:8081/api/v1/openai"` 설정 후, FastAPI 모델 서버(openai)를 8081에서 먼저 실행한 뒤 Django를 실행하세요.
