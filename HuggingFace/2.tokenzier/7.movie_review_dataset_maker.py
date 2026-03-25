import csv
import random
import re
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

TOTAL_SAMPLES = 100000
POS_COUNT = TOTAL_SAMPLES // 2
NEG_COUNT = TOTAL_SAMPLES // 2
OUTPUT_FILE = "movie.csv"


subjects = [
    "이 영화", "이 작품", "이번 영화", "이번 작품", "이 영화는", "이 작품은",
    "개인적으로 이 영화", "개인적으로 이 작품", "기대 없이 본 이 영화", "기대 없이 본 이 작품",
    "오랜만에 본 영화", "오랜만에 본 작품", "주말에 본 영화", "주말에 본 작품",
    "극장에서 본 이 영화", "OTT로 본 이 작품", "어제 본 영화", "오늘 본 작품", "이번에 개봉한 영화",
    "친구 추천으로 본 영화", "입소문 듣고 본 작품", "최근에 본 영화"
]

watch_contexts = [
    "주말 저녁에 봤는데", "혼자 봤는데", "가족이랑 같이 봤는데", "친구랑 봤는데",
    "큰 기대 없이 틀었는데", "퇴근하고 봤는데", "비 오는 날 봤는데", "늦은 밤에 봤는데",
    "재관람했는데", "OTT에서 우연히 봤는데", "극장에서 봤는데", "집에서 편하게 봤는데",
    "쉬는 날 봤는데", "연휴에 몰아서 봤는데", "심심해서 봤는데", "기대 많이 하고 봤는데",
    "평이 좋아서 봤는데", "후기 보고 봤는데", "예고편 보고 봤는데", "아무 정보 없이 봤는데"
]

positive_openers = [
    "정말 좋았어요.", "기대 이상이었어요.", "오랜만에 만족스러운 영화였어요.", "생각보다 훨씬 괜찮았어요.",
    "완성도가 높았어요.", "몰입감이 좋았어요.", "끝까지 재밌게 봤어요.", "생각보다 훨씬 잘 만들었네요.",
    "보는 내내 집중했어요.", "개인적으로 꽤 마음에 들었어요.", "생각보다 훨씬 인상 깊었어요.",
    "잔잔한데도 좋았어요.", "이 정도면 충분히 잘 만든 영화예요.", "보길 잘했다는 생각이 들었어요.",
    "괜히 평이 좋은 게 아니네요.", "전체적으로 아주 만족스러웠어요."
]

negative_openers = [
    "정말 별로였어요.", "기대 이하였어요.", "솔직히 실망스러웠어요.", "끝까지 보기 힘들었어요.",
    "시간이 아까웠어요.", "몰입이 잘 안 됐어요.", "생각보다 너무 평범했어요.", "아쉬움이 많이 남았어요.",
    "보는 내내 지루했어요.", "왜 평이 좋은지 잘 모르겠어요.", "기대한 것보다 한참 아쉬웠어요.",
    "개인적으로는 별로였네요.", "잘 만들었다는 느낌은 못 받았어요.", "끝나고 나서 허무했어요.",
    "이 정도면 많이 아쉬운 편이에요.", "솔직히 추천하기는 어렵네요."
]

positive_short = [
    "재밌었어요", "좋았어요", "괜찮았어요", "몰입감 좋네요", "추천합니다", "생각보다 좋음",
    "여운 남아요", "연기 좋았어요", "스토리 좋네요", "완성도 높음", "진짜 괜찮다", "다시 보고 싶어요",
    "배우들 연기 굿", "재밌게 봤어요", "잘 만든 영화", "수작이네요", "인생영화급", "존잼", "꿀잼",
    "좋네요", "최고였어요", "기대 이상", "개좋음", "진짜 좋았음", "만족", "강추", "추천", "호불호 덜할 듯"
]

negative_short = [
    "별로였어요", "지루했어요", "실망", "시간 아까움", "추천 안 함", "스토리 뻔함",
    "연기 어색함", "결말 아쉬움", "몰입 안 됨", "그냥 그랬어요", "노잼", "개노잼",
    "많이 아쉬움", "기대 이하", "별로네요", "진짜 별로", "보다 말 뻔", "다신 안 봄",
    "실망했어요", "평범함", "억지스러움", "너무 늘어짐", "지루함", "비추", "아쉬워요", "그닥", "음...", "애매함"
]

acting_positive = [
    "배우들의 연기가 정말 자연스러웠어요", "주연 배우가 감정을 섬세하게 잘 살렸어요",
    "조연들까지 연기가 안정적이었어요", "캐릭터 표현이 살아 있었어요", "감정선 전달이 좋았어요",
    "인물마다 개성이 분명했어요", "배우들 합이 좋았어요", "주연의 몰입도가 상당했어요",
    "표정 연기가 인상적이었어요", "대사 전달력이 좋았어요", "감정 표현이 과하지 않고 좋았어요",
    "연기가 극 분위기를 잘 끌고 갔어요", "인물 해석이 좋아 보였어요", "캐릭터에 설득력이 있었어요",
    "감정 변화가 자연스럽게 느껴졌어요", "어색한 장면이 거의 없었어요", "연기 보는 맛이 있었어요",
    "배우들이 캐릭터에 잘 녹아들었어요", "몰입을 깨는 연기가 없었어요", "주연 배우 존재감이 컸어요"
]

acting_negative = [
    "배우들의 연기가 전반적으로 어색했어요", "주연 배우의 감정 표현이 단조로웠어요",
    "조연 연기가 자꾸 튀었어요", "캐릭터 표현이 평면적이었어요", "감정선 전달이 잘 안 됐어요",
    "인물마다 개성이 약했어요", "배우들 합이 좋은 편은 아니었어요", "주연의 몰입도가 아쉬웠어요",
    "표정 연기가 부자연스러웠어요", "대사 전달이 어색했어요", "감정 표현이 과해서 몰입이 깨졌어요",
    "연기가 극 분위기를 못 살렸어요", "인물 해석이 설득력 없었어요", "캐릭터가 살아 있지 않았어요",
    "감정 변화가 뜬금없게 느껴졌어요", "어색한 장면이 꽤 있었어요", "연기 보는 맛이 없었어요",
    "배우들이 캐릭터에 잘 녹아들지 못했어요", "몰입을 깨는 연기가 종종 있었어요", "주연 배우 존재감이 약했어요"
]

story_positive = [
    "스토리가 탄탄했어요", "전개가 깔끔했어요", "서사가 차근차근 쌓였어요", "이야기 흐름이 자연스러웠어요",
    "구성이 안정적이었어요", "대본이 잘 쓰인 느낌이었어요", "전개 속도가 적절했어요", "지루할 틈이 없었어요",
    "중반 이후 몰입감이 더 좋아졌어요", "복선 회수가 괜찮았어요", "뻔하지 않게 잘 풀어갔어요",
    "잔잔하지만 힘이 있었어요", "장면 연결이 매끄러웠어요", "감정선이 잘 이어졌어요",
    "주제가 비교적 선명했어요", "메시지가 부담스럽지 않게 전달됐어요", "클리셰를 잘 활용했어요",
    "긴 러닝타임이 크게 길게 느껴지지 않았어요", "이야기가 끝까지 힘을 유지했어요", "후반부 집중력이 좋았어요"
]

story_negative = [
    "스토리가 너무 뻔했어요", "전개가 늘어졌어요", "서사가 헐거웠어요", "이야기 흐름이 부자연스러웠어요",
    "구성이 불안정했어요", "대본이 허술하게 느껴졌어요", "전개 속도가 애매했어요", "지루한 구간이 많았어요",
    "중반 이후 힘이 빠졌어요", "복선 회수가 허술했어요", "뻔한 방향으로만 흘러갔어요",
    "잔잔한 게 아니라 심심했어요", "장면 연결이 매끄럽지 않았어요", "감정선이 잘 이어지지 않았어요",
    "주제가 선명하지 않았어요", "메시지가 너무 직접적이었어요", "클리셰가 진부하게 느껴졌어요",
    "러닝타임이 유독 길게 느껴졌어요", "이야기가 끝까지 힘을 못 유지했어요", "후반부 집중력이 떨어졌어요"
]

visual_positive = [
    "영상미가 뛰어났어요", "연출이 세련됐어요", "촬영이 인상적이었어요", "미장센이 좋았어요",
    "색감이 분위기를 잘 살렸어요", "음악이 장면과 잘 어울렸어요", "장면 구성이 깔끔했어요",
    "화면 보는 맛이 있었어요", "사운드 활용도 좋았어요", "감정 장면 연출이 좋았어요",
    "연출이 과하지 않아서 더 좋았어요", "시각적으로 만족도가 높았어요", "배경과 조명이 예뻤어요",
    "음악이 몰입을 도와줬어요", "카메라 워크가 안정적이었어요", "분위기 연출이 좋아요",
    "장면 하나하나 공들인 느낌이었어요", "전체 톤이 잘 맞았어요", "영상과 감정의 호흡이 좋았어요",
    "극장 화면으로 보면 더 좋을 것 같아요"
]

visual_negative = [
    "영상미가 특별하진 않았어요", "연출이 평범했어요", "촬영이 인상적이지 않았어요", "미장센이 밋밋했어요",
    "색감이 애매했어요", "음악이 장면과 따로 노는 느낌이었어요", "장면 구성이 산만했어요",
    "화면 보는 맛이 없었어요", "사운드 활용이 아쉬웠어요", "감정 장면 연출이 밋밋했어요",
    "연출이 과해서 오히려 방해됐어요", "시각적으로 만족도가 낮았어요", "배경과 조명이 어색했어요",
    "음악이 몰입을 깨는 순간이 있었어요", "카메라 워크가 불안정했어요", "분위기 연출이 부족했어요",
    "장면 하나하나 공들인 느낌은 아니었어요", "전체 톤이 잘 안 맞았어요", "영상과 감정의 호흡이 안 맞았어요",
    "극장에서 봐도 큰 감흥은 없을 것 같아요"
]

ending_positive = [
    "결말이 깔끔했어요", "엔딩이 좋았어요", "마무리가 안정적이었어요", "후반부가 인상적이었어요",
    "마지막 장면이 오래 남아요", "클라이맥스가 좋았어요", "엔딩이 여운을 남겼어요",
    "결말까지 보고 나니 더 좋게 느껴졌어요", "후반부 감정 정리가 잘 됐어요", "마무리가 과하지 않았어요",
    "엔딩이 작품 분위기와 잘 맞았어요", "끝맺음이 좋았어요", "후반부 집중력이 살아 있었어요",
    "결말이 납득 가능했어요", "마지막이 감정을 잘 끌어올렸어요"
]

ending_negative = [
    "결말이 아쉬웠어요", "엔딩이 별로였어요", "마무리가 급했어요", "후반부가 힘이 빠졌어요",
    "마지막 장면이 크게 남지 않았어요", "클라이맥스가 약했어요", "엔딩이 여운을 망쳤어요",
    "결말까지 보고 나니 더 아쉽게 느껴졌어요", "후반부 감정 정리가 잘 안 됐어요", "마무리가 과했어요",
    "엔딩이 작품 분위기와 잘 안 맞았어요", "끝맺음이 허무했어요", "후반부 집중력이 무너졌어요",
    "결말이 납득하기 어려웠어요", "마지막이 감정을 제대로 못 살렸어요"
]

positive_feelings = [
    "보고 나서 기분이 좋아졌어요", "여운이 오래 남았어요", "다 보고 나니 다시 보고 싶더라고요",
    "시간 가는 줄 모르고 봤어요", "감정적으로 꽤 크게 와닿았어요", "캐릭터에게 자연스럽게 이입됐어요",
    "오랜만에 영화 잘 봤다는 생각이 들었어요", "관람 후 만족감이 컸어요", "마음에 남는 장면이 많았어요",
    "생각보다 더 좋게 기억에 남을 것 같아요", "극장을 나와서도 계속 생각났어요", "호감이 많이 남는 작품이었어요"
]

negative_feelings = [
    "보고 나서 남는 게 별로 없었어요", "끝나고 나니 허무했어요", "시간이 유독 길게 느껴졌어요",
    "집중이 자꾸 끊겼어요", "캐릭터에게 감정 이입이 안 됐어요", "왜 좋은 평가를 받는지 잘 모르겠어요",
    "보고 나서 바로 잊힐 것 같아요", "관람 후 만족감이 거의 없었어요", "기억에 남는 장면이 많지 않았어요",
    "생각보다 더 아쉽게 기억될 것 같아요", "극장을 나와도 별 감흥이 없었어요", "호감보다 피로감이 컸어요"
]

positive_recommends = [
    "추천하고 싶어요.", "한 번쯤 볼 만해요.", "비슷한 장르 좋아하면 만족할 것 같아요.",
    "주변에도 추천할 생각이에요.", "재관람 의사 있어요.", "개인적으로는 꽤 추천입니다.",
    "극장에서 봐도 아깝지 않을 작품이에요.", "취향 맞으면 정말 좋게 볼 영화예요.",
    "이런 분위기 좋아하면 잘 맞을 거예요.", "생각보다 많은 분들이 좋아할 만해요."
]

negative_recommends = [
    "추천하기는 어려워요.", "굳이 볼 필요는 없을 것 같아요.", "다시 볼 생각은 없어요.",
    "기대하고 보면 더 실망할 수 있어요.", "개인적으로는 비추천이에요.", "시간 내서 볼 정도는 아닌 것 같아요.",
    "취향 타는 정도가 아니라 완성도 자체가 아쉬워요.", "입소문만큼은 아니에요.", "이건 굳이 챙겨보진 않아도 될 듯해요.",
    "개인적으로 만족도는 낮았어요."
]

positive_extras = [
    "억지로 감동을 밀어붙이지 않아서 더 좋았어요.", "작은 대사 하나도 허투루 쓰지 않은 느낌이었어요.",
    "잔잔한데도 지루하지 않게 끌고 가는 힘이 있었어요.", "캐릭터들의 선택이 이해돼서 몰입이 잘 됐어요.",
    "자극적이지 않아도 충분히 재미를 만들 수 있다는 걸 보여줬어요.", "감독이 하고 싶은 말이 비교적 선명하게 전달됐어요.",
    "장르적 재미와 감정선을 동시에 챙긴 느낌이었어요.", "과장되지 않은 분위기가 오히려 더 좋았어요.",
    "중간중간 웃음 포인트도 자연스러웠어요.", "감정이 올라오는 타이밍이 좋았어요.",
    "설정만 요란한 영화들과는 결이 달랐어요.", "배우와 연출이 서로 잘 받쳐줬어요."
]

negative_extras = [
    "억지로 감동을 만들려는 느낌이 강했어요.", "대사들이 너무 익숙해서 새롭지 않았어요.",
    "잔잔한 게 아니라 그냥 심심한 쪽에 가까웠어요.", "캐릭터들의 선택이 잘 이해되지 않았어요.",
    "자극적인 장면이 없으면 버티기 힘들 정도로 전개 힘이 약했어요.", "감독이 하고 싶은 말은 알겠는데 전달 방식이 너무 직접적이었어요.",
    "장르적 재미도 감정선도 애매했어요.", "과장된 분위기가 오히려 몰입을 방해했어요.",
    "중간중간 웃음 포인트도 뜬금없었어요.", "감정이 올라와야 할 타이밍이 자꾸 빗나갔어요.",
    "설정만 있어 보이고 내용은 빈약했어요.", "배우와 연출이 따로 노는 느낌이었어요."
]

joiners = [
    "그리고", "게다가", "무엇보다", "특히", "전반적으로 보면", "개인적으로는",
    "무난하게", "결과적으로", "생각해보면", "한편으로는"
]

internet_positive = [
    "존잼이었어요", "꿀잼", "생각보다 개좋았음", "와 이건 진짜 좋네요", "연기 미쳤어요 좋게",
    "스토리 진짜 잘 빠졌네요", "끝나고 여운 남는 거 오랜만", "의외로 너무 괜찮았어요",
    "이거 왜 이제 봤지", "재밌게 잘 봄", "호평 많은 이유 알겠음", "와 생각보다 훨씬 좋다",
    "이건 추천할만함", "몰입감 좋았음", "잔잔한데 좋음", "가볍게 보기 좋았어요"
]

internet_negative = [
    "개노잼", "솔직히 너무 별로였음", "왜 재밌다는지 모르겠어요", "시간 아까웠어요 진심",
    "스토리 너무 뻔함", "연기 왜 이렇게 어색하지", "끝까지 보기 힘들었음", "이건 좀 심했어요",
    "너무 루즈해요", "몰입 1도 안 됨", "평점 너무 후한 듯", "진짜 아쉬움",
    "보다가 몇 번 끊었어요", "기대만 컸네요", "이건 비추", "그냥 그랬음"
]

typo_map = {
    "정말": ["정말", "정말", "진짜", "진짜", "정말루"],
    "좋았어요": ["좋았어요", "좋았어요", "좋았음", "좋았어용"],
    "별로였어요": ["별로였어요", "별로였음", "별루였어요"],
    "재밌었어요": ["재밌었어요", "재밌었음", "잼났어요"],
    "지루했어요": ["지루했어요", "지루했음", "루즈했어요"],
    "추천합니다": ["추천합니다", "추천해요", "추천함"],
    "비추천": ["비추천", "비추", "추천 안 함"],
    "몰입감": ["몰입감", "몰입감", "몰입도"],
    "아쉬웠어요": ["아쉬웠어요", "아쉬웠음", "아쉽네요"],
}

# --- 고도화: 맞춤법 오류 — 실제 오타 패턴 적용 ---
typo_patterns = {
    "정말": ["정말", "진짜", "정말루", "정라"],
    "좋았어요": ["좋았어요", "좋았음", "좋았어용", "좋았어"],
    "별로였어요": ["별로였어요", "별로였음", "별루", "별로"],
    "재밌었어요": ["재밌었어요", "재밌었음", "잼났", "재미있었음"],
    "지루했어요": ["지루했어요", "지루했음", "루즈", "지루함"],
    "추천합니다": ["추천합니다", "추천해요", "추천함", "추천"],
    "비추천": ["비추천", "비추", "추천 안 함", "비추요"],
    "몰입감": ["몰입감", "몰입도", "몰입"],
    "아쉬웠어요": ["아쉬웠어요", "아쉬웠음", "아쉽네요", "아쉽다"],
    "완성도": ["완성도", "완성도가", "완성도가 높았어요"],
}

# --- 고도화: 실제 리뷰 길이 분포 (한국 영화 리뷰 실제 통계 기반) ---
# 평균 120자, 표준편차 50자, 10자 이하 & 300자 초과는 제한
def sample_review_length():
    length = int(np.random.normal(120, 50))
    return max(10, min(length, 300))  # 현실적 범위

# --- 고도화: 감정 혼합 리뷰 생성 로직 (긍정+부정 혼합, 20% 확률) ---
def build_hybrid_review():
    # 혼합 리뷰: 절반은 긍정, 절반은 부정
    pos_part = random.choice([
        random.choice(acting_positive),
        random.choice(story_positive),
        random.choice(visual_positive),
        random.choice(ending_positive)
    ])
    neg_part = random.choice([
        random.choice(acting_negative),
        random.choice(story_negative),
        random.choice(visual_negative),
        random.choice(ending_negative)
    ])
    # 긍정 → 부정 순서로 자연스럽게 전환
    connector = random.choice(["그런데", "그런데도", "그럼에도 불구하고", "다만", "아쉬운 건"])
    hybrid = f"{pos_part} {connector} {neg_part}"
    if random.random() < 0.3:
        hybrid += " " + random.choice(positive_recommends)
    else:
        hybrid += " " + random.choice(negative_recommends)
    return hybrid

# --- 고도화: 사용자 연령대 기반 언어 가중치 ---
# 20대: 인터넷어, 30대: 중간, 40대: 정중한 표현
age_weights = {
    "young": (0.6, 0.3, 0.1),  # 인터넷어 : 단기 : 장기
    "mid":   (0.3, 0.5, 0.2),
    "old":   (0.1, 0.3, 0.6)
}

def select_language_by_age(label, age_group="mid"):
    if label == 1:  # 긍정
        sources = [
            (internet_positive, age_weights[age_group][0]),
            (positive_short, age_weights[age_group][1]),
            (positive_openers + positive_feelings + positive_recommends, age_weights[age_group][2])
        ]
    else:  # 부정
        sources = [
            (internet_negative, age_weights[age_group][0]),
            (negative_short, age_weights[age_group][1]),
            (negative_openers + negative_feelings + negative_recommends, age_weights[age_group][2])
        ]
    
    pool = []
    for items, weight in sources:
        pool.extend([(item, weight) for item in items])
    
    # 가중치 기반 샘플링
    items, weights = zip(*pool) if pool else ([], [])
    return random.choices(items, weights=weights, k=1)[0]


def maybe_typo(text, p=0.18):
    if random.random() > p:
        return text
    for k, vals in typo_map.items():
        if k in text and random.random() < 0.5:
            text = text.replace(k, random.choice(vals), 1)
    return text

def maybe_add_emoji(text, label):
    if random.random() < 0.06:
        emo = random.choice(["ㅎㅎ", "ㅋㅋ", "ㅠㅠ", "!", "!!", "..."])
        if not text.endswith((".", "!", "?", "요", "음", "함", "네요", "ㅠㅠ", "ㅋㅋ", "ㅎㅎ", "...")):
            text += emo
        else:
            text += f" {emo}"
    return text

def clean_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.!?])", r"\1", text)
    text = text.replace("..", ".").replace(" .", ".")
    return text.strip()

def build_pos_short():
    return random.choice(positive_short)

def build_neg_short():
    return random.choice(negative_short)

def build_pos_medium():
    parts = [
        random.choice(watch_contexts),
        random.choice(positive_openers),
        random.choice(positive_feelings) + ".",
        random.choice(positive_recommends)
    ]
    return " ".join(parts)

def build_neg_medium():
    parts = [
        random.choice(watch_contexts),
        random.choice(negative_openers),
        random.choice(negative_feelings) + ".",
        random.choice(negative_recommends)
    ]
    return " ".join(parts)

def build_pos_long():
    parts = [
        f"{random.choice(subjects)} {random.choice(['보면서', '보는 동안', '끝까지'])}",
        random.choice(acting_positive) + ".",
        f"{random.choice(joiners)} {random.choice(story_positive)}.",
        f"{random.choice(joiners)} {random.choice(visual_positive)}.",
        random.choice(ending_positive) + ".",
        random.choice(positive_extras),
        random.choice(positive_feelings) + ".",
        random.choice(positive_recommends)
    ]
    return " ".join(parts)

def build_neg_long():
    parts = [
        f"{random.choice(subjects)} {random.choice(['보면서', '보는 동안', '끝까지'])}",
        random.choice(acting_negative) + ".",
        f"{random.choice(joiners)} {random.choice(story_negative)}.",
        f"{random.choice(joiners)} {random.choice(visual_negative)}.",
        random.choice(ending_negative) + ".",
        random.choice(negative_extras),
        random.choice(negative_feelings) + ".",
        random.choice(negative_recommends)
    ]
    return " ".join(parts)

def build_pos_mixed():
    t = random.randint(1, 8)
    if t == 1:
        return select_language_by_age(1, random.choice(["young", "mid", "old"]))
    if t == 2:
        return random.choice(internet_positive)
    if t == 3:
        return f"{random.choice(subjects)} {random.choice(['정말', '진짜', '생각보다'])} {random.choice(['좋았어요', '괜찮았어요', '인상적이었어요'])}. {random.choice(positive_recommends)}"
    if t == 4:
        return f"{random.choice(acting_positive)}. {random.choice(story_positive)}. {random.choice(positive_recommends)}"
    if t == 5:
        return f"{random.choice(visual_positive)}. {random.choice(ending_positive)}. {random.choice(positive_feelings)}."
    if t == 6:
        return build_pos_medium()
    if t == 7:
        return build_pos_long()
    return f"{random.choice(watch_contexts)} {random.choice(positive_openers)} {random.choice(acting_positive)}. {random.choice(positive_extras)} {random.choice(positive_recommends)}"

def build_neg_mixed():
    t = random.randint(1, 8)
    if t == 1:
        return select_language_by_age(0, random.choice(["young", "mid", "old"]))
    if t == 2:
        return random.choice(internet_negative)
    if t == 3:
        return f"{random.choice(subjects)} {random.choice(['정말', '진짜', '생각보다'])} {random.choice(['별로였어요', '아쉬웠어요', '실망스러웠어요'])}. {random.choice(negative_recommends)}"
    if t == 4:
        return f"{random.choice(acting_negative)}. {random.choice(story_negative)}. {random.choice(negative_recommends)}"
    if t == 5:
        return f"{random.choice(visual_negative)}. {random.choice(ending_negative)}. {random.choice(negative_feelings)}."
    if t == 6:
        return build_neg_medium()
    if t == 7:
        return build_neg_long()
    return f"{random.choice(watch_contexts)} {random.choice(negative_openers)} {random.choice(acting_negative)}. {random.choice(negative_extras)} {random.choice(negative_recommends)}"

def diversify_style(text, label):
    if random.random() < 0.20:
        text = text.replace("입니다.", "이에요.").replace("합니다.", "해요.")
    if random.random() < 0.12:
        text = text.replace("요.", ".")
    if random.random() < 0.10 and len(text) > 20:
        text = text.replace("개인적으로", "솔직히", 1)
    text = maybe_typo(text)
    text = maybe_add_emoji(text, label)
    return clean_text(text)

# --- 고도화: 하이브리드 리뷰 확률 적용 (20% 확률로 혼합) ---
def build_mixed_review(label):
    if random.random() < 0.20:  # 20% 확률로 혼합 리뷰
        return build_hybrid_review()
    return build_pos_mixed() if label == 1 else build_neg_mixed()

def realistic_typo(text):
    if random.random() > 0.15:  # 15% 확률로 오타 삽입
        return text
    
    # 오타는 자주 쓰이는 주요 단어에서만 발생
    for key, variants in typo_patterns.items():
        if key in text and random.random() < 0.6:  # 키워드가 있으면 60% 확률로 교체
            text = text.replace(key, random.choice(variants), 1)
            break
    return text

# --- 고도화: 이모티콘/구두점 분포 현실화 ---
def realistic_emoji(text, label):
    if random.random() < 0.08:  # 8% 확률로 이모티콘
        if label == 1:  # 긍정: "ㅋㅋ", "ㅎㅎ", "!"
            emo = random.choice(["!", "!!", "ㅋㅋ", "ㅋㅋㅋ", "ㅎㅎ", "😍", "👍"])
        else:  # 부정: "ㅠㅠ", "...", "…", "😑"
            emo = random.choice(["ㅠㅠ", "ㅡㅡ^", "ㅜㅜ", "...", "…", "😑", "👎"])
        
        if text and text[-1] not in ".!?…~":
            text += emo
        else:
            text += " " + emo
    return text.strip()

def generate_unique_reviews(target_count, label):
    results = []
    max_tries = target_count * 80
    tries = 0

    while len(results) < target_count and tries < max_tries:
        text = build_mixed_review(label)
        text = realistic_typo(text)
        text = realistic_emoji(text, label)
        text = clean_text(text)

        if 10 <= len(text) <= 300:  # 현실적 길이
            results.append({"content": text, "label": label})

        tries += 1

    if len(results) < target_count:
        raise ValueError(f"{'긍정' if label == 1 else '부정'} 데이터 생성 부족: 목표={target_count}, 생성={len(results)}")

    return results

# --- 데이터 생성 및 pandas DataFrame으로 관리 ---
pos_data = generate_unique_reviews(POS_COUNT, 1)
neg_data = generate_unique_reviews(NEG_COUNT, 0)

dataset = pos_data + neg_data
random.shuffle(dataset)

# --- pandas를 이용한 추가 통계적 고도화 ---
df = pd.DataFrame(dataset)

# 1. 길이 분포 추가 (실제 데이터 분석에 유용)
df['length'] = df['content'].str.len()

# 2. 감정 혼합 리뷰 비율 확인
df['is_hybrid'] = df['content'].apply(lambda x: any(w in x for w in ["그런데", "다만", "그럼에도 불구하고"]) and any(w in x for w in story_positive + acting_positive + visual_positive + ending_positive) and any(w in x for w in story_negative + acting_negative + visual_negative + ending_negative))

# 3. 언어 스타일 분류 (간단한 텍스트 기반)
df['language_style'] = df['content'].apply(lambda x: 
    "internet" if any(k in x for k in internet_positive + internet_negative) else
    "short" if len(x) < 40 else
    "medium" if len(x) < 120 else "long"
)

# 4. 품질 필터링: 3자 이하 리뷰 제거
df = df[df['length'] >= 5].reset_index(drop=True)

# 5. 라벨 균형 재확인
print(f"✅ 최종 데이터셋 크기: {len(df)}")
print(f"✅ 긍정: {df['label'].sum()}, 부정: {len(df) - df['label'].sum()}")

# 6. 길이 분포 통계 출력
print("\n📊 리뷰 길이 통계 (pandas 기반):")
print(df['length'].describe().round(1))

# 7. 하이브리드 리뷰 비율
hybrid_ratio = df['is_hybrid'].mean()
print(f"\n🔄 하이브리드 리뷰 비율: {hybrid_ratio:.2%}")

# 8. 언어 스타일 분포
print("\n📖 언어 스타일 분포:")
print(df['language_style'].value_counts(normalize=True).round(3))

# CSV 저장
df[['content', 'label']].to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

print(f"\n✅ {OUTPUT_FILE} 생성 완료")
