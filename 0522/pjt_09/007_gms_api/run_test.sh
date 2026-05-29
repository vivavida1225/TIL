#!/usr/bin/env bash

echo ""
echo "========================================"
echo "Image Generation API 테스트"
echo "========================================"

URL_IMAGE="http://localhost:8000/api/v1/images/generations"
# PROMPT_IMAGE="귀여운 고양이가 해변에 앉아 있는 그림"
PROMPT_IMAGE="귀여운 고양이가 해변에 앉아 있는 그림"

echo "$URL_IMAGE 요청"
echo "prompt: $PROMPT_IMAGE"
echo "----------------------------------------"

RESPONSE=$(curl -s -X POST "$URL_IMAGE" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "prompt": "$PROMPT_IMAGE"
}
EOF
)

IMAGE_URL=$(printf "%s" "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('url', ''))")

if [ -z "$IMAGE_URL" ]; then
  echo "image url 추출 실패"
  echo "raw response:"
  echo "$RESPONSE"
  exit 1
fi

echo "image url (preview):"
printf "%.120s\n" "$IMAGE_URL"

case "$IMAGE_URL" in
  data:image/*)
    echo "base64 이미지 감지: generated.png로 저장 후 열기"
    printf "%s" "$IMAGE_URL" | python -c "import sys, base64; s=sys.stdin.read().strip(); b=s.split(',', 1)[1]; open('generated.png', 'wb').write(base64.b64decode(b))"
    powershell.exe -NoProfile -Command "Start-Process -FilePath 'generated.png'" >/dev/null 2>&1
    ;;
  *)
    echo "url 이미지 감지: 브라우저로 열기"
    powershell.exe -NoProfile -Command "Start-Process -FilePath '$IMAGE_URL'" >/dev/null 2>&1
    ;;
esac

echo ""
echo "----------------------------------------"
echo "테스트 완료"

# 상세 설명:
# - 이미지 생성 API를 호출해 응답에서 `url` 값을 꺼낸 뒤 자동으로 열어주는 테스트 스크립트입니다.
# - 응답이 Base64 데이터 URL이면 `generated.png` 파일로 저장 후 이미지 뷰어를 실행합니다.
# - 일반 URL이면 브라우저로 바로 엽니다.
# - 즉, 응답 타입이 달라도 사용자 입장에선 "자동으로 이미지 확인"이 가능하도록 만든 스크립트입니다.