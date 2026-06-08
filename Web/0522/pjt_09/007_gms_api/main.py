from dotenv import load_dotenv
import os
import requests
from pydantic import BaseModel
from fastapi import FastAPI,HTTPException

load_dotenv(".env")

GMS_KEY = os.getenv("GMS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GMS_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"
OPENAI_URL = "https://api.openai.com/v1"
MODE = os.getenv("MODE", "GMS")

headers = {
    "Authorization": f"Bearer {GMS_KEY}",
    "Accept": "application/json",
}

gms_headers = {
    "Authorization": f"Bearer {GMS_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

openai_headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
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
    response = requests.post(f"{GMS_URL}/chat/completions", headers=headers, json=payload_data)
    res_data = response.json()

    content_str = res_data["choices"][0]["message"]["content"]
    
    result = json.loads(content_str)
    return result




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




class ImageGenerationRequest(BaseModel):
    prompt: str


class ImageGenerationResponse(BaseModel):
    url: str


@app.post("/api/v1/images/generations", response_model=ImageGenerationResponse)
def get_image_generation_response(image_generation_request: ImageGenerationRequest):
    prompt = image_generation_request.prompt

    payload_data = {
        "model": "gpt-image-1-mini",
        "prompt": prompt,
        "size": "1024x1024",
    }

    try:
        if MODE == "GMS":
            response = requests.post(
                f"{GMS_URL}/images/generations",
                headers=gms_headers,
                json=payload_data,
                timeout=60,
            )
        elif MODE == "OPENAI":
            response = requests.post(
                f"{OPENAI_URL}/images/generations",
                headers=openai_headers,
                json=payload_data,
                timeout=60,
            )
        else:
            raise ValueError(f"Invalid MODE: {MODE}. Use GMS or OPENAI.")
        res_json = response.json()
        if "data" in res_json and len(res_json["data"]) > 0:
            image_obj = res_json["data"][0]
            
            # 1. url이 있는지 먼저 확인
            if "url" in image_obj:
                return {"url": image_obj["url"]}
            
            # 2. url이 없고 b64_json이 있다면 (지금 상황)
            elif "b64_json" in image_obj:
                # 웹 브라우저가 인식할 수 있는 데이터 URL 형태로 가공합니다.
                b64_data = image_obj["b64_json"]
                image_url = f"data:image/png;base64,{b64_data}"
                return {"url": image_url}

        # 둘 다 없으면 에러 출력
        print(f"이미지 데이터 추출 실패! 응답 구조: {res_json.keys()}")
        raise HTTPException(status_code=500, detail="이미지 데이터를 찾을 수 없습니다.")
        url = response.json()["data"][0]["url"]
        return {"url": "hello"}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    



# 상세 설명:
# - 이 버전은 이미지 생성 API(`/api/v1/images/generations`)를 추가한 단계입니다.
# - `MODE` 값을 통해 GMS/OpenAI 중 어떤 백엔드를 쓸지 분기합니다.
# - 응답이 URL 방식일 수도, Base64(`b64_json`) 방식일 수도 있어 둘 다 처리합니다.
# - Base64인 경우 `data:image/png;base64,...` 형태로 바꿔 프론트/브라우저에서 바로 표시 가능하게 합니다.
# - 외부 API 호출 실패 시 `HTTPException(500)`으로 에러를 명확히 반환합니다.
