echo "/repeat-test POST 요청"

# curl -X POST "http://127.0.0.1:8000/repeat-test" -H "Content-Type: application/json" -d '{"message": "hi", "count": 3}'

curl -d '{"message": "hi", "count": 3}' -H "Content-Type: application/json" "http://127.0.0.1:8000/repeat-test"

# 상세 설명:
# - `-d`는 서버로 보낼 본문(body) 데이터를 의미합니다.
# - 여기서는 JSON 문자열 `{"message":"hi","count":3}`를 전송합니다.
# - `-H "Content-Type: application/json"`은 "지금 보내는 데이터가 JSON"이라고 서버에 알려줍니다.
# - URL 끝의 `/repeat-test`는 서버 코드에서 만든 POST 엔드포인트와 정확히 일치해야 합니다.