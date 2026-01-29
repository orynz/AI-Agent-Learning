from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi import FastAPI, Query, Form, File, UploadFile
from typing import Optional, List

from fastapi.middleware.cors import CORSMiddleware



class Message(BaseModel):
    text: str
    
class Login(BaseModel):
    name:str
    id:str
    pw:str
    
app = FastAPI()

# 1. 허용할 출처(Origin) 목록 설정
origins = [
    "http://localhost",       # 로컬 환경
    "http://127.0.0.1:5500",  # VS Code Live Server 등을 사용할 경우 포트 포함
    "http://127.0.0.1:8000",
]

# 2. 미들웨어 추가 (보안 설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 모든 곳에서 접속 허용 (개발 시 편리함)
    allow_credentials=True,
    allow_methods=["*"],      # GET, POST, OPTIONS 등 모든 메소드 허용
    allow_headers=["*"],      # 모든 헤더 허용
)

app.mount("/public", StaticFiles(directory="public", html=True), name="public")

@app.post("/")
def root():
    return {"message":"hello"}


@app.post("/echo")
def echo(msg: Message):
    return {
        "received_text": msg.text,
        "length": len(msg.text)
    }

@app.get("/items/{item_id}")
async def read_item(
    item_id: int,                    # 경로 파라미터 (Path Parameter)
    q: Optional[str] = None,         # 쿼리 파라미터 (Query Parameter)
    tags: List[str] = Query(None)    # 리스트형 쿼리 파라미터
):
    return {
        "item_id": item_id,
        "query": q,
        "tags": tags
    }
    
@app.post("/urlencoded")
async def urlencoded(info: Login = Form(...)):
    return {
        "name": info.name,
        "id": info.id,
        "pw": info.pw,
    }

from fastapi import FastAPI, Form, File, UploadFile

@app.post("/form-data")
async def process_form_data(
    name: str = Form(...), 
    profile_img: UploadFile = File(...)
):
    return {"name": name, "filename": profile_img.filename}

@app.post("/upload/user-profile")
async def create_user_profile(
    # 일반 텍스트 데이터 (Form 사용)
    username: str = Form(..., description="사용자 이름"),
    age: int = Form(..., description="사용자 나이"),
    # 파일 데이터 (File/UploadFile 사용)
    profile_img: UploadFile = File(..., description="프로필 이미지 파일")
):
    # 파일 정보 읽기
    content = await profile_img.read()
    
    return {
        "status": "success",
        "user_info": {
            "username": username,
            "age": age
        },
        "file_info": {
            "filename": profile_img.filename,
            "content_type": profile_img.content_type,
            "size": len(content)
        }
    }
