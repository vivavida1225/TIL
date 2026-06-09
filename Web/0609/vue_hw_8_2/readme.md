### 처음에 구버전 패키지 밀고 신버전으로 바꿔야 실행됨

```bash
rm -rf node_modules package-lock.json
npx npm-check-updates -u
npm install
npm i vue-router
```

### settings.py 설정

```python
INSTALLED_APPS = [
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173'
]
```