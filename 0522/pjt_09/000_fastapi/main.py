from fastapi import FastAPI

app = FastAPI()
#웹 API 서버 앱 객체를 만듬


#브라우저 주소가 / 일 때" 아래 함수를 실행
@app.get("/")
async def root():
    return {"message": "Hello World"}

