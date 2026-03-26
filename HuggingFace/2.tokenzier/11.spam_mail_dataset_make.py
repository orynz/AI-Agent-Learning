"""
generate_dataset_advanced.py — 실전형 스팸/햄 데이터셋 고도화 생성기
label: 1 = 정상 메일(Ham), 0 = 스팸 메일(Spam)
"""

import random
import re
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


# ─────────────────────────────────────────
# 한국어 조사 처리
# ─────────────────────────────────────────
def get_josa(word: str, josa_pair: tuple[str, str]) -> str:
    with_jongseong, without_jongseong = josa_pair
    if not word:
        return without_jongseong
    last_char = word[-1]
    code = ord(last_char) - 0xAC00
    if code < 0 or code > 11171:
        return without_jongseong
    return with_jongseong if (code % 28) != 0 else without_jongseong

_JOSA_RULES: dict[str, tuple[str, str]] = {
    "을를": ("을", "를"),
    "은는": ("은", "는"),
    "이가": ("이", "가"),
    "와과": ("과", "와"),
}


# ─────────────────────────────────────────
# 스팸 노이즈 — 실제 스팸에서 쓰이는 우회 기법
# ─────────────────────────────────────────
_HOMOGLYPHS: dict[str, list[str]] = {
    "o": ["0", "ο", "О"],
    "a": ["@", "а"],
    "e": ["3", "е"],
    "i": ["1", "l", "ı"],
    "s": ["$", "ѕ"],
    "무": ["무료", "무·료"],
    "공": ["공짜", "공·짜"],
}

_SPAM_DECORATORS = ["★", "◆", "▶", "※", "【", "】", "☎", "✔", "♣", "✉"]
_EMPHASIS_MARKS  = ["!!", "!!!", "~~", "^^ ", " ☞ ", " → "]


def _obfuscate_word(word: str) -> str:
    """단어 일부를 동형이자 또는 특수문자로 치환 (길이 3 이상만)"""
    if len(word) < 3:
        return word
    chars = list(word)
    for i, ch in enumerate(chars):
        if ch in _HOMOGLYPHS and random.random() < 0.35:
            chars[i] = random.choice(_HOMOGLYPHS[ch])
    return "".join(chars)


def _insert_zwsp(text: str) -> str:
    """단어 사이에 제로-폭 공백 삽입 (필터 우회 기법)"""
    words = text.split()
    result = []
    for w in words:
        if random.random() < 0.25 and len(w) >= 2:
            mid = random.randint(1, len(w) - 1)
            w = w[:mid] + "\u200b" + w[mid:]   # zero-width space
        result.append(w)
    return " ".join(result)


def _add_decoration(text: str) -> str:
    """앞뒤에 강조 기호 추가"""
    dec = random.choice(_SPAM_DECORATORS)
    emp = random.choice(_EMPHASIS_MARKS)
    patterns = [
        lambda t: f"{dec} {t} {dec}",
        lambda t: f"{t}{emp}",
        lambda t: f"{dec}{dec} {t}",
        lambda t: t.replace(" ", random.choice(["·", "~", " "]), 1),
    ]
    return random.choice(patterns)(text)


def _number_formatting(text: str) -> str:
    """금액/퍼센트 숫자 강조 변형: 100만원 → [100]만원, 50% → 50%↑"""
    text = re.sub(r"(\d+)(만원|억|%)", lambda m: f"[{m.group(1)}]{m.group(2)}", text)
    return text


def apply_spam_noise(text: str, intensity: float = 0.6) -> str:
    """
    intensity: 0.0(무노이즈) ~ 1.0(최고강도)
    여러 기법을 확률적으로 조합해 실제 스팸처럼 다양하게 만들어냄.
    """
    if random.random() > intensity:
        return text

    # 기법 1: 숫자/금액 강조
    if random.random() < 0.5:
        text = _number_formatting(text)

    # 기법 2: 동형이자 치환 (30% 확률)
    if random.random() < 0.3:
        words = text.split()
        text = " ".join(_obfuscate_word(w) if random.random() < 0.4 else w for w in words)

    # 기법 3: 제로-폭 공백 삽입 (25% 확률)
    if random.random() < 0.25:
        text = _insert_zwsp(text)

    # 기법 4: 장식 기호 추가 (50% 확률)
    if random.random() < 0.5:
        text = _add_decoration(text)

    return text


# ─────────────────────────────────────────
# 날짜/시간 헬퍼
# ─────────────────────────────────────────
def _rand_date(days_ahead: int = 7) -> str:
    d = datetime.now() + timedelta(days=random.randint(1, days_ahead))
    return d.strftime("%m월 %d일")

def _rand_time() -> str:
    h = random.randint(9, 18)
    m = random.choice([0, 30])
    return f"{'오전' if h < 12 else '오후'} {h if h <= 12 else h-12}시{'30분' if m else ''}"

def _rand_amount() -> str:
    return random.choice(["30만원", "50만원", "100만원", "200만원", "500만원", "1억"])

def _rand_rate() -> str:
    return random.choice(["15%", "20%", "30%", "50%", "200%", "최대 300%"])

def _rand_phone() -> str:
    return f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def _make_suffix() -> str:
    """메일 고유번호처럼 보이는 suffix"""
    today = datetime.now().strftime("%Y%m%d")
    return f" [REF:{today}-{random.randint(10000, 99999)}]"


# ─────────────────────────────────────────
# 데이터 풀 — 스팸(spam_*) / 정상(ham_*)
# ─────────────────────────────────────────
POOLS: dict[str, dict] = {

    # ══════════════ 스팸 ══════════════

    "spam_phishing": {
        "templates": [
            "[{brand}] 고객님의 {issue} 확인이 필요합니다. {deadline}까지 {action}하지 않으면 계정이 정지됩니다. {url}",
            "긴급 보안 알림 | {brand}에서 {issue} 이상 징후 감지. 즉시 {action} 바랍니다. {url}",
            "{brand} 고객센터: {issue} 관련 본인인증이 미완료되었습니다. {deadline} 이내 {url} 접속 필요.",
            "[중요] {brand} 계정에서 {issue}이 확인되었습니다. {action}을 완료하지 않으면 {deadline}에 서비스 이용이 제한됩니다.",
            "{brand}에서 고객님 계정의 {issue}를 감지했습니다. 보안을 위해 {deadline}까지 {url}에서 {action} 해주세요.",
            "⚠️ {brand} 보안센터: {issue} 발생! 지금 바로 {action}하세요 → {url}",
            "[자동발송] {brand} {issue} 처리 안내. {deadline} 초과 시 자동 탈퇴 처리됩니다. {action}: {url}",
        ],
        "brand":    ["KB국민은행", "카카오뱅크", "네이버페이", "국세청", "건강보험공단", "NH농협은행", "삼성카드", "하나은행", "쿠팡"],
        "issue":    ["비정상 로그인 시도", "미납 세금 고지", "개인정보 유출 가능성", "계정 도용 의심 접속", "카드 한도 초과 결제 시도", "포인트 만료 예정", "보안등급 하락"],
        "action":   ["비밀번호 즉시 재설정", "본인인증 완료", "계좌 잠금 해제", "신분증 사진 재등록", "OTP 재발급"],
        "url":      ["bit.ly/3kRx9z", "naver-secure.net/auth", "kb-check.link", "gov-iden.kr/verify", "kakao-safe.net"],
        "deadline": ["24시간 이내", "오늘(금) 오후 6시", "48시간 이내", "3일 이내"],
    },

    "spam_investment": {
        "templates": [
            "[비공개 투자 정보] {region} {asset} 관련 세력 매집 정보 공유. {benefit} 가능. {contact} 참여하세요.",
            "기관 투자자 전용 {asset} 리포트 배포 중. {region} 관련 {benefit} 예상. 지금 {contact} 입장하세요.",
            "{region} 개발호재 선점! {asset}으로 {benefit} 실현한 분들의 후기 공유 → {contact}",
            "주식 고수의 단기 {asset} 픽! {region} 테마주 {benefit} 예측. 참여 희망 시 {contact} 문의.",
            "오늘 딱 {num}명만 모집합니다. {region} {asset} {benefit} 보장. 서두르세요 → {contact}",
            "✅ 검증된 {asset} 전략으로 지난달 {benefit} 달성. {region} 다음 타깃 공개 중. {contact}",
            "[극비] {region} {asset} 내부 정보. 공개 전 {benefit} 기회. 지금 {contact} 클릭.",
        ],
        "region":  ["강남 재건축", "GTX-A 노선 인근", "용인 반도체 클러스터", "판교 제2테크노밸리", "인천 검단 신도시", "세종 행정중심지", "부산 에코델타시티"],
        "asset":   ["급매물 아파트", "비상장 코인", "세력 집중 중소형주", "청약 당첨권 양도", "NFT 선착순 민팅", "원자재 선물 포지션"],
        "benefit": ["시세차익 3억 이상", "연 수익률 200%", "원금 2배 보장", "30일 내 50% 수익", "리스크 제로 안전 수익"],
        "contact": ["하단 오픈카톡 참여", "1:1 텔레그램 채널 입장", "아래 링크 클릭", "010-XXXX-XXXX 문자"],
        "num":     ["5", "10", "선착순 3"],
    },

    "spam_impersonation": {
        "templates": [
            "{relation}야 나 지금 급해. {emergency} 때문에 {demand} 가능해? {followup}",
            "{relation}아 폰 잃어버려서 친구 PC로 연락해. {emergency}인데 {demand} 부탁해도 될까? {followup}",
            "나 {relation}인데 지금 {emergency}. {demand} 해줄 수 있어? {followup}",
            "[{relation} 번호 변경 안내] 새 번호로 저장해줘. 그리고 {emergency}라서 {demand} 급하게 부탁해. {followup}",
            "{relation} 나야. {emergency} 상황인데 {demand} 잠깐만 해줄 수 있어? {followup}",
        ],
        "relation":  ["엄마", "아빠", "친구", "동기", "팀장님", "선배", "이모"],
        "emergency": ["지갑을 잃어버려서", "해외 출장 중인데 카드가 막혀서", "급하게 계약금을 내야 해서", "통장 점검 중이라", "사고가 나서 병원비가 필요해서"],
        "demand":    ["구글 기프트카드 10만원권 3장만 구매해줘", "내 계좌로 50만원만 송금해줘", "편의점 상품권 30만원어치만 끊어줘", "네이버페이로 바로 100만원 보내줘"],
        "followup":  ["저녁에 바로 갚을게", "계좌번호 알려주면 바로 보낼게", "내일 오전에 현금으로 줄게", "카톡으로 링크 보낼게 거기서 처리해줘"],
    },

    "spam_tech_alert": {
        "templates": [
            "[System Alert] {device}에서 {threat} 감지됨. 즉시 {action} 요망. 방치 시 {consequence}. → {url}",
            "귀하의 {device}이 {threat}에 노출되어 있습니다. {deadline}까지 {action}하지 않으면 {consequence}. {url}",
            "보안 경고: {device} {threat} 발생. 아래 {action}를 반드시 수행하세요. {url}",
            "[긴급] {device} 보안 취약점 발견 — {threat}. 무료 {action}으로 즉시 해결: {url}",
            "ALERT: Your {device}이 {threat}로 감염된 것으로 보입니다. 지금 {action}: {url} ({deadline})",
        ],
        "device":      ["Windows 11 PC", "iPhone / Android 기기", "공유기(Router)", "회사 사내망 IP", "등록된 모바일 기기"],
        "threat":      ["치명적 랜섬웨어 감염 징후", "해외 IP 무단 접속 시도 23건", "개인정보 유출 악성코드", "DDOS 공격 대상 등록", "불법 채굴 소프트웨어"],
        "action":      ["무료 백신 즉시 설치", "방화벽 긴급 패치 적용", "계정 보호 조치 완료", "원격 보안 점검 예약"],
        "consequence": ["데이터 전체 삭제", "금융 정보 유출", "계정 영구 정지", "법적 책임 발생"],
        "url":         ["protect-pc.kr/scan", "mobile-guard.net", "secure-update.link"],
        "deadline":    ["24시간 내", "즉시", "오늘 자정 전"],
    },

    "spam_ad_illegal": {
        "templates": [
            "성인 {product} 무료 체험 이벤트. {offer}. 지금 신청: {contact}",
            "[19금 한정] {product} 회원 가입 시 {offer}. 비밀 보장 {contact}",
            "불법 {product} 공급망 직접 연결. {offer}. 문의: {contact} (수사망 피해 운영 중)",
            "{product} {offer} 보장. 타 업체 비교 불가. 전국 배송 {contact}",
            "오늘만 {product} {offer} 진행 중. 재고 소진 시 마감. 바로 연락: {contact}",
        ],
        "product": ["대출 작업", "신분증 대여", "통장 매입", "불법 의약품", "도박 사이트 가입코드"],
        "offer":   ["수수료 0원", "당일 처리 100%", "전액 선불 없이 진행", "무한 리필 서비스"],
        "contact": ["텔레그램 @xxxx", "카톡 ID: spam0001", "010-XXXX-XXXX", "비밀 채널 링크 DM"],
    },

    "spam_lottery": {
        "templates": [
            "축하합니다! 고객님이 {prize} 당첨되셨습니다. {deadline}까지 {action}하시면 즉시 지급. {url}",
            "[당첨 안내] {event} 추첨 결과, 고객님이 {prize} 수령 대상입니다. {action}: {url}",
            "🎉 특별 추첨에서 {prize} 당첨! 수령을 위해 {deadline}까지 {action}해주세요. {url}",
            "{event} 이벤트 참여 완료! {prize} 발송을 위해 개인정보 확인이 필요합니다. {url}",
        ],
        "prize":    ["100만원 상품권", "최신 아이폰 15 Pro", "해외여행 패키지 2인", "300만원 현금", "명품 가방"],
        "event":    ["연말 감사", "1억 명 달성 기념", "창립 20주년", "봄맞이 특별"],
        "action":   ["배송지 입력", "본인인증 완료", "세금 처리 비용 납부", "계좌번호 등록"],
        "url":      ["event-win.kr/claim", "prize-check.net", "gift-award.link"],
        "deadline": ["48시간 이내", "3일 이내", "내일 자정 전"],
    },


    # ══════════════ 정상 메일 ══════════════

    "ham_work": {
        "templates": [
            "[{sender}] {topic} 관련 {doc_type}을 공유드립니다. {action} 부탁드립니다.",
            "안녕하세요, {sender}입니다. {topic} 건으로 {doc_type} 첨부하오니 검토 후 {action} 주시기 바랍니다.",
            "{sender} 드림: {topic} 관련 {action} 요청드립니다. 기한은 {deadline}입니다.",
            "수신: 전체 / 발신: {sender} | 제목: {topic} {doc_type} 안내 — {action} 바랍니다.",
            "안녕하세요. {topic} 관련하여 {doc_type}을 아래와 같이 전달드립니다. {action}.",
            "[{sender}] {topic}에 대한 검토 의견 요청드립니다. {deadline}까지 회신 부탁드립니다.",
        ],
        "sender":    ["기획팀 이준혁 과장", "마케팅부 박소연 대리", "CFO 실", "인사팀 김민정", "영업1팀 최동훈", "법무팀"],
        "topic":     ["Q3 실적 검토", "신규 파트너사 계약", "내년도 예산 편성", "조직 개편 방향", "프로젝트 킥오프", "고객사 제안서"],
        "doc_type":  ["초안", "최종본", "검토 요청 문서", "계약서 사본", "발표 자료", "회의록"],
        "action":    ["검토 후 의견 주시면 감사하겠습니다", "확인 후 서명 요청드립니다", "내용 참고 부탁드립니다", "수정 사항 있으시면 알려주세요", "첨부 파일 확인 부탁드립니다"],
        "deadline":  ["이번 주 금요일 오전까지", "내일 오후 5시까지", "다음 주 월요일 오전까지", "3월 31일(월)까지"],
    },

    "ham_meeting": {
        "templates": [
            "[회의 일정] {topic} 관련 {type} 안내: {date} {time}, {location}에서 진행됩니다. {extra}",
            "안녕하세요. {date} {time} {topic} {type}이 {location}에서 예정되어 있습니다. {extra}",
            "{topic} {type} 일정 공유드립니다. 일시: {date} {time} / 장소: {location}. {extra}",
            "수신 확인 부탁드립니다. {date} {time} {type}({topic}) 참석 가능 여부를 {deadline}까지 회신주세요.",
            "[{type} 초대] {topic} / {date} {time} / {location} / 준비물: {extra}",
        ],
        "topic":    ["주간 업무 보고", "신규 서비스 런칭 계획", "임원 전략 회의", "팀 빌딩 워크숍", "고객사 미팅", "하반기 OKR 점검"],
        "type":     ["회의", "화상 회의", "워크숍", "세미나", "킥오프 미팅", "브리핑"],
        "date":     ["3월 28일(금)", "4월 1일(화)", "4월 3일(목)", "4월 7일(월)", "3월 31일(월)"],
        "time":     ["오전 10시", "오후 2시", "오후 3시30분", "오전 11시", "오후 4시"],
        "location": ["본사 3층 대회의실", "판교 오피스 B동 612호", "Zoom 링크(내부 캘린더)", "여의도 IFC 20층", "부산지사 세미나실"],
        "extra":    ["사전 자료는 첨부 파일을 확인해 주세요.", "간단한 현황 공유 후 질의응답 순으로 진행됩니다.", "온/오프라인 하이브리드로 진행됩니다.", "노트북 지참 바랍니다."],
        "deadline": ["내일 오후 3시", "이번 주 목요일", "오늘 중"],
    },

    "ham_delivery": {
        "templates": [
            "[{courier}] 주문번호 {order_id} 상품이 {status}. {detail}",
            "{courier} 배송 안내: {order_id}번 주문 상품이 현재 {status} 상태입니다. {detail}",
            "안녕하세요. {courier}입니다. 고객님의 {order_id} 주문이 {status}하였습니다. {detail}",
            "[배송 완료 알림] {courier}을 통해 발송된 상품({order_id})이 {status}. {detail}",
        ],
        "courier":  ["CJ대한통운", "롯데택배", "한진택배", "쿠팡로켓배송", "네이버쇼핑 배송"],
        "order_id": ["ORD-28471920", "ORD-93847561", "ORD-11029384", "ORD-66738291", "ORD-44920183", "ORD-75610293"],
        "status":   ["출고 완료되어 배송 중입니다", "오늘 오전 중 도착 예정입니다", "배송 완료되었습니다", "물류 센터 입고 처리되었습니다"],
        "detail":   ["배송 현황은 앱에서 실시간으로 확인하실 수 있습니다.", "부재 시 경비실에 맡겨드렸습니다.", "도착 전 미리 연락드리겠습니다.", "배송 관련 문의는 고객센터(1588-XXXX)로 연락주세요."],
    },

    "ham_newsletter": {
        "templates": [
            "[{sender}] {date_str} {topic} 주요 뉴스 브리핑입니다. {headline}",
            "{sender} 뉴스레터: {topic} 동향 및 {keyword} 심층 분석 — {headline}",
            "📰 {sender} 오늘의 {topic}: {headline} 외 {num}건의 주요 기사.",
            "[{sender} 주간 리포트] {topic} 분야 이번 주 핵심 이슈: {headline}",
            "{sender}에서 전달드리는 {topic} 인사이트 레터 ({date_str}) — {headline}",
        ],
        "sender":    ["매일경제 뉴스레터", "토스증권 리서치", "삼프로TV", "한국경제 마켓", "블룸버그 코리아", "딥다이브 by 조선일보"],
        "topic":     ["글로벌 증시", "국내 경기 지표", "부동산 시장 동향", "AI·빅테크 기업 실적", "금리·통화 정책", "스타트업 투자"],
        "keyword":   ["투자 지표 변화", "기준금리 전망", "배당·수익률 추이", "공시 자료 분석", "섹터 순환매"],
        "headline":  ["미국 연준 금리 동결 여파 분석", "국내 반도체 수출 7개월 연속 증가", "2025 상반기 IPO 시장 전망", "챗GPT 경쟁사 발표에 엔비디아 강세"],
        "date_str":  ["03/26", "03/25", "03/24", "03/20", "03/17", "03/10"],
        "num":       ["3", "5", "7", "10"],
    },

    "ham_bank_legit": {
        "templates": [
            "[{sender}] {customer}님, {service} 내역서가 발급되었습니다. 앱 또는 {url}에서 확인하세요.",
            "{sender} 안내: {customer}님의 {service} 만기일({deadline})이 도래합니다. 앱에서 연장 신청 바랍니다.",
            "[{sender}] 이달 {service} 청구금액은 {amount}입니다. {deadline} 자동이체 예정입니다.",
            "{sender} 보안 안내: {customer}님 계정 {service} 변경이 완료되었습니다. 본인이 아닌 경우 고객센터(☎{phone})로 즉시 연락 주세요.",
            "[{sender}] {service} 이용 내역 알림 — {amount} 결제 완료 ({deadline}). 이상 거래 시 {phone} 문의.",
        ],
        "sender":    ["신한카드", "국민은행", "우리은행", "카카오페이", "토스뱅크", "하나카드", "농협카드", "우리카드", "신한은행", "국민카드", "삼성카드", "우리금융", "대신증권", "키움증권", "신협", "신한금융투자"],
        "customer":  ["홍길동", "김철수", "이영희", "박지민", "VIP 고객"],
        "service":   ["신용대출 이자", "카드 이용 대금", "주택담보대출", "마이너스 통장 한도", "해외 결제 내역"],
        "amount":    ["10,000원", "38,500원", "125,000원", "250,000원", "480,000원", "15,000원", "72,000원"],
        "deadline":  ["이달 25일", "다음 달 1일", "3월 31일", "4월 10일", "이번 주 금요일"],
        "url":       ["www.shinhan.com", "www.kbstar.com", "app.kakaopay.com"],
        "phone":     ["1588-7942", "1599-0000", "1588-9999", "1544-5000"],
    },

    "ham_security_notice": {
        "templates": [
            "[사내공지 | IT지원팀] {topic} 관련 전사 {action}이 진행됩니다. {detail} ({url})",
            "IT보안팀 안내: {topic} 정기 점검으로 인해 {date_str} {action}이 실시됩니다. {detail}",
            "[필독] {topic} 보안 패치 적용 안내 — {date_str} 적용 예정. {action}. 문의: {url}",
            "전 임직원 대상 {topic} 교육이 {date_str}까지 의무 이수 사항입니다. {detail}: {url}",
        ],
        "topic":    ["정보보안 정기 교육", "사내 VPN 업데이트", "비밀번호 변경 캠페인", "PC 보안 패치", "클라우드 접근 권한 점검"],
        "action":   ["시스템 재시작", "필수 소프트웨어 업데이트", "비밀번호 재설정 안내", "접근 권한 재인증"],
        "detail":   ["업무 시간 외(오후 11시~새벽 2시) 진행 예정입니다", "포털 로그인 후 'My보안' 메뉴에서 완료하세요", "미이수 시 시스템 접근이 제한될 수 있습니다"],
        "date_str": ["3월 28일", "4월 1일", "3월 31일", "4월 7일", "이번 주 금요일"],
        "url":      ["intranet.company.com/security", "hr-portal.local/edu", "itsupport@company.com"],
    },

    "ham_subscription": {
        "templates": [
            "[{service}] {customer}님의 {plan} 구독이 {date_str}에 {action}됩니다. 금액: {amount}.",
            "{service} 이용 안내: {plan} 플랜이 {date_str} 자동 갱신될 예정입니다. 변경을 원하시면 {url}에서 관리해 주세요.",
            "안녕하세요, {service}입니다. {customer}님 {plan} 구독 {action} 알림 ({date_str}). {amount} 결제 예정.",
            "[{service}] 멤버십 만료 {deadline} 전 알림 — {plan} 갱신 시 {amount}가 청구됩니다. {url}",
        ],
        "service":   ["Netflix", "YouTube Premium", "Adobe Creative Cloud", "Microsoft 365", "Spotify", "웨이브(wavve)", "Notion"],
        "customer":  ["회원님", "구독자님", "사용자님"],
        "plan":      ["개인 Standard", "Family Premium", "Business Basic", "Pro 연간"],
        "action":    ["자동 갱신", "청구", "만료"],
        "amount":    ["9,900원", "13,900원", "15,900원", "19,900원", "29,900원", "59,800원"],
        "date_str":  ["4월 1일", "3월 31일", "4월 7일", "4월 14일", "다음 달 1일"],
        "deadline":  ["7일", "3일", "1일"],
        "url":       ["www.netflix.com/account", "myaccount.google.com", "account.adobe.com"],
    },

    "ham_hr": {
        "templates": [
            "[인사팀] {year}년 {quarter} {topic} 일정을 안내드립니다. {detail}",
            "안녕하세요. {topic} 관련 {year}년 {quarter} 일정이 확정되었습니다. {detail}",
            "수신: 전 임직원 / 인사팀 안내: {topic}({quarter}) 신청 기간은 {deadline}입니다. {detail}",
            "[공지] {year}년 {quarter} {topic} 안내 — {detail}. 문의: 인사팀({phone})",
        ],
        "topic":    ["성과평가 면담", "연차 소진 권고", "교육 이수 안내", "복지 포인트 사용"],
        "year":     ["2025", "2024"],
        "quarter":  ["1분기", "2분기", "상반기", "하반기"],
        "detail":   ["사내 포털에서 신청 가능합니다", "해당 기간 내 미신청 시 자동 배정될 수 있습니다", "첨부 파일의 일정을 참고해 주세요", "부서장 사전 승인 후 신청 바랍니다"],
        "deadline": ["3월 31일", "4월 7일", "이번 주 금요일", "다음 주 월요일", "4월 14일"],
        "phone":    ["내선 1234", "내선 5678", "내선 2901", "내선 3312"],
    },
}


# ─────────────────────────────────────────
# 템플릿 채우기
# ─────────────────────────────────────────
def fill_template(template: str, pool: dict) -> str:
    placeholders = re.findall(r"\{(\w+)\}", template)
    mapping: dict[str, str] = {}

    for ph in placeholders:
        if ph in mapping:
            continue

        resolved_josa = False
        for suffix, josa_pair in _JOSA_RULES.items():
            if ph.endswith(f"_{suffix}"):
                base_key = ph[: -(len(suffix) + 1)]
                if base_key not in pool:
                    continue
                base_val = mapping.get(base_key)
                if base_val is None:
                    raw = random.choice(pool[base_key])
                    base_val = raw() if callable(raw) else raw
                    mapping[base_key] = base_val
                mapping[ph] = get_josa(base_val, josa_pair)
                resolved_josa = True
                break

        if not resolved_josa:
            if ph not in pool:
                mapping[ph] = f"[{ph}]"
                continue
            raw = random.choice(pool[ph])
            mapping[ph] = raw() if callable(raw) else raw

    return template.format(**mapping)


# ─────────────────────────────────────────
# 데이터셋 생성
# ─────────────────────────────────────────
def generate_dataset(
    target_count: int = 10000,
    spam_ratio: float = 0.5,
    seed: int = 42,
) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)

    spam_cats = [k for k in POOLS if not k.startswith("ham_")]
    ham_cats  = [k for k in POOLS if k.startswith("ham_")]

    n_spam = int(target_count * spam_ratio)
    n_ham  = target_count - n_spam

    rows: list[dict] = []
    unique_texts: set[str] = set()

    spam_collected = ham_collected = 0
    attempts = 0

    while len(rows) < target_count and attempts < 500_000:
        attempts += 1

        need_spam = spam_collected < n_spam
        need_ham  = ham_collected  < n_ham

        if need_spam and need_ham:
            is_spam = random.random() < spam_ratio
        else:
            is_spam = need_spam

        category = random.choice(spam_cats if is_spam else ham_cats)
        pool     = POOLS[category]

        template = random.choice(pool["templates"])
        raw_text = fill_template(template, pool)

        # 스팸: suffix + 노이즈 / 정상: suffix만
        if is_spam:
            raw_text  += _make_suffix()
            final_text = apply_spam_noise(raw_text, intensity=0.65)
        else:
            final_text = raw_text   # 정상 메일에는 suffix/노이즈 없음

        if final_text in unique_texts:
            continue

        unique_texts.add(final_text)
        # label: 1 = 정상(Ham), 0 = 스팸(Spam)
        rows.append({"text": final_text, "label": 1 if not is_spam else 0})
        if is_spam:
            spam_collected += 1
        else:
            ham_collected += 1

    df = pd.DataFrame(rows)[["text", "label"]]
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


# ─────────────────────────────────────────
# 실행
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 고도화된 스팸/햄 데이터셋 생성 중 ...")
    df = generate_dataset(target_count=10000, spam_ratio=0.5)

    label_counts = df["label"].value_counts()
    print(f"  ✅ 정상(1): {label_counts.get(1, 0):,}건 / 스팸(0): {label_counts.get(0, 0):,}건")
    print(f"  📝 총 {len(df):,}건 생성")

    out = Path("spam_mail_dataset.csv")
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"  💾 저장 완료: {out}")

    # 샘플 미리보기
    print("\n─── 스팸 샘플 3건 ───")
    for txt in df[df["label"] == 0]["text"].head(3):
        print(f"  {txt[:90]}...")

    print("\n─── 정상 샘플 3건 ───")
    for txt in df[df["label"] == 1]["text"].head(3):
        print(f"  {txt[:90]}...")