
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB, MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import utils

train_texts = [
    "당첨! 무료 쿠폰을 받으려면 아래 링크를 클릭하세요.",
    "오늘 회의 시간은 오후 3시입니다. 확인 부탁드려요.",
    "입금 확인 바랍니다. 이번 달 카드 명세서입니다.",
    "대출 최저 금리 보장! 지금 바로 상담 신청하세요.",
    "팀장님, 요청하신 보고서 초안 송부드립니다."
]
train_labels = [0, 1, 1, 0, 1]  # 0: 스팸, 1: 정상


df = pd.read_csv(str(utils.path_mgr.get_dir() / "spam_mail_dataset.csv"))
print(df.info())

x = df['text']
y = df['label']   # 1=정상, 0=스팸

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)
print(f"훈련셋: {x_train.shape}, 검증셋: {x_test.shape}")


model = Pipeline([
    ('tfidf', TfidfVectorizer(
        analyzer='char_wb',   # ← 핵심: 한국어는 어절이 아닌 문자 n-gram이 유효
        ngram_range=(2, 4),   #   (2,4)-gram이 형태소 없이 한국어 패턴 포착
        max_features=30000,   # ← 특성 수 확대
        sublinear_tf=True,    # ← log(1+tf) 스케일링, 빈도 폭발 억제
        min_df=2,             # ← 2번 이상 등장한 n-gram만 사용 (노이즈 제거)
    )),
    ('clf', ComplementNB(     # ← MultinomialNB보다 텍스트 분류에 강건
        alpha=1.0,            # ← 기본값(라플라스 스무딩), 0.1은 너무 낮았음
        norm=True,            # ← 클래스 불균형 보정
    )),
])

print("🚀 학습 시작...")
model.fit(x_train, y_train)
print("✅ 학습 완료!")

train_score = model.score(x_train, y_train)
test_score  = model.score(x_test,  y_test)
print(f"\n훈련 정확도: {train_score:.4f}")
print(f"검증 정확도: {test_score:.4f}")

# # 단순 accuracy보다 정밀한 평가
# print("\n📊 분류 리포트:")
# y_pred = model.predict(X_test)
# print(classification_report(y_test, y_pred,
#       target_names=["스팸(0)", "정상(1)"]))

# print("혼동 행렬:")
# cm = confusion_matrix(y_test, y_pred)
# print(f"  TN={cm[0,0]}  FP={cm[0,1]}")
# print(f"  FN={cm[1,0]}  TP={cm[1,1]}")

# 테스트 예측
test_texts = [
    "안녕하세요 팀장님, 내일 점심 식사 가능하신가요?",
    "축하합니다! 1억 원 경품에 당첨되셨습니다. 지금 클릭!",
    "광고) 최저 금리 대출 상품 안내 드립니다.",
    "[신한카드] 이달 카드 이용 대금 청구금액은 125,000원입니다.",
    "[IT지원팀] 사내 VPN 업데이트 관련 필수 패치가 진행됩니다. intranet.company.com",
]

predictions   = model.predict(test_texts)
probabilities = model.predict_proba(test_texts)

print("\n🔍 분석 결과:")
for text, pred, prob in zip(test_texts, predictions, probabilities):
    label = "🚨 스팸(SPAM)" if pred == 0 else "✅ 정상(HAM)"
    score = round(prob[pred] * 100, 2)
    print(f"  메일: {text[:45]}...")
    print(f"  결과: {label}  확신도: {score}%")
    print("  " + "-" * 48)