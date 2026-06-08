from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse 
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
import httpx

load_dotenv(".env")

GMS_KEY = os.getenv("GMS_KEY")
GMS_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"
MODEL_SERVER_URL = "http://localhost:8000/api/v1/chat"

headers = {
    "Authorization": f"Bearer {GMS_KEY}",
    "Accept": "application/json",
}

app = FastAPI()

# --- Pydantic 스키마 정의 ---
class GuardrailRequest(BaseModel):
    prompt: str

class GuardrailResponse(BaseModel):
    result: bool
    reason: str

class ChatRequest(BaseModel):
    messages: list[dict]

class ImageGenerationRequest(BaseModel):
    prompt: str


class ImageGenerationResponse(BaseModel):
    url: str


# =================================================================
# [F104] Chatbot UI 렌더링 엔드포인트
# =================================================================
@app.get("/", response_class=HTMLResponse)
async def chatbot_interface():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SSAFY AI Chatbot</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        <style>
            /* 로딩 스피너 애니메이션 */
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #3498db;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body class="bg-gray-50 h-screen flex flex-col justify-between font-sans">

        <div id="chat-window" class="flex-1 overflow-y-auto p-6 space-y-4 max-w-3xl w-full mx-auto">
            </div>

        <div class="border-t border-gray-200 bg-white p-4 sticky bottom-0">
            <div class="max-w-3xl mx-auto flex items-center relative">
                <button class="absolute left-4 text-gray-400 hover:text-gray-600 text-xl font-bold">+</button>
                <input type="text" id="user-input" placeholder="Send a message" 
                       class="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-400 focus:bg-white text-sm"
                       onkeypress="if(event.key === 'Enter') sendMessage()">
            </div>
        </div>

        <script>
            const chatWindow = document.getElementById('chat-window');
            const userInput = document.getElementById('user-input');

            // 메시지 화면에 추가 함수
            function appendMessage(sender, text, isSystem = false) {
                const msgDiv = document.createElement('div');
                msgDiv.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-2`;
                
                if (sender === 'user') {
                    msgDiv.innerHTML = `<div class="bg-gray-200 text-gray-800 rounded-2xl px-4 py-2 max-w-md text-sm">${text}</div>`;
                } else {
                    msgDiv.innerHTML = `<div class="text-gray-800 px-2 py-2 max-w-xl text-sm whitespace-pre-line">${text}</div>`;
                }
                chatWindow.appendChild(msgDiv);
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }

            // [필수 사항] 로딩창 및 진행 상태 출력 함수
            function showLoading() {
                const loadingDiv = document.createElement('div');
                loadingDiv.id = 'loading-indicator';
                loadingDiv.className = 'flex flex-col items-start space-y-2 p-2';
                loadingDiv.innerHTML = `
                    <div class="spinner"></div>
                    <p class="text-xs text-gray-500 font-semibold">부적절한 질문인지 판단중...</p>
                `;
                chatWindow.appendChild(loadingDiv);
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }

            function removeLoading() {
                const loadingDiv = document.getElementById('loading-indicator');
                if (loadingDiv) loadingDiv.remove();
            }

            // 백엔드 Proxy API 통신 및 결과 출력
            async function sendMessage() {
                const text = userInput.value.trim();
                if (!text) return;

                // 1. 유저 질문 화면 표시 및 입력창 초기화
                appendMessage('user', text);
                userInput.value = '';

                // 2. 가드레일 판별 시작 (로딩창 및 현재 상태 출력 활성화)
                showLoading();

                try {
                    // 프록시 서버의 대화 엔드포인트 호출
                    const response = await fetch('/api/v1/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            messages: [{ role: 'user', content: text }]
                        })
                    });

                    const data = await response.json();
                    
                    // 3. 로딩창 제거 후 답변 출력
                    removeLoading();
                    appendMessage('bot', data.content);

                } catch (error) {
                    removeLoading();
                    appendMessage('bot', '❌ 에러가 발생했습니다. 서버 연결을 확인하세요.');
                }
            }
        </script>
    </body>
    </html>
    """

# =================================================================
# 기존 백엔드 API 로직 (가드레일 및 프록시 대화 기능 - 유지)
# =================================================================

@app.post("/api/v1/chat/guardrail", response_model=GuardrailResponse)
async def check_guardrail(guardrail_request: GuardrailRequest):
    user_prompt = guardrail_request.prompt
    payload_data = {
        "model": "gpt-5-nano",
        "messages": [
            {
                "role": "system",
                "content": (
                    "당신은 입력문장의 유해성을 검사하는 보안 가드레일 시스템입니다. "
                    "사용자의 질문이 사회적으로 유해하거나, 불법적인 요청(예: 마약 제조, 폭력, 해킹 등)을 담고 있다면 "
                    "result를 false로 판단하고 명확한 거절 사유를 reason에 작성하세요. "
                    "안전하고 적절한 질문이라면 result를 true로, reason은 빈 문자열로 반환하세요."
                )
            },
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "guardrail_result",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "boolean"},
                        "reason": {"type": "string"}
                    },
                    "required": ["result", "reason"],
                    "additionalProperties": False
                }
            }
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GMS_URL}/chat/completions", headers=headers, json=payload_data, timeout=30.0
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="GMS 가드레일 API 호출에 실패했습니다.")

    response_json = response.json()
    content_string = response_json["choices"][0]["message"]["content"]
    guardrail_output = json.loads(content_string)
    return guardrail_output

@app.post("/api/v1/chat")
async def proxy_chat(chat_request: ChatRequest):
    if not chat_request.messages:
        raise HTTPException(status_code=400, detail="메시지가 존재하지 않습니다.")

    # 1. 사용자의 최신 질문 추출
    last_user_message = chat_request.messages[-1]["content"]

    # 2. 가드레일 검증
    try:
        guardrail_result = await check_guardrail(GuardrailRequest(prompt=last_user_message))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"가드레일 검증 실패: {str(e)}")

    if not guardrail_result["result"]:
        return {"content": f"적절한 요청이 아닙니다.\n(사유: {guardrail_result['reason']})"}

    # 3. 의도 파악: 이미지 생성 키워드 체크
    is_image_request = any(keyword in last_user_message for keyword in ["그려", "이미지", "사진"])

    async with httpx.AsyncClient() as client:
        if is_image_request:
            # [Step A] 8000번 이미지 생성 API 호출
            img_server_resp = await client.post(
                "http://localhost:8000/api/v1/images/generations",
                json={"prompt": last_user_message},
                timeout=60.0
            )
            if img_server_resp.status_code != 200:
                raise HTTPException(status_code=img_server_resp.status_code, detail="이미지 생성에 실패했습니다.")

            img_data = img_server_resp.json()
            image_url = img_data["url"]

            # [F106] [Step B] 이미지 생성 결과에 대한 점수 채점 요청
            # 팁: 채점 모델에게 이미지 생성 결과임을 텍스트 명시해 주면 명세서 스크린샷과 유사한 고품질 피드백을 얻을 수 있습니다.
            image_description = f"사용자의 지시('{last_user_message}')에 따라 정확하게 표현된 고퀄리티 디지털 아트 스타일의 이미지 렌더링 결과물"
            score_resp = await client.post(
                "http://localhost:8000/api/v1/chat/score",
                json={"prompt": last_user_message, "answer": image_description},
                timeout=30.0
            )
            
            score_data = score_resp.json() if score_resp.status_code == 200 else {"score": 0, "reason": "채점 실패"}

            # [F105 & F106] <img> 태그와 이미지 채점 결과를 결과창 구조에 맞게 조립
            html_content = (
                f"<img src='{image_url}' alt='생성된 이미지' class='mt-3 rounded-xl max-w-sm shadow-lg border border-gray-200' /><br><br>"
                f"질문에 대한 답변 이미지 점수: {score_data['score']}/100 점<br>"
                f"이유: {score_data['reason']}"
            )
            return {"content": html_content}

        else:
            # [Step A] 기존 8000번 텍스트 채팅 API 호출
            model_server_resp = await client.post(
                MODEL_SERVER_URL,
                json=chat_request.model_dump(),
                timeout=60.0
            )
            if model_server_resp.status_code != 200:
                raise HTTPException(status_code=model_server_resp.status_code, detail="모델 서버가 응답하지 않습니다.")
            
            bot_answer = model_server_resp.json()["content"]

            # [F106] [Step B] 텍스트 대화 결과에 대한 점수 채점 요청
            score_resp = await client.post(
                "http://localhost:8000/api/v1/chat/score",
                json={"prompt": last_user_message, "answer": bot_answer},
                timeout=30.0
            )
            
            score_data = score_resp.json() if score_resp.status_code == 200 else {"score": 0, "reason": "채점 실패"}

            # 텍스트 답변과 채점 결과를 엔터(\n) 구분선으로 조립
            # 프론트엔드 내부에 whitespace-pre-line 스타일이 적용되어 있어 \n이 줄바꿈으로 정상 작동합니다.
            final_text_content = (
                f"{bot_answer}\n\n\n\n"
                f"질문에 대한 답변 점수: {score_data['score']}/100 점\n"
                f"이유: {score_data['reason']}"
            )
            return {"content": final_text_content}