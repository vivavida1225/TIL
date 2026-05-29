"""
ASGI config for api_gateway project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_gateway.settings')

application = get_asgi_application()

# 상세 설명:
# - ASGI 서버(Uvicorn, Daphne 등)로 Django를 실행할 때 사용하는 진입 파일입니다.
# - 비동기 통신(WebSocket 등)과 궁합이 좋은 실행 방식에서 사용됩니다.
