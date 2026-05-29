#!/bin/bash
# FastAPI Chat API 테스트 스크립트

URL="http://localhost:8000/api/v1/chat"

MESSAGE="안녕, 간단히 자기소개 해줘"

echo "$URL 요청"
echo "메시지: $MESSAGE"
echo "----------------------------------------"

curl -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "messages": [
    {"role": "user", "content": "$MESSAGE"}
  ]
}
EOF

# 상세 설명:
# - `#!/bin/bash`는 이 파일을 bash 셸 스크립트로 실행하겠다는 선언입니다.
# - `URL`, `MESSAGE` 변수에 값을 넣어두면 재사용이 쉬워집니다.
# - `<<EOF ... EOF`는 여러 줄 JSON을 curl에 그대로 넘기기 위한 문법(Here Document)입니다.
# - 이 스크립트를 실행하면 서버 `/api/v1/chat` 엔드포인트가 정상 동작하는지 빠르게 확인할 수 있습니다.
