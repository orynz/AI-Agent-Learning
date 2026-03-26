from pydantic import BaseModel

class SpamRequest(BaseModel):
    text: str
    model_config = {"json_schema_extra": {"example": {"text": "(광고) 국민은행 당첨! 현금 100만원 받으시려면 지금 클릭하세요"}}}

class SpamResponse(BaseModel):
    label: str                  # "spam" | "ham"
    label_ko: str               # "스팸" | "정상"
    probability: float          # 해당 클래스 확률
    spam_probability: float     # 스팸일 확률 (0~1)
    risk_level: str             # "높음" | "중간" | "낮음"

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str