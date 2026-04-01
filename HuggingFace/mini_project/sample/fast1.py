from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(
    directory="./templates"
)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    context = {
        "request": request,
        "name": "홍길동",
        "movies": ["인셉션", "인터스텔라", "다크 나이트"],
    }
    return templates.TemplateResponse("index.html", context=context)

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("fast1:app", reload=True, host="localhost", port=8000)