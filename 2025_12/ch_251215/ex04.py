
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

a = input("주제를 입력하세요>>>  ")
b = input("가치를 입력하세요>>>  ")

prompt = f"""
다음 예시 문장을 참고하여 같은 패턴의 새로운 문장을 작성하시오.

예시1: {a}은 미래 직업 역량을 키우는 데 필수적이다.
예시2: {a}은 문제 해결 능력을 강화하는 핵심 요소이다.

과제: '{a}의 {b} 가치'에 대해 같은 패턴으로 문장을 한 줄 작성하시오.
"""
print("\n[입력 결과]: \n", prompt)
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("\n[출력 결과]")
print(resp.choices[0].message.content)
