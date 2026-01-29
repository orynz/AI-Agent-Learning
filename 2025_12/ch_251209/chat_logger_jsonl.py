# chat_logger_jsonl.py
from datetime import datetime
import json, traceback, os
import logging

CHAT_LOG = "chat_log.jsonl"
ERR_LOG = "error.log"

def now() -> str:
    return datetime.now().isoformat(timespec="seconds")

def append_jsonl(record: dict, path: str) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def log_exception_json(e: BaseException) -> None:
    append_jsonl({
        "ts": now(),
        "level": "ERROR",
        "error": type(e).__name__,
        "message": str(e),
        "trace": traceback.format_exc()
    }, ERR_LOG)

def generate_reply(user_text: str) -> str:
    return f"요약: {user_text[:60]}..." if len(user_text) > 60 else f"요약: {user_text}"

def main() -> None:
    print("JSONL 로그 모드 시작(종료: 빈 입력).")
    while True:
        try:
            user = input("USER> ").strip()
            if not user:
                print("종료한다.")
                break

            append_jsonl({"ts": now(), "role": "user", "text": user}, CHAT_LOG)
            reply = generate_reply(user)
            append_jsonl({"ts": now(), "role": "assistant", "text": reply}, CHAT_LOG)
            print(f"ASSISTANT> {reply}")
            
            raise

        except Exception as e:
            log_exception_json(e)
            print("오류가 발생했으나 계속 진행한다.")

if __name__ == "__main__":
    main()
