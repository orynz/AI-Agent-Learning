"""
generate_dataset_advanced.py — 실전형 스팸/햄 데이터셋 고도화 생성기
"""

import random
import re
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd



# ══════════════════════════════════════════════════════════════════════════════
# 1. 한국어 조사 헬퍼 (기존 유지)
# ══════════════════════════════════════════════════════════════════════════════

def get_josa(word: str, josa_pair: tuple[str, str]) -> str:
    with_jongseong, without_jongseong = josa_pair
    if not word:
        return without_jongseong

    last_char = word[-1]
    code = ord(last_char) - 0xAC00

    if code < 0 or code > 11171:
        return without_jongseong

    has_jongseong = (code % 28) != 0
    return with_jongseong if has_jongseong else without_jongseong

_JOSA_RULES: dict[str, tuple[str, str]] = {
    "을를": ("을", "를"),
    "은는": ("은", "는"),
    "이가": ("이", "가"),
    "와과": ("과", "와"),
}

# ══════════════════════════════════════════════════════════════════════════════
# 2. 스팸 노이즈(Noise) 생성기 (필터 우회 흉내)
# ══════════════════════════════════════════════════════════════════════════════

def apply_spam_noise(text: str, noise_probability: float = 0.6) -> str:
    """
    일정 확률로 스팸 문장에 오타, 특수문자 삽입, 우회 표현을 적용합니다.
    """
    if random.random() > noise_probability:
        return text

    words = text.split()
    noisy_words = []
    
    for word in words:
        # 30% 확률로 각 단어에 노이즈 적용 (너무 깨지면 형태소 분석이 불가하므로 조절)
        if random.random() < 0.3 and len(word) > 1:
            # 1. 숫자 강조 우회 (예: 100% -> [100%])
            word = re.sub(r'(\d+)', r'[\1]', word)
            
            # 2. 단어 사이 특수문자 삽입 (예: 주식 -> 주.식, 투/자)
            separator = random.choice(['.', '/', '^', ' ', '*', ''])
            if separator:
                word = separator.join(list(word))
                
            # 3. 특수 기호 붙이기
            if random.random() < 0.2:
                word += random.choice(['!!', '~', '♥', '※'])
                
        noisy_words.append(word)
        
    return " ".join(noisy_words)

# ══════════════════════════════════════════════════════════════════════════════
# 3. 고도화된 데이터 풀 (페르소나 및 Hard Ham 추가)
# ══════════════════════════════════════════════════════════════════════════════

POOLS: dict[str, dict] = {
    # --- [기존 스팸 카테고리] ---
    "phishing": {
        "templates": [
            "[{brand}] {issue}. 확인을 위해 {url} 접속 바랍니다.",
            "긴급! {brand} {issue} 안내. {deadline}까지 {action}하지 않으면 제한됩니다. {url}",
        ],
        "brand": ["국민은행", "카카오", "네이버", "국세청"],
        "issue": ["비정상적인 로그인", "미납 세금 안내", "계정 정지 예정"],
        "action": ["비밀번호 재설정", "본인 확인"],
        "url": ["bit.ly/v39x", "secure-check.net"],
        "deadline": ["24시간 이내", "오늘까지"],
    },
    # --- [신규 스팸: 페르소나 다양화] ---
    "spam_urgent": { # 지인 사칭, 다급한 심리 조종
        "templates": [
            "{relation}아 나 지금 {emergency}해서 그런데 {demand} 가능해? {action}.",
            "나 {relation}인데 폰 고장나서 PC로 톡해. {emergency} 때문인데 {demand} 부탁해. {action}!",
        ],
        "relation": ["엄마", "아빠", "친구", "동기"],
        "emergency": ["지갑을 잃어버려서", "급하게 결제할 게 있어서", "사고가 좀 나서"],
        "demand": ["구글 기프트카드 50만원만", "내 계좌로 100만원만 송금", "상품권 대리 결제"],
        "action": ["이따 저녁에 바로 갚을게", "링크로 빨리 보내줘", "확인하면 답장줘"],
    },
    "spam_tech": { # 기술적 보안 경고 흉내 (HTML 메일 스타일)
        "templates": [
            "[System Alert] {device}에서 {threat}가 감지되었습니다. 즉시 {action} 요망. {url}",
            "Webmaster 안내: 귀하의 {device} IP가 {threat}로 차단될 예정입니다. {action}: {url}",
        ],
        "device": ["Windows 10 PC", "Apple iPhone", "등록된 모바일 기기", "회사 사내망"],
        "threat": ["치명적인 트로이목마", "해외 IP 무단 접속", "랜섬웨어 감염 징후"],
        "action": ["백신 다운로드", "방화벽 업데이트", "계정 보호 조치"],
        "url": ["update-korea.com", "sys-defense.net"],
    },
    "spam_info": { # 부동산/투자 등 정보성으로 위장한 스팸
        "templates": [
            "[{region} 개발호재] {asset} {benefit}! {contact}로 연락주시면 고급 정보 드립니다.",
            "여의도 기관 투자자 비공개 {asset} 리포트. {benefit} 보장. {contact} 입장하세요.",
        ],
        "region": ["용인 반도체 클러스터", "강남 재건축", "GTX 노선 신설", "판교 테크노밸리"],
        "asset": ["급매물", "청약 우선권", "세력 매집주", "비상장 코인"],
        "benefit": ["시세차익 3억", "원금 200% 보장", "리스크 제로"],
        "contact": ["하단 카톡방", "1:1 비밀 챗방", "010-XXXX-XXXX"],
    },
    
    # --- [기존 정상(Ham) 카테고리] ---
    "ham_basic": {
        "templates": [
            "{sender}님, {topic}{topic_은는} {time}에 진행될 예정입니다. {detail}",
        ],
        "sender": ["김철수 과장", "이영희", "인사팀"],
        "topic": ["주간 회의", "배송 안내", "결재 요청"],
        "detail": ["확인 부탁드립니다.", "참고하세요."],
        "time": ["오후 2시", "오전 11시"],
    },
    
    # --- [신규 정상: Hard Ham (스팸으로 오해하기 쉬운 정상 메일)] ---
    "ham_newsletter": { # 수익, 투자 단어가 들어가지만 정상적인 뉴스레터
        "templates": [
            "[{sender}] 이번 주 {topic} 동향 및 {keyword} 분석 리포트입니다.",
            "{sender}에서 보내드리는 일일 {keyword} 브리핑. 오늘의 {topic} 주요 뉴스입니다.",
        ],
        "sender": ["매일경제", "토스증권", "삼프로TV", "블룸버그"],
        "topic": ["글로벌 증시", "국내 경제", "부동산 시장", "IT 기업 실적"],
        "keyword": ["투자 지표", "수익률 추이", "금리 인상", "배당금"],
    },
    "ham_bank": { # 결제, 대출 단어가 들어가지만 정상적인 은행 고지서
        "templates": [
            "[{sender}] {customer} 고객님, 이달의 {service} 내역서가 발급되었습니다. (보안메일)",
            "{sender} 안내: {customer}님의 {service} 만기일이 다가오고 있습니다. 앱에서 연장 신청 바랍니다.",
        ],
        "sender": ["신한카드", "국민은행", "우리은행 대출부서", "카카오페이"],
        "customer": ["김철수", "이영희", "박지민", "VIP"],
        "service": ["신용대출 이자 납부", "카드 결제 예정 대금", "주택담보대출", "마이너스 통장"],
    },
    "ham_notice": { # 보안 경고나 링크 클릭을 요구하지만 정상적인 사내 공지
        "templates": [
            "[사내공지] 전사 임직원 대상 {topic} 안내. {action} 바랍니다. {url}",
            "IT지원팀입니다. 최근 {topic} 관련하여 시스템 패치가 진행됩니다. {action} (필수: {url})",
        ],
        "topic": ["정보보안 정기 교육", "비밀번호 변경 캠페인", "사내망 VPN 업데이트"],
        "action": ["금요일까지 필수 이수", "첨부된 매뉴얼을 확인 후 적용", "포털 로그인 후 인증"],
        "url": ["intranet.company.com", "hr-system.local"],
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# 4. 코어 로직 (유효성 검사 및 템플릿 채우기 - 기존 로직 유지)
# ══════════════════════════════════════════════════════════════════════════════
def validate_pools(pools: dict[str, dict]) -> list[str]:
    # (기존 검사 로직과 동일하므로 생략 없이 사용)
    errors: list[str] = []
    for cat, pool in pools.items():
        for tmpl in pool.get("templates", []):
            for placeholder in re.findall(r"\{(\w+)\}", tmpl):
                base_key = placeholder
                for suffix in _JOSA_RULES:
                    if placeholder.endswith(f"_{suffix}"):
                        base_key = placeholder[: -(len(suffix) + 1)]
                        break
                if base_key not in pool and base_key != placeholder:
                    errors.append(f"[{cat}] 템플릿 조사 키 '{placeholder}' → 기준 키 '{base_key}'가 pool에 없음")
    return errors

def fill_template(template: str, pool: dict) -> str:
    placeholders = re.findall(r"\{(\w+)\}", template)
    mapping: dict[str, str] = {}

    for ph in placeholders:
        if ph in mapping: continue
        resolved = False
        for suffix, josa_pair in _JOSA_RULES.items():
            if ph.endswith(f"_{suffix}"):
                base_key = ph[: -(len(suffix) + 1)]
                base_val = mapping.get(base_key) or random.choice(pool[base_key])
                mapping.setdefault(base_key, base_val)
                mapping[ph] = get_josa(base_val, josa_pair)
                resolved = True
                break
        if not resolved:
            mapping[ph] = random.choice(pool[ph])

    return template.format(**mapping)

def _make_suffix() -> str:
    today = datetime.now().strftime("%m/%d")
    return f" [{today} {random.randint(1000, 9999)}]"

# ══════════════════════════════════════════════════════════════════════════════
# 5. 메인 생성 함수
# ══════════════════════════════════════════════════════════════════════════════

def generate_hardcore_dataset(
    target_count: int = 10000,
    spam_ratio: float = 0.5,
    seed: int = 42
) -> pd.DataFrame:
    
    random.seed(seed)
    np.random.seed(seed)

    # 스팸과 정상 카테고리 자동 분류
    spam_cats = [k for k in POOLS.keys() if "ham_" not in k]
    ham_cats = [k for k in POOLS.keys() if "ham_" in k]

    n_spam = int(target_count * spam_ratio)
    n_ham  = target_count - n_spam

    rows: list[dict] = []
    unique_texts: set[str] = set()

    spam_collected = 0
    ham_collected  = 0
    attempts = 0

    while len(rows) < target_count and attempts < 300000:
        attempts += 1
        need_spam = spam_collected < n_spam
        need_ham  = ham_collected  < n_ham

        if need_spam and need_ham:
            is_spam = random.random() < spam_ratio
        else:
            is_spam = need_spam

        # 스팸/정상 카테고리 무작위 선택
        category = random.choice(spam_cats) if is_spam else random.choice(ham_cats)
        label = 1 if is_spam else 0
        
        # 텍스트 생성
        p = POOLS[category]
        template = random.choice(p["templates"])
        raw_text = fill_template(template, p) + _make_suffix()
        
        # ★ 핵심: 스팸 데이터에만 노이즈 적용 ★
        if is_spam:
            final_text = apply_spam_noise(raw_text, noise_probability=0.7)
        else:
            final_text = raw_text

        if final_text not in unique_texts:
            unique_texts.add(final_text)
            rows.append({"text": final_text, "label": label, "type": category})
            if is_spam: spam_collected += 1
            else: ham_collected += 1

    df = pd.DataFrame(rows)
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)

# ══════════════════════════════════════════════════════════════════════════════
# 실행 및 결과 확인
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("🚀 고도화된 하드코어 데이터셋 생성 중...")
    df = generate_hardcore_dataset(target_count=10000, spam_ratio=0.5)
    
    # X = df['text']
    # y = df['label']
    # spam_pipeline = Pipeline([
    #     ('cleaner', SpamTextCleaner(remove_special_chars=True)),  # 1단계: 꼼수(특수문자) 제거
    #     ('tfidf', TfidfVectorizer(max_features=10000)),           # 2단계: 단어 임베딩
    #     ('classifier', RandomForestClassifier(random_state=42))   # 3단계: 분류 모델
    # ])
    
    # spam_pipeline.fit(X, y)
    # cleaned_texts = spam_pipeline.named_steps['cleaner'].transform(X)
    # print("--- 클리닝 전 ---")
    # print(X.tolist())
    # print("\n--- 클리닝 후 (모델이 실제로 보는 텍스트) ---")
    # print(cleaned_texts)
    
    out = Path("spam_mail_dataset.csv")
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"저장 완료: {out}")
