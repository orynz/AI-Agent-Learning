from fastapi import FastAPI, Form

app = FastAPI()


@app.get("/")
def read_root():
    obj = {
        "message": '안녕하세요!',
        "user": "KBJ"
    }
    return obj

@app.get("/hello")
def g_hello(name = "hong"):
    print("[Get] Name: ", name)
    return {"name":name}

@app.post("/hello")
def p_hello(name = Form(...)):
    print("[Post] Name: ", name)
    return {"name":name}