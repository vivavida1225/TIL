# views.py

import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatRequestSerializer, ChatResponseSerializer


@api_view(["POST"])
def chat_view(request):
    # 요청 데이터 검증
    serializer = ChatRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    messages = serializer.validated_data["messages"]

    payload_data = {
        "messages": messages
    }

    try:
        model_response = requests.post(
            f"{settings.MODEL_SERVER_URL}/chat",
            json=payload_data
        )
        model_response.raise_for_status()
    except requests.RequestException as e:
        return Response(
            {"error": "Model server request failed"},
            status=status.HTTP_502_BAD_GATEWAY
        )

    content = model_response.json().get("content")

    response_serializer = ChatResponseSerializer(data={"content": content})
    response_serializer.is_valid(raise_exception=True)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def audio_speech_view(request):
    """TTS 요청을 gms_api(모델 서버)로 프록시"""
    try:
        model_response = requests.post(
            f"{settings.MODEL_SERVER_URL}/audio/speech",
            json=request.data,
            timeout=60,
        )
        model_response.raise_for_status()
        return Response(model_response.json(), status=model_response.status_code)
    except requests.RequestException:
        return Response(
            {"error": "Model server request failed"},
            status=status.HTTP_502_BAD_GATEWAY,
        )