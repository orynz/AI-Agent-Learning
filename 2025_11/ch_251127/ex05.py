

# 삼항 연산자
# age = 21
# print("성인" if age > 20 else "미성년")
# print(f'나이가 {age}살이면 { "성인" if age > 20 else """미성년""" }입니다.')

# AI 자동화 루프 시뮬레이션
print("=== AI 추천 시스템 루프 시작 ===")
idx = 0
idx+=1
print(idx)

preference = 5  # 초기 사용자 선호도 점수
for day in range(1, 6):  # 5일 동안 반복
    print(f"\n[{day}일차]")
    print(f"현재 선호도 점수: {preference}")

    # AI가 추천을 생성하고 피드백 반영
    recommendation = preference * 1.1
    print(f"AI 추천 결과: 점수 {recommendation:.2f} 영화 추천")

    # 사용자 피드백 입력
    feedback = float(input("이 추천이 만족스러웠다면 1, 아니면 0을 입력하세요: "))

    # 피드백 반영하여 선호도 조정
    if feedback == 1:
        preference += 0.5
    else:
        preference -= 0.5
print("\n=== 루프 종료: AI 추천 모델 개선 완료 ===")
