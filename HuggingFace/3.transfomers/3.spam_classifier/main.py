"""
한국어 금융 스팸 메일 분류 API
"""
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.schema import SpamRequest, SpamResponse, HealthResponse
from app.predictor import predictor

VERSION = "1.1.0"

app = FastAPI(
    title="Korean Spam Classifier API",
    description="한국어 금융 스팸 메일 분류 REST API (TF-IDF + Logistic Regression)",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# 정적 파일 디렉토리 마운트 (예: /static/)
app.mount("/static", StaticFiles(directory="templates"), name="static")

# 루트 경로(/)에 index.html을 직접 반환
@app.get("/", tags=["Root"])
async def read_root():
    return FileResponse("templates/index.html")

# @app.get("/", tags=["Root"])
# def root():
#     return {"message": "Korean Spam Classifier API is running", "version": VERSION, "docs": "/docs"}


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health():
    return HealthResponse(status="ok", model_loaded=True, version=VERSION)


@app.post("/predict", response_model=SpamResponse, tags=["Predict"])
def predict_spam(req: SpamRequest):
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="text 필드가 비어 있습니다.")
    result = predictor.predict(req.text)
    return SpamResponse(**result)


@app.post("/predict/batch", tags=["Predict"])
def predict_batch(requests: list[SpamRequest]):
    if len(requests) > 100:
        raise HTTPException(status_code=400, detail="한 번에 최대 100건까지 허용됩니다.")
    results = []
    for req in requests:
        result = predictor.predict(req.text)
        results.append({"text": req.text[:60] + ("..." if len(req.text) > 60 else ""), **result})
    return {"count": len(results), "results": results}


@app.get("/metrics", tags=["Evaluate"])
def get_metrics():
    """최근 학습에서 생성된 평가 지표 반환"""
    metrics_path = os.path.join("reports", "metrics.json")
    if not os.path.exists(metrics_path):
        raise HTTPException(status_code=404, detail="metrics.json 없음. 먼저 모델을 학습하세요.")
    with open(metrics_path, encoding="utf-8") as f:
        return json.load(f)