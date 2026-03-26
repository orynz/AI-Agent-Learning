"""
스팸 분류 모델 학습 + 평가/검증 스크립트
"""
import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
import platform
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, accuracy_score,
    roc_curve, precision_recall_curve, average_precision_score,
    ConfusionMatrixDisplay,
)

# ─── 폰트 설정 (한글) ────────────────────────────────
# 한글 폰트 설정 (Windows의 경우 맑은 고딕 사용)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac
    plt.rc('font', family='AppleGothic')
else: # Linux/Colab (나눔폰트 설치 필요)
    plt.rc('font', family='NanumGothic')

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False


REPORT_DIR = "reports"
MODEL_DIR  = "model"


def _ensure_dirs():
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR,  exist_ok=True)

# ─────────────────────────────────────────────────────
# 노이즈 제거 함수 (실제 스팸/정상 메일의 본질 텍스트만 추출)
# ─────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """
    스팸/정상 메일에서 노이즈를 제거하고 본질적인 한국어 텍스트만 남김.
    - 이모지, 특수문자, URL, UUID, 전화번호, 반복 기호, 줄임말, 랜덤 문자 제거
    - 공백 정리, 한글/숫자/영문/표준 문장부호만 유지
    """
    if not isinstance(text, str):
        return ""

    # 1. 이모지 제거
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # 2. URL/짧은 링크 제거
    text = re.sub(r'https?://[^\s]+', '', text)
    text = re.sub(r'bit\.ly/[^\s]+', '', text)
    text = re.sub(r'[\w-]{6,10}\.com', '', text)

    # 3. UUID, ID 패턴 제거
    text = re.sub(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', '', text, flags=re.IGNORECASE)

    # 4. 전화번호/계좌번호 제거
    text = re.sub(r'☎\s*\d{3}-\d{4}-\d{4}', '', text)
    text = re.sub(r'계좌:\s*\d{3}-\d{3}-\d{6}', '', text)

    # 5. 특수문자 과도한 반복 제거 (예: !!!! → !, ★★★ → ★)
    text = re.sub(r'([!@#$%^&*()_+\-=\[\]{}|;:,.<>?~`№§])\1+', r'\1', text)

    # 6. 휴대폰 문자 줄임말 제거 (ㅇㅋ, ㅈㅈ, ㄳ 등)
    text = re.sub(r'\b[ㄱ-ㅎㅏ-ㅣ가-힣]{1,2}\b', '', text)  # 1~2글자 한글은 대부분 줄임말

    # 7. 랜덤 삽입 문자 제거 (문장 중간에 삽입된 한글/영문/숫자 1~3글자)
    # → 단어 단위로 분리 후, 1~3글자이며 일반 단어가 아닌 경우 제거
    words = text.split()
    cleaned_words = []
    for word in words:
        if len(word) <= 3 and not re.fullmatch(r'[가-힣]+|[a-zA-Z]+|[0-9]+', word):
            continue  # 랜덤 삽입 문자로 간주
        cleaned_words.append(word)
    text = ' '.join(cleaned_words)

    # 8. 반복 강조 제거 (예: "지금!!!" → "지금")
    text = re.sub(r'([!？？!?]{2,})', '', text)

    # 9. 공백 정리
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# ─────────────────────────────────────────────────────
# 학습 & 평가
# ─────────────────────────────────────────────────────
def train_and_evaluate(csv_path: str = "spam_dataset.csv"):
    _ensure_dirs()

    # 1. 데이터 로드
    df = pd.read_csv(csv_path)
    print(f"[INFO] 데이터 로드: {len(df)}건  |  스팸: {df['label'].sum()}  정상: {(df['label']==0).sum()}")

    X, y = df["text"], df["label"]

    # 2. Train / Test 분리 (80:20, stratified)
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 3. 텍스트 정제: 학습은 노이즈 포함, 테스트는 노이즈 제거
    # X_train  = [clean_text(text) for text in X_train_raw]  # 노이즈 제거하여 테스트
    # X_test  = [clean_text(text) for text in X_test_raw]    # 노이즈 제거하여 테스트
    X_train = X_train_raw.tolist()  # 노이즈 그대로 사용
    X_test = X_test_raw.tolist()    # 노이즈 그대로 사용

    print(f"[INFO] 테스트 데이터 노이즈 제거 완료: {len(X_test)}건")
    
    # 4. TF-IDF 벡터화 (한국어 char n-gram 포함)
    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(2, 5),
        sublinear_tf=True,
        analyzer="char_wb",   # 한국어 형태소보다 char-level이 robust
        min_df=2,
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec  = vectorizer.transform(X_test)

    # 5. 모델 학습
    model = LogisticRegression(
        C=1.0,
        max_iter=1000,
        class_weight="balanced",
        solver="lbfgs",
        random_state=42,
    )
    model.fit(X_train_vec, y_train)

    # ─── 6. 기본 평가 ────────────────────────────────
    preds      = model.predict(X_test_vec)
    probs      = model.predict_proba(X_test_vec)[:, 1]
    roc_auc    = roc_auc_score(y_test, probs)
    avg_prec   = average_precision_score(y_test, probs)
    accuracy   = accuracy_score(y_test, preds)
    cm         = confusion_matrix(y_test, preds)

    report_str = classification_report(y_test, preds, target_names=["정상(Ham)", "스팸(Spam)"])
    print("\n" + "="*55)
    print("[MODEL REPORT]")
    print(f"모델 정확도: {accuracy * 100}%")
    print(report_str)
    print(f"ROC-AUC : {roc_auc:.4f}")
    print(f"Avg Precision (PR-AUC): {avg_prec:.4f}")
    
    df_conf = pd.DataFrame(cm, columns=['예측_정상', '예측_스팸'], index=['실제_정상', '실제_스팸'])
    print("\n ----- 혼동행렬 -----")
    print(df_conf)

    # ─── 7. Cross-validation ─────────────────────────
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    from sklearn.pipeline import Pipeline
    pipe = Pipeline([("tfidf", vectorizer), ("lr", model)])
    # vectorizer는 이미 fit 됐으므로 전체 데이터로 CV
    from sklearn.base import clone
    pipe2 = Pipeline([
        ("tfidf", clone(vectorizer)),
        ("lr",    clone(model)),
    ])
    cv_scores = cross_val_score(pipe2, X, y, cv=skf, scoring="roc_auc")
    print(f"\n5-Fold CV ROC-AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"  per-fold: {[f'{s:.4f}' for s in cv_scores]}")

    # ─── 8. 시각화 저장 ──────────────────────────────
    _plot_confusion_matrix(cm)
    _plot_roc_curve(y_test, probs, roc_auc)
    _plot_pr_curve(y_test, probs, avg_prec)
    _plot_score_distribution(y_test, probs)
    _plot_top_features(model, vectorizer)

    # ─── 9. JSON 리포트 ──────────────────────────────
    report_dict = classification_report(
        y_test, preds, target_names=["ham", "spam"], output_dict=True
    )
    report_dict["roc_auc"]       = roc_auc
    report_dict["pr_auc"]        = avg_prec
    report_dict["cv_roc_auc_mean"] = float(cv_scores.mean())
    report_dict["cv_roc_auc_std"]  = float(cv_scores.std())

    with open(f"{REPORT_DIR}/metrics.json", "w", encoding="utf-8") as f:
        json.dump(report_dict, f, ensure_ascii=False, indent=2)
    print(f"\n[INFO] 리포트 저장: {REPORT_DIR}/metrics.json")

    # ─── 10. 모델 저장 ────────────────────────────────
    save_path = os.path.join(MODEL_DIR, "spam_model.pkl")
    joblib.dump((model, vectorizer), save_path)
    print(f"[INFO] 모델 저장: {save_path}")

    return model, vectorizer


# ─────────────────────────────────────────────────────
# 시각화 함수들
# ─────────────────────────────────────────────────────
def _plot_confusion_matrix(cm):
    fig, ax = plt.subplots(figsize=(5, 4))
    disp = ConfusionMatrixDisplay(cm, display_labels=["정상(Ham)", "스팸(Spam)"])
    disp.plot(ax=ax, colorbar=False, cmap="Blues")
    ax.set_title("혼동 행렬 (Confusion Matrix)")
    plt.tight_layout()
    plt.savefig(f"{REPORT_DIR}/confusion_matrix.png", dpi=150)
    plt.close()
    print(f"[INFO] 저장: {REPORT_DIR}/confusion_matrix.png")


def _plot_roc_curve(y_test, probs, roc_auc):
    fpr, tpr, _ = roc_curve(y_test, probs)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(fpr, tpr, color="#4F81BD", lw=2, label=f"ROC-AUC = {roc_auc:.4f}")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC 커브")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(f"{REPORT_DIR}/roc_curve.png", dpi=150)
    plt.close()
    print(f"[INFO] 저장: {REPORT_DIR}/roc_curve.png")


def _plot_pr_curve(y_test, probs, avg_prec):
    prec, rec, _ = precision_recall_curve(y_test, probs)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(rec, prec, color="#C0504D", lw=2, label=f"PR-AUC = {avg_prec:.4f}")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall 커브")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(f"{REPORT_DIR}/pr_curve.png", dpi=150)
    plt.close()
    print(f"[INFO] 저장: {REPORT_DIR}/pr_curve.png")


def _plot_score_distribution(y_test, probs):
    fig, ax = plt.subplots(figsize=(6, 4))
    spam_probs = probs[y_test == 1]
    ham_probs  = probs[y_test == 0]
    ax.hist(ham_probs,  bins=50, alpha=0.6, color="#4F81BD", label="정상(Ham)")
    ax.hist(spam_probs, bins=50, alpha=0.6, color="#C0504D", label="스팸(Spam)")
    ax.axvline(0.5, color="black", linestyle="--", lw=1.2, label="Threshold=0.5")
    ax.set_xlabel("스팸 확률")
    ax.set_ylabel("빈도")
    ax.set_title("스팸 확률 분포")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{REPORT_DIR}/score_distribution.png", dpi=150)
    plt.close()
    print(f"[INFO] 저장: {REPORT_DIR}/score_distribution.png")


def _plot_top_features(model, vectorizer, top_n=20):
    feature_names = np.array(vectorizer.get_feature_names_out())
    coefs = model.coef_[0]

    top_spam = np.argsort(coefs)[-top_n:][::-1]
    top_ham  = np.argsort(coefs)[:top_n]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.barh(range(top_n), coefs[top_spam][::-1], color="#C0504D", alpha=0.8)
    ax1.set_yticks(range(top_n))
    ax1.set_yticklabels(feature_names[top_spam][::-1], fontsize=8)
    ax1.set_title(f"스팸 Top {top_n} 특성")
    ax1.set_xlabel("계수(Coefficient)")

    ax2.barh(range(top_n), coefs[top_ham][::-1], color="#4F81BD", alpha=0.8)
    ax2.set_yticks(range(top_n))
    ax2.set_yticklabels(feature_names[top_ham][::-1], fontsize=8)
    ax2.set_title(f"정상 Top {top_n} 특성")
    ax2.set_xlabel("계수(Coefficient)")

    plt.suptitle("중요 특성 (TF-IDF Char n-gram)", fontsize=13)
    plt.tight_layout()
    plt.savefig(f"{REPORT_DIR}/top_features.png", dpi=150)
    plt.close()
    print(f"[INFO] 저장: {REPORT_DIR}/top_features.png")


if __name__ == "__main__":
    train_and_evaluate()
