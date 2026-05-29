#!/bin/bash
# FastAPI Chat API 테스트 스크립트

echo ""
echo "========================================"
echo "Chat Score API 테스트"
echo "========================================"

URL_SCORE="http://localhost:8000/api/v1/chat/score"
PROMPT="1+1은?"
ANSWER="2입니다."

echo "$URL_SCORE 요청"
echo "prompt: $PROMPT, answer: $ANSWER"
echo "----------------------------------------"

curl -X POST "$URL_SCORE" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "prompt": "$PROMPT",
  "answer": "$ANSWER"
}
EOF