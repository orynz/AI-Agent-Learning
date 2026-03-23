# 보통 AI 모델을 돌리려면 
# 텍스트 전처리(Tokenizer) -> 
# 모델 로드 -> 
# 예측(Inference) -> 
# 결과 해석이라는 복잡한 과정을 거쳐야 합니다. 
# pipeline은 이 모든 과정을 자동으로 묶어줍니다.
from transformers import pipeline

# 감정 분석(sentiment-analysis)용 pipeline 생성 (기본 영어 모델 자동 다운로드)
classifier = pipeline("sentiment-analysis",  # 수행할 작업(Task)을 지정,텍스트의 감정을 분석하는 작업
                       # distilbert-base-uncased : DistilBERT 기반의 경량화된 BERT 모델
                       # finetuned-sst-2-english : SST-2 감정 분석 데이터셋으로 추가 학습된 모델
                      model="distilbert-base-uncased-finetuned-sst-2-english",
                      framework="pt")#사용할 딥러닝 프레임워크 지정, "pt"는 PyTorch를 의미

sentences = [
    "I love using Hugging Face transformers!",  # 긍정적인 문장 예시
    "That is wonderful magic!",                  # 또 다른 긍정적인 문장 예시
    "나는 허깅 페이스를 사랑한다.",
    "나는 지금 너무 힘들다"
]

# 준비한 문장들을 감정 분석 실행
results = classifier(sentences)

# 각 문장과 결과를 함께 출력하기 위해 반복문 사용
for sentence, result in zip(sentences, results):
    print(f"문장: {sentence}")  # 원본 문장 출력
    print(f"감성: {result['label']}, 신뢰도: {result['score']:.4f}")  