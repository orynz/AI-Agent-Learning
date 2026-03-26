# 한국어 금융 스팸 분류기

## 프로젝트 구조

```
spam_project/
├── run_pipeline.py          # ✅ 전체 파이프라인 한 번에 실행
├── main.py                  # FastAPI 서버
├── requirements.txt
├── app/
│   ├── schema.py            # Pydantic 요청/응답 모델
│   └── predictor.py         # 모델 로드 & 예측 (싱글톤)
├── scripts/
│   ├── generate_data.py     # 한국어 스팸/정상 데이터 생성기
│   └── train_model.py       # 학습 + 평가 + 시각화
├── model/
│   └── spam_model.pkl       # 학습된 모델 (run 후 생성)
└── reports/
    ├── metrics.json          # 평가 지표 (JSON)
    ├── confusion_matrix.png
    ├── roc_curve.png
    ├── pr_curve.png
    ├── score_distribution.png
    └── top_features.png
```

## 빠른 시작

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 전체 파이프라인 실행 (데이터 생성 → 학습 → 평가 → 샘플 예측)
python run_pipeline.py

# 3. API 서버 실행
uvicorn main:app --reload

# 4. Swagger UI 접속
# http://127.0.0.1:8000/docs
```

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/` | 상태 확인 |
| GET | `/health` | 헬스 체크 |
| POST | `/predict` | 단건 예측 |
| POST | `/predict/batch` | 배치 예측 (최대 100건) |
| GET | `/metrics` | 평가 지표 조회 |

### 단건 예측 예시

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "(광고) 국민은행 당첨! 현금 100만원 받으시려면 지금 클릭하세요"}'
```

응답:
```json
{
  "label": "spam",
  "label_ko": "스팸",
  "probability": 0.98,
  "spam_probability": 0.98,
  "risk_level": "높음"
}
```

## 모델 상세

- **벡터화**: TF-IDF (char n-gram 1~2, max_features=10000)
- **분류기**: Logistic Regression (C=1.0, class_weight=balanced)
- **데이터**: 한국어 금융 스팸/정상 템플릿 기반 20,000건
- **성능**: Accuracy 1.00 / ROC-AUC 1.00 (5-Fold CV)