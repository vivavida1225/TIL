from django.urls import path
from .views import chat_view, audio_speech_view

urlpatterns = [
    path("chat", chat_view),
    path("audio/speech", audio_speech_view),
]

# 상세 설명:
# - URL 경로와 view 함수를 연결하는 라우팅 파일입니다.
# - `/chat` 요청은 `chat_view`, `/audio/speech` 요청은 `audio_speech_view`가 처리합니다.