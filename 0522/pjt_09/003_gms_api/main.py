from dotenv import load_dotenv
import os
import requests
from pydantic import BaseModel
from fastapi import FastAPI

load_dotenv(".env")

GMS_KEY = os.getenv("GMS_KEY")
GMS_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"

headers = {
    "Authorization": f"Bearer {GMS_KEY}",
    "Accept": "application/json",
}

app = FastAPI()

import json

class ChatScoreRequest(BaseModel):
    prompt: str
    answer: str


class ChatScoreResponse(BaseModel):
    score: int
    reason: str

@app.post("/api/v1/chat/score", response_model=ChatScoreResponse)
def get_chat_score(chat_score_request: ChatScoreRequest):
    prompt = chat_score_request.prompt
    answer = chat_score_request.answer

    messages = [
        {
            "role": "developer",
            "content": """너는 질문 prompt에 대한 답변 answer이 몇 점짜리인지 판단하는 시스템이다.
            질문에 대한 적절한 답변인지의 점수를 0 ~ 100점으로 리턴하라.
            또한, 해당 이유에 대해서도 reason에 기입한다.
            응답은 반드시 json 형식으로 작성해야 한다."""
        },
        {
            "role": "user", "content": f"prompt: {prompt}, answer: {answer}"
        }
    ]

    payload_data = {"model": "gpt-5-nano", "messages": messages}
    response = requests.post(
        f"{GMS_URL}/chat/completions", headers=headers, json=payload_data
    )
    res_data = response.json()

    content_str = res_data["choices"][0]["message"]["content"]
    
    #AI의 답변 문자열 -> 딕셔너리로 변환
    #json.loads 문자열 -> 파이썬객체
    #json.load 파일 -> 파이썬 객체
    result = json.loads(content_str)
    return result