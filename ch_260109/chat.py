from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import secrets
import string
import random
app = FastAPI()

# CORS 설정 (브라우저 보안 정책 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 설정 (public 폴더 내의 index.html 등을 서빙)
app.mount("/public", StaticFiles(directory="public", html=True), name="public")

# 전역 메시지 저장소
messages = []  # 구조: {"sender": "...", "text": "...", "time": "..."}

def create_chat_id():
    # 8자리의 영문+숫자 혼합 아이디 생성
    pool = string.ascii_letters + string.digits
    return "".join(secrets.choice(pool) for _ in range(8))

def create_chat_nickname():
    #  형용사 + 명사 조합 (닉네임 방식)
    adjectives = ["행복한", "빠른", "조용한", "푸른", "빛나는", "에쁜", "어둠", "귀여운"]
    nouns = ["사자", "고래", "구름", "별빛", "호랑이", "병아리", "참새", "코알라", "오리"]
    
    adj = random.sample(adjectives, 1)
    noun = random.sample(nouns, 1)
    num = random.randint(10, 1000)
    
    return f"{adj[0]}{noun[0]}{num}"

@app.get("/")
def root():
    return {"message": "Chat Server is Running", "status code": 200}

# 1. 메시지 받기 (클라이언트가 서버로 전송)
@app.get("/receive")
def receive(sender: str = Query(...), message: str = Query(...)):
    now = datetime.now().strftime("%H:%M")
    new_msg = {"sender": sender, "text": message, "time": now}
    messages.append(new_msg)
    return {"status": "success", "msg": new_msg}

# 2. 메시지 보내기 (서버가 클라이언트에 새 메시지 전달)
@app.get("/send")
def send(size: int = Query(0)):
    # 클라이언트가 가진 메시지 개수(size) 이후의 새로운 메시지만 반환
    new_messages = messages[size:]
    return {
        "new_messages": new_messages,
        "total_size": len(messages)
    }
    
@app.get("/get-id")
async def get_id():
    return {"random_id": create_chat_nickname()}