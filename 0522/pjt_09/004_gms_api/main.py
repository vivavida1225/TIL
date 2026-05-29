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
            또한, 해당 이유에 대해서도 reason에 기입한다."""
        },
        {
            "role": "user", "content": f"prompt: {prompt}, answer: {answer}"
        }
    ]
    
    #`response_format`에 JSON Schema를 지정해 "모델 응답 형식"을 더 강하게 고정한 버전
    #즉, 모델이 자유 텍스트가 아니라 `score`, `reason` 키를 가진 JSON만 반환하도록 유도
    #`strict: True`와 `required` 설정은 응답 구조 일관성을 높여 파싱 오류를 줄임

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "score_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "score": {
                        "type": "integer",
                        "description": "질문에 대한 답변 점수를 0점부터 100점 사이로 반환",
                    },
                    "reason": {
                        "type": "string",
                        "description": "score 가 도출된 이유에 대해 간단한 설명",
                    },
                },
                "required": ["score", "reason"],
                "additionalProperties": False,
            },
        },
    }

    payload_data = {"model": "gpt-5-nano", "messages": messages, "response_format": response_format,}
    response = requests.post(
        f"{GMS_URL}/chat/completions", headers=headers, json=payload_data
    )
    res_data = response.json()

    content_str = res_data["choices"][0]["message"]["content"]
    
    result = json.loads(content_str)
    return result

