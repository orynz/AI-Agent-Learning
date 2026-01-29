from typing import List

def save_event(name: str, date: str, participants: List[str] | None = None) -> None:
    ##############################################
    # 실제 이벤트를 저장하는 코드 (여기서는 구현 생략) #
    ##############################################
    print("=== 이벤트 저장 하기 ===")
    print(f"이름: {name}")
    print(f"날짜: {date}")
    print("참가자들:")
    if participants:
        for p in participants:
            print(f"  - {p}")


if __name__ == "__main__":
    save_event(name="과학 박람회", date="금요일", participants=["철수", "영희"])
