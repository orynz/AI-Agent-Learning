from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.get("/Doc")
def read_doc():
    return {"message": "Hello FastAPI: Doc"}
