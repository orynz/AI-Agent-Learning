from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# (선택) public 폴더의 정적 파일 제공
# http://127.0.0.1:8000/public/count.html 로 접속 가능
app.mount("/public", StaticFiles(directory="public", html=True), name="public")

# (선택) 다른 포트(예: Live Server, Tomcat 등)에서 HTML을 띄우고 호출할 때 필요합니다.
# 같은 FastAPI에서 HTML을 제공하면 사실상 없어도 되지만, 실습 편의상 열어둡니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status_code": "200 OK"}

server_cnt = 0
@app.get("/count")
def requestCount():
    global server_cnt
    server_cnt += 1
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    return {
        "now": now,
        "count" : server_cnt
    }

@app.get("/update")
def update():
    global server_cnt
    
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    return {
        "now": now,
        "count" : server_cnt
    }

@app.get("/change/{cnt}")
def change(cnt: int):
    global server_cnt
    
    server_cnt += cnt
    if server_cnt < 0: server_cnt = 0
    
    now = datetime.now().strftime("%Y-%m-%d %H%M%S")
    return {
        "now": now,
        "count" : server_cnt
    }