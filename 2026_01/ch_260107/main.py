from fastapi import FastAPI, Form
from pydantic import BaseModel

class Message(BaseModel):
    message:str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI 서버 실행 확인!"}

@app.get("/items")
def read_items(category:str, page:int=1):
    return {
        "category": category,
        "page": page
    }

@app.post("/echo")
def echo(msg: Message):
    return {
        "received_text": msg.message,
        "length": len(msg.message)
    }

@app.post("/login")
def login(username:str = Form(...), password:str=Form(...)):
    return {
        "username":username,
        "password":password
    }