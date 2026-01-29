from fastapi import FastAPI, Form, Query, staticfiles
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount(path="/public", app=StaticFiles(directory="public", html=True), name="public")

@app.get("/")
def root():
    return {"status_code": "200 OK"}

# 서버에서 계산기 구현
# pathparam - 연산자, 항1, 항2을 받아서
# 우아한 url

@app.get("/plus/{a}/{b}")
def puls(a:int, b:int):
    print(a, b)
    return f"{a} + {b} = {a + b}"

@app.get("/min/{a}/{b}")
def min(a:int, b:int):
    print(a, b)
    return f"{a} - {b} = {a - b}"

@app.get("/mult/{a}/{b}")
def mult(a:int, b:int):
    print(a, b)
    return f"{a} * {b} = {a * b}"

@app.get("/div/{a}/{b}")
def div(a:int, b:int):
    print(a, b)
    return f"{a} / {b} = {a / b}"
