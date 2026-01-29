from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 정적 파일 설정 (public 폴더 내의 index.html 등을 서빙)
app.mount("/public", StaticFiles(directory="public", html=True), name="public")

# CORS 설정 (브라우저 보안 정책 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "OK", "status code": 200}

@app.get("/calc/{a}/{b}/{oper}")
def calc(a:int, b:int, oper:str):
    if oper == "add":
        c = f"{a + b}"
    elif oper == "sub":
        c = f"{a - b}"
    elif oper == "mul":
        c = f"{a * b}"
    elif oper == "div":
        c = f"{a / b:.2}"
    
    result = {"a": a, "b": b, "result": c}
    
    return result