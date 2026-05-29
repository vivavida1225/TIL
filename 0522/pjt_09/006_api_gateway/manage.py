#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_gateway.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# 상세 설명:
# - `manage.py`는 Django 프로젝트의 "명령 실행 진입점" 파일입니다.
# - 예: `python manage.py runserver`, `python manage.py migrate` 같은 명령을 처리합니다.
# - `DJANGO_SETTINGS_MODULE`을 설정해 어떤 설정 파일을 사용할지 Django에 알려줍니다.
