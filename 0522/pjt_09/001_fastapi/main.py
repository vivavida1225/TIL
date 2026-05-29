from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


#클라이언트가 보내는 JSON 데이터의 규격을 정의하고, 서버로 들어오기 전에 자동으로 검증
from pydantic import BaseModel


#클라이언트가 본문(Request Body)에 담아 보내야 하는 JSON 데이터의 '명세서(틀)'
class MessageRepeatRequest(BaseModel):
    message: str
    count: int

class MessageRepeatResponse(BaseModel):
    new_message: str
    success: bool

@app.post("/repeat-test", response_model=MessageRepeatResponse)
def repeat_test(request: MessageRepeatRequest):
    message = request.message
    count = request.count

    repeated_message = message * count
    
    return MessageRepeatResponse(
        new_message=repeated_message,
        success=True
    )
