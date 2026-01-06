# main.py
from typing import List, Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# 1) 정적 파일(public) 제공:  http://localhost:8000/  하위에서 정적 리소스 접근 가능
#    예: /css/style.css, /js/app.js 등
app.mount("/", StaticFiles(directory="public", html=True), name="public")

# 2) 템플릿(views) 설정 (Express의 app.set('views', ...)와 동일 역할)
templates = Jinja2Templates(directory="templates")


# 3) 데이터(임시 in-memory)
class Car(BaseModel):
    seq: int
    name: str
    price: int
    company: str
    year: int


car_list: List[Car] = [
    Car(seq=1001, name="SONATA", price=2000, company="HYUNDAI", year=2020),
    Car(seq=1002, name="K7", price=3700, company="KIA", year=2018),
    Car(seq=1003, name="SM6", price=1800, company="르노", year=2017),
    Car(seq=1004, name="G80", price=5000, company="제니시스", year=2017),
]

# Express의 sequence++ 대응
sequence = max(c.seq for c in car_list) + 1


# 4) 라우트들
@app.get("/test/", response_class=HTMLResponse)
def test(request: Request):
    # Express 예제의 res.writeHead + res.write + res.end에 해당
    # req.url 문자열도 함께 출력
    html = f"GET - /test/beomjoon<br/>{request.url.path}"
    return HTMLResponse(content=html, status_code=200)


@app.get("/car/list", response_class=HTMLResponse)
def car_list_page(request: Request):
    # Express: req.app.render("car/list", {carList}, ...)
    return templates.TemplateResponse(
        "car/list.html",
        {"request": request, "carList": car_list},
    )


@app.post("/car/input")
def car_input(
    name: str = Form(...),
    price: int = Form(...),
    company: str = Form(...),
    year: int = Form(...),
):
    # Express: req.body + sequence++ + push + redirect
    global sequence
    new_car = Car(seq=sequence, name=name, price=price, company=company, year=year)
    car_list.append(new_car)
    sequence += 1
    return RedirectResponse(url="/car/list", status_code=303)


@app.get("/car/modify/{seq}", response_class=HTMLResponse)
def car_modify_page(request: Request, seq: int):
    # Express: /car/modify/:seq GET
    car = next((c for c in car_list if c.seq == seq), None)
    if car is None:
        return RedirectResponse(url="/car/list", status_code=303)

    return templates.TemplateResponse(
        "car/modify.html",
        {"request": request, "car": car},
    )


@app.post("/car/modify/{seq}")
def car_modify(
    seq: int,
    name: str = Form(...),
    price: int = Form(...),
    company: str = Form(...),
    year: int = Form(...),
):
    # Express: /car/modify/:seq POST
    idx = next((i for i, c in enumerate(car_list) if c.seq == seq), -1)
    if idx != -1:
        car_list[idx] = Car(seq=seq, name=name, price=price, company=company, year=year)
    return RedirectResponse(url="/car/list", status_code=303)


@app.get("/car/delete/{seq}")
def car_delete(seq: int):
    # Express: car/delete/:seq (원본은 라우트 문자열 오타가 있었음)
    idx = next((i for i, c in enumerate(car_list) if c.seq == seq), -1)
    if idx != -1:
        car_list.pop(idx)
    return RedirectResponse(url="/car/list", status_code=303)
