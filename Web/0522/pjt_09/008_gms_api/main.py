from dotenv import load_dotenv
import os
import requests
import base64
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

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용. 배포 시엔 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    input: str


class TTSResponse(BaseModel):
    audio_data: str


@app.post("/api/v1/audio/speech", response_model=TTSResponse)
def get_tts_response(tts_request: TTSRequest):
    text = tts_request.input

    payload_data = {
        "model": "gpt-4o-mini-tts",
        "input": text,
        "voice": "nova",
        "response_format": "mp3",
    }

    try:
        if MODE == "GMS":
            response = requests.post(
                f"{GMS_URL}/audio/speech",
                headers=gms_headers,
                json=payload_data,
                timeout=30,
            )
        elif MODE == "OPENAI":
            response = requests.post(
                f"{OPENAI_URL}/audio/speech",
                headers=openai_headers,
                json=payload_data,
                timeout=30,
            )
        else:
            raise ValueError(f"Invalid MODE: {MODE}. Use GMS or OPENAI.")

        response.raise_for_status()
        audio_data = base64.b64encode(response.content).decode("utf-8")
        return {"audio_data": audio_data}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))    

# 상세 설명:
# - 이 파일은 텍스트를 음성으로 바꾸는 TTS API(`/api/v1/audio/speech`)를 제공합니다.
# - 입력으로 받은 문장(`input`)을 외부 TTS 모델(`gpt-4o-mini-tts`)에 보내 mp3 데이터를 받습니다.
# - 받은 바이너리 오디오를 Base64 문자열로 변환해 JSON으로 전달합니다.
# - Base64를 쓰는 이유는 "이진 파일(mp3)"을 HTTP JSON 응답으로 안전하게 보내기 위해서입니다.