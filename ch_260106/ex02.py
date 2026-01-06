# 실습:
'''
신장 정보 입력을 받도록 form
성명, 주소, 전화버노, 이메일, 나이, 성별 등
main.py엣 터미널 출력 및 파일로 저장
'''

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from datetime import datetime
import csv
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
    
@app.get("/")
def show_form(request: Request) :
    return templates.TemplateResponse(
        "join-us.html", {"request": request}
    )

@app.post("/join")
def join(request : Request, 
         name=Form(...),
        address=Form(...),
        phone=Form(...),
        email=Form(...),
        age:int=Form(...),
        sex=Form(...),
):
    print(name, address, phone, email, age, sex)
    text = f"""
    이름: {name}
    나이: {age}
    전화번호: {phone}
    성별: {sex}
    주소: {address}
    이메일: {email}
    """
    with open ("info.txt", "w", encoding="utf-8") as f:
        f.write(text)   
    
    created_at = datetime.now().strftime("%Y%m%d%H%M%S")
    result = {
        "request": request,
        "created_at": created_at,
        "name": name, 
        "address": address, 
        "phone": phone,  
        "email": email, 
        "age": age, 
        "sex": sex
    }
    save_user_info(result)
    return templates.TemplateResponse("result.html", result)
    return HTMLResponse(f"""
                        <!DOCTYPE html>
                        <html>
                        <body>
                        <h1>결과페이지<h1>
                        <ul>
                        <li>성명: {name}</li>
                        <li>주소: {address}</li>
                        <li>이메일: {email}</li>
                        </ul>
                        </body>
                        </html>
                        """)
    
def save_user_info(content: dict):
    
    file_name = "user_infos.csv"
    with open (file_name, "a+", newline="", encoding="utf-8") as f:
        f.seek(0)                           # 커서의 위치를 파일의 가장 처음(0번 바이트)으로 이동시키는 명령
        first_line = f.readline().strip()   # 첫 라인 읽기
        
        w = csv.writer(f)        
        if not first_line:
            w.writerow(["created_at","name","address","phone","email","sex","age"])
        
        values = list(content.values())
        w.writerow(values[1:])