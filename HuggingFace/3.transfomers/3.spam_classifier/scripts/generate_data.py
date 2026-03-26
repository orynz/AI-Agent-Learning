"""
한국어 스팸/정상 메일 데이터셋 생성기
"""
import random
import pandas as pd

# ─────────────────────────────────────────
# 노이즈 추가 유틸리티 함수
# ─────────────────────────────────────────

def add_typo(text: str, prob: float = 0.3) -> str:
    """문장 내 무작위 글자에 오타 삽입"""
    if random.random() > prob:
        return text
    chars = list(text)
    for i in range(len(chars)):
        if chars[i].isalpha() or chars[i].isdigit():
            if random.random() < 0.1:  # 10% 확률로 글자 변경
                if chars[i].isalpha():
                    chars[i] = random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
                else:
                    chars[i] = str(random.randint(0, 9))
    return ''.join(chars)

def add_symbols(text: str, prob: float = 0.4) -> str:
    """특수문자 무작위 삽입"""
    if random.random() > prob:
        return text
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?~`№§"
    chars = list(text)
    for _ in range(random.randint(1, 3)):
        pos = random.randint(0, len(chars))
        chars.insert(pos, random.choice(symbols))
    return ''.join(chars)

def add_code_like(text: str, prob: float = 0.25) -> str:
    """URL, UUID, 비밀번호 등 코드 유사 패턴 삽입"""
    if random.random() > prob:
        return text
    if random.random() < 0.5:
        short_url = "bit.ly/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=6))
        text = text + " " + short_url
    else:
        uuid = "".join(random.choices("0123456789abcdef", k=8)) + "-" + "".join(random.choices("0123456789abcdef", k=4))
        text = text + " [ID: " + uuid + "]"
    return text

def add_emoji(text: str, prob: float = 0.35) -> str:
    """이모지 삽입"""
    if random.random() > prob:
        return text
    emojis = ["💰", "🚀", "🔥", "⚠️", "📱", "💳", "✅", "💯", "🎯", "✨", "‼️", "❗", "🤑"]
    for _ in range(random.randint(1, 2)):
        text += " " + random.choice(emojis)
    return text

def add_repetition(text: str, prob: float = 0.2) -> str:
    """과도한 강조 및 반복"""
    if random.random() > prob:
        return text
    repeats = ["!!", "!!!", "★★★", "MAX", "지금!!", "지금 지금!!", "무조건!!", "즉시!!"]
    if "마감" in text or "클릭" in text:
        text += random.choice(repeats)
    return text

def add_whitespace(text: str, prob: float = 0.2) -> str:
    """불필요한 공백/탭/줄바꿈 삽입"""
    if random.random() > prob:
        return text
    ws = [" ", "  ", "\t", "\n", " \t ", " \n "]
    words = text.split()
    for i in range(random.randint(1, len(words)//2)):
        pos = random.randint(0, len(words))
        words.insert(pos, random.choice(ws))
    return ''.join(words)

def add_phone_or_account(text: str, prob: float = 0.2) -> str:
    """가짜 전화번호/계좌번호 삽입"""
    if random.random() > prob:
        return text
    if random.random() < 0.5:
        phone = f"☎ {random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        text += " " + phone
    else:
        account = f"계좌: {random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100000, 999999)}"
        text += " " + account
    return text

def add_korean_slang(text: str, prob: float = 0.15) -> str:
    """휴대폰 문자 스타일 줄임말 삽입"""
    if random.random() > prob:
        return text
    slangs = ["ㅇㅋ", "ㅈㅈ", "ㄳ", "ㄷㄷ", "ㅋㅋ", "ㅠㅠ", "ㅎㅎ", "ㄱㅇ", "ㅇㅇ", "ㄴㄴ"]
    if "클릭" in text or "확인" in text:
        text += " " + random.choice(slangs)
    return text

def insert_random_chars(text: str, prob: float = 0.1) -> str:
    """문장 중간에 랜덤 한글/영문/숫자 1~3글자 삽입"""
    if random.random() > prob:
        return text
    chars = "가나다라마바사아자차카타파하abcdefghijklmnopqrstuvwxyz0123456789"
    for _ in range(random.randint(1, 3)):
        pos = random.randint(1, len(text) - 1)
        insert = "".join(random.choice(chars) for _ in range(random.randint(1, 3)))
        text = text[:pos] + insert + text[pos:]
    return text

def apply_all_noise(text: str) -> str:
    """모든 노이즈 적용"""
    text = add_typo(text, 0.4)
    text = add_symbols(text, 0.5)
    text = add_code_like(text, 0.3)
    text = add_emoji(text, 0.4)
    text = add_repetition(text, 0.25)
    text = add_whitespace(text, 0.2)
    text = add_phone_or_account(text, 0.2)
    text = add_korean_slang(text, 0.2)
    text = insert_random_chars(text, 0.15)
    return text.strip()

# ─────────────────────────────────────────
# 스팸 템플릿 & 변수
# ─────────────────────────────────────────
SPAM_TEMPLATES = [
    "{prefix} {bank} {event}! {benefit} 받으시려면 {action}",
    "{prefix} {loan_type} 대상자 선정. {interest} 금리로 {action}",
    "{prefix} {profit} 확정! {crypto} VVIP 정보 {action}",
    "{urgent} {scam_urgent}. 본인이 아니시면 {action}",
    "{prefix} {discount} 혜택이 {deadline} 마감됩니다. {action}",
    "{urgent} {bank} {scam_urgent} 안내. 즉시 {action}",
    "{prefix} 정부지원 {loan_type} 승인 안내. {benefit} 확인 후 {action}",
    "[{bank}] {person}님, {crypto} 폭등 예정 종목. {profit} 원하시면 {action}",
    "{urgent} 계정 보안 위협 감지. {scam_urgent} 확인을 위해 {action}",
    "{prefix} {person}님 전용 {loan_type} 한도 조회 무료! 지금 {action}",
    "(광고) 신용불량자도 가능한 {loan_type}. {interest}. {action}",
    "[이벤트] {bank} X {crypto} 콜라보. {profit} 기회 {action}",
    "{urgent} 개인정보 유출 의심. {scam_urgent}. 지금 {action}",
    "{prefix} {benefit} 미수령 확인됨. 수령기한 {deadline}. {action}",
    "★ {crypto} {profit} 검증 완료! 오늘만 무료 공개. {action}",
]

SPAM_VARS = {
    "prefix": ["(광고)", "[광고]", "(Web발신)", "[WEB발신]", "[Web발신]", "(web발신)", "▶광고◀", "【광고】", "(이벤트)", "[이벤트]"],
    "urgent": ["[긴급]", "[필독]", "[중요]", "[경고]", "[안내]", "[시스템 경고]", "【긴급】", "【중요】"],
    "bank": ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "카카오뱅크",
             "토스뱅크", "케이뱅크", "기업은행", "SC제일은행", "새마을금고", "우체국"],
    "event": ["당첨", "특별 선정", "VVIP 대상자", "미수령 혜택", "지원금 대상",
              "우수고객 혜택", "특별 이벤트", "환급금 발생"],
    "benefit": ["현금 100만원", "무료 쿠폰", "백화점 상품권", "지원금 50만원",
                "투자 지원금", "무료 주식 1주", "스타벅스 기프티콘", "첫 달 이자 면제"],
    "action": ["지금 클릭하세요", "링크 확인", "무료 상담 신청", "바로 접속",
               "고객센터 문의", "앱 다운로드", "여기를 눌러주세요", "채팅방 입장"],
    "loan_type": ["신용 대출", "대환 대출", "소상공인 대출", "정부지원 대출",
                  "전세자금 대출", "마이너스 통장", "무보증 대출", "생계자금 대출", "햇살론"],
    "interest": ["연 1.5%", "최저 2.9%", "3%대 고정", "무이자", "금리 인하", "연 2%대", "초저금리"],
    "profit": ["수익률 300%", "월 500만 수익", "원금 200% 보장", "상한가 적중",
               "매일 10% 수익", "고수익 보장", "손실 복구"],
    "crypto": ["비트코인", "이더리움", "알트코인", "상장 예정 코인", "세력주",
               "급등주", "AI 테마주", "2차전지 관련주", "공모주"],
    "scam_urgent": ["해외 결제 승인", "이상 거래 탐지", "계좌 일시 정지",
                    "비밀번호 변경 알림", "본인 인증 실패", "대출 연체 경고", "단말기 등록 알림"],
    "discount": ["초특가 할인", "한정 특가", "수수료 면제", "VIP 수수료 할인", "가입비 면제"],
    "deadline": ["오늘", "자정", "내일 오전", "마감 임박", "선착순 100명", "금일 18시"],
    "person": ["고객", "회원", "투자자", "사장", "대표"],
}

# ─────────────────────────────────────────
# 정상 템플릿 & 변수
# ─────────────────────────────────────────
HAM_TEMPLATES = [
    "{prefix} 안녕하세요 {person}님, {topic} 관련해서 연락드립니다.",
    "[{dept}] {date} {topic} {request}.",
    "{prefix} {date} {time}에 {activity} 예정입니다. {request}.",
    "{prefix} {bank} {finance_action} 안내드립니다. (금액: {amount})",
    "{person}님, 요청하신 {doc_type} 첨부해 드립니다. {request}.",
    "[{dept}] {doc_type} 결재 요청의 건",
    "FW: {topic} 진행 상황 공유드립니다.",
    "RE: {date} {activity} 관련 문의 사항",
    "[{dept}] {date} {time} {activity} 일정 확인 요청",
    "{person}님, {doc_type} 검토 후 {request}",
    "안녕하세요. {dept}입니다. {topic} 관련 {request}.",
    "[시스템 알림] {bank} {finance_action} 처리 완료되었습니다.",
    "{prefix} {date} {activity} 참석 여부 확인 부탁드립니다.",
    "수신: {person}님 / 발신: {dept} / 건: {doc_type} 제출",
    "[알림] {date} {time} {activity}가 확정되었습니다. {request}.",
]

HAM_VARS = {
    "prefix": ["[알림]", "[안내]", "[공지]", "[회신]", "[공유]", "[요청]"],
    "dept": ["재무팀", "인사팀", "영업본부", "마케팅팀", "회계팀", "전략기획실",
             "IT지원팀", "감사팀", "컴플라이언스팀", "보안팀", "경영지원팀", "법무팀"],
    "topic": ["주간 업무", "프로젝트 결산", "월간 보고서", "TF팀 회의",
              "내년도 예산안", "신규 계약건", "고객사 미팅", "감사 준비", "보안 지침"],
    "date": ["오늘", "내일", "이번 주 금요일", "다음 주", "금일", "명일", "10일", "15일", "월말"],
    "time": ["오전 10시", "오후 2시", "오후 3시 반", "오전 11시", "퇴근 전", "업무 시작 전"],
    "request": ["자료 검토 부탁드립니다", "메일 확인 바랍니다", "피드백 요청드립니다",
                "승인 부탁드립니다", "회신 요망", "첨부파일 참조 바랍니다", "서명 부탁드립니다"],
    "activity": ["임원진 미팅", "주간 회의", "부서 점심 약속", "업무 협의",
                 "킥오프 미팅", "화상 회의", "세미나", "워크샵", "팀 빌딩"],
    "person": ["팀장", "부장", "과장", "대리", "사원", "담당자", "본부장", "차장", "주임"],
    "bank": ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "기업은행", "법인카드"],
    "finance_action": ["입금 완료", "출금 안내", "자동이체 예정", "카드 대금 명세서",
                       "이체 내역", "급여 입금", "세금계산서 발행"],
    "amount": ["1,000,000원", "500,000원", "3,500,000원", "150,000원", "10,000,000원", "별도 첨부"],
    "doc_type": ["결산 보고서", "지출 결의서", "품의서", "급여 명세서", "세금계산서",
                 "계약서 초안", "기안서", "회의록", "견적서", "업무 일지"],
}


def _fill(template: str, variables: dict) -> str:
    keys = [k for _, k, _, _ in template._formatter_parser() if k]  # type: ignore
    return template.format(**{k: random.choice(variables[k]) for k in keys if k in variables})


def _fill_template(template: str, variables: dict) -> str:
    import string
    formatter = string.Formatter()
    keys = [field_name for _, field_name, _, _ in formatter.parse(template) if field_name]
    filled = template.format(**{k: random.choice(variables[k]) for k in keys if k in variables})
    return filled


def generate_dataset(size: int = 10000, spam_ratio: float = 0.5, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    n_spam = int(size * spam_ratio)
    n_ham = size - n_spam

    spam_texts = [_fill_template(random.choice(SPAM_TEMPLATES), SPAM_VARS) for _ in range(n_spam)]
    ham_texts  = [_fill_template(random.choice(HAM_TEMPLATES),  HAM_VARS)  for _ in range(n_ham)]

    # 노이즈 적용
    spam_texts = [apply_all_noise(text) for text in spam_texts]
    ham_texts  = [apply_all_noise(text) for text in ham_texts]  # 정상 메일에도 약간의 노이즈 (정상 메일도 실제엔 오류 있을 수 있음)

    texts  = spam_texts + ham_texts
    labels = [1] * n_spam + [0] * n_ham

    df = pd.DataFrame({"text": texts, "label": labels})
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


if __name__ == "__main__":
    df = generate_dataset(size=1000)
    out = "spam_dataset.csv"
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"[INFO] 데이터셋 생성 완료: {out} ({len(df)}건)")
    print(df["label"].value_counts())
