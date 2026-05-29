from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json      # 최상단으로 이동
import requests

# .env 파일의 환경변수 읽기
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

app = FastAPI()

# --- Pydantic 스키마 정의 ---

class ChatRequest(BaseModel):
    messages: list[dict]

class ChatResponse(BaseModel):
    content: str

class ChatScoreRequest(BaseModel):
    prompt: str
    answer: str

class ChatScoreResponse(BaseModel):
    score: int
    reason: str

class GuardrailRequest(BaseModel):
    prompt: str

class GuardrailResponse(BaseModel):
    result: bool
    reason: str

class ImageGenerationRequest(BaseModel):
    prompt: str

class ImageGenerationResponse(BaseModel):
    url: str


# --- API 엔드포인트 구현 ---

# [F103] 1. 텍스트 대화 API (이벤트 루프 병목 방지를 위해 def로 변경)
@app.post("/api/v1/chat", response_model=ChatResponse)
def get_chat_response(chat_request: ChatRequest):
    messages = chat_request.messages

    payload_data = {"model": "gpt-5-nano", "messages": messages}
    response = requests.post(
        f"{GMS_URL}/chat/completions", headers=headers, json=payload_data
    )
    
    content = response.json()["choices"][0]["message"]["content"]
    return {"content": content}


# 2. 답변 점수 채점 API
@app.post("/api/v1/chat/score", response_model=ChatScoreResponse)
def get_chat_score(chat_score_request: ChatScoreRequest):
    prompt = chat_score_request.prompt
    answer = chat_score_request.answer

    messages = [
        {
            "role": "developer",
            "content": (
                "너는 질문 prompt에 대한 답변 answer이 몇 점짜리인지 판단하는 시스템이다. "
                "질문에 대한 적절한 답변인지의 점수를 0 ~ 100점으로 리턴하라. "
                "또한, 해당 이유에 대해서도 reason에 기입한다."
            )
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

    payload_data = {"model": "gpt-5-nano", "messages": messages, "response_format": response_format}
    response = requests.post(f"{GMS_URL}/chat/completions", headers=headers, json=payload_data)
    res_data = response.json()

    content_str = res_data["choices"][0]["message"]["content"]
    return json.loads(content_str)


# [F102] 3. Guardrail API (프록시 서버가 내부적으로 체킹할 원본 API)
@app.post("/api/v1/chat/guardrail", response_model=GuardrailResponse)
def get_guardrail_response(guardrail_request: GuardrailRequest):
    prompt = guardrail_request.prompt

    system_content = """
        너는 질문 prompt 가 적절한지 판단하는 Guardrail 이다.
        질문에 적절한지 여부를 result 에 boolean 으로 응답하라.
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
    response = requests.post(f"{GMS_URL}/chat/completions", headers=headers, json=payload_data)

    result_dict = json.loads(response.json()["choices"][0]["message"]["content"])
    return {"result": result_dict["result"], "reason": result_dict["reason"]}


# [F105] 4. 이미지 생성 API (죽은 코드 정리 및 흐름 개선)
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
        
        # 데이터가 정상적으로 들어온 경우 파싱 후 즉시 리턴
        if "data" in res_json and len(res_json["data"]) > 0:
            image_obj = res_json["data"][0]
            
            # URL 형태인 경우
            if "url" in image_obj:
                return {"url": image_obj["url"]}
            
            # Base64 문자열 형태인 경우 데이터 URL 형식으로 변환
            elif "b64_json" in image_obj:
                b64_data = image_obj["b64_json"]
                return {"url": f"data:image/png;base64,{b64_data}"}

        # 파싱 실패 혹은 데이터 유실 시 에러 로그 출력 후 HTTPException 반환
        print(f"이미지 데이터 추출 실패! 응답 구조: {res_json.keys()}")
        raise HTTPException(status_code=500, detail="이미지 데이터를 찾을 수 없습니다.")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))