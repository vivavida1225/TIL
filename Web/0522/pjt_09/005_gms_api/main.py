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

class GuardrailRequest(BaseModel):
    prompt: str


class GuardrailResponse(BaseModel):
    result: bool
    reason: str

@app.post("/api/v1/chat/guardrail", response_model=GuardrailResponse)
def get_guardrail_response(guardrail_request: GuardrailRequest):
    prompt = guardrail_request.prompt

    system_content = """
        너는 질문 prompt 가 적절한지 판단하는 Guardrail 이다.
        질문이 적절한지 여부를 result 에 boolean 으로 응답하라.
        기준은 선정성과 법률 위배 가능성이다.
        그리고 그렇게 판단한 이유를 reason 에 기입하라.
    """
    messages = [
        {"role": "developer", "content": system_content},
        {"role": "user", "content": f"prompt: {prompt}"},
    ]

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "guardrail_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": "boolean",
                        "description": "사용자의 prompt 가 적절한지 여부",
                    },
                    "reason": {
                        "type": "string",
                        "description": "result 가 도출된 이유",
                    },
                },
                "required": ["result", "reason"],
                "additionalProperties": False,
            },
        },
    }

    payload_data = {"model": "gpt-5-nano", "messages": messages, "response_format": response_format}


    response = requests.post(f"{GMS_URL}/chat/completions",headers=headers, json=payload_data)

    result_dict = json.loads(response.json()["choices"][0]["message"]["content"])
    result = result_dict["result"]
    reason = result_dict["reason"]
    return {"result": result, "reason": reason}

