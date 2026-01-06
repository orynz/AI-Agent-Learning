from typing import List, Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# 1) 정적 파일(public) 제공:  http://localhost:8000/  하위에서 정적 리소스 접근 가능
#    예: /css/style.css, /js/app.js 등
# views의 root와 충돌나지 않도록 구분해야함
app.mount("/public", StaticFiles(directory="public", html=True), name="public")

# 2) 템플릿(views) 설정 (Express의 app.set('views', ...)와 동일 역할)
templates = Jinja2Templates(directory="views")


# 데이터 모델
class Car(BaseModel):
    seq: int
    name: str
    price: int
    company: str
    year: int

# 더미 데이터
car_list: List[Car] = [
    Car(seq=1001, name="SONATA", price=2000, company="HYUNDAI", year=2020),
    Car(seq=1002, name="K7", price=3700, company="KIA", year=2018),
    Car(seq=1003, name="SM6", price=1800, company="르노", year=2017),
    Car(seq=1004, name="G80", price=5000, company="제니시스", year=2017),
]

# 자동 증가(Auto-increment) 
sequence = max(c.seq for c in car_list) + 1

# root
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )

@app.get("/car/list", response_class=HTMLResponse)
def car_list_page(request: Request):
  return templates.TemplateResponse(
      "/car/list.html",
      {"request":request, "car_list": car_list}
  )

@app.post("/car/input")
def car_input(
    name: str = Form(...),
    price: int = Form(...),
    company: str = Form(...),
    year: int = Form(...),
):
    global sequence
    car_list.append(Car(seq=sequence, name=name, price=price, company=company, year=year))
    sequence += 1
    return RedirectResponse(url="/car/list", status_code=303)

@app.get("/car/modify/{seq}", response_class=HTMLResponse)
def car_modify_page(request: Request, seq: int):
    return templates.TemplateResponse(
        "/car/modify.html",
        {
            "request": request, 
            "car":next((c for c in car_list if c.seq == seq), None)
    })

@app.post("/car/modify/{seq}")
def car_modify(
    seq: int,
    name: str = Form(...),
    price: int = Form(...),
    company: str = Form(...),
    year: int = Form(...),
):
    car = next((c for c in car_list if c.seq == seq), None)
    if car:
        car.name, car.price, car.company, car.year = name, price, company, year
        return RedirectResponse(url="/car/list", status_code=303)
    

@app.get("/car/delete/{seq}")
def car_delete(seq: int):
    global car_list
    car_list = [c for c in car_list if c.seq != seq]
    return RedirectResponse(url="/car/list", status_code=303)

