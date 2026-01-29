from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os
import json

# 프롬프트 기봄 템플릿
template = """
[역할] {role}
[요청] {task}
[출력] {format}
[제약] {constraints}
[예시] {examples}
"""

CHAT_LOG = "chat_log.jsonl"

# 사용자 입력 로직 : role, task, format, constraints, examples
# 입력된 데이터를 바탕으로 프롬프트 문자열을 자동 생성
def user_inputFn() -> dict:
    title_print("프롬프트를 작성하세요.")
    user_input = {
        "role": input("역할*> "),
        "task": input("요청*> "),
        "format": input("출력*> "),
        "constraints": input("제약*> "),
        "examples": input("예시(선택)> ")
    }
    
    return user_input

# 사용자 입력 데이터 확인 : 필수 입력 데이터 누락시 재요청 처리
def check_prompt(user_data: dict) -> str:
    for k, v in user_data.items():
        if k == "role" and v == "":
            title_print("역할 누락: 다시 입력하세요.")
            while user_data["role"] == "":
                user_data["role"] = user_data("역할*> ")
                
        if k == "task" and v == "":
            title_print("요청 누락: 다시 입력하세요.")
            while user_data["task"] == "":
                user_data["task"] = user_data("요청*> ")
                
        if k == "format" and v == "":
            title_print("출력 누락: 다시 입력하세요.")
            while user_data["format"] == "":
                user_data["format"] = user_data("출력*> ")
                
        if k == "constraints" and v == "":
            title_print("제약 누락: 다시 입력하세요.")
            while user_data["constraints"] == "":
                user_data["constraints"] = user_data("제약*> ")
    
    prompt = template.format(
        role = user_data["role"],
        task = user_data["task"],
        format = user_data["format"] + (", 최종 출력물은 반드시 완변학 JSON 형태로 정리합니다."),
        constraints = user_data["constraints"],
        examples =  user_data["examples"]
    )
    return prompt

# 제목 중앙 정렬 - 가독성 향상
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
    print()
    print(f"{'#' * total_width}")
    print(f"{padding}{text}")
    print(f"{'#' * total_width}")
    print()

def now() -> str:
    return datetime.now().isoformat(timespec="seconds")

def append_jsonl(record: dict, path: str) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        
# Json 스키마 검증
def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False

def main():
    user_input = user_inputFn()
    prompt = check_prompt(user_input)
    title_print("입력하신 프롬프트 내용입니다.")
    print(prompt)
    
    load_dotenv()
    api_key = os.getenv("API_KEY")
    
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-5",
        input=[{"role":"user", "content":prompt}])
    
    if (is_valid_json(response.output_text)):
        title_print("올바른 JSON 형태 입니다.")
    else:
        title_print("JSON 형태가 올바르지 않습니다.")
    
    append_jsonl({"ts": now(), "role": "user", "text": prompt}, CHAT_LOG)
    append_jsonl({"ts": now(), "role": "assistant", "text": response.output_text}, CHAT_LOG)
    
    print(response.output_text)

if __name__ == "__main__":
    main()