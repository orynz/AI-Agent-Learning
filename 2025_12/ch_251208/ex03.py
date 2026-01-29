from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# 가상 검색 도구
def fake_search(query):
    data = {
        "Python function": "Python 함수는 def 키워드로 정의하며 입력값과 반환값 개념을 포함한다.",
        "OOP concept": "객체지향은 클래스, 객체, 상속, 캡슐화, 다형성 개념을 포함한다.",
        "Python study tips": "짧은 단위 실습 반복과 즉시 실행을 통해 이해를 높일 수 있다."
    }
    return data.get(query, "검색 결과 없음")

def run_react(prompt):
    messages = [{"role": "user", "content": prompt}]

    while True:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        content = resp.choices[0].message.content
        print(content)

        action_match = re.search(r"Action\s*\d*\s*:\s*Search\[(.*)\]", content)
        finish_match = re.search(r"Finish\[(.*)\]", content)

        if finish_match:
            print("\n=== 최종 답 ===")
            print(finish_match.group(1))
            break

        if action_match:
            query = action_match.group(1).strip('" ')
            obs = fake_search(query)
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": f"Observation: {obs}"})
        else:
            break

prompt = """
문제: '초보자가 Python 함수 개념을 이해하도록 3단계 학습 플랜을 설계하라.'
ReAct 규칙 준수:
- Thought
- Action: Search[...] 또는 Finish[...]
- Observation
"""
run_react(prompt)
