"""
전체 파이프라인 실행
  1. 데이터 생성
  2. 모델 학습 + 평가
  3. 샘플 예측 테스트
"""
import sys
import os

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.dirname(__file__))

from scripts.generate_data import generate_dataset
from scripts.train_model import train_and_evaluate


SAMPLE_TEXTS = [
    # 스팸 예시
    "(광고) 국민은행 당첨! 현금 100만원 받으시려면 지금 클릭하세요",
    "[긴급] 신한은행 이상 거래 탐지. 본인이 아니시면 링크 확인",
    "(Web발신) 비트코인 폭등 예정 종목. 수익률 300% 확정! 바로 접속",
    "[필독] 정부지원 신용 대출 승인 안내. 지원금 50만원 확인 후 무료 상담 신청",
    "(광고) 신용불량자도 가능한 햇살론. 연 1.5%. 앱 다운로드",
    "[토스뱅크] 카드 이용 대금 이용 내역 알림 — 10,000원 결제 완료 (3월 31일). 이상 거래 시 1588-7942 문의",
    "건강보험공단에서 고객님 계정의 계정 도용 의심 접속를 감지했습니다. 보안을 위해 48시간 이내까지 kakao-safe.net에서 신분증 사진 재등록 해주세요.",
    "[19금 한정] 통장 매입 회원 가입 시 당일 처리 100%. 비밀 보장 카톡 ID: spam0001",
    "♣♣ 축하합니다! 고객님이 해외여행 패키지 2인 당첨되셨습니다. 3일 이내까지 배송지 입력하시면 즉시 지급. prize-check.net ",
    
    # 정상 예시
    "오랜만입니다~ 팀장님, 주간 업무 관련해서 연락드립니다.",
    "[재무팀] 오늘 월간 보고서 첨부파일 참조 바랍니다.",
    "[안내] 오후 2시에 임원진 미팅 예정입니다. 자료 검토 부탁드립니다.",
    "대리님, 요청하신 결산 보고서 첨부해 드립니다. 피드백 요청드립니다.",
    "[알림] 하나은행 급여 입금 안내드립니다. (금액: 3,500,000원)",
    "딥다이브 by 조선일보 뉴스레터: 부동산 시장 동향 동향 및 투자 지표 변화 심층 분석 — 2025 상반기 IPO 시장 전망",
    "IT보안팀 안내: 비밀번호 변경 캠페인 정기 점검으로 인해 3월 28일 시스템 재시작이 실시됩니다. 포털 로그인 후 'My보안' 메뉴에서 완료하세요",
    "카카오페이 안내: VIP 고객님의 카드 이용 대금 만기일(4월 10일)이 도래합니다. 앱에서 연장 신청 바랍니다.",
]


def run():
    print("=" * 60)
    print("  한국어 금융 스팸 분류기 — 전체 파이프라인")
    print("=" * 60)

    # ── STEP 1: 데이터 생성 ──────────────────────────
    print("\n[STEP 1] 데이터셋 생성 (20,000건) ...")
    df = generate_dataset(size=20000, spam_ratio=0.5)
    csv_path = "spam_dataset.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"  저장: {csv_path}  |  스팸: {df['label'].sum()}  정상: {(df['label']==0).sum()}")

    # ── STEP 2: 학습 & 평가 ──────────────────────────
    print("\n[STEP 2] 모델 학습 & 평가 ...")
    model, vectorizer = train_and_evaluate(csv_path)

    # ── STEP 3: 샘플 예측 ────────────────────────────
    print("\n[STEP 3] 샘플 예측 테스트")
    print("-" * 60)
    for text in SAMPLE_TEXTS:
        vec   = vectorizer.transform([text])
        pred  = model.predict(vec)[0]
        proba = model.predict_proba(vec)[0]
        label = "스팸 🚫" if pred == 1 else "정상 ✅"
        print(f"  [{label}] (스팸확률 {proba[1]:.2f})  {text[:55]}")
    print("-" * 60)

    print("\n✅  파이프라인 완료!")
    print("   API 서버 실행:  uvicorn main:app --reload")
    print("   Swagger UI:     http://127.0.0.1:8000/docs")
    print(f"   리포트 폴더:    reports/")
    
if __name__ == "__main__":
    run()
