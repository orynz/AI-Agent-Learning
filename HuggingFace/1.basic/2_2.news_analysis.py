from transformers import pipeline
import torch

classifier_finbert = pipeline(
    "text-classification",
    model="snunlp/KR-FinBert-SC", # 금융 특화
    
    # GPU 사용 가능 여부 확인 및 device 설정
    device=(0 if torch.cuda.is_available() else -1)
)

classifier_multilang = pipeline(
    "text-classification",
    model="tabularisai/multilingual-sentiment-analysis", # 일반적 댓글 특화
    device=(0 if torch.cuda.is_available() else -1)
)

sentences = [
    "현대바이오, '폴리탁셀' 코로나19 치료 가능성에 19% 급등",	
    "이수화학, 3분기 휴익 176억…전년比 80%↑",
    '"GKL, 7년 만에 두 자릿수 성장 전망"',
    "위지인스튜디오, 유니버스에 최초의 사상 1000억원이 있습니다.",
    "삼성전자, 2년 만에 인도 스마트폰 시장 경고 1위 '왕좌 탈환'",
    '"CJ CGV 올 4000억 뺄 날도 있겠네요”',
    "C쇼크에 멈춘 흑자비행… 대한항공 1 분기적자 566억",
    '1000억대 횡령·배임, 최신원 청와대…SK네트웍스 "경영 확장 방지 최선"',
    '부품공급 차질에…기아차 광주공장 전면 가동 중단',
    '현대제철, 비동기식 3,313억원···전년比 67.7% 예상',
    
    "이 영화 진짜 인생 영화네요! 너무 감동적이에요.",
    "배송이 너무 느려서 실망했어요. 다시는 안 살 듯.",
    "그냥 평범한 식당이네요. 나쁘지도 좋지도 않음."
]

# 주 모델로 분석
results_finbert = classifier_finbert(sentences)

# 보완 모델로 분석
results_multilang = classifier_multilang(sentences)

# 결과 통합 출력
print(f"{'문장':<60} {'KR-FinBert':<10} {'KoBERT':<10}")
print("-" * 90)

for i, sent in enumerate(sentences):
    
    finbert_label = results_finbert[i]['label']
    finbert_score = results_finbert[i]['score']
    kobert_label = results_multilang[i]['label']
    kobert_score = results_multilang[i]['score']
    print(f"{sent[:37] + '...' if len(sent) > 40 else sent:<40} | "
          f"{finbert_label:<10} | {kobert_label:<10}")