import torch                                     # 파이토치 임포트
from transformers import AutoTokenizer, AutoModelForSequenceClassification # 토크나이저와 모델 로더 임포트
import torch.nn.functional as F                  # 확률 계산을 위한 소프트맥스 함수용 임포트

from pathlib import Path

# 1. 저장된 모델과 토크나이저 경로 설정
model_path = Path(__file__).parent / "my_movie_model"
base_model = "bert-base-multilingual-cased"      # 원본 베이스 모델 이름

tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

model.eval()

def predict_sentiment(text):
    """문장을 입력받아 긍정/부정 결과를 반환하는 함수"""
    
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding = True, max_length=64)
    
    with torch.no_grad():
        outputs = model(**inputs)

    # 결과 해석 (Logits -> Softmax 확률 변환)
    logits = outputs.logits
    probs = F.softmax(logits, dim=-1)            # 각 라벨(0, 1)에 대한 확률 계산
    
    prediction = torch.argmax(probs, dim=-1).item() # 가장 확률이 높은 값의 클래스 인덱스 선택
    conf = torch.max(probs).item() * 100 # 퍼센트로 변환
    
    sentiment = "긍정(Positive)" if prediction ==1 else "부정(Negative)"
    print(f"\n입력문자: {text}")
    print(f"분석 결과: {sentiment} ({conf:.2f}# 확신)")
    
if __name__ == "__main__":
    
    while True:
        text = input("분석할 리뷰를 입력하세요: ")
        predict_sentiment(text)
    

