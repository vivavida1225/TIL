from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

# 상세 설명:
# - Django 앱(`api`)의 기본 설정 정보를 담는 파일입니다.
# - `name = 'api'`는 앱 이름, `default_auto_field`는 기본 PK 타입 설정입니다.
