from datetime import datetime
import traceback



path = "chat_log.txt"
def main():
    
    title_print("프롬프트 로그 기록기")
    
    while True:
        user = input("USER> ").strip()
        if user == "":
            print("종료합니다.")
            break
            
        message = "CHAT_KOG> " + user
        with open(path, "a", encoding="utf-8") as f:
            f.write(message + str(datetime.now()) + "\n")

def title_print(text: str):
    total_width = 50 # 전체 문자열 폭
    text_width = 0   # 입력된 문자열 폭 계산
    for char in text:
        if ord('가') <= ord(char) <= ord('힣'): # 한글 폭 = 2
            text_width += 2
        else:
            text_width += 1
    
    # 글자 폭의 절반 만큼 앞쪽에 여백 처리-> 중앙 정렬
    padding = ' ' * ((total_width - text_width)//2)
    print(f"{'#' * total_width}")
    print(f"{padding}{text}")
    print(f"{'#' * total_width}")

if __name__ == "__main__":
    main();

# from datetime import datetime
# import traceback

# CHAT_LOG = "chat_log.txt"
# ERR_LOG = "error.log"

# def now() -> str:
#     return datetime.now().isoformat(timespec="seconds")

# def append_chat_log(role:str, text: str) -> None:
#     line = f"{now()} | {role.upper()} | {text} \n"
#     with open(CHAT_LOG, "a", encoding="utf-8") as f:
#         f.write(line)
        
# def log_exception(exc: BaseException) -> None:
#     header = f"{now()} | {type(exc).__name__} | {exc}"
#     stack = traceback.format_exc()
#     with open(ERR_LOG, "a", encoding="utf-8") as f:
#         f.write(header + "\n")
#         f.write(stack + "\n")

        
# def generate_reply(user_text:str) -> str:
#     preview = user_text.strip().replace("\n", " ")
#     if len(preview) > 50:
#         preview = preview[:50] + "..."
#     return f"요청을 확인했다. 핵심은 다음과 같다 : {preview}"

# def main() -> None:
#     while True:
#         try:
#             user = input("USER> ").strip();
#             if user == "":
#                 print("종료~!")
#                 break
#             append_chat_log("User", user)
            
            
#             reply = generate_reply(user)            
#             append_chat_log("AI", reply)
            
#         except Exception as e:
            
#             log_exception(e)
#             print("오류가 발생했으나 계속 진행합니다.")


# now = datetime.now()
# print(f"현재 시간: {now}")

# if __name__ == "__main__":
    
#     main()