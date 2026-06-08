URL="http://localhost:8000/api/v1/chat/score"

PROMPT="FastAPI의 장점에 대해 설명해줘."
ANSWER="FastAPI는 파이썬 기반의 현대적이고 빠른 웹 프레임워크로, 자동 문서화와 빠른 성능이 장점입니다."

echo "URL 요청: $URL"
echo "질문(Prompt): $PROMPT"
echo "답변(Answer): $ANSWER"
echo "----------------------------------------"

curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "prompt": "$PROMPT",
  "answer": "$ANSWER"
}
EOF
