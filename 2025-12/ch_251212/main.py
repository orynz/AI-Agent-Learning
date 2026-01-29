# main.py
from llm_client import ask_llm

if __name__ == "__main__":
    answer = ask_llm("요약: LLM 개발 환경 분리가 왜 중요한지 한 줄로 설명해 주세요.")
    print(answer)