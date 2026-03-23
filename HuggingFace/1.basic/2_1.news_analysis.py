from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="snunlp/KR-FinBert-SC"
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
]

results = classifier(sentences)

for i, (sentence, result) in enumerate(zip(sentences, results), start=1):
    print(f"{i}. 문장: {sentence}")
    print(f"감정: {result["label"]} / 신뢰도: {result["score"]}\n")