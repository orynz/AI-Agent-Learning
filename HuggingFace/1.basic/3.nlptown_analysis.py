from transformers import pipeline
import torch


classifier = pipeline(
    task="text-classification", 
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    device=(0 if torch.cuda.is_available() else -1)
)

sentences = [
    "오늘은 날씨가 맑고 따뜻해서 산책하기에 정말 좋은 하루입니다.",
    "한 여름에 눈이 내려서 너무 행복해.",
    "최고예요! 이 제품은 정말 만족스럽습니다.",
    "디자인이 멋져서 매일 사용하고 싶어요.",

    "가격이 합리적이라 부담이 없어요.",
    "고객 서비스가 친절해서 감동했습니다.",
    "배송이 너무 늦어서 실망했습니다.",    
    "품질이 기대보다 떨어져서 실망이에요.",
    
    "사용 중 오류가 자주 발생해요.",
    "광고와 실제 제품이 차이가 크네요.",
]

results = classifier(sentences)

for i, (sentence, result) in enumerate(zip(sentences, results), start=1):
    print(f"{i}. 문장: {sentence}")
    print(f"감정: {result["label"]} / 신뢰도: {result["score"]}\n")
    