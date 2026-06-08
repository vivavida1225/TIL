#!/bin/bash
# API Gateway Chat API 테스트 스크립트

BASE_URL="http://localhost:8001"
URL="$BASE_URL/api/v1/chat"
MESSAGE="안녕, 간단히 자기소개 해줘"

echo "API Gateway 테스트: $URL"
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

echo ""
echo "----------------------------------------"
echo "테스트 완료"
