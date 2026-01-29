# chat_logger.py
from datetime import datetime
import traceback

CHAT_LOG = "chat_log.txt"
ERR_LOG = "error.log"

# 현재 시간을 구해옴
def now() -> str:
    return datetime.now().isoformat(timespec="seconds")

# 로그 기록 남기기
def append_chat_log(role: str, text: str) -> None:
    line = f"{now()} | {role.upper()} | {text}\n"
    with open(CHAT_LOG, "a", encoding="utf-8") as f:
        f.write(line)

# 에러 기록 남기기
def log_exception(exc: BaseException) -> None:
    header = f"{now()} | {type(exc).__name__} | {exc}"
    stack = traceback.format_exc()
    with open(ERR_LOG, "a", encoding="utf-8") as f:
        f.write(header + "\n")
        f.write(stack + "\n")

# 응답 결과 내용을 요약하여 반환
def generate_reply(user_text: str) -> str:
    # 이후 LLM 연동 시 이 함수를 교체하면 된다.
    # 여기서는 예시로 요약형 응답을 생성한다.
    preview = user_text.strip().replace("\n", " ")
    if len(preview) > 50:
        preview = preview[:50] + "..."
    return f"요청을 확인했다. 핵심은 다음과 같다: {preview}"

def main() -> None:
    print("프롬프트 로그 기록기 시작(종료: 빈 입력 후 Enter).")
    while True:
        try:
            user = input("USER> ").strip()
            if user == "":
                print("종료한다.")
                break

            # 사용자 입력 로그
            append_chat_log("user", user)

            # 응답 생성
            reply = generate_reply(user)

            # 응답 로그 및 출력
            append_chat_log("assistant", reply)
            print(f"ASSISTANT> {reply}")

        except Exception as e:
            # 예외를 기록하고 루프를 지속한다.
            log_exception(e)
            print("오류가 발생했으나 계속 진행한다. 상세는 error.log 참조.")

if __name__ == "__main__":
    main()
