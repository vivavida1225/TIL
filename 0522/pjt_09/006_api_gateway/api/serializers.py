# serializers.py

from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    messages = serializers.ListField(
        child=serializers.DictField()
    )


class ChatResponseSerializer(serializers.Serializer):
    content = serializers.CharField()

# 상세 설명:
# - Serializer는 API 입력/출력 데이터의 "형식 검증기 + 변환기" 역할을 합니다.
# - `ChatRequestSerializer`는 요청에 `messages` 리스트가 있는지 검사합니다.
# - `ChatResponseSerializer`는 응답에 `content` 문자열이 있는지 검사합니다.