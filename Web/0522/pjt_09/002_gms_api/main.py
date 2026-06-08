from dotenv import load_dotenv
import os
import requests
from pydantic import BaseModel
from fastapi import FastAPI

#.env 파일의 비밀값(API 키 등)을 환경변수를 읽기
load_dotenv(".env")

#읽은 값중에서 꺼내오기
GMS_KEY = os.getenv("GMS_KEY")
GMS_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"

headers = {
    "Authorization": f"Bearer {GMS_KEY}",
    "Accept": "application/json",
}

class ChatRequest(BaseModel):
    messages: list[dict]

class ChatResponse(BaseModel):
    content: str


app = FastAPI()

@app.post("/api/v1/chat", response_model=ChatResponse)
async def get_chat_response(chat_request: ChatRequest):
    messages = chat_request.messages

    payload_data = {"model": "gpt-5-nano", "messages": messages}
    response = requests.post(
        f"{GMS_URL}/chat/completions", headers=headers, json=payload_data
    )
    
    content = response.json()["choices"][0]["message"]["content"]
    return {"content": content}
